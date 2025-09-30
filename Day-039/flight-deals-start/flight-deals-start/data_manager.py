import requests
from pprint import pprint
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/5ecbf44d11a7aef36b1970057b67ee0a/flightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._user = os.environ["SHEETY_USRERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        # pprint(data)

        return self.destination_data


    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)


