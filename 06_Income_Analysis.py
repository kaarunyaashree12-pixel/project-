import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Income Analysis", layout="wide")
st.title("💰 Income Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    # Filtering extreme outliers for better visualization of the distribution
    q_low = df['AMT_INCOME_TOTAL'].quantile(0.01)
    q_hi  = df['AMT_INCOME_TOTAL'].quantile(0.99)
    df_filtered = df[(df['AMT_INCOME_TOTAL'] < q_hi) & (df['AMT_INCOME_TOTAL'] > q_low)].copy()
    return df, df_filtered

df_full, df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Median Income", f"${df_full['AMT_INCOME_TOTAL'].median():,.2f}")
with col2:
    st.metric("Average Income", f"${df_full['AMT_INCOME_TOTAL'].mean():,.2f}")
with col3:
    st.metric("Highest Recorded Income", f"${df_full['AMT_INCOME_TOTAL'].max():,.2f}")

st.markdown("---")

# 1. Income Distribution
st.subheader("Income Distribution (98th Percentile)")
fig_dist = px.histogram(df, x='AMT_INCOME_TOTAL', color='TARGET',
                       nbins=50, marginal='box',
                       title="Applicant Income Distribution by Target",
                       labels={'AMT_INCOME_TOTAL': 'Total Annual Income'},
                       color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig_dist, use_container_width=True)

# 2. Income by Category
st.subheader("Income Levels by Occupation & Education")
cat_option = st.selectbox("View Income by:", ['OCCUPATION_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_INCOME_TYPE'])
fig_box = px.box(df, x=cat_option, y='AMT_INCOME_TOTAL', color='TARGET',
                title=f"Income Spread across {cat_option}",
                points=False)
st.plotly_chart(fig_box, use_container_width=True)

# 3. Default Rate by Income Quantile
st.subheader("Risk Analysis by Income Percentile")
df_full['INCOME_QUARTILE'] = pd.qcut(df_full['AMT_INCOME_TOTAL'], 4, labels=['Low', 'Medium', 'High', 'Very High'])
income_risk = df_full.groupby('INCOME_QUARTILE', observed=False)['TARGET'].mean().reset_index()
income_risk['Default Rate (%)'] = income_risk['TARGET'] * 100

fig_risk = px.bar(income_risk, x='INCOME_QUARTILE', y='Default Rate (%)',
                 text_auto='.2f', color='Default Rate (%)',
                 title="Default Rate per Income Quartile")
st.plotly_chart(fig_risk, use_container_width=True)