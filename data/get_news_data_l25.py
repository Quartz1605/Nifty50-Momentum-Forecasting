from datetime import datetime, timedelta
import pandas as pd
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NEWSAPI_KEY")
newsapi = NewsApiClient(api_key=api_key)

all_articles = []

# Define your start and end dates
start_range = datetime(2025, 8, 20)
end_range = datetime(2025, 9, 11)

# Loop through each day in the range
current_date = start_range
while current_date <= end_range:
    start_date = current_date.strftime('%Y-%m-%d')
    end_date = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')

    print(f"📅 Fetching articles from {start_date} to {end_date}")

    # 🔑 Only one request per day (free tier = page=1 only)
    response = newsapi.get_everything(
        q="India stock market OR Sensex OR Nifty",
        from_param=start_date,
        to=end_date,
        language="en",
        sort_by="publishedAt",
        page_size=100,
        page=1
    )

    articles = response.get("articles", [])

    for article in articles:
        all_articles.append({
            "source": article["source"]["name"] if article.get("source") else None,
            "author": article.get("author"),
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "published_at": article.get("publishedAt"),
            "content": article.get("content")
        })

    # ✅ move to next date
    current_date += timedelta(days=1)

# Save all collected articles
df = pd.DataFrame(all_articles)
df.to_csv("india_stock_market_Aug20_to_Sep11.csv", index=False, encoding="utf-8")

print(f"✅ Saved {len(df)} articles to india_stock_market_Aug20_to_Sep11.csv")



