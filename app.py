import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Setup
# --------------------------------------------------
st.set_page_config(
    page_title="Interactive Sales Analytics Dashboard",
    layout="wide"
)

st.title("Interactive Sales Analytics Dashboard")
st.subheader("BOWIE STATE UNIVERSITY 2026")
st.write("BUIS 305 / INSS 405 - Module 5 - Assignment 5")
st.write("Topic: Web Development with Streamlit & Python")

# --------------------------------------------------
# File Uploader Requirement
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload your juice sales dataset (CSV or Excel file)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # --------------------------------------------------
    # Load CSV or Excel Dataset
    # --------------------------------------------------
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    st.success("File uploaded successfully!")

    # --------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------
    st.write("### Preview of Dataset")
    st.dataframe(df.head())

    st.write("### Dataset Columns")
    st.write(list(df.columns))

    # --------------------------------------------------
    # Clean Required Columns
    # --------------------------------------------------
    df["$ Sales"] = pd.to_numeric(df["$ Sales"], errors="coerce")
    df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")
    df["Service Satisfaction Rating"] = pd.to_numeric(
        df["Service Satisfaction Rating"],
        errors="coerce"
    )

    # --------------------------------------------------
    # Bonus Requirement: Dashboard Tabs
    # --------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "Category Sales",
        "Sales Over Time",
        "Satisfaction Ratings"
    ])

    # --------------------------------------------------
    # Question 1: Category Sales Comparison
    # --------------------------------------------------
    with tab1:
        st.header("Question 1: Compare Sales Performance of Juices vs Smoothies")

        category_sales = df.groupby("Category")["$ Sales"].sum()

        fig1, ax1 = plt.subplots(figsize=(8, 5))
        category_sales.plot(kind="bar", ax=ax1)

        ax1.set_title("Total Sales: Juices vs Smoothies")
        ax1.set_xlabel("Product Category")
        ax1.set_ylabel("Total Sales ($)")
        ax1.tick_params(axis="x", rotation=0)

        st.pyplot(fig1)

        top_category = category_sales.idxmax()
        top_sales = category_sales.max()

        st.write("### Interpretation")
        st.write(
            f"The bar chart compares total sales between Juices and Smoothies. "
            f"The category with the highest revenue is **{top_category}**, with total sales of "
            f"**${top_sales:,.2f}**. This shows which product category generated more revenue."
        )

    # --------------------------------------------------
    # Question 2: Sales Over Time
    # --------------------------------------------------
    with tab2:
        st.header("Question 2: Create a Sales Over Timeline Chart")

        daily_sales = df.groupby("Date Ordered")["$ Sales"].sum().sort_index()

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        daily_sales.plot(kind="line", marker="o", ax=ax2)

        ax2.set_title("Daily Sales Trend Over Time")
        ax2.set_xlabel("Date Ordered")
        ax2.set_ylabel("Total Sales ($)")

        st.pyplot(fig2)

        highest_date = daily_sales.idxmax()
        highest_sales = daily_sales.max()

        st.write("### Interpretation")
        st.write(
            f"The line chart shows how sales changed over time using the Date Ordered column. "
            f"The highest sales occurred on **{highest_date.date()}**, with total sales of "
            f"**${highest_sales:,.2f}**. This helps identify daily sales trends and peak sales days."
        )

    # --------------------------------------------------
    # Question 3: Service Satisfaction Distribution
    # --------------------------------------------------
    with tab3:
        st.header("Question 3: Visualize Service Satisfaction Distribution")

        satisfaction = df["Service Satisfaction Rating"].dropna()
        satisfaction_counts = satisfaction.value_counts().sort_index()

        fig3, ax3 = plt.subplots(figsize=(8, 5))
        satisfaction_counts.plot(kind="bar", ax=ax3)

        ax3.set_title("Service Satisfaction Rating Distribution")
        ax3.set_xlabel("Service Satisfaction Rating")
        ax3.set_ylabel("Number of Customers")
        ax3.tick_params(axis="x", rotation=0)

        st.pyplot(fig3)

        most_common_rating = satisfaction_counts.idxmax()
        most_common_count = satisfaction_counts.max()

        st.write("### Interpretation")
        st.write(
            f"The chart shows how customers rated the service. Missing values were removed before "
            f"creating the chart. The most common service satisfaction rating is "
            f"**{most_common_rating}**, selected by **{most_common_count}** customers."
        )

else:
    st.info("Please upload the juice sales dataset to begin.")
