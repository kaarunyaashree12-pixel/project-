
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Regional Risk Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Regional Risk Analysis")
st.markdown(
    "Analyze whether customer location characteristics are associated "
    "with loan default risk."
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
# CHECK REQUIRED COLUMNS
# ---------------------------------------------------------
required_columns = [
    "REGION_POPULATION_RELATIVE",
    "REGION_RATING_CLIENT",
    "REGION_RATING_CLIENT_W_CITY",
    "REG_REGION_NOT_LIVE_REGION",
    "REG_REGION_NOT_WORK_REGION",
    "REG_CITY_NOT_LIVE_CITY",
    "REG_CITY_NOT_WORK_CITY",
    "TARGET",
    "AMT_CREDIT",
    "AMT_INCOME_TOTAL"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "The following required columns are missing from the dataset:"
    )
    st.write(missing_columns)
    st.stop()

# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------
most_common_rating = (
    df["REGION_RATING_CLIENT"]
    .mode(dropna=True)
)

if not most_common_rating.empty:
    most_common_rating = int(most_common_rating.iloc[0])
else:
    most_common_rating = 0

rating_risk = (
    df.groupby("REGION_RATING_CLIENT")["TARGET"]
    .mean()
)

if not rating_risk.empty:
    highest_risk_rating = int(
        rating_risk.idxmax()
    )
else:
    highest_risk_rating = 0

avg_population_indicator = (
    df["REGION_POPULATION_RELATIVE"].mean()
)

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Most Common Region Rating",
        str(most_common_rating)
    )

with col2:
    st.metric(
        "Highest Risk Region Rating",
        str(highest_risk_rating)
    )

with col3:
    st.metric(
        "Avg Regional Population Indicator",
        f"{avg_population_indicator:.4f}"
    )

st.markdown("---")

# ---------------------------------------------------------
# CUSTOMERS BY REGION RATING
# ---------------------------------------------------------
st.subheader("1. Customers by Region Rating")

