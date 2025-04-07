import streamlit as st
import requests
from utils.ui_helper import display_results

st.set_page_config(page_title="SHL Recommender", page_icon="🧠")
st.title("🧠 SHL Assessment Recommendation Engine")

st.markdown("Paste a job description below to get matching SHL assessments.")

query = st.text_area("Job Description", height=200)

if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a valid job description.")
    else:
        with st.spinner("Analyzing and fetching recommendations..."):
            response = requests.post(
                "https://job-recommender-5vsn.onrender.com/recommend",  # update if needed
                json={"query": query}
            )
            if response.status_code == 200:
                display_results(response.json())
            else:
                st.error("Failed to fetch recommendations from backend.")
