import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Page Configuration
st.set_page_config(
    page_title="Customer Support Analtics",
    page_icon="📊",
    layout="wide"
)

# Load Data
def load_data():
    df = pd.read_csv("/workspaces/Customer_Support_Pipeline/data/raw_comments.csv")
    df["created_at"] = pd.to_datetime(df['created_at'])
    return df

# Load trained model for live SLA predictions
@st.cache_resource
def load_model():
    with open("/workspaces/Customer_Support_Pipeline/models/sla_model.pkl", "rb") as f:
        return pickle.load(f)
    
df = load_data()
model = load_model()

# Dashboard Title
st.title("📊 Customer Support Analytics Dashboard")
st.markdown("Real time insights into customer support operations and SLA performance")

# Sidebar Filters
st.sidebar.title("Filters")

# Filter by category
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Filter by priority
selected_priority = st.sidebar.multiselect(
    "Select Priority",
    options=df['priority'].unique(),
    default=df['priority'].unique()
)

# Filter by channel
selected_channel = st.sidebar.multiselect(
    "Select Channel",
    options=df['channel'].unique(),
    default=df['channel'].unique()
)

# Apply filters to dataframe
filtered_df = df[
    (df['category'].isin(selected_category)) &
    (df['priority'].isin(selected_priority)) &
    (df['channel'].isin(selected_channel))
]

# Overview Metrics 

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Tickets", f"{len(filtered_df):,}")

with col2:
    review_count = filtered_df[filtered_df['sla_flag'] == 'Review Required'].shape[0]
    st.metric("Needs Review", f"{review_count:,}")

with col3:
    ok_count = filtered_df[filtered_df['sla_flag'] == 'OK'].shape[0]
    st.metric("SLA OK", f"{ok_count:,}")

with col4:
    high_priority = filtered_df[filtered_df['high_priority_flag'] == 1].shape[0]
    st.metric("High Priority", f"{high_priority:,}")

with col5:
    avg_likes = round(filtered_df['likes_count'].mean(), 1)
    st.metric("Avg Likes", avg_likes)

st.divider()

# Row 1 Charts 
col1, col2 = st.columns(2)

with col1:
    st.subheader("SLA Flag Breakdown")
    sla_counts = filtered_df['sla_flag'].value_counts().reset_index()
    sla_counts.columns = ['sla_flag', 'count']
    fig = px.pie(
        sla_counts,
        names='sla_flag',
        values='count',
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Priority Breakdown")
    priority_counts = filtered_df['priority'].value_counts().reset_index()
    priority_counts.columns = ['priority', 'count']
    fig = px.bar(
        priority_counts,
        x='priority',
        y='count',
        color='priority',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# Row 2 Charts 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tickets By Category")
    category_counts = filtered_df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']
    fig = px.bar(
        category_counts,
        x='count',
        y='category',
        orientation='h',
        color='count',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sentiment Distribution")
    sentiment_counts = filtered_df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    fig = px.pie(
        sentiment_counts,
        names='sentiment',
        values='count',
        color_discrete_sequence=['#3498db', '#95a5a6', '#e74c3c']
    )
    st.plotly_chart(fig, use_container_width=True)

