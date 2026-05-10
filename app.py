"""
DataChat — Natural Language Data Analyst
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd

from src.loader import load_file, summarise_dataframe
from src.agent import build_agent, ask
from src.visualiser import auto_chart, detect_chart_intent
from src.config import MAX_ROWS_PREVIEW

# ── Page setup ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataChat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "df" not in st.session_state:
    st.session_state.df = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("💬 DataChat")
    st.caption("Ask questions about any CSV or Excel file in plain English.")
    st.divider()

    st.subheader("1. Upload your data")
    uploaded = st.file_uploader(
        "CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Any work spreadsheet — sales data, project tracker, survey results, anything.",
    )

    if uploaded and uploaded.name != st.session_state.file_name:
        with st.spinner("Loading file..."):
            try:
                df = load_file(uploaded)
                agent = build_agent(df)
                st.session_state.df = df
                st.session_state.agent = agent
                st.session_state.file_name = uploaded.name
                st.session_state.messages = []
                st.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")
            except Exception as e:
                st.error(f"Error loading file: {e}")

    # Load sample data
    st.divider()
    st.subheader("Or try the sample")
    if st.button("Load sample sales data", use_container_width=True):
        try:
            df = load_file("data/sample_sales.csv")
            agent = build_agent(df)
            st.session_state.df = df
            st.session_state.agent = agent
            st.session_state.file_name = "sample_sales.csv"
            st.session_state.messages = []
            st.success("Sample data loaded!")
            st.rerun()
        except Exception as e:
            st.error(f"{e}")

    # Data preview
    if st.session_state.df is not None:
        st.divider()
        st.subheader("Data preview")
        st.caption(f"{st.session_state.file_name}")
        st.dataframe(
            st.session_state.df.head(MAX_ROWS_PREVIEW),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            f"{len(st.session_state.df):,} rows · "
            f"{len(st.session_state.df.columns)} columns"
        )

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("[GitHub](https://github.com/YOUR_USERNAME/datachat) · Built with LangChain + Groq + Streamlit")


# ── Main area ──────────────────────────────────────────────────────────────────
st.title("💬 DataChat — Talk to your data")

if st.session_state.agent is None:
    # Welcome screen
    st.info("👈 Upload a CSV or Excel file in the sidebar, or load the sample data to start.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("What you can ask")
        example_questions = [
            "What are the total sales by region?",
            "Which product made the most profit?",
            "Show me revenue trend over time",
            "Who is the top performing sales rep?",
            "What is the average profit margin?",
            "Compare units sold by product",
            "Which month had the highest revenue?",
            "What percentage of revenue came from laptops?",
        ]
        for q in example_questions:
            if st.button(q, key=q, use_container_width=True):
                st.session_state.pending_question = q
                st.rerun()

    with col2:
        st.subheader("How it works")
        st.markdown("""
1. **Upload** any CSV or Excel file — from work, a personal project, anywhere
2. **Ask** a question in plain English — no formulas, no SQL, no code
3. **Get** an instant answer, with an automatic chart where relevant

**Powered by:**
- 🦙 Llama 3.3 (via Groq — free, no credit card)
- 🔗 LangChain pandas agent
- 📊 Plotly for charts
- 🎈 Streamlit for the UI
        """)

else:
    # Chat interface
    # Handle pre-filled question from welcome screen
    pending = st.session_state.pop("pending_question", None)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("figure"):
                st.plotly_chart(message["figure"], use_container_width=True)

    # Suggested questions (shown when chat is empty)
    if not st.session_state.messages:
        st.caption("Try asking:")
        cols = st.columns(4)
        suggestions = [
            "Total revenue by region?",
            "Top product by profit?",
            "Revenue trend over time?",
            "Best sales rep?",
        ]
        for col, suggestion in zip(cols, suggestions):
            with col:
                if st.button(suggestion, use_container_width=True):
                    pending = suggestion

    # Chat input
    question = pending or st.chat_input("Ask anything about your data...")

    if question:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Analysing your data..."):
                answer = ask(st.session_state.agent, question)

            st.markdown(answer)

            # Generate chart if relevant
            figure = auto_chart(st.session_state.df, question)
            if figure:
                st.plotly_chart(figure, use_container_width=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "figure": figure,
        })

        st.rerun()
