
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Default Analysis",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Default / Target Analysis")
st.markdown(
    "Analysis of the TARGET variable to understand repayment and default patterns."
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
# BASIC COUNTS
# ---------------------------------------------------------
total_customers = len(df)
non_default = (df["TARGET"] == 0).sum()
default = (df["TARGET"] == 1).sum()

default_rate = (default / total_customers) * 100
non_default_rate = (non_default / total_customers) * 100

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "TARGET = 0",
        f"{non_default:,}"
    )

with col2:
    st.metric(
        "TARGET = 1",
        f"{default:,}"
    )

with col3:
    st.metric(
        "Default Rate",
        f"{default_rate:.2f}%"
    )

with col4:
    st.metric(
        "Non-Default Rate",
        f"{non_default_rate:.2f}%"
    )

st.markdown("---")

# ---------------------------------------------------------
# TARGET COUNT
# ---------------------------------------------------------
st.subheader("1. TARGET Distribution")

target_counts = (
    df["TARGET"]
    .value_counts()
    .sort_index()
    .reset_index()
)

target_counts.columns = ["TARGET", "Customers"]

target_counts["Status"] = target_counts["TARGET"].map({
    0: "Non-Default / Repaid",
    1: "Default / Payment Difficulty"
})

fig_target = px.bar(
    target_counts,
    x="Status",
    y="Customers",
    text="Customers",
    title="Number of Customers by TARGET",
    labels={
        "Status": "Customer Status",
        "Customers": "Number of Customers"
    }
)

fig_target.update_traces(texttemplate="%{text:,}", textposition="outside")

st.plotly_chart(fig_target, use_container_width=True)

# ---------------------------------------------------------
# TARGET PIE
# ---------------------------------------------------------
st.subheader("2. Default vs Non-Default Percentage")

fig_pie = px.pie(
    target_counts,
    values="Customers",
    names="Status",
    hole=0.45,
    title="Customer Repayment Status"
)

st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------------
# GENDER DEFAULT RATE
# ---------------------------------------------------------
st.subheader("3. Default Rate by Gender")

gender_risk = (
    df.groupby("CODE_GENDER", dropna=False)["TARGET"]
    .mean()
    .reset_index()
)

gender_risk["Default Rate (%)"] = gender_risk["TARGET"] * 100

fig_gender = px.bar(
    gender_risk,
    x="CODE_GENDER",
    y="Default Rate (%)",
    text="Default Rate (%)",
    title="Default Rate by Gender"
)

fig_gender.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_gender, use_container_width=True)

# ---------------------------------------------------------
# INCOME TYPE
# ---------------------------------------------------------
st.subheader("4. Default Rate by Income Type")

income_risk = (
    df.groupby("NAME_INCOME_TYPE", dropna=False)["TARGET"]
    .mean()
    .reset_index()
)

income_risk["Default Rate (%)"] = income_risk["TARGET"] * 100

income_risk = income_risk.sort_values(
    "Default Rate (%)",
    ascending=False
)

fig_income = px.bar(
    income_risk,
    x="Default Rate (%)",
    y="NAME_INCOME_TYPE",
    orientation="h",
    text="Default Rate (%)",
    title="Default Rate by Income Type"
)

fig_income.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_income, use_container_width=True)

# ---------------------------------------------------------
# EDUCATION
# ---------------------------------------------------------
st.subheader("5. Default Rate by Education")

education_risk = (
    df.groupby("NAME_EDUCATION_TYPE", dropna=False)["TARGET"]
    .mean()
    .reset_index()
)

education_risk["Default Rate (%)"] = (
    education_risk["TARGET"] * 100
)

education_risk = education_risk.sort_values(
    "Default Rate (%)",
    ascending=False
)

fig_education = px.bar(
    education_risk,
    x="Default Rate (%)",
    y="NAME_EDUCATION_TYPE",
    orientation="h",
    text="Default Rate (%)",
    title="Default Rate by Education Level"
)

fig_education.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_education, use_container_width=True)

# ---------------------------------------------------------
# CONTRACT TYPE
# ---------------------------------------------------------
st.subheader("6. Default Rate by Contract Type")

contract_risk = (
    df.groupby("NAME_CONTRACT_TYPE", dropna=False)["TARGET"]
    .mean()
    .reset_index()
)

contract_risk["Default Rate (%)"] = (
    contract_risk["TARGET"] * 100
)

fig_contract = px.bar(
    contract_risk,
    x="NAME_CONTRACT_TYPE",
    y="Default Rate (%)",
    text="Default Rate (%)",
    title="Default Rate by Contract Type"
)

fig_contract.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(fig_contract, use_container_width=True)

# ---------------------------------------------------------
# SUMMARY TABLE
# ---------------------------------------------------------
st.subheader("7. Default Analysis Summary")

summary = pd.DataFrame({
    "Metric": [
        "Total Customers",
        "Non-Default Customers",
        "Default Customers",
        "Non-Default Rate",
        "Default Rate"
    ],
    "Value": [
        f"{total_customers:,}",
        f"{non_default:,}",
        f"{default:,}",
        f"{non_default_rate:.2f}%",
        f"{default_rate:.2f}%"
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)