import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mock-up Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Mock-up Chatbot (Dataset Q&A)")

# --- Load dataset ---
try:
    df = pd.read_csv("financial_transactions.csv")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
except Exception as e:
    st.error("Could not load financial_transactions.csv. Please place it in the root folder.")
    st.stop()

# --- Simple memory for chat history ---
if "chat" not in st.session_state:
    st.session_state.chat = [
      {"role": "assistant", "content": """\
      Hi! 👋 I can help you explore the dataset.  
      Here are the things you can ask me:

      - 💰 **Total spend** (sum of all amounts)  
      - 📊 **Transaction count** (how many transactions)  
      - 🏪 **Top merchants by spend** (e.g., top 5 or top 10)  
      - 📂 **Top categories by spend** (e.g., top 5 or top 10)  
      - 💳 **Payment mix** (distribution of payment methods)  
      - ⚠️ **Outlier summary** (transactions above IQR threshold)  
      - 🗓 **Date range** (earliest to latest transaction date)  

      Try typing one of these questions, like *“What's the total spend?”* or *“Show me top 10 merchants*.
      """}
    ]

# --- Function to generate answers ---
def answer_query(q: str, df: pd.DataFrame) -> str:
    ql = q.lower()

    if "total" in ql and ("spend" in ql or "amount" in ql):
        total = pd.to_numeric(df.get("amount", pd.Series(dtype=float)), errors="coerce").sum()
        return f"💰 Total spend is **{total:,.2f}**."

    if "how many" in ql or "count" in ql:
        return f"📊 Number of transactions: **{len(df):,}**."

    if "top" in ql and "merchant" in ql:
        n = 10 if "10" in ql else 5
        if "merchant" in df.columns and "amount" in df.columns:
            top = (df.groupby("merchant")["amount"].sum()
                     .sort_values(ascending=False)
                     .head(n))
            return "🏪 **Top merchants by spend:**\n\n" + top.to_frame("total_amount").to_markdown()
        return "I can't find `merchant` or `amount`."

    if "top" in ql and "categories" in ql:
        n = 10 if "10" in ql else 5
        if "category" in df.columns and "amount" in df.columns:
            top = (df.groupby("category")["amount"].sum()
                     .sort_values(ascending=False)
                     .head(n))
            return "📂 **Top categories by spend:**\n\n" + top.to_frame("total_amount").to_markdown()
        return "I can't find `category` or `amount`."

    if "payment" in ql and ("mix" in ql or "share" in ql or "distribution" in ql):
        if "payment_method" in df.columns:
            mix = df["payment_method"].value_counts(normalize=True).mul(100).round(2)
            return "💳 **Payment mix (% of transactions):**\n\n" + mix.to_frame("%").to_markdown()
        return "I can't find `payment_method`."

    if "outlier" in ql:
        if "amount" in df.columns:
            amt = pd.to_numeric(df["amount"], errors="coerce")
            q1, q3 = amt.quantile([0.15, 0.85])
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            mask = amt > upper
            cnt = int(mask.sum())
            val = float(amt[mask].sum())
            return f"⚠️ There are **{cnt}** outlier transactions (IQR rule), totaling **{val:,.2f}**."
        return "I can't find `amount`."

    if "date range" in ql:
        if "date" in df.columns:
            dmin = pd.to_datetime(df["date"], errors="coerce").min()
            dmax = pd.to_datetime(df["date"], errors="coerce").max()
            return f"🗓 Date range: **{dmin.date()} → {dmax.date()}**."
        return "I can't find `date`."

    return "I can help with: total spend, counts, top merchants/categories, spend by payment mix, outliers, and date range."

# --- Render chat history ---
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- Input box ---
user_msg = st.chat_input("Ask me about the dataset…")
if user_msg:
    st.session_state.chat.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    reply = answer_query(user_msg, df)
    st.session_state.chat.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
