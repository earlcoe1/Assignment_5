import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("Interactive Sales Analytics Dashboard")
st.write("BUIS 305 / INSS 405 - Assignment 5")

uploaded_file = st.file_uploader(
    "Upload your juice sales dataset (CSV or Excel file)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.success("File uploaded successfully!")

        st.write("### Preview of the Dataset")
        st.dataframe(df.head())
        st.dataframe(df.tail())

        st.write("### Dataset Columns")
        st.write(list(df.columns))

        # Clean required columns
        if "$ Sales" in df.columns:
            df["$ Sales"] = pd.to_numeric(df["$ Sales"], errors="coerce")

        tab1, tab2, tab3 = st.tabs([
            "Category Sales",
            "Sales Over Time",
            "Satisfaction Ratings"
        ])

        # Question 1
        with tab1:
            st.subheader("Question 1: Sales Performance of Juices vs Smoothies")

            if "Category" in df.columns and "$ Sales" in df.columns:
                category_sales = df.groupby("Category")["$ Sales"].sum().sort_values(ascending=False)

                fig1, ax1 = plt.subplots()
                category_sales.plot(kind="bar", ax=ax1)

                ax1.set_title("Total Sales by Category")
                ax1.set_xlabel("Category")
                ax1.set_ylabel("Total Sales ($)")
                ax1.tick_params(axis="x", rotation=0)

                st.pyplot(fig1)

                top_category = category_sales.idxmax()
                top_sales = category_sales.max()

                st.write("### Interpretation")
                st.write(
                    f"The bar chart compares total sales between Juices and Smoothies. "
                    f"{top_category} generated the highest total revenue with "
                    f"${top_sales:,.2f} in sales."
                )
            else:
                st.error("Required columns 'Category' and/or '$ Sales' not found.")

        # Question 2
        with tab2:
            st.subheader("Question 2: Sales Over Timeline Chart")

            if "Date Ordered" in df.columns and "$ Sales" in df.columns:
                df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")

                daily_sales = (
                    df.dropna(subset=["Date Ordered"])
                    .groupby("Date Ordered")["$ Sales"]
                    .sum()
                    .sort_index()
                )

                fig2, ax2 = plt.subplots()
                daily_sales.plot(kind="line", marker="o", ax=ax2)

                ax2.set_title("Daily Sales Trend Over Time")
                ax2.set_xlabel("Date Ordered")
                ax2.set_ylabel("Total Sales ($)")

                st.pyplot(fig2)

                highest_date = daily_sales.idxmax()
                highest_sales = daily_sales.max()

                st.write("### Interpretation")
                st.write(
                    f"The line chart shows how total sales changed over time. "
                    f"The highest sales occurred on {highest_date.date()} with "
                    f"${highest_sales:,.2f} in total sales."
                )
            else:
                st.error("Required columns 'Date Ordered' and/or '$ Sales' not found.")

        # Question 3
        with tab3:
            st.subheader("Question 3: Service Satisfaction Distribution")

            if "Service Satisfaction Rating" in df.columns:
                satisfaction = df["Service Satisfaction Rating"].dropna()
                satisfaction_counts = satisfaction.value_counts().sort_index()

                fig3, ax3 = plt.subplots()
                satisfaction_counts.plot(kind="bar", ax=ax3)

                ax3.set_title("Service Satisfaction Rating Distribution")
                ax3.set_xlabel("Satisfaction Rating")
                ax3.set_ylabel("Number of Customers")
                ax3.tick_params(axis="x", rotation=0)

                st.pyplot(fig3)

                most_common_rating = satisfaction_counts.idxmax()
                most_common_count = satisfaction_counts.max()

                st.write("### Interpretation")
                st.write(
                    f"The chart shows how customers rated service satisfaction. "
                    f"The most common rating was {most_common_rating}, selected by "
                    f"{most_common_count} customers."
                )
            else:
                st.error("Required column 'Service Satisfaction Rating' not found.")

    except Exception as e:
        st.error("An error occurred while processing the file.")
        st.write(e)

else:
    st.info("Please upload a dataset to begin.")
