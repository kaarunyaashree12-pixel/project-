import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Contract Analysis", layout="wide")
st.title("📝 Contract Type Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    # Feature Engineering for ratio comparison
    df['CREDIT_INCOME_RATIO'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
    return df

df = load_data()

# Grouping for KPIs
contract_stats = df.groupby('NAME_CONTRACT_TYPE').agg({
    'TARGET': 'mean',
    'AMT_CREDIT': 'mean',
    'AMT_INCOME_TOTAL': 'mean',
    'SK_ID_CURR': 'count'
}).reset_index()

contract_stats['Default Rate (%)'] = contract_stats['TARGET'] * 100

# KPI Cards
st.subheader("Quick Metrics by Contract Type")
col1, col2 = st.columns(2)
for i, row in contract_stats.iterrows():
    with (col1 if i == 0 else col2):
        st.metric(row['NAME_CONTRACT_TYPE'],
                  f"{row['SK_ID_CURR']:,} Apps",
                  f"{row['Default Rate (%)']:.2f}% Default Rate",
                  delta_color="inverse")

st.markdown("---")

# Visualization 1: Default Rate Comparison
st.subheader("Default Risk by Contract Type")
fig_risk = px.bar(contract_stats, x='NAME_CONTRACT_TYPE', y='Default Rate (%)',
             color='NAME_CONTRACT_TYPE', text_auto='.2f',
             title="Comparison of Default Rates")
st.plotly_chart(fig_risk, use_container_width=True)

# Visualization 2: Credit Amount Distribution
st.subheader("Credit Amount Distribution by Contract Type")
fig_box = px.box(df, x='NAME_CONTRACT_TYPE', y='AMT_CREDIT',
                color='NAME_CONTRACT_TYPE', points=False,
                title="Credit Amount Range per Contract Type")
st.plotly_chart(fig_box, use_container_width=True)

# Visualization 3: Credit-to-Income Ratio
st.subheader("Credit-to-Income Ratio Analysis")
fig_ratio = px.violin(df, x='NAME_CONTRACT_TYPE', y='CREDIT_INCOME_RATIO',
                    color='NAME_CONTRACT_TYPE', box=True,
                    title="Financial Burden (Credit/Income) by Contract Type")
st.plotly_chart(fig_ratio, use_container_width=True)