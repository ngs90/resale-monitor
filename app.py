# app.py
from flask import Flask, request
import requests
import json
import logging 
import os 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting Flask App")
app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def index():
    verify_token = os.getenv('VERIFY_TOKEN')

    if 'hub.mode' in request.args:
        mode = request.args.get('hub.mode')
        print(mode)
    if 'hub.verify_token' in request.args:
        token = request.args.get('hub.verify_token')
        print(token)
    if 'hub.challenge' in request.args:
        challenge = request.args.get('hub.challenge')
        print(challenge)

    if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')

        if mode == 'subscribe' and token == verify_token:
            print("WEBHOOK VERIFIED")
            challenge = requests.args.get('hub.challenge')
            return challenge, 200
        else:
            return "Verification failed", 403


    data = requests.data # byte format 
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

def handle_message(sender_psid, message):
    print('message: ', message)

    if 'text' in message:
        reponse = {"text": f"You just sent me: {message['text']}"}
        send_message(sender_psid, response)
    else:
        response = {"text": "This chatbot only accepts text messages"}
        send_message(sender_psid, response)


def send_message(sender_psid, response):

    access_token = config.ACCESS_TOKEN

    payload = {
        "recipient": {"id": sender_psid},
        "message": response,
        "messaging_type": "RESPONSE"
    }

    headers = {"content-type": "application/json"}

    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={access_token}"

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

@app.route('/')
def home():
    return f"Hello, World! Your Flask App is running on Heroku with HTTPS!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)