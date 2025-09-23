import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("financial_transactions.csv")

st.set_page_config(page_title="Financial Transactions Visualisation", layout="wide")
st.title("📊 Data Visualisation")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(df):,}")
col2.metric("Total Amount", f"{df['amount'].sum():,.2f}")
col3.metric("Average Amount", f"{df['amount'].mean():,.2f}")
col4.metric("Median Amount", f"{df['amount'].median():,.2f}")

st.subheader("Plot Data")

# ensure date column is datetime
if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

columns = ["date", "amount", "category", "merchant",
           "payment_method", "account_type", "transaction_type"]
col = st.selectbox("Choose a column to visualize", columns)

# for date column: time series
if col == "date" and "date" in df.columns:
    frequency = st.selectbox("Frequency", ["D (daily)", "W (weekly)", "M (monthly)"], index=2)
    metric = st.selectbox("Metric", ["Transaction count", "Sum of amount", "Mean amount"], index=0)

    rule = {"D (daily)": "D", "W (weekly)": "W", "M (monthly)": "M"}[frequency]
    d = df.dropna(subset=["date"]).set_index("date").sort_index()

    if metric == "Transaction count":
        series = d["id"].resample(rule).count() if "id" in d.columns else d.resample(rule).size()
        ylab = "Count"
        title = f"Transactions over time ({frequency[0]})"
    elif metric == "Sum of amount":
        series = d["amount"].resample(rule).sum()
        ylab = "Sum of amount"
        title = f"Sum of amount over time ({frequency[0]})"
    else:
        series = d["amount"].resample(rule).mean()
        ylab = "Mean amount"
        title = f"Mean amount over time ({frequency[0]})"

    x = series.index
    if isinstance(x, pd.PeriodIndex):
        x = x.to_timestamp()
    x = pd.to_datetime(x, errors="coerce").to_numpy()
    y = series.to_numpy()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, y)
  
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylab)
    st.pyplot(fig)

# amount column: histogram + box plot
elif col == "amount":
    bins = st.slider("Number of bins", 5, 30, 10)
    series = pd.to_numeric(df["amount"], errors="coerce").dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(series, bins=bins)
    ax.set_title("Histogram of amount")
    ax.set_xlabel("amount")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots(figsize=(6, 1.8))
    ax2.boxplot(series, vert=False)
    ax2.set_title("Box plot of amount")
    ax2.set_xlabel("amount")
    st.pyplot(fig2)

# categorical columns: bar chart
else:
    agg_mode = st.selectbox("Y value", ["Count (value_counts)", "Sum of amount", "Mean amount"], index=0)
    top_n = st.slider("Top N categories", 5, 40, 20)
    sort_choice = st.selectbox("Sort by", ["Count/Metric (desc)", "Label (A→Z)"], index=0)

    s = df[col].copy()

    # counts
    if agg_mode == "Count (value_counts)":
        series = s.value_counts(dropna=False)
        ylab = "Count"
        title = f"Distribution of {col}"
    else:
        g = df.groupby(col)["amount"]
        series = g.sum() if agg_mode == "Sum of amount" else g.mean()
        ylab = "Sum of amount" if agg_mode == "Sum of amount" else "Mean amount"
        title = f"{ylab} by {col}"

    # sorting + top N
    if sort_choice == "Label (A→Z)":
        series = series.sort_index()
    else:
        series = series.sort_values(ascending=False)
    series = series.head(top_n)

    # plot
    fig, ax = plt.subplots(figsize=(9, 5))
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(col)
    ax.set_ylabel(ylab)
    ax.tick_params(axis="x", rotation=45, labelrotation=45)
    st.pyplot(fig)

st.subheader("🔥 Heatmaps")

heatmap_choice = st.selectbox(
    "Choose a heatmap",
    [
        "Category x Payment Method (count)",
        "Category x Merchant (count, top 20 merchants)",
        "Month x Category (sum of amount)",
        "Correlation of daily features (sum / mean / count)"
    ],
    index=0
)

# --- Category x Payment Method (count)
if heatmap_choice == "Category x Payment Method (count)":
    if all(c in df.columns for c in ["category", "payment_method"]):
        ct = pd.crosstab(df["category"], df["payment_method"])
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(ct, annot=True, fmt=".0f", linewidths=.5, ax=ax)
        ax.set_title("Frequency: Category x Payment Method")
        st.pyplot(fig)
    else:
        st.info("Need 'category' and 'payment_method' columns.")

# --- Category x Merchant (count, top N merchants)
elif heatmap_choice == "Category x Merchant (count, top 20 merchants)":
    if all(c in df.columns for c in ["category", "merchant"]):
        topN = st.slider("Top N merchants", 5, 40, 20)
        top_merchants = df["merchant"].value_counts().head(topN).index
        sub = df[df["merchant"].isin(top_merchants)]
        ct = pd.crosstab(sub["category"], sub["merchant"])
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(ct, annot=True, fmt=".0f", linewidths=.5, ax=ax)
        ax.set_title(f"Frequency: Category x Top-{topN} Merchants")
        st.pyplot(fig)
    else:
        st.info("Need 'category' and 'merchant' columns.")

# --- Month x Category (sum of amount)
elif heatmap_choice == "Month x Category (sum of amount)":
    if "date" in df.columns and "amount" in df.columns:
        dd = df.dropna(subset=["date"]).copy()
        dd["month"] = pd.to_datetime(dd["date"]).dt.to_period("M").dt.to_timestamp()
        piv = pd.pivot_table(
            dd, index="month", columns="category", values="amount",
            aggfunc="sum", fill_value=0.0
        )
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(piv, annot=False, cmap="YlGnBu", ax=ax)
        ax.set_title("Monthly Spend by Category (sum of amount)")
        st.pyplot(fig)
    else:
        st.info("Need 'date' and 'amount' columns.")

# --- Correlation heatmap of engineered daily features
elif heatmap_choice == "Correlation of daily features (sum / mean / count)":
    if "date" in df.columns and "amount" in df.columns:
        dly = (df.dropna(subset=["date"])
                 .set_index(pd.to_datetime(df["date"], errors="coerce"))
                 .sort_index()
                 .resample("D")
                 .agg(amount_sum=("amount", "sum"),
                      amount_mean=("amount", "mean"),
                      transaction_count=("amount", "count"))
              )
        corr = dly.corr()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(corr, annot=True, vmin=-1, vmax=1, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation of Daily Features")
        st.pyplot(fig)
    else:
        st.info("Need 'date' and 'amount' columns.")
