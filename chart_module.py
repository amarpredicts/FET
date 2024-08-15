import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def prepare_data(data_dict, group_by='country', stack_by=None, operation='sum'):
    chart_data = []
    for entry in data_dict.values():
        group_value = entry[group_by]
        stack_value = entry.get(stack_by)
        for activity in entry['activities']:
            data_entry = {group_by: group_value, 'category': activity['category'], 'cost': float(activity['cost'])}
            if stack_by:
                data_entry[stack_by] = stack_value
            chart_data.append(data_entry)
    df = pd.DataFrame(chart_data)
    agg_func = 'mean' if operation == 'mean' else 'sum'
    pivot_args = {'values': 'cost', 'index': [group_by] if not stack_by else [group_by, stack_by], 'columns': 'category', 'aggfunc': agg_func}
    return df.pivot_table(**pivot_args).fillna(0)

def prepare_data_salary(data_dict, group_by='category', stack_by=None, operation='sum'):
    chart_data = []
    for entry in data_dict.values():
        group_value = entry[group_by]
        stack_value = None
        if stack_by:
            if stack_by == 'month_year':
                date = pd.to_datetime(entry['date'])
                stack_value = date.strftime('%Y-%m')
            else:
                stack_value = entry[stack_by]
        data_entry = {group_by: group_value, 'amount': float(entry['amount'])}
        if stack_by:
            data_entry[stack_by] = stack_value
        chart_data.append(data_entry)
    df = pd.DataFrame(chart_data)
    agg_func = 'mean' if operation == 'mean' else 'sum'
    group_columns = [group_by] if not stack_by else [group_by, stack_by]
    return df.groupby(group_columns, as_index=False).agg({'amount': agg_func})

def create_bar_traces(df_pivot, index_level=0):
    traces = []
    x_values = df_pivot.index.get_level_values(index_level)
    for category in df_pivot.columns:
        traces.append(go.Bar(x=x_values, y=df_pivot[category], name=category))
    return traces

def display_grouped_bar_chart(df_pivot):
    fig = go.Figure(create_bar_traces(df_pivot, index_level=0))
    fig.update_layout(title="Total Costs by Country and Category", xaxis_title="Country", yaxis_title="Total Cost", barmode='group', bargap=0.15, bargroupgap=0.1)
    st.plotly_chart(fig)

def display_stacked_bar_chart(df_pivot):
    fig = go.Figure()
    for category in df_pivot.columns:
        fig.add_trace(go.Bar(x=df_pivot.index.get_level_values(1), y=df_pivot[category], name=category, hoverinfo="x+y+name"))
    fig.update_layout(title="Total Costs by City and Category", xaxis_title="City", yaxis_title="Total Cost", barmode='stack', xaxis_tickangle=-45)
    st.plotly_chart(fig)

def display_average_cost_chart(df_pivot):
    fig = go.Figure(create_bar_traces(df_pivot, index_level=0))
    fig.update_layout(title="Average Costs by Country and Category", xaxis_title="Country", yaxis_title="Average Cost", barmode='stack', bargap=0.15, bargroupgap=0.1)
    st.plotly_chart(fig)

def display_grouped_pie_chart(df_salary):
    fig = px.pie(df_salary, names='category', values='amount', title='In Total Money Received')
    # Update the chart to display the amount in the slices instead of percentage
    fig.update_traces(
        textinfo='value', # Shows category labels and actual values
        hovertemplate='%{label}: %{value:.2f}'  # Hover shows the category and exact amount
    )
    # Display the pie chart in Streamlit
    st.plotly_chart(fig)

def display_monthly_bar_chart(df_salary):
    fig = px.bar(
    df_salary,
    x='month_year',
    y='amount',
    color='category',
    title='Monthly Expenses Breakdown by Category',
    labels={'month_year': 'Month-Year', 'amount': 'Total Amount'},
    text_auto=True
)

    # Update layout for better readability
    fig.update_layout(
        barmode='stack',  # Stack the bars by categories
        xaxis_tickangle=-45  # Rotate x-axis labels for better visibility
    )

    # Update x-axis with proper labels
    fig.update_xaxes(
        tickangle=-45,    # Rotate for visibility
        tickmode='array'
    )

    fig.add_shape(
    type="line",
    opacity=0.8,
    x0=df_salary['month_year'].min(),  # Start of x-axis
    x1=df_salary['month_year'].max(),  # End of x-axis
    y0=2762,  # The y-coordinate for the line
    y1=2762,  # The y-coordinate for the line (same as y0 for a horizontal line)
    line=dict(color="Red", width=2, dash="dash"),  # Customize the line
    name="Target Line"
    )

    # Optionally add annotation to describe the line
    fig.add_annotation(
        x=df_salary['month_year'].max(),
        y=2760,
        text="Telekom: 2.762",
        showarrow=False,
        yshift=10,  # Adjust this value as needed
        xshift=10  # Adjust this value as needed
    )

    st.plotly_chart(fig)