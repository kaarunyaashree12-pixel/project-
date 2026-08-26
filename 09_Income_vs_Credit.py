import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("📈 Income vs Credit Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    df['CREDIT_INCOME_RATIO'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
    return df

df = load_data()

# Ratio KPIs
avg_ratio = df['CREDIT_INCOME_RATIO'].mean()
st.metric("Average Credit-to-Income Ratio", f"{avg_ratio:.2f}")

# Scatter Plot
st.subheader("Income vs Credit Scatter Plot")
fig_scatter = px.scatter(df.sample(min(10000, len(df))),
                        x='AMT_INCOME_TOTAL',
                        y='AMT_CREDIT',
                        color='TARGET',
                        trendline="ols",
                        title="Income vs Credit Amount (Sampled)",
                        labels={'AMT_INCOME_TOTAL': 'Total Income', 'AMT_CREDIT': 'Credit Amount'})
st.plotly_chart(fig_scatter, use_container_width=True)

# Risk Grouping
st.subheader("Default Rate by Credit-to-Income Ratio")
# Create bins for the ratio
bins = [0, 2, 4, 6, 10, 50]
labels = ['Low (<2)', 'Moderate (2-4)', 'High (4-6)', 'Very High (6-10)', 'Extreme (>10)']
df['RATIO_GROUP'] = pd.cut(df['CREDIT_INCOME_RATIO'], bins=bins, labels=labels)

risk_groups = df.groupby('RATIO_GROUP', observed=False)['TARGET'].mean().reset_index()
risk_groups['Default Rate (%)'] = risk_groups['TARGET'] * 100

fig_ratio = px.bar(risk_groups, x='RATIO_GROUP', y='Default Rate (%)',
                  title='Default Rate by Credit/Income Ratio Group',
                  color='Default Rate (%)',
                  text_auto='.2f')
st.plotly_chart(fig_ratio, use_container_width=True)