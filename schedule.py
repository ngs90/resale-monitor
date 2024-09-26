import requests
from listener import check_ticket_availability
from database_operations import register_ticket_availability
from database import Session, UserSubscription
from dotenv import load_dotenv
load_dotenv()
from config import TICKET_CHECK_URL, ACCESS_TOKEN

def send_message(sender_psid, response):
    payload = {
        "recipient": {"id": sender_psid},
        "message": response,
        "messaging_type": "RESPONSE"
    }
    headers = {"content-type": "application/json"}
    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={ACCESS_TOKEN}"
    response = requests.post(url, json=payload, headers=headers)
    print(f"Besked sendt til {sender_psid}: {response.status_code}")

def main():
    availability = check_ticket_availability(TICKET_CHECK_URL)
    register_ticket_availability(availability)
    
    # Hvis der er billetter tilgængelige, send beskeder til abonnenter
    if availability > 0:
        with Session() as session:
            subscribers = session.query(UserSubscription).all()
            for subscriber in subscribers:
                message = {
                    "text": f"Good news. There are now tickets available for the CPH Marathon '25. Check them out here: {TICKET_CHECK_URL}"
                }
                send_message(subscriber.user_psid, message)

if __name__ == "__main__":
    main()