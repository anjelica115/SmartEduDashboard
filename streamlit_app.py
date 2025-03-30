import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="EduInsight Canada Dashboard", layout="wide")

st.title("🎓 EduInsight – Canadian University KPI Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("combined_kpi_data.csv")

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Data")

universities = sorted(df["University"].unique())
provinces = sorted(df["Province"].unique())
years = sorted(df["Year"].unique())

selected_unis = st.sidebar.multiselect("Select Universities", universities, default=universities[:2])
selected_provinces = st.sidebar.multiselect("Select Provinces", provinces)
selected_years = st.sidebar.slider("Select Year Range", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

selected_metric = st.sidebar.radio(
    "Select Metric to Display",
    ["Employment at 6 Months", "Graduate Satisfaction", "Employer Satisfaction", "Graduation Rate"]
)

# Column mapping
metric_map = {
    "Employment at 6 Months": "EmploymentRate6Months",
    "Graduate Satisfaction": "GradSatisfaction",
    "Employer Satisfaction": "EmployerSatisfaction",
    "Graduation Rate": "GraduationRate"
}
metric_col = metric_map[selected_metric]

# --- Filter Dataset ---
filtered_df = df[
    (df["University"].isin(selected_unis)) &
    (df["Year"] >= selected_years[0]) &
    (df["Year"] <= selected_years[1])
]

if selected_provinces:
    filtered_df = filtered_df[filtered_df["Province"].isin(selected_provinces)]

# --- Chart ---
if filtered_df.empty:
    st.warning("No data matches your selection. Please adjust the filters.")
else:
    chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y(f"{metric_col}:Q", title=f"{selected_metric} (%)"),
        color="University:N",
        tooltip=["University", "Province", "Year", metric_col]
    ).properties(
        title=f"{selected_metric} Over Time",
        width=800,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

with st.expander("📊 View Raw Data"):
    st.dataframe(filtered_df.sort_values(by=["University", "Year"]))
