import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API endpoint
url = "https://dummyjson.com/comments"

logging.info("Starting API extraction...")

# Send GET request
response = requests.get(url)

# Convert API response to JSON
data = response.json()

# Extract comments section
comments = data["comments"]

# Convert to DataFrame
df = pd.DataFrame(comments)

logging.info(f"Extracted {len(df)} records from API")

# Show first rows
print(df.head())

# Save raw data
df.to_csv("data/raw_comments.csv", index=False)

logging.info("Raw data saved to data/raw_comments.csv")
logging.info("Data extracted successfully!")
