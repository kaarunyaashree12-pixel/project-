import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Annuity Analysis", layout="wide")
st.title("📅 Annuity Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Annuity", f"${df['AMT_ANNUITY'].mean():,.2f}")
with col2:
    st.metric("Median Annuity", f"${df['AMT_ANNUITY'].median():,.2f}")
with col3:
    st.metric("Highest Annuity", f"${df['AMT_ANNUITY'].max():,.2f}")

st.markdown("---")

# 1. Annuity Distribution
st.subheader("Annuity Amount Distribution")
fig_dist = px.histogram(df, x='AMT_ANNUITY', color='TARGET',
                       nbins=50, marginal='box',
                       title="Annual Loan Payment (Annuity) Distribution",
                       labels={'AMT_ANNUITY': 'Annuity Amount'},
                       color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig_dist, use_container_width=True)

# 2. Annuity by Target and Category
st.subheader("Annuity Spread by Category")
cat_var = st.selectbox("Select Category:", ['NAME_INCOME_TYPE', 'NAME_CONTRACT_TYPE', 'CODE_GENDER'])
fig_box = px.box(df, x=cat_var, y='AMT_ANNUITY', color='TARGET',
                title=f"Annuity Amount across {cat_var}",
                points=False)
st.plotly_chart(fig_box, use_container_width=True)

# 3. Annuity vs Credit Amount
st.subheader("Annuity vs Total Credit")
fig_scatter = px.scatter(df.sample(min(5000, len(df))), x='AMT_CREDIT', y='AMT_ANNUITY',
                        color='TARGET', opacity=0.5,
                        title="Relationship between Credit Amount and Annual Payment (Sampled)")
st.plotly_chart(fig_scatter, use_container_width=True)