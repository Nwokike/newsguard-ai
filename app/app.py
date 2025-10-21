import streamlit as st
from pathlib import Path
import importlib

st.set_page_config(page_title="NewsGuard AI", page_icon="📰", layout="wide")

st.title("📰 NewsGuard AI")
st.write("Paste a news article below to analyze. Features are modular — if a model is not ready it will show 'Coming Soon'.")

text = st.text_area("Paste article text here", height=300)

# Sidebar toggles
st.sidebar.header("Options")
show_topic = st.sidebar.checkbox("Show Topic Classification", value=True)
show_fake = st.sidebar.checkbox("Show Fake News Detection", value=True)
show_sentiment = st.sidebar.checkbox("Show Sentiment Analysis", value=True)
show_clickbait = st.sidebar.checkbox("Show Clickbait (headline)", value=False)

# Utility to attempt import of a model function and call it safely
def safe_call(module_path, func_name, *args, **kwargs):
    try:
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        return func(*args, **kwargs)
    except Exception as e:
        return f"Coming Soon or Error: {e}"

if st.button("Analyze"):
    if not text.strip():
        st.warning("Please paste an article to analyze.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Topic")
            if show_topic:
                res = safe_call('model_functions.topic', 'predict_topic', text)
                st.write(res)
            else:
                st.write("Disabled")

            st.subheader("Fake News")
            if show_fake:
                res = safe_call('model_functions.fake', 'predict_fake', text)
                st.write(res)
            else:
                st.write("Disabled")

            st.subheader("Sentiment")
            if show_sentiment:
                res = safe_call('model_functions.sentiment', 'predict_sentiment', text)
                st.write(res)
            else:
                st.write("Disabled")

        with col2:
            st.subheader("Clickbait (headline)")
            if show_clickbait:
                # For clickbait we expect a headline; use first line as headline
                headline = text.strip().split('\n')[0]
                res = safe_call('model_functions.clickbait', 'is_clickbait', headline)
                st.write(res)
            else:
                st.write("Disabled")

            st.subheader("Raw text preview")
            st.write(text[:1000] + ("..." if len(text) > 1000 else ""))

        st.info("If any model shows \"Coming Soon\", the developer for that model should add the prediction function under `model_functions/` and submit a PR.")
