import requests 
import regex as re 
from bs4 import BeautifulSoup


def ticket_availability(uri):

    response = requests.get(uri)
    soup = BeautifulSoup(response.text, 'html.parser')

    text = soup.get_text()

    if "There are currently no race numbers for sale. Try again later." in text:
        return "No race numbers for sale"
    else:
        return f"""There seems to be race numbers for sale.\n\nGo check them out here:\n{uri}"""

    print('message:', message)

# # Send message via Meta Graph API
# def send_fb_besked(modtager_psid, besked_tekst):
#     access_token = "EAALTB3GWwuQBO5pxZCYyfAes3eZAtV7VwTshC3PmDE91kpxujjyMYgffniOpw75MS1gqweNQOu6LMpy8xQnNw3og3TclW4w0ijZB3yZAbzEXObJuiwBn2aEfM5eWuWAdzGHuHZCcsEKwZBxlugQ9VcnqlFjrKGm4SgqEpMESaWyvHspddfEOo7gRyZB5B7rV0jXaXwSN39sBVfs3FUZD"
#     page_id = "61566582682564" # "794978877358820"
#     api_version = "v20.0"  # Opdater dette til den nyeste version efter behov
    
#     url = f"https://graph.facebook.com/{api_version}/{page_id}/messages"
    
#     payload = {
#         "recipient": {"id": modtager_psid},
#         "message": {"text": besked_tekst},
#         "messaging_type": "MESSAGE_TAG",
#         "tag": "CONFIRMED_EVENT_UPDATE"
#     }
    
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     response = requests.post(url, json=payload, headers=headers)
    
#     if response.status_code == 200:
#         print(f"Besked sendt til {modtager_psid}: {besked_tekst}")
#     else:
#         print(f"Fejl ved afsendelse af besked: {response.text}")

# # Erstat 'MODTAGER_PSID' med den faktiske modtager-PSID
# send_fb_besked('MODTAGER_PSID', message)

# #print(soup.get_text())