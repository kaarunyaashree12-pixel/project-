import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Missing Value Analysis", layout="wide")
st.title("🔍 Missing Value Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# Calculate Missingness
missing_stats = df.isnull().sum().reset_index()
missing_stats.columns = ['Column', 'Missing Count']
missing_stats['Missing %'] = (missing_stats['Missing Count'] / len(df)) * 100
missing_stats = missing_stats.sort_values('Missing %', ascending=False)

# KPI Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Columns", len(df.columns))
with col2:
    st.metric("Columns with Missing Data", len(missing_stats[missing_stats['Missing Count'] > 0]))
with col3:
    st.metric("Critical Columns (>50% Null)", len(missing_stats[missing_stats['Missing %'] > 50]))

st.markdown("---")

# Visualization 1: Top Missing Columns
st.subheader("Top 20 Columns with Most Missing Values")
fig_bar = px.bar(missing_stats.head(20), x='Missing %', y='Column',
             orientation='h',
             color='Missing %',
             text_auto='.1f',
             title="Missing Percentage by Feature")
st.plotly_chart(fig_bar, use_container_width=True)

# Visualization 2: Distribution of Missingness
st.subheader("Distribution of Missing Data across all Columns")
fig_hist = px.histogram(missing_stats, x='Missing %',
                       nbins=20,
                       title="How many columns have X% missing data?")
st.plotly_chart(fig_hist, use_container_width=True)

# Detailed Table
st.subheader("Complete Missing Data Report")
st.dataframe(missing_stats[missing_stats['Missing Count'] > 0], use_container_width=True)