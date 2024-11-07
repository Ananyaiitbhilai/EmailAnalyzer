from pymongo import MongoClient
import logging
from datetime import datetime, timezone
from bson import ObjectId
import uuid

logger = logging.getLogger(__name__)

class MongoHelper:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.emailclassifiersimple
        
        # Collections
        self.classifications = self.db.classifications
        self.visualizations = self.db.visualizations
        self.reports = self.db.reports
        self.raw_emails = self.db.raw_emails
        self.email_requests = self.db.email_requests
    
    def save_classification_results(self, user_email, results, session_id):
        """Save classification results with user and timestamp"""
        try:
            if not results:
                return
            
            for result in results:
                result['user_email'] = user_email
                result['session_id'] = session_id  # Add session ID to classification results
                
            self.classifications.insert_many(results)
            logger.info(f"Saved classification results for user {user_email}")
        except Exception as e:
            logger.error(f"Error saving classification results: {e}")
            raise

    def get_classification_results(self, user_email, session_id=None):
        """Get classification results for the most recent session if session_id is not provided"""
        try:
            if session_id:
                # Get results for specific session
                cursor = self.classifications.find({
                    'user_email': user_email,
                    'session_id': session_id
                })
            else:
                # Get the most recent session ID
                latest_session = self.email_requests.find_one(
                    {'user_email': user_email},
                    sort=[('timestamp', -1)]
                )
                if not latest_session:
                    return []
                    
                cursor = self.classifications.find({
                    'user_email': user_email,
                    'session_id': latest_session['session_id']
                })
            
            return list(cursor)
        except Exception as e:
            logger.error(f"Error getting classification results: {e}")
            raise

    def save_visualization_data(self, user_email, visualization_data):
        """Save visualization data"""
        try:
            document = {
                'user_email': user_email,
                'timestamp': datetime.utcnow(),
                'data': visualization_data
            }
            result = self.visualizations.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving visualization data: {e}")
            raise

    def save_fetched_emails(self, user_email, emails_data, session_id):
        """Save fetched emails to MongoDB"""
        try:
            if not emails_data:
                return
            
            processed_emails = []
            for email in emails_data:
                email['user_email'] = user_email
                email['timestamp'] = datetime.utcnow()
                email['session_id'] = session_id  # Add session ID to each email
                processed_emails.append(email)
            
            if processed_emails:
                result = self.raw_emails.insert_many(processed_emails)
                logger.info(f"Saved {len(processed_emails)} emails for user {user_email}")
                return result.inserted_ids
            
        except Exception as e:
            logger.error(f"Error saving fetched emails: {e}")
            raise

    def save_email_request(self, user_email, request_data):
        """Save email request data"""
        try:
            # Generate a unique session ID for this classification run
            session_id = str(uuid.uuid4())
            document = {
                'user_email': user_email,
                'timestamp': datetime.utcnow(),
                'request_data': request_data,
                'session_id': session_id,
                'status': 'pending'
            }
            self.email_requests.insert_one(document)
            return session_id
        except Exception as e:
            logger.error(f"Error saving email request: {e}")
            raise

    def get_raw_emails(self, user_email, session_id=None):
        """Retrieve raw emails for a specific user and optionally filter by session"""
        try:
            if session_id:
                cursor = self.raw_emails.find({
                    'user_email': user_email,
                    'session_id': session_id
                })
            else:
                # If no session_id provided, get the most recent session
                latest_session = self.email_requests.find_one(
                    {'user_email': user_email},
                    sort=[('timestamp', -1)]
                )
                if latest_session:
                    session_id = latest_session['session_id']
                    cursor = self.raw_emails.find({
                        'user_email': user_email,
                        'session_id': session_id
                    })
                else:
                    cursor = self.raw_emails.find({'user_email': user_email})
            
            return list(cursor)
        except Exception as e:
            logger.error(f"Error retrieving raw emails: {e}")
            raise