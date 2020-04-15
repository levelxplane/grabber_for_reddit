#!/usr/bin/env python
import os

def api():
    return {
        'BASE_API': 'https://reddit.com/api/v1/',
        'KEY': os.getenv('REDDIT_KEY', 'aksdlfjlkajsd'),
        'SECRET': os.getenv('REDDIT_SECRET', 'asdfjl;aksjdlf'),
        'USERNAME': os.getenv('REDDIT_USERNAME', 'derpname'),
        'PW': os.getenv('REDDIT_PW', 'derpword') ,
        'TWILIO_ID': os.getenv('TWILIO_ID', 'poop' ),
        'TWILIO_KEY': os.getenv('TWILIO_KEY', 'poop')
    }
