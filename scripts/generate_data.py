import pandas as pd
import logging
import random

#faker - used to generate fake data 
from faker import Faker

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format= ('%(asctime)s | %(levelname)s | %(message)s')
)

#Intialise Faker
fake=Faker()

#Ensure same data generated every run
random.seed(42)
Faker.seed(42)

# Load Real API Data First
api_df=pd.read_csv("data/raw_comments.csv")

# Real support categories a call centre would handle
categories= [
    "Billing Issue",
    "Techical Support",
    "Account Access",
    "Product Complaint",
    "Refund Request",
    "Delivery Problem",
    "General Enquiry",
    "Service Cancellation"
]

#support channels
channels=['Email','Phone','Chat','Social Media','WhatsAPP']

#ticket status
statuses= ['Open','Closed','Pending', 'Esclated','Resolved']

#priority level
priorities=['Low','Medium', 'High']

#sentiment values
sentiments=['Positive','Neutral','High']

# agent names
agents = [
    'Lesego Tladi', 'Thabo Nkosi', 'Priya Patel',
    'John Smith', 'Amara Diallo', 'Sarah Johnson',
    'Mohammed Ali', 'Zanele Mokoena', 'David Chen']

# Generate synthetic records to fill up to 10000
#calculate how may sythetic record we need
records_needed=10000 - len(api_df)
print(f'Generating {records_needed} synthetic records')

records= []

for i in rage(len(api_df) +1.10001):
    category = random.choice(categories)

    comment_map={
        
    }

