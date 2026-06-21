import os

import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
MY_LNG = 121.534563
MY_LAT = 25.026456
parameters = {
    "lat": MY_LAT,
    "lon": MY_LNG,
    "appid": api_key,
    "cnt": 4
}
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()
data = response.json()

will_rain = False
for hour in data["list"]:
    weather_id = hour["weather"][0]["id"]
    if int(weather_id) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="+16812756586",
        to="+886989190620",
    )
    print(message.status)




