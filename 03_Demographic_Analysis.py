
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Demographic Analysis",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Demographic Analysis")
st.markdown(
    "Explore applicant demographics and their relationship with credit default risk."
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv")

    # Age in years
    df["AGE_YEARS"] = df["DAYS_BIRTH"].abs() / 365

    # Age groups
    bins = [18, 25, 30, 35, 40, 45, 50, 55, 60, 100]
    labels = [
        "18-25",
        "26-30",
        "31-35",
        "36-40",
        "41-45",
        "46-50",
        "51-55",
        "56-60",
        "61+"
    ]

    df["AGE_GROUP"] = pd.cut(
        df["AGE_YEARS"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Demographic Filters")

gender_options = sorted(
    df["CODE_GENDER"].dropna().unique().tolist()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    default=gender_options
)

family_options = sorted(
    df["NAME_FAMILY_STATUS"].dropna().unique().tolist()
)

selected_family = st.sidebar.multiselect(
    "Family Status",
    family_options,
    default=family_options
)

education_options = sorted(
    df["NAME_EDUCATION_TYPE"].dropna().unique().tolist()
)

selected_education = st.sidebar.multiselect(
    "Education",
    education_options,
    default=education_options
)

housing_options = sorted(
    df["NAME_HOUSING_TYPE"].dropna().unique().tolist()
)

selected_housing = st.sidebar.multiselect(
    "Housing Type",
    housing_options,
    default=housing_options
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------
filtered_df = df[
    df["CODE_GENDER"].isin(selected_gender) &
    df["NAME_FAMILY_STATUS"].isin(selected_family) &
    df["NAME_EDUCATION_TYPE"].isin(selected_education) &
    df["NAME_HOUSING_TYPE"].isin(selected_housing)
].copy()

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
total_customers = len(filtered_df)

average_age = filtered_df["AGE_YEARS"].mean()

male_customers = (
    filtered_df["CODE_GENDER"] == "M"
).sum()

female_customers = (
    filtered_df["CODE_GENDER"] == "F"
).sum()

average_family_size = filtered_df["CNT_FAM_MEMBERS"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Average Age",
        f"{average_age:.1f} Years"
    )

with col3:
    st.metric(
        "Male Customers",
        f"{male_customers:,}"
    )

with col4:
    st.metric(
        "Female Customers",
        f"{female_customers:,}"
    )

with col5:
    st.metric(
        "Average Family Size",
        f"{average_family_size:.1f}"
    )

st.markdown("---")

# ---------------------------------------------------------
# GENDER DISTRIBUTION
# ---------------------------------------------------------
st.subheader("1. Customers by Gender")

gender_count = (
    filtered_df["CODE_GENDER"]
    .value_counts()
    .reset_index()
)

gender_count.columns = ["Gender", "Customers"]

fig_gender = px.bar(
    gender_count,
    x="Gender",
    y="Customers",
    text="Customers",
    title="Applicant Distribution by Gender"
)

fig_gender.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_gender, use_container_width=True)

# ---------------------------------------------------------
# AGE GROUP
# ---------------------------------------------------------
st.subheader("2. Customers by Age Group")

age_count = (
    filtered_df["AGE_GROUP"]
    .value_counts()
    .sort_index()
    .reset_index()
)

age_count.columns = ["Age Group", "Customers"]

fig_age = px.bar(
    age_count,
    x="Age Group",
    y="Customers",
    text="Customers",
    title="Applicant Distribution by Age Group"
)

fig_age.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_age, use_container_width=True)

# ---------------------------------------------------------
# FAMILY STATUS
# ---------------------------------------------------------
st.subheader("3. Customers by Family Status")

family_count = (
    filtered_df["NAME_FAMILY_STATUS"]
    .value_counts()
    .reset_index()
)

family_count.columns = ["Family Status", "Customers"]

fig_family = px.bar(
    family_count,
    x="Customers",
    y="Family Status",
    orientation="h",
    text="Customers",
    title="Applicant Distribution by Family Status"
)

fig_family.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_family, use_container_width=True)

# ---------------------------------------------------------
# EDUCATION
# ---------------------------------------------------------
st.subheader("4. Customers by Education")

education_count = (
    filtered_df["NAME_EDUCATION_TYPE"]
    .value_counts()
    .reset_index()
)

education_count.columns = ["Education", "Customers"]

fig_education = px.bar(
    education_count,
    x="Customers",
    y="Education",
    orientation="h",
    text="Customers",
    title="Applicant Distribution by Education"
)

fig_education.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_education, use_container_width=True)

# ---------------------------------------------------------
# HOUSING
# ---------------------------------------------------------
st.subheader("5. Customers by Housing Type")

housing_count = (
    filtered_df["NAME_HOUSING_TYPE"]
    .value_counts()
    .reset_index()
)

housing_count.columns = ["Housing Type", "Customers"]

fig_housing = px.bar(
    housing_count,
    x="Customers",
    y="Housing Type",
    orientation="h",
    text="Customers",
    title="Applicant Distribution by Housing Type"
)

fig_housing.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_housing, use_container_width=True)

# ---------------------------------------------------------
# DEFAULT RATE BY DEMOGRAPHIC GROUP
# ---------------------------------------------------------
st.subheader("6. Default Rate by Demographic Group")

demographic_choice = st.selectbox(
    "Select demographic variable:",
    [
        "CODE_GENDER",
        "AGE_GROUP",
        "NAME_FAMILY_STATUS",
        "NAME_EDUCATION_TYPE",
        "NAME_HOUSING_TYPE"
    ]
)

demo_risk = (
    filtered_df
    .groupby(demographic_choice, dropna=False)["TARGET"]
    .mean()
    .reset_index()
)

demo_risk["Default Rate (%)"] = (
    demo_risk["TARGET"] * 100
)

demo_risk = demo_risk.sort_values(
    "Default Rate (%)",
    ascending=False
)

fig_demo = px.bar(
    demo_risk,
    x="Default Rate (%)",
    y=demographic_choice,
    orientation="h",
    text="Default Rate (%)",
    title=f"Default Rate by {demographic_choice}"
)

fig_demo.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_demo, use_container_width=True)

# ---------------------------------------------------------
# SUMMARY TABLE
# ---------------------------------------------------------
st.subheader("7. Demographic Summary")

summary = (
    filtered_df
    .groupby("CODE_GENDER")
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean"),
        Average_Income=("AMT_INCOME_TOTAL", "mean"),
        Average_Credit=("AMT_CREDIT", "mean")
    )
    .reset_index()
)

summary["Default_Rate"] = summary["Default_Rate"] * 100

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)