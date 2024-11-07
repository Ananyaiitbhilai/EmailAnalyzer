import base64
import json
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.utils import parseaddr, parsedate_to_datetime
import re
from bs4 import BeautifulSoup
import logging
import time
import random
from .text_preprocessor import TextPreprocessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GmailFetcher:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
        self.batch_size = 100  # Number of emails to process in each batch
        self.text_preprocessor = TextPreprocessor() 

    def _extract_email_content(self, message):
        """Extract email content with improved handling for all parts."""
        if 'payload' not in message:
            return message.get('snippet', '')  # Don't preprocess snippet fallback

        def decode_part(part_body):
            """Helper function to decode message parts."""
            try:
                if 'data' in part_body:
                    # Remove padding calculation - let base64 handle it
                    return base64.urlsafe_b64decode(part_body['data']).decode('utf-8', errors='replace')
                return ''
            except Exception as e:
                logger.error(f"Decoding error: {e}")
                return ''

        def get_parts(payload, parts=None):
            """Recursively get all parts of the email."""
            if parts is None:
                parts = []
                
            if 'parts' in payload:
                # Multiple parts - process recursively
                for part in payload['parts']:
                    get_parts(part, parts)
            else:
                # Single part - add to list
                parts.append(payload)
            return parts

        try:
            # Get all parts of the message
            all_parts = get_parts(message['payload'])
            content_parts = []

            for part in all_parts:
                mime_type = part.get('mimeType', '')
                
                # Handle different content types
                if mime_type.startswith('text/'):
                    body = part.get('body', {})
                    if body.get('size', 0) > 0:
                        content = decode_part(body)
                        
                        if mime_type == 'text/html':
                            try:
                                soup = BeautifulSoup(content, 'html.parser')
                                # Remove only script and style elements
                                for script in soup(["script", "style"]):
                                    script.decompose()
                                # Preserve more whitespace and structure
                                text = soup.get_text(separator='\n', strip=True)
                                # Less aggressive whitespace normalization
                                text = re.sub(r'\n{3,}', '\n\n', text)
                                content_parts.append(text)
                            except Exception as e:
                                logger.error(f"HTML parsing error: {e}")
                                content_parts.append(content)  # Use raw content as fallback
                        else:
                            # Plain text - preserve as is
                            content_parts.append(content)

            # Combine all parts with double newline
            full_content = '\n\n'.join(filter(None, content_parts))
            
            # If no content was extracted, use full message
            if not full_content.strip():
                full_content = message.get('snippet', '') + '\n' + message.get('body', {}).get('data', '')

            # Less aggressive preprocessing
            processed_content = self.text_preprocessor.clean_text(full_content, preserve_length=True)
            return processed_content

        except Exception as e:
            logger.error(f"Error extracting content: {e}")
            # Return both snippet and any available body data
            return message.get('snippet', '') + '\n' + message.get('body', {}).get('data', '')

    def _process_single_email(self, message_id, max_retries=3):
        """Process a single email with retries."""
        for attempt in range(max_retries):
            try:
                # Get the full message with improved error handling
                message = self._fetch_email_content(message_id, attempt)
                if message is None:  # Skip if message is not accessible
                    return None

                headers = {header['name']: header['value'] 
                         for header in message['payload']['headers']}

                # Extract email addresses
                from_name, from_email = parseaddr(headers.get('From', ''))
                to_list = [parseaddr(addr.strip()) 
                          for addr in headers.get('To', '').split(',') if addr.strip()]
                cc_list = [parseaddr(addr.strip()) 
                          for addr in headers.get('Cc', '').split(',') if addr.strip()]

                # Convert date
                date_str = headers.get('Date', '')
                try:
                    date = parsedate_to_datetime(date_str).isoformat()
                except:
                    date = datetime.datetime.now().isoformat()

                # Extract content
                content = self._extract_email_content(message)

                return {
                    'id': message['id'],
                    'custodian_id': None,
                    'date': date,
                    'last_action': None,
                    'from': [from_name, from_email],
                    'to': [[name, email] for name, email in to_list],
                    'cc': [[name, email] for name, email in cc_list],
                    'subject': headers.get('Subject', ''),
                    'content': content
                }

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for email {message_id}: {e}")
                if attempt < max_retries - 1:
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                    continue
                
            logger.error(f"Failed to process email {message_id} after {max_retries} attempts")
            return None

    def _fetch_email_content(self, message_id, attempt=0):
        """Fetch email content with improved error handling."""
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            return message
            
        except HttpError as error:
            if error.resp.status == 400 and 'failedPrecondition' in str(error):
                logger.warning(f"Message {message_id} not accessible (possibly deleted)")
                return None
            elif error.resp.status in [429, 500, 503]:
                logger.warning(f"Temporary error for message {message_id} on attempt {attempt + 1}: {error}")
                raise  # Let the retry logic in _process_single_email handle it
            else:
                logger.error(f"Permanent error fetching message {message_id}: {error}")
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error fetching message {message_id}: {e}")
            raise

    def fetch_emails(self, max_results=100, start_date=None, end_date=None, 
                    sender=None, category='all', progress_callback=None):
        """Fetch emails with improved error handling."""
        query_parts = []
        if start_date:
            query_parts.append(f'after:{start_date}')
        if end_date:
            query_parts.append(f'before:{end_date}')
        if sender:
            query_parts.append(f'from:{sender}')
        if category != 'all':
            query_parts.append(f'category:{category}')
        
        query = ' '.join(query_parts)

        try:
            # Get message IDs in batches
            messages = []
            page_token = None
            
            while len(messages) < max_results:
                try:
                    results = self.service.users().messages().list(
                        userId='me',
                        q=query,
                        pageToken=page_token,
                        maxResults=min(max_results - len(messages), 100)
                    ).execute()
                    
                    if 'messages' in results:
                        messages.extend(results['messages'])
                    
                    page_token = results.get('nextPageToken')
                    if not page_token or len(messages) >= max_results:
                        break
                        
                except Exception as e:
                    logger.error(f"Error fetching message list: {e}")
                    break

            # Process messages sequentially with progress
            emails = []
            total_messages = len(messages)
            
            for i, msg in enumerate(messages, 1):
                if progress_callback:
                    progress_callback(i, total_messages)
                
                result = self._process_single_email(msg['id'])
                if result:
                    emails.append(result)
                
                # Add a small delay between requests to avoid rate limiting
                time.sleep(0.1)

            return emails

        except Exception as e:
            logger.error(f"Error in fetch_emails: {e}")
            return []

    def get_total_email_count(self, query=""):
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=1
            ).execute()
            return results.get('resultSizeEstimate', 0)
        except Exception as e:
            logger.error(f"Error getting email count: {e}")
            return 0

    def get_message_details(self, message_id):
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            # Additional processing if needed
            return message
        except Exception as e:
            logger.error(f"Error fetching message {message_id}: {e}")
            return None