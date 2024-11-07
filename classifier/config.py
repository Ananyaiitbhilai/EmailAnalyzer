FUNCTION_DEFINITION = {
    "name": "classify_email",
    "description": "Classify an email based on toxicity, task-relatedness, relationship analysis, and identify harmful phrases",
    "parameters": {
        "type": "object",
        "properties": {
            "Non-toxic": {"type": "integer", "enum": [0, 1]},
            "toxic": {
                "type": "object",
                "properties": {
                    "Impolite: Sarcasm": {"type": "integer", "enum": [0, 1]},
                    "Impolite: Stereotype": {"type": "integer", "enum": [0, 1]},
                    "Impolite: Forced teaming": {"type": "integer", "enum": [0, 1]},
                    "Impolite: Authoritarian": {"type": "integer", "enum": [0, 1]},
                    "Impolite: Rude": {"type": "integer", "enum": [0, 1]},
                    "Impolite: Trivialising Sensitive topics": {"type": "integer", "enum": [0, 1]},
                    "Impolite: Lack of empathy": {"type": "integer", "enum": [0, 1]},
                    "Negative Gossip: Mocking": {"type": "integer", "enum": [0, 1]},
                    "Negative Gossip: Complain": {"type": "integer", "enum": [0, 1]},
                    "Offensive: Profanity": {"type": "integer", "enum": [0, 1]},
                    "Offensive: Discrimination": {"type": "integer", "enum": [0, 1]},
                    "Offensive: Bullying": {"type": "integer", "enum": [0, 1]},
                    "Offensive: Violence": {"type": "integer", "enum": [0, 1]},
                    "Offensive: Harassment": {"type": "integer", "enum": [0, 1]},
                    "Passive-aggressive": {"type": "integer", "enum": [0, 1]},
                    "Condescending": {"type": "integer", "enum": [0, 1]},
                    "Microaggression": {"type": "integer", "enum": [0, 1]},
                    "Other": {"type": "integer", "enum": [0, 1]}
                }
            },
            "Explanation": {"type": "string"},
            "task_related": {
                "type": "object",
                "properties": {
                    "is_task_related": {"type": "integer", "enum": [0, 1]},
                    "microaggression_seen": {"type": "integer", "enum": [0, 1]}
                },
                "required": ["is_task_related"]
            },
            "harmful_phrases": {"type": "array", "items": {"type": "string"}},
            "sender_name": {"type": "string"},
            "recipient_name": {"type": "string"},
            "relationship_analysis": {
                "type": "object",
                "properties": {
                    "professional_cordial": {"type": "integer", "enum": [0, 1]},
                    "professional_neutral": {"type": "integer", "enum": [0, 1]},
                    "professional_toxic": {"type": "integer", "enum": [0, 1]},
                    "playful_banter": {"type": "integer", "enum": [0, 1]},
                    "Collegial": {"type": "integer", "enum": [0, 1]},
                    "Mentor_Mentee": {"type": "integer", "enum": [0, 1]},
                    "Cross_Functional_Partnerships": {"type": "integer", "enum": [0, 1]},
                    "Too_personal": {"type": "integer", "enum": [0, 1]}
                }
            }
        },
        "required": ["toxic", "Non-toxic", "Explanation", "task_related", "harmful_phrases", "sender_name", "recipient_name", "relationship_analysis"]
    }
}