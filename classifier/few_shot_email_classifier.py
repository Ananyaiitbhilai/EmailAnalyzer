few_shot_examples = """
### Few-shot Examples

Example 1:
[Email] 
Subject: Meeting Rescheduling 
Content: "Hey, how are you holding up? Can you please reschedule the meeting for tomorrow?" 
[/Email]
[NonToxic] 1
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 2:
[Email] 
Subject: Today is the review-meeting 
Content: "You need big glasses huh, LOL!!!? It's 11:00AM" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 1, "Implicit bias": 0, "Other": 0}

Example 3:
[Email] 
Subject: Office Potluck 
Content: "Ladies, since you all are good at cooking and are used to it, I invite you to participate for potluck in office." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 4:
[Email] 
Subject: Information about new-policy 
Content: "We all are victims of the new policy. Let the retaliation begin!" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 1, "Impolite: Authoritarian": 0, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 5:
[Email] 
Subject: Urgent Request for Numbers 
Content: "I want you to give me the numbers by 9PM today. I do not have time to wait until tomorrow." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 6:
[Email] 
Subject: Project discussion meeting 
Content: "I did not want to yell at you in front of everyone, but you are performing poorly!" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 7:
[Email] 
Subject: On a vacation 
Content: "When I take a long time I am slow and when my boss takes a long time, he is thorough." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 8:
[Email] Subject: Office poster presentation 
Content: "How does this guy function in society?" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 9:
[Email] 
Subject: Let's buck up 
Content: "Let's kiss their ass and get it done." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 1, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 1, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 10:
[Email] 
Subject: Who you are? 
Content: "Would you rather be called African-American or black?" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 1, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 11:
[Email] 
Subject: The Tags! 
Content: "Whoever is doing these tags is brain dead enough to send the wrong tag." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 12:
[Email] 
Subject: Don't be Lazy 
Content: "All Africans are lazy and don't deserve to work here." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 1, "Other": 0}

Example 13:
[Email] 
Subject: Hey, there! 
Content: "Your backside is banging in that dress." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 14:
[Email] 
Subject: Project Update Request 
Content: "Hi team, could you please send me your progress reports by end of day Friday? Let me know if you need any help or have questions." [
/Email]
[NonToxic] 1
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 15:
[Email] 
Subject: Team Building Activity 
Content: "I'm organizing a voluntary team lunch next week to celebrate our recent project completion. Please let me know if you'd like to join!" 
[/Email]
[NonToxic] 1
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 0, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 16:
[Email] 
Subject: Missed Deadline 
Content: "Oh great job, Einstein! You've only missed the third deadline this month. Setting a new record?" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 17:
[Email] 
Subject: New Software Implementation 
Content: "Wow, this new system is so 'user-friendly' that even a toddler could mess it up faster than you!" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 18:
[Email] 
Subject: Tech Support Request 
Content: "Can we get someone young to handle this? You know how these older folks struggle with technology." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 19:
[Email] 
Subject: Team Assignment 
Content: "Let's put John in charge of the numbers. You know how good Asians are with math." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 20:
[Email] 
Subject: Overtime Request 
Content: "We're all in this together, right? So you won't mind staying late every day this week to meet the deadline." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 1, "Impolite: Authoritarian": 1, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 21:
[Email] 
Subject: Budget Cuts 
Content: "As a family, we need to tighten our belts. I'm sure you understand why your raise isn't happening this year."
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 1, "Impolite: Authoritarian": 1, "Impolite: Rude": 0, "Impolite: Trivialising Sensitive topics": 1, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 22:
[Email] 
Subject: Project Changes 
Content: "I've decided to change the entire project scope. Make it happen by next week, no excuses." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 23:
[Email] 
Subject: Vacation Request 
Content: "Your vacation request is denied. I don't care about your plans, the company comes first." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 1, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 24:
[Email] 
Subject: Presentation Feedback 
Content: "Your presentation was a complete waste of everyone's time. Do better next time." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 25:
[Email] 
Subject: Meeting Interruption 
Content: "Can you stop talking? Your ideas are useless and you're just slowing us down." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 26:
[Email] 
Subject: New Hire 
Content: "Did you see the new guy's attempt at using the copier? I swear, a monkey could do better!" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 27:
[Email] 
Subject: Team Lead's Decision 
Content: "Our fearless leader strikes again with another brilliant idea. I can't wait to see how this one fails spectacularly." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 28:
[Email] 
Subject: Manager's Decision 
Content: "Can you believe what Sarah did in the meeting? She always takes credit for everyone else's work." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 29:
[Email] 
Subject: Office Politics 
Content: "Mark only got that promotion because he's always sucking up to the boss. It's so unfair." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 1, "Condescending": 0, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 30:
[Email] 
Subject: Project Delays 
Content: "This f***ing project is a complete sh*tshow. Get your act together!" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 1, "Offensive: Profanity": 1, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 31:
[Email] 
Subject: Equipment Malfunction 
Content: "Who the hell broke the printer again? I swear, you're all useless pieces of cr*p!" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 1, "Offensive: Profanity": 1, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 32:
[Email] 
Subject: Hiring Decision 
Content: "We shouldn't hire her. Women always end up leaving for maternity leave anyway." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 1, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 0, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 33:
[Email] 
Subject: Team Assignment 
Content: "Let's not put any Muslims on the client-facing team. It might make some customers uncomfortable." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 1, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 1, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 1, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 1, "Other": 0}

Example 34:
[Email] 
Subject: Performance Review 
Content: "You're lucky we even keep you around. Maybe you should start looking for a job more suited to your limited abilities." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 1, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 35:
[Email] 
Subject: Team Meeting 
Content: "Oh look, the village idiot has something to say. This should be good for a laugh." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 1, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 1, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 36:
[Email] 
Subject: Conflict Resolution 
Content: "If you don't fix this mess, I swear I'll come over there and knock some sense into you." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 1, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 37:
[Email] 
Subject: Project Frustration 
Content: "One more screw-up like that and I'll make sure you never work in this industry again." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 1, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 1, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 1, "Microaggression": 0, "Implicit bias": 0, "Other": 0}

Example 38:
[Email] 
Subject: After-work Invitation 
Content: "Come on, loosen up and have a drink with me. I promise I'll make it worth your while." 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 1, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 0, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 0, "Other": 0}

Example 39:
[Email] 
Subject: Office Attire 
Content: "That new outfit really shows off your assets. Why don't you wear things like that more often?" 
[/Email]
[NonToxic] 0
[Toxic] {"Impolite: Sarcasm": 0, "Impolite: Stereotype": 0, "Impolite: Forced teaming": 0, "Impolite: Authoritarian": 0, "Impolite: Rude": 1, "Impolite: Trivialising Sensitive topics": 1, "Impolite: Lack of empathy": 1, "Negative Gossip: Mocking": 0, "Negative Gossip: Complain": 0, "Offensive: Profanity": 0, "Offensive: Discrimination": 0, "Offensive: Bullying": 0, "Offensive: Violence": 0, "Offensive: Harassment": 1, "Passive-aggressive": 0, "Condescending": 0, "Microaggression": 1, "Implicit bias": 1, "Other": 0}
"""


