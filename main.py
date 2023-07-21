import requests
from datetime import date
from datetime import timedelta
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
MY_MOBILE = ''

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

APY_KEY_Alpha_Vantage = "NURUSL8SZ0HDZDE0"
APY_KEY_news = "55a954b676d040c9a74b305858c8fec9"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": APY_KEY_Alpha_Vantage,
}

tesla_price_reguest = requests.get(url=STOCK_ENDPOINT, params=parameters)
tesla_price_reguest.raise_for_status()
tesla_price = tesla_price_reguest.json()

date = date.today()
yesterday_date = date - timedelta(days=1)
yesterday_date_str = str(yesterday_date)
day_before_yesterday_str = str(date - timedelta(days=2))

yesterday_tesla_closing_price = (tesla_price["Time Series (Daily)"][yesterday_date_str]["4. close"])
day_before_yesterday_tesla_closing_price = (tesla_price["Time Series (Daily)"][day_before_yesterday_str]["4. close"])



absolute_deference_prices = abs(float(yesterday_tesla_closing_price) - float(day_before_yesterday_tesla_closing_price))

average = (float(yesterday_tesla_closing_price) + float(day_before_yesterday_tesla_closing_price)) / 2
percentage_difference = round((absolute_deference_prices / average) * 100, 2)

if percentage_difference >= 5:

    parameters_news = {
        "q": "keyword="+COMPANY_NAME,
        "apiKey": APY_KEY_news
    }
    tesla_news_request = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    tesla_news = tesla_news_request.json()

    top_3_tesla_news = tesla_news["articles"][:2]

    article_points = [f"Headline: {news['title']}.\nArticle: {news['description']}" for news in top_3_tesla_news]
    print(article_points)

    if float(yesterday_tesla_closing_price) >= float(day_before_yesterday_tesla_closing_price):
        arrow = "🔺"
    else:
        arrow = "🔻"


    for x in article_points:
        text_massage = f"""
            TSLA: {arrow} {percentage_difference}%\n{x}"""
        account_sid = "ACdaf9bc4967bed2a843319922ca615247"
        auth_token = "7c0b880b9dc23677f3ceb6c395cf41ed"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=text_massage,
            from_='+12176802639',
            to=MY_MOBILE
        )
        print(message.status)

