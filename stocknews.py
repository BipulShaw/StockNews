import requests
from twilio.rest import Client

STOCK_NAME = "META"
COMPANY_NAME = "Facebook"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"

STOCK_API_KEY = "7UJ8IKCOXV1GURLA"
NEWS_API_KEY = "6e8b2c7ac2f243b28d82c6ed91f0dbc8"

TWILIO_SID = "ACc0316b22da647a3c164483f320b415ad"
TWILIO_AUTH_TOKEN = "a9a1f1e8dd1a3c2e729c1d0f176dd433"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params = stock_params)


#data from yesterday
data = response.json()["Time Series (Daily)"]
#Converting dict to list for easy access to yesterdays' data
data_list = [value for (key, value) in data.items()]
yester_data = data_list[0]
yester_close_price = yester_data["4. close"]
print(yester_close_price)


#Day before yesterday closing stock price
befor_yester = data_list[1]
befor_yester_clos = befor_yester["4. close"]
print(befor_yester_clos)

#Difference between yesterday and day before yesterday price
diff = abs(float(yester_close_price) - float(befor_yester_clos))
emoji = None
if float(yester_close_price) - float(befor_yester_clos) > 0:
    emoji = "⬆️"
else:
    emoji = "⬇️"

print(diff)

#Percentage difference
diff_percent = (diff/float(yester_close_price))*100;
print(diff_percent)

#Get news
if diff_percent > 0.5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_resp = requests.get(NEWS_ENDPOINT, params = news_params)
    articles = news_resp.json()["articles"]
    # print(articles)

#Slicing the article data
three = articles[:3]
print(three)

#Create the formatted message to be sent
formatted = [f"{STOCK_NAME}: {emoji}{round(diff_percent, 3)}%\n 📰 Headline: {article['title']}.\n 🌐 Read Here: {article['url']}" for article in three]

#Send each article as a separate message via Twilio.
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in formatted:
    message = client.messages.create(
        body = article,
        from_= "+19517499080",
        to = "+918240970952"
    )