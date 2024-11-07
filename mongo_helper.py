from pymongo import MongoClient
from datetime import datetime, UTC
import logging
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)

logger = logging.getLogger(__name__)

class MongoHelper:
    def __init__(self):
        self.db = client.email_analyzer
        self.classifications = self.db.classifications

    def save_classification_results(self, user_email, results):
        """
        Save classification results to MongoDB, preserving old results
        """
        try:
            # Process results to add metadata
            processed_results = []
            for result in results:
                result['user_email'] = user_email
                result['classified_at'] = datetime.now(UTC)
                processed_results.append(result)

            # Insert new results without deleting old ones
            if processed_results:
                self.classifications.insert_many(processed_results)
                logger.info(f"Saved {len(processed_results)} new classification results for {user_email}")
            return True

        except Exception as e:
            logger.error(f"Error saving classification results: {str(e)}")
            raise

    def get_classification_results(self, user_email):
        """
        Retrieve all classification results for a user
        """
        try:
            results = list(self.classifications.find(
                {"user_email": user_email},
                {'_id': 0}  # Exclude MongoDB's _id field
            ).sort("classified_at", -1))  # Sort by newest first
            
            return results

        except Exception as e:
            logger.error(f"Error retrieving classification results: {str(e)}")
            raise

    def get_email_details(self, user_email, email_id):
        """
        Retrieve specific email details
        """
        try:
            email = self.classifications.find_one(
                {
                    "user_email": user_email,
                    "id": email_id
                },
                {'_id': 0}
            )
            return email

        except Exception as e:
            logger.error(f"Error retrieving email details: {str(e)}")
            raise

    def get_user_statistics(self, user_email):
        """
        Get statistics for user's classified emails
        """
        try:
            pipeline = [
                {"$match": {"user_email": user_email}},
                {"$group": {
                    "_id": None,
                    "total_emails": {"$sum": 1},
                    "toxic_emails": {
                        "$sum": {"$cond": [{"$eq": ["$Non-toxic", 0]}, 1, 0]}
                    },
                    "latest_classification": {"$max": "$classified_at"}
                }}
            ]
            
            stats = list(self.classifications.aggregate(pipeline))
            return stats[0] if stats else None

        except Exception as e:
            logger.error(f"Error retrieving user statistics: {str(e)}")
            raise

    def save_fetched_emails(self, user_email, emails_data):
        """
        Save fetched emails to MongoDB
        """
        try:
            if not emails_data:
                return
            
            # Add user_email to each email document
            for email in emails_data:
                email['user_email'] = user_email
                email['classified_at'] = datetime.now(UTC)
            
            result = self.classifications.insert_many(emails_data)
            logger.info(f"Saved {len(emails_data)} emails for user {user_email}")
            return result.inserted_ids
        except Exception as e:
            logger.error(f"Error saving emails to MongoDB: {str(e)}")
            raise