few_shot_task_related = """
### Few-shot Examples

1. Example (Task-related):
[Email]
Subject: Project X Update Required
Content: Hi team, I need everyone to send me their progress reports on Project X by Friday. Please include any challenges you're facing and your estimated completion dates for your assigned tasks.
[/Email]
[TaskRelated] 1

2. Example (Not task-related):
[Email]
Subject: Office Party Next Week
Content: Just a reminder that we're having our annual office party next Friday at 6 PM. Don't forget to RSVP if you haven't already. Looking forward to seeing everyone there!
[/Email]
[TaskRelated] 0

3. Example (Task-related):
[Email]
Subject: Quarterly Review Meeting
Content: Hello all, This is to inform you that our quarterly review meeting is scheduled for next Tuesday at 10 AM. Please come prepared with your department's performance metrics and goals for the next quarter.
[/Email]
[TaskRelated] 1

4. Example (Not task-related):
[Email]
Subject: Happy Birthday!
Content: Hey Sarah, Just wanted to wish you a very happy birthday! Hope you have a fantastic day filled with joy and celebration. Cheers!
[/Email]
[TaskRelated] 0

5. Example (Task-related):
[Email]
Subject: Urgent: Client Presentation Feedback Needed
Content: Hi John, I've attached the draft of our client presentation for tomorrow. Could you please review it and provide your feedback by 5 PM today? We need to finalize it before the meeting.
[/Email]
[TaskRelated] 1

6. Example (Not task-related):
[Email]
Subject: Lunch Today?
Content: Hey Lisa, I was wondering if you'd like to grab lunch together today. I heard there's a new sushi place that just opened up down the street. Let me know if you're free!
[/Email]
[TaskRelated] 0

7. Example (Task-related):
[Email]
Subject: New Project Assignment
Content: Dear Mark, I'm assigning you to lead our new marketing campaign for Product Y. Please start putting together a team and draft an initial strategy by next week. We'll discuss the budget and timeline in our upcoming meeting.
[/Email]
[TaskRelated] 1

8. Example (Not task-related):
[Email]
Subject: Company Newsletter - April Edition
Content: Dear all, The April edition of our company newsletter is now available. You can find it attached to this email. It includes updates on recent company events, employee spotlights, and upcoming social activities.
[/Email]
[TaskRelated] 0

"""


