from flask import FLask, request, redirect
from twilio.rest import Client

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])

account_sid = 'AC6543523cc0a87d4c3da895b76fa027d5'
auth_token = 'b6cf30d56a1d725f6974f2838ec9606e'

client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='TESTING HACKATHON!!',
                              from_='+18646591878',
                              to='+19253007799'
                          )

print(message.sid)

if __name__ == "__main__"