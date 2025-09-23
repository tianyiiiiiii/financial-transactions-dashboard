import streamlit as st
import pandas as pd

df = pd.read_csv("financial_transactions.csv")

st.set_page_config(page_title="Financial Transactions Data Exploration", layout="wide")
st.title("📊 Data Exploration")

st.write(df.head())
st.write("Summary:", df.describe(include='all'))
st.write("Shape:", df.shape)

st.subheader("Filter Data")
columns = df.columns.tolist()
selected_column = st.selectbox("Select Column to filter by", columns)
unique_valus = df[selected_column].unique()
selected_value = st.selectbox("Select Value", unique_valus)
filtered_df = df[df[selected_column] == selected_value]
st.write(filtered_df)

st.write("Missing Values:", df.isnull().sum())
st.write("Duplicates:", df.duplicated().sum())