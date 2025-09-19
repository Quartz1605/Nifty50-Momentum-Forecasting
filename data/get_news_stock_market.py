from dotenv import load_dotenv
import os
from newsapi import NewsApiClient
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

api_key = os.getenv("NEWSAPI_KEY")
newsapi = NewsApiClient(api_key=api_key)


yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

everything = newsapi.get_everything(
    q='India stock market OR Sensex OR Nifty',
    from_param=yesterday,
    to=datetime.now().strftime('%Y-%m-%d'),
    language='en',
    sort_by='publishedAt'
)

articles = everything['articles']

df = pd.DataFrame([{
  'source' : article['source']['name'],
  'author' : article['author'],
  'title' : article['title'],
  'description' : article['description'],
  'url' : article['url'],
  'published_at' : article['publishedAt']
}for article in articles])



df.to_csv("indian_stock_market_news_datewise.csv", index=False, encoding="utf-8")