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

#Encode target column
df[target]= df[target].apply(lambda x:1 if x== 'Review Required' else 0)

# Prepare features and target
X=df[features]
y=df[target]

#Split data into training and testing sets
X_train,X_test,y_train,y_test = train_test_split(
    X,y,
    test_size= 0.2,
    random_state=42
)

logging.info(f"Training set size : {len(X_train)} records")
logging.info(f"Testing set size  : {len(X_test)} records")

# Train Random Forest Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train,y_train)
logging.info("Model training complete")

# Evaluate Model Performance
y_pred = model.predict(X_test)

# Accuracy - percentage of correct predictions
accuracy = accuracy_score(y_test,y_pred)
logging.info(f"Model accuracy: {round(accuracy * 100, 2)}%")


# Performance report showing precision , recall , f1-score
print(classification_report(y_test, y_pred, target_names=['OK', 'Review Required']))

# Confusion matrix shows correct vs incorrect predictions
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm,
    index=['Actual OK', 'Actual Review Required'],
    columns=['Predicted OK', 'Predicted Review Required']
)
print(cm_df)

# Shows which features had the most impact on predictions
feature_importance_df = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance_df)

# Save feature importance to reports folder
feature_importance_df.to_csv("reports/feature_importance.csv", index=False)
logging.info("Feature importance saved to reports/feature_importance.csv")

# pickle saves the trained model so it can be loaded later
# in the dashboard without retraining
with open("models/sla_model.pkl", "wb") as f:
    pickle.dump(model, f)

logging.info("Trained model saved to models/sla_model.pkl")
logging.info("Machine learning pipeline complete")