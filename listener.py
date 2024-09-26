import requests 
from bs4 import BeautifulSoup

def check_ticket_availability(uri):

    response = requests.get(uri)
    soup = BeautifulSoup(response.text, 'html.parser')

    text = soup.get_text()

    if "There are currently no race numbers for sale. Try again later." in text:
        return 0 # "No race numbers for sale"
    else:
        return 1 # f"""There seems to be race numbers for sale.\n\nGo check them out here:\n{uri}"""
