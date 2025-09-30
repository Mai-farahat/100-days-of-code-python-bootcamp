import requests
from datetime import datetime

USERNAME = "mayosh"
TOKEN = "hjutfdxduioohbbhpkmv"
GRAPH_ID = "graph1"
pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Programming graph",
    "unit": "hr",
    "type": "float",
    "color": "ajisai",
}
headers = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

post_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

#today = datetime.now()
today = datetime(year=2024, month=8, day=18)
post_config = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "7",
}
# response = requests.post(url=post_endpoint, json=post_config, headers=headers)
# print(response.text)

pixela_update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
put_config = {
    "quantity": "3",
}
response = requests.put(url=pixela_update_endpoint, json=put_config, headers=headers)
print(response.text)

# response = requests.delete(url=pixela_update_endpoint, json=put_config, headers=headers)
# print(response.text)

