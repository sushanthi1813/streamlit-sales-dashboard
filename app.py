import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Database connection

import os

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("localhost"),
            user=os.getenv("root"),
            password=os.getenv("password"),
            database=os.getenv("ecommerce")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Query execution function
def execute_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit app
st.title("E-commerce Analytics Dashboard")
st.sidebar.header("Select Query")

# Query options
queries = [
    "List all unique cities where customers are located.",
    "Count the number of orders placed in 2017.",
    "Find the total sales per category.",
    "Calculate the percentage of orders that were paid in installments.",
    "Count the number of customers from each state."
]
selected_query = st.sidebar.selectbox("Choose a query to execute:", queries)

# Execute queries based on selection
if selected_query == queries[0]:
    st.subheader("Unique Cities Where Customers Are Located")
    query = "SELECT DISTINCT(customer_city) AS city FROM customers"
    df = execute_query(query)
    st.dataframe(df)

elif selected_query == queries[1]:
    st.subheader("Total Orders in 2017")
    query = """SELECT COUNT(order_id) 
               FROM orders 
               WHERE YEAR(order_purchase_timestamp) = 2017"""
    df = execute_query(query)
    st.write(f"Total orders placed in 2017: {df.iloc[0, 0]}")

elif selected_query == queries[2]:
    st.subheader("Total Sales Per Category")
    query = """
        SELECT UPPER(products.product_category) AS category, 
               ROUND(SUM(payments.payment_value), 2) AS sales
        FROM products
        JOIN order_items ON products.product_id = order_items.product_id
        JOIN payments ON payments.order_id = order_items.order_id
        GROUP BY category
    """
    df = execute_query(query)
    st.dataframe(df)

    # Bar chart for visualization
    fig = px.bar(df, x="category", y="sales", title="Total Sales Per Category")
    st.plotly_chart(fig)

elif selected_query == queries[3]:
    st.subheader("Percentage of Orders Paid in Installments")
    query = """
        SELECT 
            ROUND(
                (SUM(CASE WHEN payment_type = 'Installments' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2
            ) AS percentage_paid_installments 
        FROM payments
    """
    df = execute_query(query)
    st.dataframe(df)

elif selected_query == queries[4]:
    st.subheader("Number of Customers From Each State")
    query = """
        SELECT customer_state AS state, COUNT(customer_id) AS num_customers 
        FROM customers 
        GROUP BY customer_state
    """
    df = execute_query(query)
    st.dataframe(df)

    # Pie chart for visualization
    fig = px.pie(df, names="state", values="num_customers", title="Customer Distribution by State")
    st.plotly_chart(fig)

# Footer
st.write("Sushanthi")

