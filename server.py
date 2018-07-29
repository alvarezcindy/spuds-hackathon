from flask import Flask, request, redirect, flash
from twilio.rest import Client
from twilio import twiml
import json
from twilio.twiml.messaging_response import MessagingResponse
# from pprint import pprin
import sys

app = Flask(__name__)

# importing remedies json file as a dictionary
json_string = open("remedies.json").read()
remedies_dict = json.loads(json_string)

# Twilip API authorization
account_sid = 'AC6543523cc0a87d4c3da895b76fa027d5'
auth_token = 'b6cf30d56a1d725f6974f2838ec9606e'

client = Client(account_sid, auth_token)

@app.route("/sms", methods=['POST','GET'])
def sms():
# twilio receives incoming text message
    number = request.form['From']
    body = request.form['Body']
    image = request.form['MediaContentType0']

    print(body)


    if image:
        image_url = request.values.get('MediaUrl0')
        print(image_url, file=sys.stderr)
    # image = request.values.get(‘MediaContentType0’)
    response = 'We got this!'
    resp = MessagingResponse()
    # resp = twiml.Response()
    resp.message('Hello! your ailment.')

    return str(resp)

#
# @app.route('/', methods=[POST])
# def geolocate_user():
#     """Find the user with cell towers and their phone #"""
#     https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyD_DOgSSqBrqTUFqeqeudDT6XlOtZ8huZQ

if __name__ == "__main__":
    app.run(debug=True)
    app.run(port=5000, host='0.0.0.0')