few_shot_workspace_relationship = """

Example 1:

[Email]
Sender: John Smith
Recipient: Sarah Johnson
Subject: Quick question about the Q3 report
Content: Hi Sarah, I hope this email finds you well. I was reviewing the Q3 report and had a quick question about the sales figures on page 5. Could you clarify where the data for the European market came from? Thanks in advance for your help! Best, John
[/Email]

[Relationship]
- professional_cordial: 1
- professional_neutral: 0
- professional_toxic: 0
- playful_banter: 0
- Collegial: 1
- Mentor_Mentee: 0
- Cross_Functional_Partnerships: 0
[/Relationship]

Example 2:

[Email]
Sender: Alex Rodriguez
Recipient: Pat Chen
Subject: RE: Project Falcon Update
Content: Pat, I'm extremely disappointed with the lack of progress on Project Falcon. Your team has missed the last two deadlines, and the client is getting impatient. I need a detailed explanation of these delays and a revised timeline on my desk by EOD tomorrow. No excuses.
[/Email]

[Relationship]
- professional_cordial: 0
- professional_neutral: 0
- professional_toxic: 1
- playful_banter: 0
- Collegial: 0
- Mentor_Mentee: 0
- Cross_Functional_Partnerships: 0
[/Relationship]

Example 3:

[Email]
Sender: Jamie Lee
Recipient: Chris Wong
Subject: Lunch plans?
Content: Hey work bestie! 🍔🍟 Ready for our weekly lunch escape? I vote we try that new Thai place down the street. I hear their tom yum soup is to die for! Let me know if you're in, or if you want to stick to our usual spot. Either way, I'm counting down the minutes till our midday gossip session! 😉
[/Email]

[Relationship]
- professional_cordial: 0
- professional_neutral: 0
- professional_toxic: 0
- playful_banter: 1
- Collegial: 1
- Mentor_Mentee: 0
- Cross_Functional_Partnerships: 0
[/Relationship]

Example 4:

[Email]
Sender: Dr. Emily Tanner
Recipient: Michael Novak
Subject: Research progress and next steps
Content: Dear Michael, I hope this email finds you well. I've reviewed the initial results from your experiment, and I'm impressed with your methodology. However, I think we need to consider adjusting the control group parameters. Let's schedule a meeting to discuss this further and plan the next phase of your research. I'm excited to see how your work progresses. Best regards, Dr. Tanner
[/Email]

[Relationship]
- professional_cordial: 1
- professional_neutral: 0
- professional_toxic: 0
- playful_banter: 0
- Collegial: 0
- Mentor_Mentee: 1
- Cross_Functional_Partnerships: 0
[/Relationship]
"""

few_shot_microagression = """
Example 1:
[Email]
Subject: Team meeting reminder
Content: Hey guys, just a quick reminder about our team meeting tomorrow at 10 AM. Don't forget to bring your ideas - we need all hands on deck for this project!
[/Email]
[Microaggression] 1
Explanation: The use of "guys" as a general term for a mixed-gender group can be considered a microaggression, as it uses male-centric language that may make women or non-binary individuals feel excluded.
Example 2:
[Email]
Subject: New project assignment
Content: Hi everyone, I'm assigning the new marketing campaign to Sarah. She's great with creative tasks, and we know women have a natural flair for this kind of work.
[/Email]
[Microaggression] 1
Explanation: This email contains a gender-based stereotype, suggesting that women are naturally better at creative tasks, which is a form of microaggression.
Example 3:
[Email]
Subject: Diversity training follow-up
Content: Thank you all for attending yesterday's diversity training. I'm impressed by how articulate and well-spoken our minority team members were during the discussion.
[/Email]
[Microaggression] 1
Explanation: Expressing surprise at how "articulate" minority team members are can be a microaggression, as it implies a preconceived notion that they wouldn't be well-spoken.
Example 4:
[Email]
Subject: Project deadline update
Content: Hello team, I wanted to inform you that we're extending the project deadline by one week. Please adjust your schedules accordingly and let me know if you have any questions or concerns.
[/Email]
[Microaggression] 0
Explanation: This email contains no microaggressions. It's a straightforward, professional communication about a deadline change.
Example 5:
[Email]
Subject: Office potluck announcement
Content: Hi all, we're organizing an office potluck next Friday. Please bring a dish to share if you'd like to participate. We welcome all types of cuisine and will ensure there are options for various dietary restrictions.
[/Email]
[Microaggression] 0


"""