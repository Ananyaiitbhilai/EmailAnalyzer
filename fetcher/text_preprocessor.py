import re
import html
import logging
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class EmailMessage:
    """Data class to store structured email information"""
    body: str
    sender: Optional[str] = None
    timestamp: Optional[datetime] = None
    subject: Optional[str] = None
    recipient: Optional[str] = None
    is_forward: bool = False
    is_reply: bool = False
    
class EmailPatterns:
    """Class containing all email-related regex patterns"""
    
    # Header patterns
    FORWARD_HEADER = r'[-]+\s*Forwarded message\s*[-]+|From:.*?\nTo:.*?\nSubject:'
    REPLY_HEADER = r'On\s+.*?wrote:|On\s+.*?,.*?at.*?,.*?wrote:'
    
    # Quote patterns
    QUOTES = [
        r'(?m)^>+.*$',  # Basic quote marks
        r'(?m)^From:.*?Sent:.*?To:.*?Subject:.*$',  # Outlook style
        r'On.*?wrote:.*$',  # Gmail style
        r'\|>.*$',  # Alternative quote style
        r'[-]+\s*Original Message\s*[-]+',  # Original message marker
    ]
    
    # Signature patterns
    SIGNATURES = [
        r'(?m)^--\s*$.*',  # Standard signature delimiter
        r'(?m)^Regards,?\s*.*$',
        r'(?m)^Best,?\s*.*$',
        r'(?m)^Thanks,?\s*.*$',
        r'(?m)^Sincerely,?\s*.*$',
        r'(?m)^Best regards,?\s*.*$',
        r'(?m)^Kind regards,?\s*.*$',
    ]
    
    # Cleaning patterns
    CLEAN_PATTERNS = {
        'urls': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        'emails': r'[\w\.-]+@[\w\.-]+\.\w+',
        'multiple_spaces': r'\s+',
        'multiple_newlines': r'\n{3,}',
        'empty_lines': r'(?m)^\s*\n',
    }

class EmailParser:
    """Class for parsing email content and extracting structured information"""
    
    def __init__(self):
        self.patterns = EmailPatterns()
        
    def extract_sender(self, text: str) -> Optional[str]:
        """Extract sender information from email text"""
        from_match = re.search(r'From:\s*(.*?)(?:\n|$)', text)
        return from_match.group(1).strip() if from_match else None
        
    def extract_timestamp(self, text: str) -> Optional[datetime]:
        """Extract timestamp from email text"""
        try:
            # Common datetime patterns in emails
            patterns = [
                r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?)',
                r'(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?)',
                r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    date_str = match.group(1)
                    # Try multiple date formats
                    for fmt in [
                        '%d %b %Y %H:%M:%S',
                        '%d %b %Y %H:%M',
                        '%m/%d/%Y %H:%M:%S',
                        '%Y-%m-%d %H:%M:%S'
                    ]:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
            return None
        except Exception as e:
            logger.error(f"Error extracting timestamp: {e}")
            return None

