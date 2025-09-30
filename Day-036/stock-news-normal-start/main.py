import requests
from twilio.rest import Client

account_sid = "AC5ba5c9b829f7644b73e84b4ab1fa2f5b"
auth_token = "1e9014dc9cd25433db7e1d807095b37c"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = "03F81GROWR3ZLX7B"
NEWS_API_KEY = "0a0aecacc1f14ab087470457c2d8d123"


    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
positive_diff = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(positive_diff)

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = (positive_diff / float(yesterday_closing_price)) * 100
print(percentage_difference)

#If TODO4 percentage is greater than 5 then print("Get News").
if percentage_difference > 0.5:
#     print("Get News")

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_param = {
        "qInTitle": COMPANY_NAME,
        "apikey": NEWS_API_KEY,
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_param)
    news_response.raise_for_status()
    news_articles =news_response.json()["articles"]
    print(news_articles)
#Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    first_3_articles = news_articles[0:3]
    print(first_3_articles)
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title
    # and description to your phone number.

#- Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article_list = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in first_3_articles]
    print(formatted_article_list)
#Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in formatted_article_list:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=article,
            to='whatsapp:+201094449984'
        )
        print(message.status)


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

