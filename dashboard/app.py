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
    
df=load_data()
model=load_model()

