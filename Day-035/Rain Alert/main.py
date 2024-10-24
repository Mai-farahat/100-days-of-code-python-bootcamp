import requests
from twilio.base.exceptions import TwilioRestException
import os
from twilio.rest import Client

api_key = "b8b3ee18396a3599e7c6a4d6ae221792"
MY_LAT = 46.020714
MY_LONG = 7.749117
account_sid = "AC5ba5c9b829f7644b73e84b4ab1fa2f5b"
auth_token = "1e9014dc9cd25433db7e1d807095b37c"
will_rain = False


parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="It's going to rain today. Remember to bring an ☂️.",
        to='whatsapp:+201094449984'
    )
    print(message.status)








