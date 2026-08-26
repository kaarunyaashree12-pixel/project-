import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("💼 Employment Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    # Cleaning and Feature Engineering
    df['DAYS_EMPLOYED'] = df['DAYS_EMPLOYED'].replace(365243, np.nan)
    df['YEARS_EMPLOYED'] = df['DAYS_EMPLOYED'].abs() / 365
    return df

df = load_data()

# Top Level Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Average Years Employed", f"{df['YEARS_EMPLOYED'].mean():.1f}")
with col2:
    st.metric("Highest Risk Occupation", "Low-skill Laborers")

# Default Rate by Income Type
st.subheader("Default Rate by Income Type")
income_type_risk = df.groupby('NAME_INCOME_TYPE')['TARGET'].mean().sort_values().reset_index()
income_type_risk['Default Rate (%)'] = income_type_risk['TARGET'] * 100
fig_income = px.bar(income_type_risk, x='Default Rate (%)', y='NAME_INCOME_TYPE', orientation='h',
                   title='Risk by Income Source', color='Default Rate (%)')
st.plotly_chart(fig_income, use_container_width=True)

# Default Rate by Occupation
st.subheader("Default Rate by Occupation")
occ_risk = df.groupby('OCCUPATION_TYPE')['TARGET'].mean().sort_values().reset_index()
occ_risk['Default Rate (%)'] = occ_risk['TARGET'] * 100
fig_occ = px.bar(occ_risk, x='Default Rate (%)', y='OCCUPATION_TYPE', orientation='h',
                 title='Risk by Occupation Type', color='Default Rate (%)')
st.plotly_chart(fig_occ, use_container_width=True)

# Employment Duration vs Default
st.subheader("Employment Duration vs Default Risk")
fig_years = px.histogram(df, x='YEARS_EMPLOYED', color='TARGET', nbins=30,
                         marginal='box', barmode='overlay',
                         title='Distribution of Years Employed by Target')
st.plotly_chart(fig_years, use_container_width=True)