import pandas as pd
import logging
from sqlalchemy  import create_engine

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# connect to existing SQLite database
engine= create_engine("sqlite:///data/customer_support.db")

#Query 1 - SLA Flag Breakdown
sla_query="""

SELECT 
    sla_flag,
    COUNT(*) as total,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(),2) AS percentage
FROM customer_support_comments
GrOUP BY sla_flag

"""

sla_df =pd.read_sql(sla_query,engine)
logging.info("SLA FLag Breakdown:")
print(sla_df)


# Query 2 — Top 10 Most Engaged Users 
users_query = """
    SELECT 
        username,
        full_name,
        SUM(likes_count) AS total_likes,
        COUNT(comment_id) AS total_comments
    FROM customer_support_comments
    GROUP BY username, full_name
    ORDER BY total_likes DESC
    LIMIT 10
"""
users_df = pd.read_sql(users_query, engine)
logging.info("Top 10 Most Engaged Users:")
print(users_df)