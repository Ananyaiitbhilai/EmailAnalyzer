from openai import OpenAI
import re
from datetime import datetime
from few_shot_email_classifier import few_shot_task_related, few_shot_workspace_relationship, few_shot_microagression

# Add client initialization
client = OpenAI()

def analyze_timestamp(timestamp):
    try:
        email_time = datetime.strptime(timestamp, "%a, %d %b %Y %H:%M:%S %z")
        hour = email_time.hour

        if 9 <= hour < 17:
            return "Sent during regular work hours"
        elif 17 <= hour < 22:
            return "Sent after regular work hours"
        else:
            return "Sent late at night or early morning"
    except ValueError:
        return "Unable to parse timestamp"


def check_task_related(subject, content):
    prompt = f"""
    Determine if the following email is task-related by analyzing both the subject and content:

    [Email]
    Subject: {subject}
    Content: {content}
    [/Email]

    An email is considered task-related if it meets ANY of the following criteria:
    1. Requests specific actions or deliverables
    2. Discusses ongoing projects or work-related activities
    3. Sets deadlines or mentions timelines
    4. Involves work assignments or responsibilities

    Respond ONLY with one of the following labels:
    [TaskRelated] 1
    [TaskRelated] 0

    Base your decision strictly on the provided email content. Here are some examples:

    0. Example (Task-related):
    [Email]
    Subject: Quarterly Review Meeting
    Content: Hello all, This is to inform you that our quarterly review meeting is scheduled for next Tuesday at 10 AM. Please come prepared with your department's performance metrics and goals for the next quarter.
    [/Email]
    [TaskRelated] 1

    {few_shot_task_related}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip().split()[-1]
        return int(result)
    except Exception as e:
        print(f"Error in check_task_related: {e}")
        return 0


def analyze_relationship(sender, recipient, subject, content):
    prompt = f"""
    Analyze the relationship between the sender and recipient based on the email content and subject:

    [Email]
    Sender: {sender}
    Recipient: {recipient}
    subject: {subject}
    Content: {content}
    [/Email]

    Consider the following aspects:
    1. Tone of communication (formal, informal, friendly, hostile)
    2. Level of familiarity (colleagues, friends, superior-subordinate)
    3. Any indications of previous interactions or shared history
    4. Power dynamics evident in the language used

    Provide a brief analysis of the relationship using ONLY the following labels:
    [Relationship]
    - professional_cordial: 1 or 0
    - professional_neutral: 1 or 0
    - professional_toxic: 1 or 0
    - playful_banter: 1 or 0
    - Collegial: 1 or 0
    - Mentor_Mentee: 1 or 0
    - Cross_Functional_Partnerships: 1 or 0
    - Too_personal: 1 or 0
    [/Relationship]

    Base your analysis strictly on the provided email content. There can be single or multiple labels for an email.  Here are some examples:
    {few_shot_workspace_relationship}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract the [Relationship] block from the response
        relationship_block = re.search(r'\[Relationship\](.*?)\[/Relationship\]', 
                                       response.choices[0].message.content, 
                                       re.DOTALL)
        
        if relationship_block:
            # Parse the relationship block into a dictionary
            relationship_dict = {}
            for line in relationship_block.group(1).strip().split('\n'):
                key, value = line.split(':')
                key = key.strip('- ').strip()
                value = int(value.strip())
                relationship_dict[key] = value
            
            # Ensure all expected keys are present
            expected_keys = [
                "professional_cordial", "professional_neutral", "professional_toxic",
                "playful_banter", "Collegial", "Mentor_Mentee", "Cross_Functional_Partnerships"
            ]
            for key in expected_keys:
                if key not in relationship_dict:
                    relationship_dict[key] = 0
            
            return {"relationship_analysis": relationship_dict}
        else:
            raise ValueError("Relationship block not found in the response")
    
    except Exception as e:
        print(f"Error in analyze_relationship: {e}")
        return {"relationship_analysis": {k: 0 for k in [
            "professional_cordial", "professional_neutral", "professional_toxic",
            "playful_banter", "Collegial", "Mentor_Mentee", "Cross_Functional_Partnerships"
        ]}}

def identify_harmful_phrases(content):
    prompt = f"""
    Analyze the following email content and identify any harmful, toxic, or inappropriate phrases:

    [Email]
    Content: {content}
    [/Email]

    Instructions:
    1. Look for phrases that could be considered offensive, derogatory, abusive words, discriminatory, or inappropriate in a workplace context.
    2. Identify subtle microaggressions or phrases that might be harmful in certain contexts.
    3. Consider the overall tone and context when identifying phrases.
    4. Return an array of harmful phrases found in the content.

    Format your response as follows:
    [HarmfulPhrases]
    - "harmful phrase 1"
    - "harmful phrase 2"
    - ...
    [/HarmfulPhrases]

    If no harmful phrases are found, respond with:
    [HarmfulPhrases]
    []
    [/HarmfulPhrases]

    Base your analysis strictly on the provided email content. There can be single or multiple harmful phrases in an email. Do not infer or assume information not present in the given data. Even in non-toxic emails some slightly or subtle harmful phrases might be present.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract the content between [HarmfulPhrases] tags
        content = response.choices[0].message.content.strip()
        start = content.find('[HarmfulPhrases]') + len('[HarmfulPhrases]')
        end = content.rfind('[/HarmfulPhrases]')
        phrases_content = content[start:end].strip()
        
        # Split the content into a list, removing empty lines
        harmful_phrases = [phrase.strip('- ').strip() for phrase in phrases_content.split('\n') if phrase.strip()]
        
        return harmful_phrases
    except Exception as e:
        print(f"Error in identify_harmful_phrases: {e}")
        return []

def detect_microaggressions(content, subject, timestamp):
    analysis_email_time = analyze_timestamp(timestamp)
    
    prompt = f"""
    Analyze the following email content, subject, and timestamp to determine if there are any microaggressions present:

    [Email]
    Subject: {subject}
    Content: {content}
    analysis_Timestamp: {analysis_email_time}
    [/Email]

    Instructions:
    1. Evaluate the overall tone and context of the message.
    2. Pay special attention to time-sensitive requests and how they relate to the timestamp.
       For example, urgent requests sent late at night or early morning might be considered microaggressive.

    Respond ONLY with one of the following labels:
    [Microaggression] 1 (if microaggressions are detected)
    [Microaggression] 0 (if no microaggressions are detected)

    Base your decision on the provided email content, subject, and analysis_Timestamp. Here are some examples:
    [Email]
    Subject: Urgent: Code needed
    Content: Please send the code right now. I need it ASAP.
    Timestamp: Sent late at night or early morning
    [/Email]
    [Microaggression] 1 (This could be considered microaggressive due to the urgent demand made at an inappropriate time)
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return int(response.choices[0].message.content.strip().split()[-1])
    except Exception as e:
        print(f"Error in detect_microaggressions: {e}")
        return 0