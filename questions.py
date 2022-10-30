import random

questions = [
    'What are your three core values?', 
    'What is one thing you desire to do right now?', 
    'What is a big goal you wish to achieve this year?'
]

def get_question():
    return random.choice(questions)