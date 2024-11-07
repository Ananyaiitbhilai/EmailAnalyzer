from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os
import logging
import tempfile
import zipfile
from pymongo import MongoClient
from bson import ObjectId
from database.mongo_helper import MongoHelper

logger = logging.getLogger(__name__)

# Initialize MongoDB helper
mongo_helper = MongoHelper(os.getenv('MONGODB_URI'))

def create_main_page(classified_emails, summary):
    """Create the main classification results page"""
    # Create the header and summary section
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Email Classification Results</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <div class="container">
            <h1>Email Classification Results</h1>
            
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Total Emails:</strong> {summary['total_emails']}</p>
                <p><strong>Toxic Emails:</strong> {summary['toxic_emails']}</p>
                <p><strong>Percentage of Toxic Emails:</strong> {summary['toxic_percentage']:.2f}%</p>
                <p><strong>Most Toxic Sender:</strong> {summary['most_toxic_sender']}</p>
            </div>

            <h2>Classified Emails</h2>
            <table class="email-table">
                <thead>
                    <tr>
                        <th>Subject</th>
                        <th>From</th>
                        <th>Classification</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
    """

    # Add each email row
    for email in classified_emails:
        html += f"""
            <tr>
                <td>{email['subject']}</td>
                <td>{email['sender_name']}</td>
                <td class="{'non-toxic' if email['non_toxic'] else 'toxic'}">
                    {'Non-Toxic' if email['non_toxic'] else 'Toxic'}
                </td>
                <td>
                    <a href="details/{email['id']}.html" class="view-details-btn">View Details</a>
                </td>
            </tr>
        """

    # Close the HTML
    html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    return html

def create_details_page(email):
    """Create the details page for a single email"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Email Details - {email['subject']}</title>
        <link rel="stylesheet" href="../styles.css">
    </head>
    <body>
        <div class="container">
            <div class="email-details">
                <h1>Email Details</h1>
                
                <div class="detail-section">
                    <div class="detail-label">Subject:</div>
                    <div class="detail-content">{email['subject']}</div>
                </div>

                <div class="detail-section">
                    <div class="detail-label">From:</div>
                    <div class="detail-content">{email['sender_name']}</div>
                </div>

                <div class="detail-section">
                    <div class="detail-label">To:</div>
                    <div class="detail-content">{email['recipient_name']}</div>
                </div>

                <div class="detail-section">
                    <div class="detail-label">Timestamp:</div>
                    <div class="detail-content">{email['timestamp']}</div>
                </div>

                <div class="detail-section">
                    <div class="detail-label">Content:</div>
                    <div class="detail-content content-box">{email['content']}</div>
                </div>

                <div class="detail-section">
                    <div class="detail-label">Classification:</div>
                    <div class="detail-content {'non-toxic' if email['non_toxic'] else 'toxic'}">
                        {'Non-Toxic' if email['non_toxic'] else 'Toxic'}
                    </div>
                </div>
    """

    # Add toxicity analysis if email is toxic
    if not email['non_toxic']:
        html += """
                <div class="detail-section">
                    <h3>Toxicity Analysis:</h3>
                    <div class="categories-grid">
        """
        for category, value in email['toxic'].items():
            html += f"""
                        <div class="category {'active' if value else ''}">
                            <div class="category-icon" style="background-color: {'#dc3545' if value else '#a0aec0'};"></div>
                            {category}
                        </div>
            """
        html += """
                    </div>
                </div>
        """

    # Add relationship analysis
    html += """
                <div class="detail-section">
                    <h3>Workplace Relationship Analysis:</h3>
                    <div class="categories-grid">
    """
    
    for key, value in email['relationship_analysis']['relationship_analysis'].items():
        html += f"""
                        <div class="category {'active' if value else ''}">
                            <div class="category-icon" style="background-color: {'#4299e1' if value else '#a0aec0'};"></div>
                            {key.replace('_', ' ').title()}
                        </div>
        """

    # Add explanation and close HTML
    html += f"""
                    </div>
                </div>

                <div class="detail-section">
                    <div class="detail-label">Explanation:</div>
                    <div class="detail-content explanation-box">{email['explanation']}</div>
                </div>

                <div class="navigation">
                    <a href="../index.html" class="back-btn">Back to Results</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def create_styles():
    """Create the CSS styles for both pages"""
    return """
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f5f5f5;
        color: #333;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    h1 {
        color: #2d3748;
        margin-bottom: 1.5rem;
    }

    .summary {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    .summary h2 {
        color: #2c5282;
        margin-top: 0;
    }

    .email-table {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }

    th {
        background-color: #f8f9fa;
        font-weight: 600;
        color: #2d3748;
    }

    .toxic { color: #dc3545; }
    .non-toxic { color: #28a745; }

    .view-details-btn {
        display: inline-block;
        padding: 8px 16px;
        background-color: #4299e1;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        transition: background-color 0.2s;
    }

    .view-details-btn:hover {
        background-color: #3182ce;
    }

    .email-details {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .detail-section {
        margin-bottom: 1.5rem;
    }

    .detail-label {
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 0.5rem;
    }

    .detail-content {
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 4px;
        border: 1px solid #e2e8f0;
    }

    .content-box {
        white-space: pre-wrap;
        font-family: monospace;
    }

    .explanation-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 4px;
        border: 1px solid #e2e8f0;
        margin-top: 10px;
    }

    .categories-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
        margin-top: 10px;
    }

    .category {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
    }

    .category.active {
        background-color: #ebf8ff;
        border-color: #90cdf4;
    }

    .category-icon {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .back-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #4299e1;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin-top: 20px;
        transition: background-color 0.2s;
    }

    .back-btn:hover {
        background-color: #3182ce;
    }

    .navigation {
        margin-top: 2rem;
        text-align: center;
    }
    """