class TextPreprocessor:
    """Main class for preprocessing email text and extracting the latest thread"""
    
    def __init__(self):
        self.patterns = EmailPatterns()
        self.parser = EmailParser()
        self._compile_patterns()
        
    def _compile_patterns(self):
        """Compile regex patterns for better performance"""
        self.compiled_quotes = [re.compile(pattern, re.MULTILINE | re.DOTALL) 
                              for pattern in self.patterns.QUOTES]
        self.compiled_signatures = [re.compile(pattern, re.MULTILINE | re.DOTALL) 
                                  for pattern in self.patterns.SIGNATURES]
        
    def remove_html(self, text: str) -> str:
        """Remove HTML tags and decode HTML entities"""
        try:
            if not text:
                return ""
                
            # Parse HTML
            soup = BeautifulSoup(text, 'html.parser')
            
            # Remove script and style elements
            for element in soup(["script", "style"]):
                element.decompose()
            
            # Get text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Decode HTML entities
            text = html.unescape(text)
            
            return text
        except Exception as e:
            logger.error(f"Error removing HTML: {e}")
            return text
            
    def clean_text(self, text: str, preserve_urls: bool = False, preserve_length: bool = True) -> str:
        """Clean text while optionally preserving URLs and email addresses"""
        try:
            if not text:
                return ""
                
            # Replace URLs and email addresses if not preserving
            if not preserve_urls:
                text = re.sub(self.patterns.CLEAN_PATTERNS['urls'], '[URL]', text)
                text = re.sub(self.patterns.CLEAN_PATTERNS['emails'], '[EMAIL]', text)
            
            if preserve_length:
                # Only normalize excessive whitespace
                text = re.sub(r'\s{4,}', ' ', text)  # Replace 4+ spaces with single space
                text = re.sub(r'\n{4,}', '\n\n', text)  # Replace 4+ newlines with double newline
            else:
                # Full whitespace normalization
                text = re.sub(self.patterns.CLEAN_PATTERNS['multiple_spaces'], ' ', text)
                text = re.sub(self.patterns.CLEAN_PATTERNS['multiple_newlines'], '\n\n', text)
                text = re.sub(self.patterns.CLEAN_PATTERNS['empty_lines'], '', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return text
            
    def remove_quotes(self, text: str) -> str:
        """Remove quoted text from email replies"""
        try:
            for pattern in self.compiled_quotes:
                text = pattern.sub('', text)
            return text.strip()
        except Exception as e:
            logger.error(f"Error removing quotes: {e}")
            return text
            

    def extract_latest_thread(self, email_text: str, clean: bool = True) -> Union[str, EmailMessage]:
        """
        Extract the most recent message from an email thread
        
        Args:
            email_text (str): The complete email thread text
            clean (bool): Whether to clean the extracted text
            
        Returns:
            Union[str, EmailMessage]: The extracted latest message
        """
        try:
            if not email_text:
                return "" if clean else EmailMessage(body="")
                
            # Remove HTML first
            text = self.remove_html(email_text)
            
            # Find the first quote marker
            first_quote_pos = float('inf')
            for pattern in self.compiled_quotes:
                match = pattern.search(text)
                if match and match.start() < first_quote_pos:
                    first_quote_pos = match.start()
            
            # Extract latest message
            if first_quote_pos == float('inf'):
                latest_message = text
            else:
                latest_message = text[:first_quote_pos].strip()
            
            # Clean if requested, but preserve length
            if clean:
                latest_message = self.clean_text(latest_message, preserve_length=True)
                # Don't remove signatures for important messages
                
                return latest_message
            
            # Create EmailMessage object
            return EmailMessage(
                body=latest_message,
                sender=self.parser.extract_sender(text),
                timestamp=self.parser.extract_timestamp(text),
                is_reply='wrote:' in text or 'Original Message' in text,
                is_forward='Forwarded message' in text
            )
            
        except Exception as e:
            logger.error(f"Error extracting latest thread: {e}")
            return "" if clean else EmailMessage(body=email_text)
            
    def get_statistics(self, text: str) -> Dict[str, Union[int, float]]:
        """Get statistics about the text"""
        try:
            clean_text = self.clean_text(text)
            words = clean_text.split()
            sentences = re.split(r'[.!?]+', clean_text)
            
            return {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'character_count': len(clean_text),
                'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                'average_sentence_length': len(words) / len(sentences) if sentences else 0
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}

def process_email_thread(email_text: str) -> Tuple[str, Dict[str, Union[int, float]]]:
    """
    Convenience function to process an email thread and get statistics
    
    Args:
        email_text (str): The email thread text
        
    Returns:
        Tuple[str, Dict]: The processed text and statistics
    """
    preprocessor = TextPreprocessor()
    processed_text = preprocessor.extract_latest_thread(email_text)
    statistics = preprocessor.get_statistics(processed_text)
    return processed_text, statistics

