import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("📄 External Credit Score Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# Main KPI Row
scores = ['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg EXT_SOURCE_1", f"{df['EXT_SOURCE_1'].mean():.3f}")
with col2:
    st.metric("Avg EXT_SOURCE_2", f"{df['EXT_SOURCE_2'].mean():.3f}")
with col3:
    st.metric("Avg EXT_SOURCE_3", f"{df['EXT_SOURCE_3'].mean():.3f}")

st.markdown("---")

# Distribution Analysis
st.subheader("Score Distribution by Loan Status")
selected_score = st.selectbox("Select Score Source", scores)

fig_dist = px.histogram(df, x=selected_score, color='TARGET',
                       marginal='box',
                       title=f'Distribution of {selected_score} vs Default Risk',
                       labels={'TARGET': 'Default (1=Yes, 0=No)'},
                       barmode='overlay',
                       opacity=0.7,
                       color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig_dist, use_container_width=True)

# Correlation Analysis
st.subheader("Relationship between External Sources")
fig_scatter = px.scatter(df.sample(5000), x='EXT_SOURCE_2', y='EXT_SOURCE_3',
                        color='TARGET',
                        title='EXT_SOURCE_2 vs EXT_SOURCE_3 (Sample of 5000)',
                        labels={'TARGET': 'Default'},
                        opacity=0.5,
                        trendline="ols")
st.plotly_chart(fig_scatter, use_container_width=True)

# Missing Value Table
st.subheader("Data Completeness")
missing_stats = df[scores].isnull().sum().reset_index()
missing_stats.columns = ['Source', 'Missing Count']
missing_stats['Missing %'] = (missing_stats['Missing Count'] / len(df)) * 100
st.table(missing_stats)