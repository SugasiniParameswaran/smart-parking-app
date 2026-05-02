import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import calendar

st.title("Admin ML Analytics")

conn = sqlite3.connect("parking.db")
df = pd.read_sql_query("SELECT login_time FROM drivers", conn)
conn.close()

if df.empty:
    st.error("No driver login data found in database.")
    st.stop()

df["login_time"] = pd.to_datetime(df["login_time"], errors="coerce")
df = df.dropna(subset=["login_time"])

if df.empty:
    st.error("No valid login time data found.")
    st.stop()

df["year"] = df["login_time"].dt.year
df["month_num"] = df["login_time"].dt.month
df["month"] = df["month_num"].apply(lambda x: calendar.month_name[x])
df["hour_num"] = df["login_time"].dt.hour

agg_df = df.groupby(["year", "month_num", "hour_num"]).size().reset_index(name="customer_count")
agg_df["month"] = agg_df["month_num"].apply(lambda x: calendar.month_name[x])

st.subheader("Year, Month and Time-wise Summary")
st.write("This table shows how many customers logged in for each year, month, and time.")
st.dataframe(agg_df[["year", "month", "hour_num", "customer_count"]])

if len(agg_df) < 2:
    st.warning("Not enough data for regression yet. Please add more driver logins at different times.")
    st.stop()

X = agg_df[["year", "month_num", "hour_num"]]
y = agg_df["customer_count"]

model = LinearRegression()
model.fit(X, y)
hour_summary = df.groupby("hour_num").size().reset_index(name="customer_count")
month_summary = df.groupby(["year", "month_num"]).size().reset_index(name="customer_count")

peak_hour_num = hour_summary.loc[hour_summary["customer_count"].idxmax(), "hour_num"]
peak_hour_label = pd.to_datetime(str(peak_hour_num), format="%H").strftime("%I %p").lstrip("0")

peak_month_row = month_summary.loc[month_summary["customer_count"].idxmax()]
peak_month_label = calendar.month_name[int(peak_month_row["month_num"])]
peak_year_label = int(peak_month_row["year"])

st.subheader("Demand Insights")
st.write(f"**Peak Time:** {peak_hour_label}")
st.write(f"**Peak Month:** {peak_month_label} {peak_year_label}")

st.subheader("Customers by Time")

# create full 24-hour sequence
full_hours = pd.DataFrame({"hour_num": list(range(24))})
hour_summary = full_hours.merge(hour_summary, on="hour_num", how="left").fillna(0)

hour_summary["time_label"] = hour_summary["hour_num"].apply(
    lambda x: pd.to_datetime(str(x), format="%H").strftime("%I %p").lstrip("0")
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(hour_summary["hour_num"], hour_summary["customer_count"], marker="o")
ax1.set_xticks(range(0, 24, 2))
ax1.set_xticklabels(
    [pd.to_datetime(str(x), format="%H").strftime("%I %p").lstrip("0") for x in range(0, 24, 2)],
    rotation=45
)
ax1.set_xlabel("Time")
ax1.set_ylabel("Number of Customers")
ax1.set_title("Customer Count by Time")
ax1.grid(True)

st.pyplot(fig1)

st.subheader("Customers by Month")

month_summary["month_label"] = month_summary["month_num"].apply(lambda x: calendar.month_name[int(x)])
month_summary["year_month"] = month_summary["month_label"] + " " + month_summary["year"].astype(str)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(month_summary["year_month"], month_summary["customer_count"], marker="o")
ax2.set_xlabel("Month")
ax2.set_ylabel("Number of Customers")
ax2.set_title("Customer Count by Month")
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True)

st.pyplot(fig2)

st.subheader("Predicted Customers by Time")
st.write("This is the Linear Regression output graph.")

selected_year = int(df["year"].mode()[0])
selected_month_num = int(df["month_num"].mode()[0])
selected_month_name = calendar.month_name[selected_month_num]

hour_range = pd.DataFrame({
    "year": [selected_year] * 24,
    "month_num": [selected_month_num] * 24,
    "hour_num": list(range(24))
})

hour_range["predicted_customer_count"] = model.predict(hour_range[["year", "month_num", "hour_num"]])
hour_range["predicted_customer_count"] = hour_range["predicted_customer_count"].clip(lower=0).round()

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(hour_range["hour_num"], hour_range["predicted_customer_count"], marker="o")
ax3.set_xticks(range(0, 24, 2))
ax3.set_xticklabels(
    [pd.to_datetime(str(x), format="%H").strftime("%I %p").lstrip("0") for x in range(0, 24, 2)],
    rotation=45
)
ax3.set_xlabel("Time")
ax3.set_ylabel("Expected Number of Customers")
ax3.set_title(f"Predicted Customers by Time for {selected_month_name} {selected_year}")
ax3.grid(True)

st.pyplot(fig3)
st.markdown("---")

if st.button("🔙 Back to Home"):
    st.markdown(
        '<a href="/" target="_self">Go to Home</a>',
        unsafe_allow_html=True
    )
