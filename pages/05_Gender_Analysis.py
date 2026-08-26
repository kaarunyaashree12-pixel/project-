
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Gender Analysis",
    page_icon="⚥",
    layout="wide"
)

st.title("⚥ Gender Analysis")
st.markdown(
    "Comparison of credit characteristics and default risk between genders."
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/application_train.csv")
    return df

df = load_data()

# ---------------------------------------------------------
# GENDER SUMMARY
# ---------------------------------------------------------
gender_summary = (
    df.groupby("CODE_GENDER")
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean"),
        Avg_Income=("AMT_INCOME_TOTAL", "mean"),
        Avg_Credit=("AMT_CREDIT", "mean"),
        Avg_Annuity=("AMT_ANNUITY", "mean")
    )
    .reset_index()
)

gender_summary["Default_Rate"] *= 100

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
male_row = gender_summary[
    gender_summary["CODE_GENDER"] == "M"
]

female_row = gender_summary[
    gender_summary["CODE_GENDER"] == "F"
]

male_customers = (
    int(male_row["Customers"].iloc[0])
    if not male_row.empty else 0
)

female_customers = (
    int(female_row["Customers"].iloc[0])
    if not female_row.empty else 0
)

male_default_rate = (
    male_row["Default_Rate"].iloc[0]
    if not male_row.empty else 0
)

female_default_rate = (
    female_row["Default_Rate"].iloc[0]
    if not female_row.empty else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Male Applicants",
        f"{male_customers:,}"
    )

with col2:
    st.metric(
        "Female Applicants",
        f"{female_customers:,}"
    )

with col3:
    st.metric(
        "Male Default Rate",
        f"{male_default_rate:.2f}%"
    )

with col4:
    st.metric(
        "Female Default Rate",
        f"{female_default_rate:.2f}%"
    )

st.markdown("---")

# ---------------------------------------------------------
# APPLICANTS BY GENDER
# ---------------------------------------------------------
st.subheader("1. Applicants by Gender")

fig_count = px.bar(
    gender_summary,
    x="CODE_GENDER",
    y="Customers",
    text="Customers",
    title="Number of Applicants by Gender"
)

fig_count.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_count, use_container_width=True)

# ---------------------------------------------------------
# DEFAULT CUSTOMERS
# ---------------------------------------------------------
st.subheader("2. Default Customers by Gender")

defaults = (
    df[df["TARGET"] == 1]
    .groupby("CODE_GENDER")
    .size()
    .reset_index(name="Defaults")
)

fig_defaults = px.bar(
    defaults,
    x="CODE_GENDER",
    y="Defaults",
    text="Defaults",
    title="Number of Default Customers by Gender"
)

fig_defaults.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(fig_defaults, use_container_width=True)

# ---------------------------------------------------------
# DEFAULT RATE
# ---------------------------------------------------------
st.subheader("3. Default Rate by Gender")

fig_risk = px.bar(
    gender_summary,
    x="CODE_GENDER",
    y="Default_Rate",
    text="Default_Rate",
    title="Default Rate Comparison",
    labels={
        "Default_Rate": "Default Rate (%)",
        "CODE_GENDER": "Gender"
    }
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_risk, use_container_width=True)

# ---------------------------------------------------------
# INCOME COMPARISON
# ---------------------------------------------------------
st.subheader("4. Average Income by Gender")

fig_income = px.bar(
    gender_summary,
    x="CODE_GENDER",
    y="Avg_Income",
    text="Avg_Income",
    title="Average Income by Gender"
)

fig_income.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(fig_income, use_container_width=True)

# ---------------------------------------------------------
# CREDIT COMPARISON
# ---------------------------------------------------------
st.subheader("5. Average Credit Amount by Gender")

fig_credit = px.bar(
    gender_summary,
    x="CODE_GENDER",
    y="Avg_Credit",
    text="Avg_Credit",
    title="Average Credit Amount by Gender"
)

fig_credit.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(fig_credit, use_container_width=True)

# ---------------------------------------------------------
# ANNUITY COMPARISON
# ---------------------------------------------------------
st.subheader("6. Average Annuity by Gender")

fig_annuity = px.bar(
    gender_summary,
    x="CODE_GENDER",
    y="Avg_Annuity",
    text="Avg_Annuity",
    title="Average Annuity by Gender"
)

fig_annuity.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(fig_annuity, use_container_width=True)

# ---------------------------------------------------------
# COMPARISON TABLE
# ---------------------------------------------------------
st.subheader("7. Gender Comparison Table")

display_table = gender_summary.copy()

display_table.columns = [
    "Gender",
    "Customers",
    "Defaults",
    "Default Rate (%)",
    "Average Income",
    "Average Credit",
    "Average Annuity"
]

display_table["Default Rate (%)"] = (
    display_table["Default Rate (%)"].round(2)
)

display_table["Average Income"] = (
    display_table["Average Income"].round(2)
)

display_table["Average Credit"] = (
    display_table["Average Credit"].round(2)
)

display_table["Average Annuity"] = (
    display_table["Average Annuity"].round(2)
)

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True
)