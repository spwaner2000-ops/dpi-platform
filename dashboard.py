import streamlit as st
import pandas as pd
import altair as alt
import os

# Set page configuration for a wider, dashboard-style layout
st.set_page_config(page_title="Partnership Dashboard", page_icon="📊", layout="wide")

st.title("📊 Staff Partnership Dashboard")
st.markdown("Monitor home-learning trends, communication reach, and actionable insights across classes.")

DATA_FILE = "engagement_data.csv"

# Function to load data, cached for performance but refreshes on new data
@st.cache_data(ttl=60)
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)

df = load_data()

if df.empty:
    st.info("No engagement data found yet. Once parents submit the Check-In form, insights will appear here.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Insights")
class_options = df["Class"].unique()
selected_classes = st.sidebar.multiselect("Select Classes to View", options=class_options, default=class_options)

# Apply filter
filtered_df = df[df["Class"].isin(selected_classes)]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- TOP KPI METRICS ---
st.subheader("Kindergarten Pulse")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Submissions", len(filtered_df))
with col2:
    avg_read = filtered_df["Reading Days"].mean()
    st.metric("Avg. Reading Days/Wk", f"{avg_read:.1f}")
with col3:
    avg_play = filtered_df["Unplugged Play Days"].mean()
    st.metric("Avg. Unplugged Play/Wk", f"{avg_play:.1f}")
with col4:
    # Calculate percentage of parents who read updates thoroughly
    thorough_reads = len(filtered_df[filtered_df["Reviewed Updates"] == "Yes, read it thoroughly"])
    read_rate = (thorough_reads / len(filtered_df)) * 100
    st.metric("High Comm. Engagement", f"{read_rate:.0f}%")

st.divider()

# --- VISUALIZATIONS ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Home Learning Averages by Class")
    # Group data by class and calculate means
    class_avg = filtered_df.groupby("Class")[["Reading Days", "Unplugged Play Days"]].mean().reset_index()
    
    # Melt dataframe for easier plotting with Altair
    melted_avg = class_avg.melt(id_vars="Class", var_name="Activity", value_name="Days")
    
    chart = alt.Chart(melted_avg).mark_bar().encode(
        x=alt.X("Class:N", title="Class Group"),
        y=alt.Y("Days:Q", title="Average Days per Week"),
        color=alt.Color("Activity:N", legend=alt.Legend(title="Activity Type")),
        xOffset="Activity:N"
    ).properties(height=350)
    
    st.altair_chart(chart, use_container_width=True)

with col_chart2:
    st.subheader("Communication Reach")
    # Count occurrences of communication engagement levels
    comm_counts = filtered_df["Reviewed Updates"].value_counts().reset_index()
    comm_counts.columns = ["Engagement Level", "Count"]
    
    pie_chart = alt.Chart(comm_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Engagement Level", type="nominal"),
        tooltip=["Engagement Level", "Count"]
    ).properties(height=350)
    
    st.altair_chart(pie_chart, use_container_width=True)

st.divider()

# --- QUALITATIVE INSIGHTS ---
st.subheader("💬 Recent Parent Insights")
st.markdown("Qualitative notes and milestones directly from home.")

# Filter out empty insights and display them beautifully
insights_df = filtered_df.dropna(subset=["Parent Insight"])
insights_df = insights_df[insights_df["Parent Insight"].str.strip() != ""]

if not insights_df.empty:
    for index, row in insights_df.iterrows():
        with st.chat_message("user", avatar="👤"):
            st.write(f"**{row['Child Name']} ({row['Class']})** — *{row['Date']}*")
            st.write(row['Parent Insight'])
else:
    st.write("No qualitative insights shared in the current filtered data.")
