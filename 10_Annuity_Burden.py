import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Annuity Burden Analysis", layout="wide")
st.title("⚖️ Annuity Burden (Annuity vs Income)")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    # Calculate the Ratio
    df['ANNUITY_INCOME_RATIO'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
    return df

df = load_data()

# KPI Row
col1, col2 = st.columns(2)
with col1:
    st.metric("Avg Annuity-to-Income Ratio", f"{df['ANNUITY_INCOME_RATIO'].mean():.2%}")
with col2:
    st.metric("Max Annuity-to-Income Ratio", f"{df['ANNUITY_INCOME_RATIO'].max():.2f}")

st.markdown("---")

# 1. Ratio Distribution
st.subheader("Repayment Burden Distribution")
st.write("The ratio of the annual payment to total annual income.")
fig_dist = px.histogram(df[df['ANNUITY_INCOME_RATIO'] < 1], x='ANNUITY_INCOME_RATIO',
                       color='TARGET', nbins=50, marginal='box',
                       title="Annuity/Income Ratio Distribution (Filtered < 100%)",
                       color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig_dist, use_container_width=True)

# 2. Risk Analysis by Burden
st.subheader("Default Risk by Burden Level")
# Define Burden Groups
bins = [0, 0.1, 0.2, 0.3, 0.5, 2]
labels = ['Low (<10%)', 'Moderate (10-20%)', 'Significant (20-30%)', 'High (30-50%)', 'Critical (>50%)']
df['BURDEN_GROUP'] = pd.cut(df['ANNUITY_INCOME_RATIO'], bins=bins, labels=labels)

risk_burden = df.groupby('BURDEN_GROUP', observed=False)['TARGET'].mean().reset_index()
risk_burden['Default Rate (%)'] = risk_burden['TARGET'] * 100

fig_burden = px.bar(risk_burden, x='BURDEN_GROUP', y='Default Rate (%)',
                   text_auto='.2f', color='Default Rate (%)',
                   title="Risk Profile across Repayment Burden Groups")
st.plotly_chart(fig_burden, use_container_width=True)

# 3. Categorical Comparison
st.subheader("Burden Comparison by Category")
cat_var = st.selectbox("Group by:", ['NAME_EDUCATION_TYPE', 'NAME_INCOME_TYPE', 'CODE_GENDER'])
fig_strip = px.box(df[df['ANNUITY_INCOME_RATIO'] < 0.8], x=cat_var, y='ANNUITY_INCOME_RATIO',
                 color='TARGET', title=f"Burden Spread across {cat_var}",
                 points=False)
st.plotly_chart(fig_strip, use_container_width=True)