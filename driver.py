from twilio.rest import Client
import os
import locale

from pycoingecko import CoinGeckoAPI


twilioapi = os.environ['TWILIOAPI']
twiliosecret = os.environ['TWILIOSECRET']
coins = os.environ['COINS']
tonumbers = os.environ["TONUMBERS"]
fromnumber = os.environ["TWILIONUMBER"]

if twiliosecret == None or twilioapi == None or coins == None or tonumbers == None or fromnumber == None:
    print("You need TWILIOAPI, TWILIOSECRET, COINS, TONUMBERS, TWILIONUMBER set as envvars.")
    exit(1)

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
cg = CoinGeckoAPI()

resp = cg.get_price(ids=coins, vs_currencies='usd')

message = ""
for k in resp.keys():
    if message == "":
        message = k + ": " + locale.currency(float(resp[k]['usd']), grouping=True)
    else:
        message += "; " + k + ": " + locale.currency(float(resp[k]['usd']), grouping=True)

print(message)
if len(message) > 10:
    account_sid = twilioapi
    auth_token  = twiliosecret

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=tonumbers,
        from_=fromnumber,
        body=message)
    print(message.sid)