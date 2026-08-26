import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Risk Factor Analysis", layout="wide")
st.title("⚖️ Correlation & Risk Factor Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    # Basic cleaning for better correlations
    df['DAYS_BIRTH'] = df['DAYS_BIRTH'].abs() / 365
    df['DAYS_EMPLOYED'] = df['DAYS_EMPLOYED'].replace(365243, np.nan).abs() / 365
    return df

df = load_data()

# 1. Correlation Heatmap
st.subheader("Feature Correlation Heatmap")
risk_cols = ['TARGET', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'AMT_INCOME_TOTAL', 'AMT_CREDIT']
corr_matrix = df[risk_cols].corr()

fig_corr = px.imshow(corr_matrix,
                    text_auto=True,
                    aspect='auto',
                    color_continuous_scale='RdBu_r',
                    range_color=[-1, 1])
st.plotly_chart(fig_corr, use_container_width=True)

# 2. Risk Factors with Target
st.markdown("---")
col1, col2 = st.columns(2)

# Calculate correlations with TARGET
target_corr = df.select_dtypes(include=[np.number]).corr()['TARGET'].sort_values()

with col1:
    st.subheader("Top Negative Correlations")
    st.write("These features decrease as default risk increases (e.g., higher scores = lower risk).")
    neg_corr = target_corr.head(5).reset_index()
    neg_corr.columns = ['Feature', 'Correlation']
    fig_neg = px.bar(neg_corr, x='Correlation', y='Feature', orientation='h', color='Correlation', color_continuous_scale='Blues_r')
    st.plotly_chart(fig_neg, use_container_width=True)

with col2:
    st.subheader("Top Positive Correlations")
    st.write("These features increase as default risk increases.")
    pos_corr = target_corr.drop('TARGET').tail(5).reset_index()
    pos_corr.columns = ['Feature', 'Correlation']
    fig_pos = px.bar(pos_corr, x='Correlation', y='Feature', orientation='h', color='Correlation', color_continuous_scale='Reds')
    st.plotly_chart(fig_pos, use_container_width=True)

# 3. Deep Dive: External Scores
st.subheader("External Score vs Default Probability")
fig_ext = px.box(df.sample(min(10000, len(df))), x='TARGET', y='EXT_SOURCE_3',
                color='TARGET', title="EXT_SOURCE_3 Impact on Default")
st.plotly_chart(fig_ext, use_container_width=True)