import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Interactive Sales Analytics Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------
st.title("Interactive Sales Analytics Dashboard")
st.subheader("Bowie State University 2026")
st.write("BUIS 305 / INSS 405 - Module 5 Assignment")
st.write("Web Development with Streamlit & Python")

# ---------------------------------------------------
# FILE UPLOADER
# ---------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload your juice sales dataset (CSV or Excel file)",
    type=["csv", "xlsx"]
)

# ---------------------------------------------------
# MAIN PROCESSING
# ---------------------------------------------------
if uploaded_file is not None:

    # Read uploaded dataset
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file type.")
            st.stop()

        st.success("Dataset uploaded successfully!")

        # Preview
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        st.write("### Dataset Columns")
        st.write(list(df.columns))

        # ---------------------------------------------------
        # CLEANING REQUIRED COLUMNS
        # ---------------------------------------------------
        df["$ Sales"] = pd.to_numeric(df["$ Sales"], errors="coerce")
        df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")
        df["Service Satisfaction Rating"] = pd.to_numeric(
            df["Service Satisfaction Rating"],
            errors="coerce"
        )

        # ---------------------------------------------------
        # BONUS QUESTION: TABS
        # ---------------------------------------------------
        tab1, tab2, tab3 = st.tabs([
            "Category Sales",
            "Sales Over Time",
            "Satisfaction Ratings"
        ])

        # ===================================================
        # QUESTION 1
        # ===================================================
        with tab1:
            st.header("Question 1: Compare Sales Performance of Juices vs Smoothies")

            st.write("""
            Create a bar chart in Streamlit that compares total sales between the two product categories:
            **Juices** and **Smoothies**
            """)

            if "Category" in df.columns and "$ Sales" in df.columns:

                # Group by category
                category_sales = df.groupby("Category")["$ Sales"].sum()

                # Plot
                fig1, ax1 = plt.subplots(figsize=(8, 5))
                category_sales.plot(kind="bar", ax=ax1)

                ax1.set_title("Total Sales by Category")
                ax1.set_xlabel("Category")
                ax1.set_ylabel("Total Sales ($)")
                ax1.tick_params(axis="x", rotation=0)

                st.pyplot(fig1)

                # Interpretation
                top_category = category_sales.idxmax()
                top_sales = category_sales.max()

                st.write("### Interpretation")
                st.write(
                    f"The bar chart compares total sales revenue between Juices and Smoothies. "
                    f"**{top_category}** generated the highest total revenue with "
                    f"**${top_sales:,.2f}** in sales, indicating stronger business performance."
                )

            else:
                st.error("Required columns 'Category' and '$ Sales' are missing.")

        # ===================================================
        # QUESTION 2
        # ===================================================
        with tab2:
            st.header("Question 2: Sales Over Timeline Chart")

            if "Date Ordered" in df.columns and "$ Sales" in df.columns:

                # Group by date
                daily_sales = (
                    df.groupby("Date Ordered")["$ Sales"]
                    .sum()
                    .sort_index()
                )

                # Plot
                fig2, ax2 = plt.subplots(figsize=(10, 5))
                daily_sales.plot(kind="line", marker="o", ax=ax2)

                ax2.set_title("Daily Sales Trend Over Time")
                ax2.set_xlabel("Date Ordered")
                ax2.set_ylabel("Total Sales ($)")

                st.pyplot(fig2)

                # Interpretation
                highest_date = daily_sales.idxmax()
                highest_sales = daily_sales.max()

                st.write("### Interpretation")
                st.write(
                    f"The line chart visualizes sales trends over time. "
                    f"The highest sales occurred on **{highest_date.date()}**, "
                    f"with total sales reaching **${highest_sales:,.2f}**. "
                    f"This chart helps identify sales fluctuations and peak business days."
                )

            else:
                st.error("Required columns 'Date Ordered' and '$ Sales' are missing.")

        # ===================================================
        # QUESTION 3
        # ===================================================
        with tab3:
            st.header("Question 3: Service Satisfaction Distribution")

            if "Service Satisfaction Rating" in df.columns:

                # Handle missing values
                satisfaction = df["Service Satisfaction Rating"].dropna()

                # Count ratings
                satisfaction_counts = satisfaction.value_counts().sort_index()

                # Plot
                fig3, ax3 = plt.subplots(figsize=(8, 5))
                satisfaction_counts.plot(kind="bar", ax=ax3)

                ax3.set_title("Service Satisfaction Rating Distribution")
                ax3.set_xlabel("Satisfaction Rating")
                ax3.set_ylabel("Number of Customers")
                ax3.tick_params(axis="x", rotation=0)

                st.pyplot(fig3)

                # Interpretation
                most_common_rating = satisfaction_counts.idxmax()
                most_common_count = satisfaction_counts.max()

                st.write("### Interpretation")
                st.write(
                    f"The satisfaction chart displays customer service ratings from 1–5. "
                    f"The most common rating was **{most_common_rating}**, selected by "
                    f"**{most_common_count}** customers. "
                    f"This provides insight into customer satisfaction trends."
                )

            else:
                st.error("Required column 'Service Satisfaction Rating' is missing.")

    except Exception as e:
        st.error("An error occurred while processing the file.")
        st.write(e)

else:
    st.info("Please upload your dataset to begin analysis.")
