# Monkey patch must be the first thing we do
import eventlet
eventlet.monkey_patch()
from eventlet import debug
debug.hub_prevent_multiple_readers(False) 

import sys
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import Flask, render_template, jsonify, session, redirect, url_for, request
from data_vis import create_toxicity_pie_chart, create_category_bar_chart, create_sender_sankey, create_relationship_analysis_chart

# Load environment variables
load_dotenv()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify required environment variables
required_env_vars = ['OPENAI_API_KEY', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'OAUTH_REDIRECT_URI']
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"{var} not found in environment variables")

# Add the classifier directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'classifier'))

from flask import Flask, render_template, jsonify, session
from flask_socketio import SocketIO, emit
import time
from tqdm import tqdm
import concurrent.futures
import json
from email_classifier import EmailClassifier

# Add this import at the top with other imports
from fetcher.gmail_fetcher import GmailFetcher
from report_generator import send_report_email
from database.mongo_helper import MongoHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
socketio = SocketIO(app, async_mode='eventlet')

# OAuth2 Configuration
SCOPES = [
       'https://www.googleapis.com/auth/gmail.readonly',  # Fetch emails
       'https://www.googleapis.com/auth/gmail.send',      # Send report
       'https://www.googleapis.com/auth/userinfo.email',  # Get user email
       'openid'                                          # Authentication
   ]
