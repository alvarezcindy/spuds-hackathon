from flask import Flask, request, redirect, flash
from twilio.rest import Client
import json
from pprint import pprint

app = Flask(__name__)

# importing remedies json file as a dictionary
json_string = open("remedies.json").read()
remedies_dict = json.loads(json_string)

# Twilip API authorization
account_sid = 'AC6543523cc0a87d4c3da895b76fa027d5'
auth_token = 'b6cf30d56a1d725f6974f2838ec9606e'

client = Client(account_sid, auth_token)

@app.route("/sms")
def sms_reply():
# twilio receives incoming text message

message = client.messages.create(
                              body='TESTING HACKATHON!!',
                              from_='+18646591878',
                              to='+19253007799'
                          )

@app.route('/', methods=[POST])
def geolocate_user():
    """Find the user with cell towers and their phone #"""
    https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyD_DOgSSqBrqTUFqeqeudDT6XlOtZ8huZQ
    
print(message.sid)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(port=5000, host='0.0.0.0')
