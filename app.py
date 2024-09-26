# app.py
from flask import Flask, request
import requests
import json
import logging 
import os 
from listener import ticket_availability

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Starting Flask App")
app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def index():
    verify_token = os.getenv('VERIFY_TOKEN')

    print('request args: ', request.args)

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

        print('ok now need to verify that', token,  verify_token, token == verify_token)

        if mode == 'subscribe' and token == verify_token:
            logging.info("WEBHOOK VERIFIED")
            challenge = request.args.get('hub.challenge')
            return challenge, 200
        else:
            logging.info("VERIFICATION FAILED")
            return "Verification failed", 403

    data = request.data # byte format 

    logging.error(f"Received data: {data}")

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

    # check ticket availability

    response_text = ticket_availability()
    if 'text' in message:
        response_text = f"""You just sent me: {message['text']}. My answer is: \n{response_text}"""
        response = {"text": response_text}
        
        send_message(sender_psid, response)
    else:
        response = {"text": f"Answer: \n{response_text}"}
        send_message(sender_psid, response)


def send_message(sender_psid, response):

    access_token = os.getenv('ACCESS_TOKEN')

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
    print('HELLO!')
    print('request args: ', request.args)
    print('request data: ', request.data)

    r = requests.post(f"https://graph.facebook.com/me/subscribed_apps?access_token={os.getenv('ACCESS_TOKEN')}", json={"subscribed_fields": ["messages", "messaging_postbacks", "messaging_referrals"]})
    response = r.json()
    if "success" in response:
        if response["success"] == True:
            print("Webhook subscriptions renewed")

    return f"Hello, World! Your Flask App is running on Heroku with HTTPS!"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)