# Configure the OAuth flow
client_config = {
    "web": {
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
        "redirect_uris": [os.getenv('OAUTH_REDIRECT_URI')],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}

flow = Flow.from_client_config(
    client_config,
    scopes=SCOPES,
    redirect_uri=os.getenv('OAUTH_REDIRECT_URI')
)

#Authentication
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def refresh_credentials():
    try:
        if 'credentials' not in session:
            return False
        
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                session['credentials'] = credentials_to_dict(credentials)
                return True
            return False
        return True
    except Exception as e:
        logger.error(f"Error refreshing credentials: {str(e)}")
        return False

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authorize')
def authorize():
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='false',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    try:
        full_url = request.url
        
        if request.headers.get('X-Forwarded-Proto') == 'https':
            full_url = full_url.replace('http:', 'https:')
        
        flow.fetch_token(authorization_response=full_url)
        credentials = flow.credentials
        
        session['credentials'] = credentials_to_dict(credentials)
        
        next_url = session.pop('next_url', url_for('index'))
        return redirect(next_url)
    except Exception as e:
        logger.error(f"Error in oauth2callback: {str(e)}")
        session.clear()
        return redirect(url_for('login'))

@app.route('/check_auth')
def check_auth():
    if 'credentials' not in session:
        return jsonify({"authenticated": False}), 401
        
    if not refresh_credentials():
        return jsonify({"authenticated": False}), 401
        
    try:
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        service.users().getProfile(userId='me').execute()
        return jsonify({"authenticated": True}), 200
    except Exception as e:
        logger.error(f"Error checking authentication: {str(e)}")
        return jsonify({"authenticated": False}), 401

@app.route('/')
def index():
    if 'credentials' not in session:
        session['next_url'] = url_for('index')
        return redirect(url_for('login'))
    
    if not refresh_credentials():
        return redirect(url_for('login'))
        
    return render_template('index.html')






#Email classification
@app.route('/classify_page')
def classify_page():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    return render_template('classify_page.html')


@app.route('/get_classification_results')
def get_classification_results():
    try:
        if 'credentials' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        # Get user email
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']

        # Get results from MongoDB
        results = mongo_helper.get_classification_results(user_email)
        if not results:
            return jsonify({'error': 'No classification results found'}), 404

        return jsonify(results)
    except Exception as e:
        logger.error(f"Error getting classification results: {str(e)}")
        return jsonify({'error': str(e)}), 500


def process_email(email_data, classifier):
    result = classifier.classify_email(email_data)
    return {**email_data, **result}

@socketio.on('start_classification')
def handle_classification(data):
    try:
        if 'credentials' not in session:
            socketio.emit('error', {'message': 'Not authenticated'})
            return

        # Get user email for MongoDB
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']
        
        # Save request and get session ID
        request_data = {
            'max_results': int(data.get('max_results', 100)),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'sender': data.get('sender'),
            'email_category': data.get('email_category', 'all')
        }
        session_id = mongo_helper.save_email_request(user_email, request_data)

        # Phase 1: Fetch Emails
        fetcher = GmailFetcher(credentials)
        
        def fetch_progress_callback(completed, total):
            progress = (completed / total) * 100
            socketio.emit('progress_update', {
                'phase': 'fetching',
                'progress': progress,
                'current': completed,
                'total': total,
                'message': f'Fetching emails: {completed}/{total}'
            })
            socketio.sleep(0)

        # Fetch and save raw emails
        emails = fetcher.fetch_emails(
            max_results=request_data['max_results'],
            start_date=request_data['start_date'],
            end_date=request_data['end_date'],
            sender=request_data['sender'],
            category=request_data['email_category'],
            progress_callback=fetch_progress_callback
        )

        # Save raw emails with session ID
        email_ids = mongo_helper.save_fetched_emails(user_email, emails, session_id)
        if not email_ids:
            raise Exception("Failed to save raw emails")

        # Explicitly emit completion of phase 1 and start of phase 2
        socketio.emit('progress_update', {
            'phase': 'fetching',
            'progress': 100,
            'message': 'Email fetching completed'
        })
        
        socketio.emit('phase_change', {
            'phase': 'classification',
            'message': 'Starting classification phase'
        })

        # Phase 2: Classification
        raw_emails = mongo_helper.get_raw_emails(user_email, session_id)
        if not raw_emails:
            raise Exception("No raw emails found for classification")

        classifier = EmailClassifier()
        total_emails = len(raw_emails)
        classification_results = []
        completed_count = 0
        start_time = time.time()

        def process_email(email):
            try:
                return classifier.classify_email(email)
            except Exception as e:
                logger.error(f"Error processing email: {e}")
                return None

        # Reset progress for phase 2
        socketio.emit('progress_update', {
            'phase': 'classification',
            'progress': 0,
            'current': 0,
            'total': total_emails,
            'message': f'Starting classification of {total_emails} emails'
        })

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_email = {executor.submit(process_email, email): email 
                             for email in raw_emails}
            
            for future in concurrent.futures.as_completed(future_to_email):
                email = future_to_email[future]
                try:
                    result = future.result()
                    if result:
                        classification_results.append({**email, **result})
                    
                    completed_count += 1
                    progress = (completed_count / total_emails) * 100
                    
                    # Calculate speed and remaining time
                    elapsed_time = time.time() - start_time
                    emails_per_second = completed_count / elapsed_time if elapsed_time > 0 else 0
                    remaining_emails = total_emails - completed_count
                    estimated_remaining_time = remaining_emails / emails_per_second if emails_per_second > 0 else 0
                    
                    socketio.emit('progress_update', {
                        'phase': 'classification',
                        'progress': progress,
                        'current': completed_count,
                        'total': total_emails,
                        'speed': round(emails_per_second, 2),
                        'remaining_time': round(estimated_remaining_time, 2),
                        'message': f'Classifying emails: {completed_count}/{total_emails}'
                    })
                    socketio.sleep(0)
                    
                except Exception as e:
                    logger.error(f"Error processing email: {e}")
                    continue

        # Save classification results
        if classification_results:
            mongo_helper.save_classification_results(user_email, classification_results, session_id)

        # Emit final completion
        socketio.emit('classification_complete', {
            'message': 'Classification completed!',
            'redirect_url': url_for('view_classifications'),
            'session_id': session_id
        })

    except Exception as e:
        logger.error(f"Error in classification: {e}")
        socketio.emit('error', {'message': f'Error in classification: {str(e)}'})


#Visualis   after classification
@app.route('/view_classifications')
def view_classifications():
    try:
        # Get user credentials and email
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']

        # Get results from MongoDB
        classified_emails = mongo_helper.get_classification_results(user_email)
        if not classified_emails:
            return render_template('no_results.html', 
                                 message="No classification results found. Please classify emails first.")

        # Calculate summary statistics
        total_emails = len(classified_emails)
        toxic_emails = sum(1 for email in classified_emails if email.get('Non-toxic', 1) == 0)
        toxic_percentage = (toxic_emails / total_emails * 100) if total_emails > 0 else 0
        
        # Find most toxic sender if there are toxic emails
        most_toxic_sender = None
        if toxic_emails > 0:
            sender_toxic_count = {}
            for email in classified_emails:
                if email.get('Non-toxic', 1) == 0:
                    sender = email.get('sender_name', 'Unknown')
                    sender_toxic_count[sender] = sender_toxic_count.get(sender, 0) + 1
            most_toxic_sender = max(sender_toxic_count.items(), key=lambda x: x[1])[0]

        summary = {
            'total_emails': total_emails,
            'toxic_emails': toxic_emails,
            'toxic_percentage': toxic_percentage,
            'most_toxic_sender': most_toxic_sender
        }

        return render_template(
            'classification_results.html',
            classified_emails=classified_emails,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error viewing classifications: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/email_details/<email_id>')
def email_details(email_id):
    if 'credentials' not in session:
        session['next_url'] = url_for('email_details', email_id=email_id)
        return redirect(url_for('authorize'))
    
    if not refresh_credentials():
        return redirect(url_for('authorize'))
        
    try:
        # Get user email
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']
        
        # Get results from MongoDB
        results = mongo_helper.get_classification_results(user_email)
        if not results:
            return render_template('error.html', error="Classification results not found")
            
        # Find the email with matching ID
        email = next((e for e in results if str(e.get('id')) == str(email_id)), None)
        
        if email:
            # Transform the email data to match the template's expectations
            email_data = {
                'id': email.get('id'),
                'subject': email.get('subject', 'No Subject'),
                'sender_name': email.get('from', ['Unknown', ''])[0],
                'recipient_name': email.get('to', [['Unknown', '']])[0][0],
                'timestamp': email.get('date'),
                'content': email.get('content', ''),
                'non_toxic': email.get('Non-toxic', 1),
                'toxic': email.get('toxic', {}),
                'relationship_analysis': email.get('relationship_analysis', {
                    'relationship_analysis': {}
                }),
                'harmful_phrases': email.get('harmful_phrases', []),
                'explanation': email.get('explanation', '')
            }
            
            return render_template('email_details.html', email=email_data)
            
        return render_template('error.html', error="Email not found")
        
    except Exception as e:
        logger.error(f"Error viewing email details: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/send_report', methods=['POST'])
def send_report():
    if 'credentials' not in session:
        session['next_url'] = url_for('send_report')
        return jsonify({"success": False, "message": "Authentication required"}), 401
    
    if not refresh_credentials():
        session['next_url'] = url_for('send_report')
        return jsonify({"success": False, "message": "Authentication required"}), 401

    try:
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']
        
        success, message = send_report_email(session['credentials'], user_email)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Report sent successfully to your email!"
            })
        else:
            return jsonify({
                "success": False,
                "message": message
            }), 500
            
    except Exception as e:
        logger.error(f"Error in send_report: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Failed to send report: {str(e)}"
        }), 500
    

