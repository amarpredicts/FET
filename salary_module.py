import streamlit as st
import pandas as pd
from chart_module import prepare_data_salary, display_grouped_pie_chart, display_monthly_bar_chart

def insert_salary(mongo_handler):
    st.subheader("Add Salary Items")
    date_input = st.date_input("Date", pd.to_datetime('today').date(), format="DD.MM.YYYY", key="Salary")
    categories = ["Base Salary", "Language Expense", "Layover Expense", "Provision", "Other"]
    category = st.selectbox("Category", options=categories)
    amount = st.text_input("Amount", "")

    if st.button("Submit", "salary_submit"):
        if not (category and amount and date_input):
            st.error("Please fill in all the information fields.")
        else:
            entry = {"category": category, "date": str(date_input), "amount": amount}
            if mongo_handler.insert_salary(entry):
                st.success("Insertion successful!")
            else:
                st.error("Insertion failed. Please try again.")

def fetch_and_display_salaries(mongo_handler):
    salary_items = mongo_handler.fetch_salary_items()

    df_monthly = prepare_data_salary(salary_items, group_by='category', stack_by='month_year', operation='sum')
    display_monthly_bar_chart(df_monthly)

    df_grouped = prepare_data_salary(salary_items, group_by='category')
    display_grouped_pie_chart(df_grouped)
    
    