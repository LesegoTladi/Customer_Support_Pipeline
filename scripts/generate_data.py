import pandas as pd
import logging
import random
from faker import Faker

# Configure logging - used instead of print() for professional grade tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialise Faker - generates realistic fake data
fake = Faker()

# Seed for reproducibility - ensures same data generated every run
random.seed(42)
Faker.seed(42)

# Real support categories a call centre would handle
categories = [
    'Billing Issue',
    'Technical Support',
    'Account Access',
    'Product Complaint',
    'Refund Request',
    'Delivery Problem',
    'General Enquiry',
    'Service Cancellation'
]

# Real support channels
channels = ['Email', 'Phone', 'Chat', 'Social Media', 'WhatsApp']

# Real ticket statuses
statuses = ['Open', 'Closed', 'Pending', 'Escalated', 'Resolved']

# Real priority levels
priorities = ['Low', 'Medium', 'High', 'Critical']

# Real sentiment values
sentiments = ['Positive', 'Neutral', 'Negative']

# Real agent names
agents = [
    'Lesego Tladi', 'Thabo Nkosi', 'Priya Patel',
    'John Smith', 'Amara Diallo', 'Sarah Johnson',
    'Mohammed Ali', 'Zanele Mokoena', 'David Chen'
]

# Load the cleaned API data from clean_transform.py
api_df = pd.read_csv("data/cleaned_comments.csv")
logging.info(f"Loaded {len(api_df)} real API records from cleaned_comments.csv")

# Add missing columns to API data with realistic random values
# Must add category, channel, status, priority BEFORE using them in flags
api_df['category'] = [random.choice(categories) for _ in range(len(api_df))]
api_df['channel'] = [random.choice(channels) for _ in range(len(api_df))]
api_df['status'] = [random.choice(statuses) for _ in range(len(api_df))]
api_df['priority'] = [random.choice(priorities) for _ in range(len(api_df))]
api_df['sentiment'] = [random.choice(sentiments) for _ in range(len(api_df))]
api_df['agent_name'] = [random.choice(agents) for _ in range(len(api_df))]
api_df['created_at'] = [fake.date_time_between(
    start_date='-1y',
    end_date='now'
).strftime('%Y-%m-%d %H:%M:%S') for _ in range(len(api_df))]

# Add source column to track where each record came from
api_df['source'] = 'API'

# High priority flag - now safe to apply because priority column exists
api_df['high_priority_flag'] = api_df['priority'].apply(
    lambda x: 1 if x in ['High', 'Critical'] else 0
)

# SLA flag - now safe to apply because comment_length exists from clean_transform.py
api_df['sla_flag'] = api_df['comment_length'].apply(
    lambda x: 'Review Required' if x > 100 else 'OK'
)

logging.info("API data enriched with additional columns")

# Calculate how many synthetic records we need to reach 10,000
records_needed = 10000 - len(api_df)
logging.info(f"Generating {records_needed} synthetic records to reach 10,000 total")

records = []

for i in range(1, records_needed + 1):

    category = random.choice(categories)

    comment_map = {
        'Billing Issue': fake.sentence(nb_words=random.randint(10, 30)),
        'Technical Support': fake.sentence(nb_words=random.randint(15, 35)),
        'Account Access': fake.sentence(nb_words=random.randint(8, 20)),
        'Product Complaint': fake.sentence(nb_words=random.randint(20, 40)),
        'Refund Request': fake.sentence(nb_words=random.randint(10, 25)),
        'Delivery Problem': fake.sentence(nb_words=random.randint(12, 30)),
        'General Enquiry': fake.sentence(nb_words=random.randint(5, 15)),
        'Service Cancellation': fake.sentence(nb_words=random.randint(15, 35))
    }

    record = {
        'comment_id': i,
        'ticket_id': random.randint(1000, 9999),
        'comment_text': comment_map[category],
        'category': category,
        'channel': random.choice(channels),
        'status': random.choice(statuses),
        'priority': random.choice(priorities),
        'sentiment': random.choice(sentiments),
        'agent_name': random.choice(agents),
        'likes_count': random.randint(0, 50),
        'user_id': random.randint(1, 500),
        'username': fake.user_name(),
        'full_name': fake.name(),
        'created_at': fake.date_time_between(
            start_date='-1y',
            end_date='now'
        ).strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'Synthetic'
    }

    records.append(record)

# Convert synthetic records to DataFrame
synthetic_df = pd.DataFrame(records)
logging.info(f"Generated {len(synthetic_df)} synthetic records")

# Comment length helps identify complex support tickets
synthetic_df['comment_length'] = synthetic_df['comment_text'].apply(len)

# Engagement flag - 1 means customer interacted, 0 means no interaction
synthetic_df['is_engaged'] = synthetic_df['likes_count'].apply(
    lambda x: 1 if x > 0 else 0
)

# SLA flag - comments longer than 100 chars flagged for agent review
synthetic_df['sla_flag'] = synthetic_df['comment_length'].apply(
    lambda x: 'Review Required' if x > 100 else 'OK'
)

# High priority flag - critical and high priority tickets flagged
synthetic_df['high_priority_flag'] = synthetic_df['priority'].apply(
    lambda x: 1 if x in ['High', 'Critical'] else 0
)

# Concatenate real API data and synthetic data into one dataset
combined_df = pd.concat([api_df, synthetic_df], ignore_index=True)
logging.info(f"Combined dataset total: {len(combined_df)} records")

# Preview first 5 rows
print(combined_df.head())

# Save combined dataset
combined_df.to_csv("data/raw_comments.csv", index=False)
logging.info("Combined dataset saved to data/raw_comments.csv")