import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'

)

#Load full combined dataset
df =pd.read_csv("/workspaces/Customer_Support_Pipeline/data/raw_comments.csv")

#Dataset Info
print(f"Rows : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print(df.dtypes)

# Mising Values check
#Identify colums with missing data
missing_values=df.isnull().sum()
missing_pct =  (missing_values/len(df)*100).round(2)
missing_df=pd.DataFrame({
    'missing_count': missing_values,
    'missing_percentage': missing_pct
    })

# Only show columns that are actually have missing values
missing_df = missing_df[missing_df['missing_count']>0]
if missing_df.empty:
    print("No missing values found")
else:
    print(missing_df)

# Duplicate records check
duplicates=df.duplicated().sum()
print(f"Total duplicate rows: {duplicates}")

# Check duplicates based on comment_id only
id_duplicates  =df.duplicated(subset=['comment_id']).sum()
print(f"Duplicated comment IDs:{id_duplicates }")

# Values distribution check
# Ensure categorical columns have expected values only
print(df['sla_flag'].value_counts())

print(df['priority'].value_counts())

print(df['status'].value_counts())

print(df['channel'].value_counts())

print(df['sentiment'].value_counts())

print(df['source'].value_counts())

#Check for outliers and unepected ranges
print(df[['likes_count', 'comment_length', 'is_engaged', 'high_priority_flag']].describe())
# Flag records where likes_count is unsually high
likes_outliers = df[df['likes_count']>45]

# Ensure all dates fall within expected range
df['created_at'] = pd.to_datetime(df['created_at'])
print(f"Earliest record : {df['created_at'].min()}")
print(f"Latest record   : {df['created_at'].max()}")

# Summarise all quality checks into one report
quality_report = {
    'total_records': [len(df)],
    'total_columns': [df.shape[1]],
    'missing_values': [missing_values.sum()],
    'duplicate_rows': [duplicates],
    'duplicate_comment_ids': [id_duplicates],
    'likes_outliers': [len(likes_outliers)],
    'date_range_start': [df['created_at'].min()],
    'date_range_end': [df['created_at'].max()],
    'sla_ok_count': [df[df['sla_flag'] == 'OK'].shape[0]],
    'sla_review_count': [df[df['sla_flag'] == 'Review Required'].shape[0]],
    'high_priority_count': [df[df['high_priority_flag'] == 1].shape[0]],
    'api_records': [df[df['source'] == 'API'].shape[0]],
    'synthetic_records': [df[df['source'] == 'Synthetic'].shape[0]]
}

# Convert quality report to DataFrame and save
report_df = pd.DataFrame(quality_report)
report_df.to_csv("reports/data_quality_report.csv", index=False)
logging.info("Data quality report saved to reports/data_quality_report.csv")
