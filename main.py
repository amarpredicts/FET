import streamlit as st
from mongo_handler import MongoDBHandler
from expense_module import insert_expense, fetch_and_display_expenses
from salary_module import insert_salary, fetch_and_display_salaries

def main():
    st.set_page_config(page_title="Expense Tracker", page_icon=":airplane:", layout="centered")
    st.title(":airplane: Expense Tracker")

    mongo_handler = MongoDBHandler()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Insert Expense",
                                            "Insert Salary",
                                            "Total Costs",
                                            "Average Costs",
                                            "Salary Breakdown"])

    with tab1:
        insert_expense(mongo_handler)

    with tab2:
        insert_salary(mongo_handler)

    with tab3:
        fetch_and_display_expenses(mongo_handler, chart_type='grouped')

    with tab4:
        fetch_and_display_expenses(mongo_handler, chart_type='average')

    with tab5:
        fetch_and_display_salaries(mongo_handler)

    mongo_handler.close_connection()

if __name__ == "__main__":
    main()
