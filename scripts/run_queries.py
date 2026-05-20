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

# Query 1 - SLA Flag Breakdown
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

# Query 3 — Average Comment Length Per SLA Flag 
length_query = """
    SELECT 
        sla_flag,
        ROUND(AVG(comment_length), 2) AS avg_comment_length,
        MAX(comment_length) AS max_comment_length,
        MIN(comment_length) AS min_comment_length
    FROM customer_support_comments
    GROUP BY sla_flag
"""
length_df = pd.read_sql(length_query, engine)
logging.info("Comment Length Analysis:")
print(length_df)

# Query 4 — Tickets By Category 
category_query = """
    SELECT 
        category,
        COUNT(*) AS total_tickets,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
    FROM customer_support_comments
    GROUP BY category
    ORDER BY total_tickets DESC
"""
category_df = pd.read_sql(category_query, engine)
logging.info("Tickets By Category:")
print(category_df)

# Query 5 — Priority Breakdown 
priority_query = """
    SELECT 
        priority,
        COUNT(*) AS total,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
    FROM customer_support_comments
    GROUP BY priority
    ORDER BY total DESC
"""
priority_df = pd.read_sql(priority_query, engine)
logging.info("Priority Breakdown:")
print(priority_df)

# Save query results to reports folder for later use in dashboard
sla_df.to_csv("reports/sla_breakdown.csv", index=False)
users_df.to_csv("reports/top_engaged_users.csv", index=False)
length_df.to_csv("reports/comment_length_analysis.csv", index=False)
category_df.to_csv("reports/category_breakdown.csv", index=False)
priority_df.to_csv("reports/priority_breakdown.csv", index=False)
logging.info("All query results saved to reports/")