# Add this route to clear session and tokens
@app.route('/clear_auth')
def clear_auth():
    session.clear()
    return redirect(url_for('login'))

# Initialize MongoDB helper
mongo_helper = MongoHelper(os.getenv('MONGODB_URI'))

@app.route('/process_emails', methods=['POST'])
def process_emails():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
        
    try:
        # Get user credentials and email
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']
        
        # Get parameters from the request
        data = request.get_json()
        max_results = int(data.get('max_results', 100))
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        sender = data.get('sender')
        email_category = data.get('email_category', 'all')
        
        # Fetch emails
        fetcher = GmailFetcher(credentials)
        emails = fetcher.fetch_emails(
            max_results=max_results,
            start_date=start_date,
            end_date=end_date,
            sender=sender,
            category=email_category
        )
        
        # Classify emails
        classifier = EmailClassifier()
        classified_emails = []
        
        for email in emails:
            result = classifier.classify_email(email)
            classified_emails.append({**email, **result})
        
        # Save results to MongoDB
        mongo_helper.save_classification_results(
            user_email=user_email,
            results=classified_emails
        )
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully processed {len(classified_emails)} emails'
        })
        
    except Exception as e:
        logger.error(f"Error processing emails: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/visualization')
def visualization():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))
    
    try:
        # Get user email
        credentials = Credentials.from_authorized_user_info(session['credentials'], SCOPES)
        service = build('gmail', 'v1', credentials=credentials)
        user_info = service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']

        # Get results from MongoDB
        emails = mongo_helper.get_classification_results(user_email)
        
        if not emails:
            return render_template('error.html', 
                error="No classification results found. Please classify emails first.")
        
        # Calculate summary
        total_emails = len(emails)
        toxic_emails = sum(1 for email in emails if not email.get('Non-toxic', True))
        toxic_percentage = (toxic_emails / total_emails * 100) if total_emails > 0 else 0
        
        # Find most toxic sender
        sender_toxicity = {}
        for email in emails:
            if not email.get('Non-toxic', True):
                sender = email.get('from', ['Unknown'])[0]
                sender_toxicity[sender] = sender_toxicity.get(sender, 0) + 1
                
        most_toxic_sender = max(sender_toxicity.items(), key=lambda x: x[1])[0] if sender_toxicity else None
        
        summary = {
            'total_emails': total_emails,
            'toxic_emails': toxic_emails,
            'toxic_percentage': toxic_percentage,
            'most_toxic_sender': most_toxic_sender
        }

        # Save visualization data to MongoDB
        visualization_data = {
            'summary': summary,
            'pie_chart': create_toxicity_pie_chart(toxic_emails, total_emails),
            'category_chart': create_category_bar_chart(emails),
            'sankey_diagram': create_sender_sankey(emails),
            'relationship_chart': create_relationship_analysis_chart(emails)
        }
        
        mongo_helper.save_visualization_data(user_email, visualization_data)
        
        return render_template(
            'visualization.html',
            summary=summary,
            pie_chart=visualization_data['pie_chart'],
            category_chart=visualization_data['category_chart'],
            sankey_diagram=visualization_data['sankey_diagram'],
            relationship_chart=visualization_data['relationship_chart']
        )
        
    except Exception as e:
        logger.error(f"Error generating visualizations: {str(e)}")
        return render_template('error.html', error=f"An error occurred while generating visualizations: {str(e)}")

@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)


