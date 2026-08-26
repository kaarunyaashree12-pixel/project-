import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Home Credit Risk Dashboard", layout="wide")

st.title("🏦 Home Credit Default Risk Analytics")
st.sidebar.success("Select a page above to begin analysis.")

st.markdown("""
### Project Overview
This dashboard provides a comprehensive analysis of loan applicants to identify factors associated with default risk.

**Key Navigation:**
- **Executive Overview:** High-level KPIs and trends.
- **Risk Analysis:** Deep dive into demographics and credit scores.
- **Customer Explorer:** Search for specific applicant profiles.
""")

# Quick Summary Metrics
st.subheader("Dataset Quick Facts")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Applications", "307,511")
with col2:
    st.metric("Average Default Rate", "8.07%")
with col3:
    st.metric("Features Analyzed", "122")