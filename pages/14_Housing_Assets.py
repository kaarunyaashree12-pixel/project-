import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Housing & Asset Analysis", layout="wide")
st.title("🏠 Housing & Asset Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv('data/application_train.csv')
    return df

df = load_data()

# KPI Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Car Owners", f"{(df['FLAG_OWN_CAR'] == 'Y').sum():,}")
with col2:
    st.metric("Property Owners", f"{(df['FLAG_OWN_REALTY'] == 'Y').sum():,}")
with col3:
    st.metric("Avg Car Age", f"{df['OWN_CAR_AGE'].mean():.1f} Years")

st.markdown("---")

# 1. Asset Ownership vs Risk
st.subheader("Default Risk by Asset Ownership")
col_a, col_b = st.columns(2)

with col_a:
    car_risk = df.groupby('FLAG_OWN_CAR')['TARGET'].mean().reset_index()
    car_risk['Default Rate (%)'] = car_risk['TARGET'] * 100
    fig_car = px.bar(car_risk, x='FLAG_OWN_CAR', y='Default Rate (%)', color='FLAG_OWN_CAR',
                    title="Risk: Car Owners vs Non-Owners", text_auto='.2f')
    st.plotly_chart(fig_car, use_container_width=True)

with col_b:
    realty_risk = df.groupby('FLAG_OWN_REALTY')['TARGET'].mean().reset_index()
    realty_risk['Default Rate (%)'] = realty_risk['TARGET'] * 100
    fig_realty = px.bar(realty_risk, x='FLAG_OWN_REALTY', y='Default Rate (%)', color='FLAG_OWN_REALTY',
                       title="Risk: Property Owners vs Non-Owners", text_auto='.2f')
    st.plotly_chart(fig_realty, use_container_width=True)

# 2. Housing Type Analysis
st.subheader("Housing Type and Credit Amount")
house_stats = df.groupby('NAME_HOUSING_TYPE').agg({'TARGET': 'mean', 'AMT_CREDIT': 'mean'}).reset_index()
house_stats['Default Rate (%)'] = house_stats['TARGET'] * 100

fig_house = px.bar(house_stats.sort_values('Default Rate (%)'), x='Default Rate (%)', y='NAME_HOUSING_TYPE',
                  orientation='h', color='Default Rate (%)', text_auto='.2f',
                  title="Default Rate by Housing Type")
st.plotly_chart(fig_house, use_container_width=True)

# 3. Car Age vs Risk
st.subheader("Impact of Car Age on Default Risk")
if not df['OWN_CAR_AGE'].dropna().empty:
    # Binning car age
    df['CAR_AGE_BIN'] = pd.cut(df['OWN_CAR_AGE'], bins=[0, 5, 10, 20, 100], labels=['New (0-5)', 'Mid (5-10)', 'Old (10-20)', 'Very Old (>20)'])
    car_age_risk = df.groupby('CAR_AGE_BIN', observed=False)['TARGET'].mean().reset_index()
    car_age_risk['Default Rate (%)'] = car_age_risk['TARGET'] * 100

    fig_car_age = px.line(car_age_risk, x='CAR_AGE_BIN', y='Default Rate (%)', markers=True,
                         title="Trend: Default Rate vs Car Age")
    st.plotly_chart(fig_car_age, use_container_width=True)