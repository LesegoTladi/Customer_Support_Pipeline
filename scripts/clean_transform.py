
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting data cleaning and transformation...")

# Load Raw Data
df = pd.read_csv("data/raw_comments.csv")
logging.info(f"Loaded {len(df)} records from raw_comments.csv")

# Inspect Data
logging.info(f"Columns: {df.columns.tolist()}")
logging.info(f"Shape: {df.shape}")
logging.info(f"Missing values:\n{df.isnull().sum()}")

# Rename Columns 
df.rename(columns={
    'id': 'comment_id',
    'body': 'comment_text',
    'postId': 'ticket_id',
    'likes': 'likes_count'
}, inplace=True)
logging.info("Columns renamed successfully")

# Clean Text Column 
df['comment_text'] = df['comment_text'].str.strip().str.lower()
logging.info("Comment text cleaned")

#  Handle Missing Values ──────────────────────────────────
df['comment_text'].fillna('no comment', inplace=True)
df['likes_count'].fillna(0, inplace=True)
logging.info("Missing values handled")

# Extract User Info
df['user_id'] = df['user'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
df['username'] = df['user'].apply(lambda x: x['username'] if isinstance(x, dict) else None)
df['full_name'] = df['user'].apply(lambda x: x['fullName'] if isinstance(x, dict) else None)
df.drop(columns=['user'], inplace=True)
logging.info("User info extracted")

# Feature Engineering 
# Comment length
df['comment_length'] = df['comment_text'].apply(len)

# Engagement flag
df['is_engaged'] = df['likes_count'].apply(lambda x: 1 if x > 0 else 0)

# SLA flag — comments longer than 100 chars flagged for review
df['sla_flag'] = df['comment_length'].apply(lambda x: 'Review Required' if x > 100 else 'OK')

logging.info("Feature engineering completed")
logging.info(f"SLA flags:\n{df['sla_flag'].value_counts()}")

# Final Inspection 
logging.info(f"Cleaned data shape: {df.shape}")
logging.info(f"Columns: {df.columns.tolist()}")
print(df.head())

# Save Cleaned Data
df.to_csv("data/cleaned_comments.csv", index=False)
logging.info("Cleaned data saved to data/cleaned_comments.csv")
logging.info("Data cleaning and transformation complete!")
