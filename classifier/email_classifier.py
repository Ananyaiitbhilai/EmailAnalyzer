import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from config import FUNCTION_DEFINITION
from few_shot_email_classifier import few_shot_examples
from utils import check_task_related, analyze_relationship, identify_harmful_phrases, detect_microaggressions

class EmailClassifier:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Set up OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not self.client.api_key:
            raise ValueError("OpenAI API key not found. Please set it in your .env file.")

        self.function = FUNCTION_DEFINITION

    def get_initial_analysis(self, email_data):
        subject = email_data.get('subject', '')
        content = email_data.get('content', '')
        prompt = f"""
        {subject}
        {content}

        Please tell if above email is toxic or not in context of professional work-space. Be attentive to subtle forms of toxicity, implicit biases, and microaggressions. Consider the overall tone, context, and potential hidden meanings. Toxicity can be on the following scale: 0 - Not present, 1 - Mild/Implicit, 2-Moderate, 3 - Explicit/Severe.
        """

        try:
            response = self.client.chat.completions.create(model="gpt-4o-mini-2024-07-18",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in get_initial_analysis: {e}")
            return "Unable to perform initial analysis"



    def classify_email(self, email_data):
        subject = email_data.get('subject', '')
        content = email_data.get('content', '')
        email_id = email_data.get('id', '')
        timestamp = email_data.get('date', '')
        sender = email_data['from'][0] if isinstance(email_data['from'], list) else email_data['from']
        recipient = email_data['to'][0][0] if isinstance(email_data['to'], list) and email_data['to'] else ''
        initial_analysis = self.get_initial_analysis(email_data)

        prompt = f"""
        [Email]
        Subject: {subject}
        Content: {content}
        [/Email]
        Initial Analysis: {initial_analysis}
        
        Now, analyze the following email considering the initial analysis, subject, and content. Reason for your classification. There might be implicit toxicity also.

        Instructions:
        1. Consider the initial analysis and further analyze the subject and content together to determine the overall tone and intent
        2. Classify the email as toxic or non-toxic.
        3. Be attentive to subtle forms of toxicity, implicit biases, and microaggressions.
        4. Consider the overall tone, context, and potential hidden meanings.
        5. Classify the toxic categories of email using the following scale: 0 - Not present, 1 - Mild/Implicit, 2-Moderate, 3 - Explicit/Severe
        6. If toxic, identify specific categories of toxicity and necessarily assign the toxic categories. 
        

        Provide a classification including:
        1. [NonToxic] Whether the email is Nontoxic (1 if applies, 0 if not).
        2. [Toxic] Specific toxic categories that apply (1 if applies, 0 if not), If any email classified as toxic, should be necessarily put in below categories, put the email into nearest toxic categories which it matches:
           - Impolite: Sarcasm 
           - Impolite: Stereotype
           - Impolite: Forced teaming
           - Impolite: Authoritarian
           - Impolite: Rude
           - Impolite: Trivialising Sensitive topics
           - Impolite: Lack of empathy
           - Negative Gossip: Mocking
           - Negative Gossip: Complain
           - Offensive: Profanity
           - Offensive: Discrimination
           - Offensive: Bullying
           - Offensive: Violence
           - Offensive: Harassment
           - Passive-aggressive
           - Condescending
           - Microaggression
           - Implicit bias
           - Other
        3. [Explanation] Provide a detailed explanation of your classification. Include your chain of thoughts and reasoning behind categorizing the email as toxic or non-toxic, and why you assigned specific toxic categories. . Give reason, Chain of Thought for all the toxic categories assigned to the email in a point-wise manner. Explain any subtle or implicit forms of toxicity you identified.


        Base your classification strictly on the provided email content, subject, initial analysis and your reasoning. There can be single or multiple labels for an email. Here are some examples:
        {few_shot_examples}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}],
                functions=[self.function],
                function_call={"name": "classify_email"}
            )

            if response.choices[0].message.function_call:
                classification = json.loads(response.choices[0].message.function_call.arguments)
                
                # Validate and fix classification labels
                self._validate_classification_labels(classification)
                
                # Get additional attributes from utils functions
                task_related = check_task_related(subject, content)
                relationship_analysis = analyze_relationship(sender, recipient, subject, content)
                harmful_phrases = identify_harmful_phrases(content)
                microaggression_seen = detect_microaggressions(subject, content, timestamp) if task_related else 2

                # Construct the final output in the desired order
                final_output = {
                    'id': email_id,
                    'timestamp': timestamp,
                    'sender_name': sender,
                    'recipient_name': recipient,
                    'content': content,
                    'subject': subject,
                    'Non-toxic': classification.get('Non-toxic'),
                    'toxic': classification.get('toxic'),
                    'explanation': classification.get('Explanation'),
                    'harmful_phrases': harmful_phrases,
                    'relationship_analysis': relationship_analysis,
                    'task_related': 1 if task_related else 0,
                    'microaggression_seen': microaggression_seen
                }

                return final_output
            else:
                raise ValueError("Function call not present in the response")

        except Exception as e:
            print(f"Error in classify_email: {e}")
            return {"error": "Unable to classify email"}

    def _validate_classification_labels(self, classification):
        """Validate and fix classification labels for consistency."""
        non_toxic = classification.get('Non-toxic', 0)
        toxic_categories = classification.get('toxic', {})
        
        # Check if any toxic category is 1
        any_toxic = any(
            value == 1 
            for category in toxic_categories.values() 
            for value in (category.values() if isinstance(category, dict) else [category])
        )
        
        # If Non-toxic is 0 and no toxic categories are marked
        if non_toxic == 0 and not any_toxic:
            # Set 'Other' to 1 in toxic categories
            if isinstance(toxic_categories, dict):
                toxic_categories['Other'] = 1
        
        # If any toxic category is 1, ensure Non-toxic is 0
        elif any_toxic and non_toxic == 1:
            classification['Non-toxic'] = 0



