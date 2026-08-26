import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Credit Amount Analysis", layout="wide")
st.title("💳 Credit Amount Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Credit", f"${df['AMT_CREDIT'].mean():,.2f}")
with col2:
    st.metric("Median Credit", f"${df['AMT_CREDIT'].median():,.2f}")
with col3:
    st.metric("Max Credit Limit", f"${df['AMT_CREDIT'].max():,.2f}")

st.markdown("---")

# 1. Credit Distribution
st.subheader("Credit Amount Distribution")
fig_dist = px.histogram(df, x='AMT_CREDIT', color='TARGET',
                       nbins=50, marginal='violin',
                       title="Distribution of Requested Credit Amounts",
                       labels={'AMT_CREDIT': 'Credit Amount'},
                       color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig_dist, use_container_width=True)

# 2. Credit by Category
st.subheader("Credit Amount by Demographics")
cat_var = st.selectbox("Select Category:", ['NAME_CONTRACT_TYPE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE'])
fig_box = px.box(df, x=cat_var, y='AMT_CREDIT', color='TARGET',
                title=f"Credit Amount Spread across {cat_var}",
                points=False)
st.plotly_chart(fig_box, use_container_width=True)

# 3. Risk by Credit Range
st.subheader("Default Risk by Credit Size")
# Custom bins for Credit Amount
bins = [0, 250000, 500000, 750000, 1000000, 5000000]
labels = ['Small (<250k)', 'Medium (250k-500k)', 'Large (500k-750k)', 'Very Large (750k-1M)', 'Premium (>1M)']
df['CREDIT_RANGE'] = pd.cut(df['AMT_CREDIT'], bins=bins, labels=labels)

credit_risk = df.groupby('CREDIT_RANGE', observed=False)['TARGET'].mean().reset_index()
credit_risk['Default Rate (%)'] = credit_risk['TARGET'] * 100

fig_risk = px.bar(credit_risk, x='CREDIT_RANGE', y='Default Rate (%)',
                 text_auto='.2f', color='Default Rate (%)',
                 title="Default Rate per Credit Range")
st.plotly_chart(fig_risk, use_container_width=True)