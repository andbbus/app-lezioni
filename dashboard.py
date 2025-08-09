import pandas as pd
import streamlit as st
from datetime import datetime

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    file_path = "Book2.xlsx"  # Make sure the Excel file is in the same folder
    df = pd.read_excel(file_path, sheet_name="TimeEdit (4)")
    # Ensure date is datetime type
    df["Start datum"] = pd.to_datetime(df["Start datum"], errors="coerce")
    return df

df = load_data()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

# Date selection (defaults to today)
default_date = datetime.today().date()
selected_date = st.sidebar.date_input("Select date", default_date)

# Pre-filters
groups = ["All"] + sorted(df["Actual Group"].dropna().unique())
selected_group = st.sidebar.selectbox("Actual Group", groups)

methods = ["All"] + sorted(df["Teaching method"].dropna().unique())
selected_method = st.sidebar.selectbox("Teaching Method", methods)

courses = ["All"] + sorted(df["Course name"].dropna().unique())
selected_course = st.sidebar.selectbox("Course Name", courses)

# -----------------------
# Filter Data
# -----------------------
filtered_df = df[df["Start datum"].dt.date == selected_date]

if selected_group != "All":
    filtered_df = filtered_df[filtered_df["Actual Group"] == selected_group]

if selected_method != "All":
    filtered_df = filtered_df[filtered_df["Teaching method"] == selected_method]

if selected_course != "All":
    filtered_df = filtered_df[filtered_df["Course name"] == selected_course]

# -----------------------
# Main Dashboard
# -----------------------
st.title("📅 Daily Course Schedule")
st.subheader(f"Date: {selected_date.strftime('%A, %d %B %Y')}")

if filtered_df.empty:
    st.warning("No courses found for this date and filter selection.")
else:
    st.dataframe(
        filtered_df[
            [
                "Starttijd",
                "Durata",
                "Course name",
                "Room/Location",
                "Teaching method",
                "Actual Group",
            ]
        ].sort_values(by="Starttijd")
    )

# -----------------------
# Navigation
# -----------------------
st.markdown("---")
st.caption("Use the sidebar to change the date and filters.")
