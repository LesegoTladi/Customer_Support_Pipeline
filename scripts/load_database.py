import pandas as pd
import logging
from sqlalchemy import create_engine, text

# Configure logging - used instead of print() for professional grade tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load cleaned data from previous step
df = pd.read_csv("data/cleaned_comments.csv")
logging.info(f"Loaded {len(df)} records from cleaned_comments.csv")

# Create SQLite database engine - creates a local database file
# No server or password needed - perfect for development
engine = create_engine("sqlite:///data/customer_support.db")

# Load DataFrame into database table
# if_exists='replace' - drops and recreates table each run
df.to_sql(
    name="customer_support_comments",
    con=engine,
    if_exists="replace",
    index=False
)
logging.info("Data loaded into customer_support_comments table")

# Verify data loaded correctly by querying it back
with engine.connect() as conn:

    # Count total records
    result = conn.execute(text("SELECT COUNT(*) FROM customer_support_comments"))
    count = result.fetchone()[0]
    logging.info(f"Verified {count} records in database")

    # Check SLA flag breakdown
    result = conn.execute(text("""
        SELECT sla_flag, COUNT(*) as total
        FROM customer_support_comments
        GROUP BY sla_flag
    """))
    rows = result.fetchall()
    for row in rows:
        logging.info(f"SLA Flag: {row[0]} — Count: {row[1]}")