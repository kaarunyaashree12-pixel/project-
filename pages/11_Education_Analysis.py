import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Education Analysis", layout="wide")
st.title("🎓 Education Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# Main Statistics
most_common_edu = df['NAME_EDUCATION_TYPE'].mode()[0]

st.markdown(f"### Summary")
st.write(f"The most common education level among applicants is **{most_common_edu}**.")

# KPI Row
edu_risk = df.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean().reset_index()
edu_risk['Default Rate (%)'] = edu_risk['TARGET'] * 100

best_edu = edu_risk.sort_values('Default Rate (%)').iloc[0]
worst_edu = edu_risk.sort_values('Default Rate (%)').iloc[-1]

col1, col2 = st.columns(2)
with col1:
    st.metric("Lowest Risk Education", best_edu['NAME_EDUCATION_TYPE'], f"{best_edu['Default Rate (%)']:.2f}% Rate")
with col2:
    st.metric("Highest Risk Education", worst_edu['NAME_EDUCATION_TYPE'], f"{worst_edu['Default Rate (%)']:.2f}% Rate", delta_color="inverse")

# Visualization 1: Distribution of Applicants by Education
st.subheader("Applicant Distribution by Education Level")
fig_dist = px.pie(df, names='NAME_EDUCATION_TYPE',
             title='Education Level of Applicants',
             hole=0.4)
st.plotly_chart(fig_dist, use_container_width=True)

# Visualization 2: Default Rate by Education
st.subheader("Credit Risk (Default Rate) by Education")
fig_risk = px.bar(edu_risk.sort_values('Default Rate (%)', ascending=False),
             x='NAME_EDUCATION_TYPE', y='Default Rate (%)',
             color='Default Rate (%)',
             text_auto='.2f',
             title='Default Rate by Education Level')
st.plotly_chart(fig_risk, use_container_width=True)

# Visualization 3: Credit Amount by Education
st.subheader("Average Credit Amount by Education")
edu_credit = df.groupby('NAME_EDUCATION_TYPE')['AMT_CREDIT'].mean().reset_index()
fig_credit = px.box(df, x='NAME_EDUCATION_TYPE', y='AMT_CREDIT',
               color='NAME_EDUCATION_TYPE',
               title='Credit Amount Spread by Education Level')
st.plotly_chart(fig_credit, use_container_width=True)