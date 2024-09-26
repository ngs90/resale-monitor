import os 

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TICKET_CHECK_URL = "https://secure.onreg.com/onreg2/bibexchange/?eventid=6591&language=us"
DATABASE_URL = os.getenv('DATABASE_URL').replace('postgres', 'postgresql')