
Thumbnails

1
/ 2


Fit Page






import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.title("Interactive Sales Analytics Dashboard")
uploaded_file = st.file_uploader(
"Upload your juice sales dataset (CSV or Excel file)",
type=["csv", "xlsx"]
)
if uploaded_file is not None:
if uploaded_file.name.endswith(".csv"):
df = pd.read_csv(uploaded_file)
else:
df = pd.read_excel(uploaded_file)
st.success("File uploaded successfully!")
st.write("### Preview of the Dataset")
st.dataframe(df.head())
st.dataframe(df.tail())
st.write("### Dataset Columns")
st.write(df.columns)
tab1, tab2, tab3 = st.tabs([
"Category Sales",
"Sales Over Time",
"Satisfaction Ratings"
])
with tab1:
st.subheader("Question 1: Sales Performance of Juices vs Smoothies")
if "Category" in df.columns and "$ Sales" in df.columns:
category_sales = df.groupby("Category")["$ Sales"].sum()
fig1, ax1 = plt.subplots()
category_sales.plot(kind="bar", ax=ax1)
ax1.set_title("Total Sales by Category")
ax1.set_xlabel("Category")
ax1.set_ylabel("Total Sales ($)")
st.pyplot(fig1)
top_category = category_sales.idxmax()
top_sales = category_sales.max()
st.write(
f"### Interpretation:\n"
f"{top_category} generated the highest total revenue "
f"with sales of ${top_sales:,.2f}."
)
else:
st.error("Required columns 'Category' and/or '$ Sales' not found.")
with tab2:
st.subheader("Question 2: Sales Over Timeline Chart")
if "Date Ordered" in df.columns and "$ Sales" in df.columns:
df["Date Ordered"] = pd.to_datetime(df["Date Ordered"])
daily_sales = df.groupby("Date Ordered")["$ Sales"].sum()
fig2, ax2 = plt.subplots()
daily_sales.plot(kind="line", ax=ax2)
ax2.set_title("Daily Sales Trend Over Time")
ax2.set_xlabel("Date Ordered")
ax2.set_ylabel("Total Sales ($)")
st.pyplot(fig2)
highest_date = daily_sales.idxmax()
highest_sales = daily_sales.max()
st.write(
f"### Interpretation:\n"
f"The highest sales occurred on {highest_date.date()} "
f"with total sales of ${highest_sales:,.2f}. "
f"This chart shows how daily sales fluctuate over time."
)
else:

st.error("Required columns 'Date Ordered' and/or '$ Sales' not found.")
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
st.pyplot(fig3)
most_common_rating = satisfaction_counts.idxmax()
most_common_count = satisfaction_counts.max()
st.write(
f"### Interpretation:\n"
f"The most common customer satisfaction rating was "
f"{most_common_rating}, with {most_common_count} customers selecting it."
)
else:
st.error("Required column 'Service Satisfaction Rating' not found.")
else:
st.info("Please upload a dataset to begin.")

