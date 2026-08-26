import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Executive Overview")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# KPI Row
col1, col2, col3 = st.columns(3)
default_rate = df['TARGET'].mean() * 100

with col1:
    st.metric("Total Applications", f"{len(df):,}")
with col2:
    st.metric("Default Rate", f"{default_rate:.2f}%")
with col3:
    st.metric("Avg Credit Amount", f"${df['AMT_CREDIT'].mean():,.2f}")

# Target Distribution
st.subheader("Default Distribution")
target_counts = df['TARGET'].value_counts().reset_index()
target_counts['Label'] = target_counts['TARGET'].map({0: 'Repaid', 1: 'Default'})
fig = px.pie(target_counts, values='count', names='Label', color_discrete_sequence=['#636EFA', '#EF553B'])
st.plotly_chart(fig, use_container_width=True)