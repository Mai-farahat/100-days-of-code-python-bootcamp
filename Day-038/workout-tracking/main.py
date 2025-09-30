from datetime import datetime
import os
import requests

GENDER = "female"
WEIGHT_KG = 39
HEIGHT_CM = 150
AGE = 21

APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ[
    "ENV_SHEETY_ENDPOINT"]
exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# bearer_headers = {
#     "Authorization": f"Bearer {os.environ['TOKEN']}"
# }

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # sheet_response = requests.post(
    #     sheet_endpoint,
    #     json=sheet_inputs,
    #     auth=(
    #         os.environ["ENV_SHEETY_USERNAME"],
    #         os.environ["ENV_SHEETY_PASSWORD"],
    #     )
    # )

    bearer_headers = {
        "Authorization": f"Bearer {os.environ['ENV_SHEETY_TOKEN']}"
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)

