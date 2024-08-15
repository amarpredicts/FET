import datetime
import streamlit as st
import pandas as pd
from chart_module import prepare_data, display_grouped_bar_chart, display_stacked_bar_chart, display_average_cost_chart

def create_activity(category, title, cost):
    return {"category": category, "title": title, "cost": cost}

def insert_expense(mongo_handler):
    if "activities" not in st.session_state:
        st.session_state.activities = []

    st.subheader("Insert Expense")
    country = st.text_input("Country", "")
    city = st.text_input("City", "")
    today = datetime.datetime.now()
    this_year = today.year
    this_month = today.month
    day_after_tomorrow = today.day + 2
    date_input = st.date_input("Date", (today, datetime.date(this_year, this_month, day_after_tomorrow)), format="DD.MM.YYYY")

    st.subheader("Add Activities")
    categories = ["Transport", "Food", "Entertainment", "Accommodation", "Shopping"]
    category = st.selectbox("Category", options=categories)
    title = st.text_input("Activity Title", "")
    cost = st.text_input("Cost", "")

    if st.button("Add Activity"):
        if title and cost:
            st.session_state.activities.append(create_activity(category, title, cost))
            st.success(f"Added activity: {title}")
        else:
            st.error("Please fill in all fields")

    if st.session_state.activities:
        st.subheader("Added Activities")
        for i, activity in enumerate(st.session_state.activities):
            st.write(f"{i + 1}. {activity['category']}: {activity['title']} - {activity['cost']} €")

    if st.button("Submit"):
        if not (country and city and date_input):
            st.error("Please fill in all the general information fields.")
        elif not st.session_state.activities:
            st.error("Please add at least one activity.")
        else:
            entry = {"country": country, "city": city, "date": str(date_input), "activities": st.session_state.activities}

            if mongo_handler.insert_expense(entry):
                st.success("Insertion successful!")
                st.session_state.activities = []  # Clear activities list
            else:
                st.error("Insertion failed. Please try again.")

def fetch_and_display_expenses(mongo_handler, chart_type='grouped'):
    entries = mongo_handler.fetch_expenses()
    if chart_type == 'grouped':
        df_grouped = prepare_data(entries, group_by='country')
        display_grouped_bar_chart(df_grouped)

        df_stacked = prepare_data(entries, group_by='country', stack_by='city')
        display_stacked_bar_chart(df_stacked)

    elif chart_type == 'average':
        df_average = prepare_data(entries, group_by='country', operation='mean')
        display_average_cost_chart(df_average)
    