def create_report_package(classified_emails, summary):
    """Create the report package with all necessary files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the styles.css file
        with open(os.path.join(temp_dir, 'styles.css'), 'w') as f:
            f.write(create_styles())
        
        # Create main index.html
        with open(os.path.join(temp_dir, 'index.html'), 'w') as f:
            f.write(create_main_page(classified_emails, summary))
        
        # Create details directory and individual email pages
        details_dir = os.path.join(temp_dir, 'details')
        os.makedirs(details_dir)
        for email in classified_emails:
            with open(os.path.join(details_dir, f"{email['id']}.html"), 'w') as f:
                f.write(create_details_page(email))
        
        # Create ZIP file containing all files
        zip_path = os.path.join(temp_dir, 'report.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Add main files
            zf.write(os.path.join(temp_dir, 'index.html'), 'index.html')
            zf.write(os.path.join(temp_dir, 'styles.css'), 'styles.css')
            
            # Add details pages
            for email in classified_emails:
                zf.write(
                    os.path.join(details_dir, f"{email['id']}.html"),
                    f"details/{email['id']}.html"
                )
        
        # Read the ZIP file
        with open(zip_path, 'rb') as f:
            return f.read()

def send_report_email(credentials, recipient_email):
    """Send the classification report via email"""
    try:
        # Create Gmail API service
        creds = Credentials.from_authorized_user_info(credentials)
        service = build('gmail', 'v1', credentials=creds)
        
        # Get results from MongoDB instead of JSON file
        results = mongo_helper.get_classification_results(recipient_email)
        
        if not results:
            return False, "No classification results found"
            
        # Transform results to match expected format
        classified_emails = []
        for email in results:
            classified_emails.append({
                'id': str(email.get('_id', ObjectId())),
                'subject': email.get('subject', 'No Subject'),
                'sender_name': email.get('from', ['Unknown', ''])[0],
                'recipient_name': email.get('to', [['Unknown', '']])[0][0],
                'timestamp': email.get('date'),
                'content': email.get('content', ''),
                'non_toxic': email.get('Non-toxic', 1),  # Note the capital N
                'toxic': email.get('toxic', {}),
                'relationship_analysis': email.get('relationship_analysis', {
                    'relationship_analysis': {}
                }),
                'harmful_phrases': email.get('harmful_phrases', []),
                'explanation': email.get('explanation', '')
            })

        # Generate summary
        total_emails = len(results)
        toxic_emails = sum(1 for email in results if not email.get('Non-toxic', True))
        toxic_percentage = (toxic_emails / total_emails * 100) if total_emails > 0 else 0

        summary = {
            'total_emails': total_emails,
            'toxic_emails': toxic_emails,
            'toxic_percentage': round(toxic_percentage, 2),
            'most_toxic_sender': 'Not Applicable' if toxic_emails == 0 else max(
                (email.get('from', ['Unknown', ''])[0] for email in results if not email.get('Non-toxic', True)),
                key=lambda x: sum(1 for e in results if e.get('from', [''])[0] == x and not e.get('Non-toxic', True))
            )
        }
        
        # Create the report package
        report_package = create_report_package(classified_emails, summary)
        
        # Create message container
        message = MIMEMultipart()
        message['to'] = recipient_email
        message['subject'] = 'Your Email Classification Report'
        
        # Add body
        html_content = """
        <html>
        <body>
            <p>Hi,</p>
            <p>Here is your email classification analysis report. To view the report:</p>
            <ol>
                <li>Download and extract the attached ZIP file</li>
                <li>Open 'index.html' in your web browser</li>
                <li>Navigate through the report using the "View Details" links</li>
            </ol>
            <p>Best regards,</p>
        </body>
        </html>
        """
        
        text_part = MIMEText(html_content, 'html')
        message.attach(text_part)
        
        # Add ZIP file as attachment
        attachment = MIMEApplication(report_package)
        attachment.add_header('Content-Disposition', 'attachment', 
                            filename='email_classification_report.zip')
        message.attach(attachment)
        
        # Encode and send the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        logger.info(f"Report sent successfully to {recipient_email}")
        return True, "Report sent successfully!"
        
    except Exception as e:
        logger.error(f"Error sending report to {recipient_email}: {str(e)}")
        return False, f"Error sending report: {str(e)}"
        return False, f"Error sending report: {str(e)}"