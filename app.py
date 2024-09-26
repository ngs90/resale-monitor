# app.py
from flask import Flask, request
import requests
import json
import logging 
import os 
from listener import check_ticket_availability
from database_operations import register_ticket_availability, register_user_subscribe, register_user_unsubscribe

from config import VERIFY_TOKEN, ACCESS_TOKEN, TICKET_CHECK_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting Flask App")
app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def index():

    if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logging.info("WEBHOOK VERIFIED")
            challenge = request.args.get('hub.challenge')
            return challenge, 200
        else:
            logging.info("VERIFICATION FAILED")
            return "Verification failed", 403

    data = request.data # byte format 

    body = json.loads(data.decode('utf-8'))

    if 'object' in body and body['object'] == 'page':
        entries = body['entry']
        for entry in entries:
            webhook_event = entry['messaging'][0]
            print(webhook_event)

            sender_psid = webhook_event['sender']['id']
            print('senderpsid: ', sender_psid)

            if 'message' in webhook_event:
                handle_message(sender_psid, webhook_event['message'])

    return "OK", 200 # with respond with 200, otherwise fb will keep sending the message.

def handle_message(sender_psid, message):
    print('message: ', message)

    uri = "https://secure.onreg.com/onreg2/bibexchange/?eventid=6591&language=us"
    response_text = check_ticket_availability(uri)

    if 'text' in message and message['text'].lower() == 'subscribe':
        register_user_subscribe(sender_psid)
        response_text = f"""You have succesfully subscribed to the CPH marathon '25 ticket availability monitoring service."""
        response = {"text": response_text}
        send_message(sender_psid, response)
    elif 'text' in message and message['text'].lower() == 'unsubscribe':
        register_user_unsubscribe(sender_psid)
        reponse_text = f"""You have succefully unsubscribed to the CPH marathon '25 ticket availability monitoring service."""
        response = {"text": reponse_text}
        send_message(sender_psid, response)
    else:
        response = {"text": f"""Welcome to the CPH marathon '25 🏃‍♂️🏃‍♀️ ticket availability monitoring service.\n\nThis is a service that will write you a message on messenger if there is one or more tickets available on the resale platform.\n\nYour options:\nTo subscribe answer "SUBCRIBE" \nTo unsubscribe answer "UNSUBSCRIBE". \nThe current status on ticket availability: {response_text} \n\nSource: {uri}
                            """}
        availability = check_ticket_availability(TICKET_CHECK_URL)
        register_ticket_availability(availability)
        send_message(sender_psid, response)

def send_message(sender_psid, response):

    payload = {
        "recipient": {"id": sender_psid},
        "message": response,
        "messaging_type": "RESPONSE"
    }

    headers = {"content-type": "application/json"}

    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={ACCESS_TOKEN}"

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

@app.route('/')
def home():
    r = requests.post(f"https://graph.facebook.com/me/subscribed_apps?access_token={ACCESS_TOKEN}", json={"subscribed_fields": ["messages", "messaging_postbacks", "messaging_referrals"]})
    response = r.json()
    if "success" in response:
        if response["success"] == True:
            print("Webhook subscriptions renewed")

    return f"Welcome to the CPH Marathon 2025 ticket availability service. To sign up for the service write to the app via the facebook page: https://www.facebook.com/profile.php?id=61566582682564"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)