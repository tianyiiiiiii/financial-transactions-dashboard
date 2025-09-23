import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Outliers", page_icon="⚠️", layout="wide")
st.title("⚠️ Outlier Detection (IQR Method)")

df = pd.read_csv("financial_transactions.csv")

df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

st.write("We detect outliers using the **Interquartile Range (IQR) method**, "
         "which is robust and widely used for skewed financial data like transaction amounts.")

# --- IQR Detection ---
amt = df["amount"].dropna()
q1, q3 = amt.quantile([0.15, 0.85])
iqr = q3 - q1
k = st.slider("IQR multiplier (k)", 0.5, 3.0, 1.5, 0.1)

upper = q3 + k * iqr
lower_toggle = st.checkbox("Also flag unusually small values (below Q1 - k*IQR)", value=False)
lower = q1 - k * iqr

if lower_toggle:
    mask = (df["amount"] > upper) | (df["amount"] < lower)
    threshold_text = f"Outliers are values > {upper:,.2f} or < {lower:,.2f}"
else:
    mask = df["amount"] > upper
    threshold_text = f"Outliers are values > {upper:,.2f}"

outliers = df[mask]

st.subheader("Results")
st.markdown(f"- Q1 = **{q1:,.2f}**, Q3 = **{q3:,.2f}**, IQR = **{iqr:,.2f}**")
st.markdown(f"- {threshold_text}")
st.markdown(f"- Found **{len(outliers):,}** outlier transactions.")

if not outliers.empty:
    st.dataframe(outliers.head(20), use_container_width=True, hide_index=True)
    csv = outliers.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Outliers (CSV)", data=csv, file_name="outliers.csv", mime="text/csv")
else:
    st.info("No outliers found with current settings.")

st.markdown("---")
st.subheader("Why only IQR?")
st.markdown("""
- **Z-score**: assumes data is normally distributed. Financial transactions are usually skewed and heavy-tailed, so Z-scores misclassify many values.  
- **Mahalanobis distance**: requires multivariate numeric features and an invertible covariance matrix. Our dataset is mostly categorical with one main numeric column (`amount`), so it adds little value.  
- **k-Nearest Neighbors (kNN)**: useful for high-dimensional anomaly detection, but computationally heavier and less interpretable for a simple financial dataset.  
- **Isolation Forest**: a tree-based anomaly detection method from scikit-learn. It works well on large, high-dimensional datasets, but is more complex, less interpretable, and unnecessary for a single-column financial dataset like this one.

👉 Since the focus is on detecting unusual **transaction amounts**, the **IQR method is simple, interpretable, and robust** to skewed data. That's why we use it here.
""")
