import pandas as pd
import logging
import pickle

#scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.preprocessing import LabelEncoder

# Configure logging
logging.basicConfig(

    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Load the combined dataset
df =pd.read_csv('/workspaces/Customer_Support_Pipeline/data/raw_comments.csv')
print(f"Loaded {len(df)} records for model training")

# Feature Selection
features=[
    'comment_length',
    'likes_count',
    'is_engaged',
    'high_priority_flag',
    'category',
    'channel',
    'priority',
    'sentiment'
]

# Target column
target = 'sla_flag'

# Encode Categorical Columns
le =LabelEncoder()

#Encode each categorical column separately
categorical_columns =['category', 'channel', 'priority', 'sentiment']

for col in categorical_columns:
    df[col]=le.fit_transform(df[col])

logging.info("Categorical columns encoded successfully")
