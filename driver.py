from twilio.rest import Client
import os
import locale

from pycoingecko import CoinGeckoAPI

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
cg = CoinGeckoAPI()

resp = cg.get_price(ids=os.environ['COINS'], vs_currencies='usd')

message = ""
for k in resp.keys():
    if message == "":
        message = k + ": " + locale.currency(float(resp[k]['usd']), grouping=True)
    else:
        message += "; " + k + ": " + locale.currency(float(resp[k]['usd']), grouping=True)

print(message)
if len(message) > 10:
    account_sid = os.environ['TWILIOAPI']
    auth_token  = os.environ['TWILIOSECRET']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=os.environ["TONUMBERS"],
        from_=os.environ["TWILIONUMBER"],
        body=message)
    print(message.sid)