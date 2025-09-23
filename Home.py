import streamlit as st
import pandas as pd

st.set_page_config(page_title="Financial Transactions", page_icon="💳", layout="wide")
st.title("💳 Financial Transactions")

st.write("Use the sidebar pages or the links below to explore the data and view analytics.")
st.page_link("pages/1_Dashboard_Analytics.py", label="📈 Dashboard & Analytics")
st.page_link("pages/2_Data_Exploration.py", label="📊 Data Exploration")
st.page_link("pages/3_Mockup_Chatbot.py", label="🤖 Mockup Chatbot")
st.page_link("pages/4_Outlier_Detection.py", label="⚠️ Outlier Detection")
