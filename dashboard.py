import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---- Title ----
st.title("Sales Performance Dashboard")

# ---- Dummy Data Generation ----
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=366)
products = ['Laptop', 'Mouse', 'Monitor', 'Keyboard']
regions = ['North', 'South', 'East', 'West']

data = {
    "Date": np.random.choice(dates, 500),
    "Product": np.random.choice(products, 500),
    "Region": np.random.choice(regions, 500),
    "Sales": np.random.uniform(100, 2000, 500),
    "Profit": np.random.uniform(-300, 800, 500)
}
df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values("Date", inplace=True)

# ---- Sidebar Filters ----
st.sidebar.header("Filters")
region_filter = st.sidebar.multiselect(
    "Select Region", options=regions, default=regions
)
product_filter = st.sidebar.multiselect(
    "Select Product", options=products, default=products
)

filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Product'].isin(product_filter))
]

# ---- KPI Row ----
total_sales = filtered_df["Sales"].sum()
average_profit = filtered_df["Profit"].mean()
total_transactions = len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Average Profit", f"${average_profit:,.2f}")
col3.metric("Total Transactions", total_transactions)

st.markdown("---")

# ---- Visualizations ----
col_v1, col_v2 = st.columns([1.3, 1.7])

# --- Bar Chart: Sales by Product ---
with col_v1:
    by_product = filtered_df.groupby("Product")["Sales"].sum().reset_index()
    fig_bar = px.bar(
        by_product,
        x="Product",
        y="Sales",
        color="Product",
        text_auto=".2s",
        title="Sales by Product",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_layout(showlegend=False, height=350, margin=dict(t=60, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Line Chart: Sales over Time (monthly) ---
with col_v2:
    monthly_sales = (
        filtered_df
        .assign(Month=filtered_df["Date"].dt.to_period("M").astype(str))
        .groupby("Month")["Sales"].sum().reset_index()
    )
    fig_line = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True,
        line_shape="spline"
    )
    fig_line.update_layout(height=350, margin=dict(t=60, b=10))
    st.plotly_chart(fig_line, use_container_width=True)

# --- Scatter Chart: Sales vs Profit ---
st.markdown("### Sales vs Profit")
fig_scatter = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Product",
    title="Sales vs Profit by Product",
    hover_data=["Region", "Date"],
    opacity=0.8,
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig_scatter.update_layout(height=400, margin=dict(t=40, b=20))
st.plotly_chart(fig_scatter, use_container_width=True)