rating_counts = (
    df["REGION_RATING_CLIENT"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_counts.columns = [
    "Region Rating",
    "Customers"
]

fig_count = px.bar(
    rating_counts,
    x="Region Rating",
    y="Customers",
    text="Customers",
    title="Number of Customers by Region Rating"
)

fig_count.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

st.plotly_chart(
    fig_count,
    use_container_width=True
)

# ---------------------------------------------------------
# DEFAULT RATE BY REGION RATING
# ---------------------------------------------------------
st.subheader("2. Default Rate by Region Rating")

rating_risk_df = (
    df.groupby("REGION_RATING_CLIENT")
    .agg(
        Customers=("TARGET", "count"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

rating_risk_df["Default_Rate"] *= 100

fig_risk = px.bar(
    rating_risk_df,
    x="REGION_RATING_CLIENT",
    y="Default_Rate",
    text="Default_Rate",
    title="Default Rate by Region Rating",
    labels={
        "REGION_RATING_CLIENT": "Region Rating",
        "Default_Rate": "Default Rate (%)"
    }
)

fig_risk.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# ---------------------------------------------------------
# CREDIT BY REGION RATING
# ---------------------------------------------------------
st.subheader("3. Average Credit by Region Rating")

credit_region = (
    df.groupby("REGION_RATING_CLIENT")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

fig_credit = px.bar(
    credit_region,
    x="REGION_RATING_CLIENT",
    y="AMT_CREDIT",
    text="AMT_CREDIT",
    title="Average Credit Amount by Region Rating",
    labels={
        "REGION_RATING_CLIENT": "Region Rating",
        "AMT_CREDIT": "Average Credit"
    }
)

fig_credit.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)

# ---------------------------------------------------------
# INCOME BY REGION RATING
# ---------------------------------------------------------
st.subheader("4. Average Income by Region Rating")

income_region = (
    df.groupby("REGION_RATING_CLIENT")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)

fig_income = px.bar(
    income_region,
    x="REGION_RATING_CLIENT",
    y="AMT_INCOME_TOTAL",
    text="AMT_INCOME_TOTAL",
    title="Average Income by Region Rating",
    labels={
        "REGION_RATING_CLIENT": "Region Rating",
        "AMT_INCOME_TOTAL": "Average Income"
    }
)

fig_income.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)

# ---------------------------------------------------------
# REGION MISMATCH ANALYSIS
# ---------------------------------------------------------
st.subheader("5. Regional Mismatch vs Default")

mismatch_columns = [
    "REG_REGION_NOT_LIVE_REGION",
    "REG_REGION_NOT_WORK_REGION"
]

mismatch_data = []

for column in mismatch_columns:

    temp = (
        df.groupby(column)["TARGET"]
        .mean()
        .reset_index()
    )

    temp["Default Rate (%)"] = (
        temp["TARGET"] * 100
    )

    temp["Mismatch Type"] = column

    temp["Status"] = temp[column].map({
        0: "No Mismatch",
        1: "Mismatch"
    })

    mismatch_data.append(temp)

region_mismatch = pd.concat(
    mismatch_data,
    ignore_index=True
)

fig_region_mismatch = px.bar(
    region_mismatch,
    x="Mismatch Type",
    y="Default Rate (%)",
    color="Status",
    barmode="group",
    text="Default Rate (%)",
    title="Default Rate by Regional Mismatch"
)

fig_region_mismatch.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_region_mismatch,
    use_container_width=True
)

# ---------------------------------------------------------
# CITY MISMATCH
# ---------------------------------------------------------
st.subheader("6. City Mismatch vs Default")

city_mismatch_columns = [
    "REG_CITY_NOT_LIVE_CITY",
    "REG_CITY_NOT_WORK_CITY"
]

city_data = []

for column in city_mismatch_columns:

    temp = (
        df.groupby(column)["TARGET"]
        .mean()
        .reset_index()
    )

    temp["Default Rate (%)"] = (
        temp["TARGET"] * 100
    )

    temp["Mismatch Type"] = column

    temp["Status"] = temp[column].map({
        0: "No Mismatch",
        1: "Mismatch"
    })

    city_data.append(temp)

city_mismatch = pd.concat(
    city_data,
    ignore_index=True
)

fig_city_mismatch = px.bar(
    city_mismatch,
    x="Mismatch Type",
    y="Default Rate (%)",
    color="Status",
    barmode="group",
    text="Default Rate (%)",
    title="Default Rate by City Mismatch"
)

fig_city_mismatch.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_city_mismatch,
    use_container_width=True
)

# ---------------------------------------------------------
# REGION RATING COMPARISON TABLE
# ---------------------------------------------------------
st.subheader("7. Regional Risk Summary")

regional_summary = (
    df.groupby("REGION_RATING_CLIENT")
    .agg(
        Customers=("SK_ID_CURR", "count"),
        Defaults=("TARGET", "sum"),
        Default_Rate=("TARGET", "mean"),
        Average_Credit=("AMT_CREDIT", "mean"),
        Average_Income=("AMT_INCOME_TOTAL", "mean"),
        Average_Population_Ratio=(
            "REGION_POPULATION_RELATIVE",
            "mean"
        )
    )
    .reset_index()
)

regional_summary["Default_Rate"] *= 100

regional_summary = regional_summary.sort_values(
    "Default_Rate",
    ascending=False
)

regional_summary.columns = [
    "Region Rating",
    "Customers",
    "Defaults",
    "Default Rate (%)",
    "Average Credit",
    "Average Income",
    "Average Population Indicator"
]

st.dataframe(
    regional_summary,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# INTERPRETATION
# ---------------------------------------------------------
st.subheader("8. Regional Risk Interpretation")

highest_risk_rate = regional_summary[
    "Default Rate (%)"
].max()

lowest_risk_rate = regional_summary[
    "Default Rate (%)"
].min()

st.write(
    f"• Highest observed default rate among region ratings: "
    f"**{highest_risk_rate:.2f}%**."
)

st.write(
    f"• Lowest observed default rate among region ratings: "
    f"**{lowest_risk_rate:.2f}%**."
)

st.info(
    "A higher region rating represents a different client-risk "
    "classification in the Home Credit dataset. Use the observed "
    "default rates together with other customer characteristics "
    "rather than treating region rating as a standalone cause of default."
)