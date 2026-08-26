import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Family & Children Analysis", layout="wide")
st.title("👪 Family & Children Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# KPI Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Family Members", f"{df['CNT_FAM_MEMBERS'].mean():.1f}")
with col2:
    st.metric("Avg Children", f"{df['CNT_CHILDREN'].mean():.1f}")
with col3:
    st.metric("Max Children Reported", int(df['CNT_CHILDREN'].max()))

st.markdown("---")

# 1. Family Status & Risk
st.subheader("Default Risk by Family Status")
fam_risk = df.groupby('NAME_FAMILY_STATUS')['TARGET'].mean().sort_values().reset_index()
fam_risk['Default Rate (%)'] = fam_risk['TARGET'] * 100

fig_fam = px.bar(fam_risk, x='Default Rate (%)', y='NAME_FAMILY_STATUS',
                orientation='h', color='Default Rate (%)',
                text_auto='.2f', title="Risk Profile by Marital/Family Status")
st.plotly_chart(fig_fam, use_container_width=True)

# 2. Impact of Children
st.subheader("Default Risk vs. Number of Children")
# Grouping high child counts to avoid long tail
df['CHILDREN_COUNT'] = df['CNT_CHILDREN'].apply(lambda x: '4+' if x >= 4 else str(int(x)))
child_risk = df.groupby('CHILDREN_COUNT', observed=False)['TARGET'].mean().reset_index()
child_risk['Default Rate (%)'] = child_risk['TARGET'] * 100

fig_child = px.bar(child_risk, x='CHILDREN_COUNT', y='Default Rate (%)',
                  color='Default Rate (%)', text_auto='.2f',
                  category_orders={"CHILDREN_COUNT": ["0", "1", "2", "3", "4+"]},
                  title="Default Rate by Number of Children")
st.plotly_chart(fig_child, use_container_width=True)

# 3. Family Size vs Income
st.subheader("Income Distribution by Family Size")
fig_box = px.box(df[df['AMT_INCOME_TOTAL'] < df['AMT_INCOME_TOTAL'].quantile(0.95)],
                x='CNT_FAM_MEMBERS', y='AMT_INCOME_TOTAL',
                title="Income Spread by Family Size (Filtered Outliers)",
                labels={'CNT_FAM_MEMBERS': 'Number of Family Members', 'AMT_INCOME_TOTAL': 'Total Income'})
st.plotly_chart(fig_box, use_container_width=True)