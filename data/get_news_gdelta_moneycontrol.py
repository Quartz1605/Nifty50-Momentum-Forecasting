import requests
from datetime import datetime, timedelta
import pandas as pd
import io

# Define time window
end_date = datetime(2025, 9, 13)
start_date = end_date - timedelta(days=90)

url = "https://api.gdeltproject.org/api/v2/doc/doc"

all_articles = []

# Loop in 7-day chunks
chunk = timedelta(days=7)
cur_start = start_date

while cur_start < end_date:
    cur_end = min(cur_start + chunk, end_date)

    params = {
        "query": '"Nifty 50" domain:moneycontrol.com',       # add quotes like in Postman
        "mode": "ArtList",           # FIX: correct case
        "format": "CSV",             # FIX: more stable than JSON
        "maxrecords": "250",
        "startdatetime": cur_start.strftime("%Y%m%d%H%M%S"),
        "enddatetime": cur_end.strftime("%Y%m%d%H%M%S")
    }

    

    res = requests.get(url, params=params)

    # Parse CSV response directly into DataFrame
    try:
        df_chunk = pd.read_csv(io.StringIO(res.text))
        all_articles.append(df_chunk)
        print(f"{cur_start.date()} → {cur_end.date()} : {len(df_chunk)} articles")
    except Exception as e:
        print(f"Error fetching {cur_start} → {cur_end}: {e}")

    cur_start = cur_end

# Merge all chunks into one DataFrame
if all_articles:
    df = pd.concat(all_articles, ignore_index=True)
    df.to_csv("nifty50_gdelt_last3months_indian.csv", index=False)
    print("✅ Total Articles Collected:", len(df))
else:
    print("⚠️ No data collected")