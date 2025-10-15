# dashboards/streamlit_app.py

# --- make `src/` importable when running from project root or /dashboards ---
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()  # reads .env for MISTRAL_API_KEY, etc.

# Import the FP&A chat helper (Mistral-backed)
from src.chatbot_app import ask_fpna_bot

# ---------------------- Helpers ----------------------
def df_to_markdown(df: pd.DataFrame, max_rows: int = 12, max_cols: int = 8) -> str:
    """Render a compact markdown table for LLM context."""
    df2 = df.copy().iloc[:max_rows, :max_cols]
    # simple numeric formatting
    for col in df2.select_dtypes(include="number").columns:
        df2[col] = df2[col].map(lambda x: f"{x:,.2f}")
    return df2.to_markdown(index=False)

def summarize_df(df: pd.DataFrame) -> str:
    """Tiny one-line summary of the uploaded dataframe."""
    rows, cols = df.shape
    colnames = ", ".join(df.columns[:8])
    return f"Rows: {rows}, Cols: {cols}. Columns: {colnames}."

# ---------------------- UI ----------------------
st.set_page_config(page_title="FP&A Insights Chatbot", page_icon="📈", layout="centered")
st.title("📈 AI-Powered FP&A Insights")
st.caption("Ask questions and provide a small data snippet (upload CSV or paste). The bot will ONLY answer from your data.")

st.subheader("Upload data (CSV) or paste a snippet")

uploaded = st.file_uploader("Upload CSV (small file, e.g., ≤ 2k rows)", type=["csv"])
pasted = st.text_area(
    "Or paste a tiny data snippet (CSV/markdown)",
    height=140,
    value="Month,Actual,Forecast\n2025-04,1200000,1150000\n2025-05,1250000,1230000\n2025-06,1285000,1260000",
)

question = st.text_input(
    "Your question",
    value="What is June variance vs forecast (%) and total variance for Q2?"
)

use_uploaded = st.checkbox("Use uploaded CSV (if provided)", value=True)
ask = st.button("Ask")

# Build the context markdown we send to the model
ctx_markdown = ""
if uploaded and use_uploaded:
    try:
        df = pd.read_csv(uploaded)
        st.markdown("### Preview")
        st.dataframe(df.head(20), use_container_width=True)
        st.caption(summarize_df(df))
        ctx_markdown = df_to_markdown(df)
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        ctx_markdown = pasted
else:
    ctx_markdown = pasted

if ask:
    with st.spinner("Thinking..."):
        try:
            answer = ask_fpna_bot(question, ctx_markdown)
            from src.chatbot_app import ask_fpna_bot_structured
            answer = ask_fpna_bot_structured(question, ctx_markdown)

            st.markdown("### ✅ Answer")
            st.write(answer)

            with st.expander("Data sent to the model"):
                st.code(ctx_markdown, language="markdown")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Tip: Keep the context small (a few rows). For best results, use clean numeric columns named like 'Actual', 'Forecast', 'Month'.")
