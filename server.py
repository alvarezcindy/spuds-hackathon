from flask import Flask, request, redirect, flash
from twilio.rest import Client
from twilio import twiml
import json
import requests
from twilio.twiml.messaging_response import MessagingResponse
# from pprint import pprin
import sys

app = Flask(__name__)

# importing remedies json file as a dictionary
json_string = open("remedies.json").read()
remedies_dict = json.loads(json_string)

# Twilip API authorization
account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

@app.route("/sms", methods=['POST','GET'])
def sms():
# twilio receives incoming text message
    number = request.form['From']
    body = request.form['Body']
    image = request.values.get('MediaContentType0')
    FromCity = request.values.get('FromCity')
    print(FromCity)
    FromState = request.values.get('FromState')
    print(FromCity)
    FromZip = request.values.get('FromZip')
    print(FromCity)
    print(body)
    resp = MessagingResponse()
    if 'clinics' in body:
        resp.message("Some nearby affordable hospitals are \n 1. Clinica Monument - Pleasant Hill, Location: 2.48 miles from Walnut Creek \n 2. El Cerrito Health Center El Cerrito Health Center - Concord, Location: 2.76 miles from Walnut Creek")
        return str(resp)

    if 'Thanks' or 'Thank you' in body:
        resp.message("Your welcome!")
        return str(resp)
    if image:
        image_url = request.values.get('MediaUrl0')
        api_1 = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/2536b569-70fe-47fd-8d44-d17bdee86539/url?iterationId=6d83ffad-cc8c-4995-a2f4-fd6012eb00fc"
        headers = {'Content-Type': 'application/json', 'Prediction-Key': '3a56dd99e664490ea22e789ab702a110'}
        payload = json.dumps({'Url': str(image_url)})
        resp_1 = requests.post(api_1, headers=headers, data=payload)
        problem_1 = resp_1.json()['predictions'][0]['tagName']
        prob=str(problem_1)

    else:
        api_2 = requests.get(
            'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/ff06620c-fbd3-4b45-9c27-e74bd2fc256e?subscription-key=f7713074ac8842908a0bab60b0153486&verbose=true&timezoneOffset=0&q=' + body)
        print(api_2.json(),file=sys.stderr)
        problem_1 = api_2.json()['entities'][0]['type']

        prob=str(problem_1)



    message = client.messages.create(to=number, from_='+18646591878', body=remedies(prob))
    # message = client.messages.create(to=number, from_='+18646591878', body=location_serv(FromCity))
    return "True"




def remedies(prob):
    with open("remedies.json", 'r') as fileHandler:
        respjson = json.load(fileHandler)
        rem = respjson[prob]
        return str("You might be experiencing {} \n".format(prob) + rem)

def location_serv(place):
        with open("locations.json", 'r') as fileHandler:
            respjson = json.load(fileHandler)
            rem = respjson[place]
            return str(" {} ".format(place) + rem)

#
# @app.route('/', methods=[POST])
# def geolocate_user():
#     """Find the user with cell towers and their phone #"""
#     https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyD_DOgSSqBrqTUFqeqeudDT6XlOtZ8huZQ

if __name__ == "__main__":
    app.run(debug=True)
    app.run(port=5000, host='0.0.0.0')
