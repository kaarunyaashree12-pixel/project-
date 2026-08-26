import streamlit as st
import pandas as pd

st.title("🔍 Customer Risk Explorer")

df = pd.read_csv('data/application_train.csv')

search_id = st.number_input("Enter Customer ID (SK_ID_CURR)", min_value=int(df['SK_ID_CURR'].min()), value=int(df['SK_ID_CURR'].iloc[0]))

if st.button("Search"):
    customer = df[df['SK_ID_CURR'] == search_id]
    if not customer.empty:
        st.write("### Customer Profile")
        st.table(customer[['SK_ID_CURR', 'TARGET', 'CODE_GENDER', 'AMT_INCOME_TOTAL', 'AMT_CREDIT']])
    else:
        st.error("Customer ID not found.")