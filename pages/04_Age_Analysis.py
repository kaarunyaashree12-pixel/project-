import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("📅 Age Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    # Preprocessing
    df['DAYS_BIRTH'] = df['DAYS_BIRTH'].abs() / 365
    df['AGE_BINNED'] = pd.cut(df['DAYS_BIRTH'], bins = np.linspace(20, 70, num = 11))
    return df

df = load_data()

# KPI Cards
col1, col2 = st.columns(2)
with col1:
    st.metric("Average Age", f"{df['DAYS_BIRTH'].mean():.1f} Years")
with col2:
    st.metric("Youngest Applicant", f"{df['DAYS_BIRTH'].min():.1f} Years")

# Age Distribution Histogram
st.subheader("Age Distribution of Applicants")
fig_hist = px.histogram(df, x='DAYS_BIRTH', color='TARGET',
                       nbins=50,
                       title='Distribution of Age by Target',
                       labels={'DAYS_BIRTH': 'Age (Years)'},
                       barmode='overlay')
st.plotly_chart(fig_hist, use_container_width=True)

# Default Rate by Age Group
st.subheader("Default Risk by Age Group")
age_groups = df.groupby('AGE_BINNED', observed=False)['TARGET'].mean().reset_index()
age_groups['Default Rate (%)'] = age_groups['TARGET'] * 100
age_groups['AGE_BINNED'] = age_groups['AGE_BINNED'].astype(str)

fig_age_risk = px.bar(age_groups, x='AGE_BINNED', y='Default Rate (%)',
                     title='Default Rate (%) by Age Group',
                     color='Default Rate (%)',
                     text_auto='.2f')
st.plotly_chart(fig_age_risk, use_container_width=True)