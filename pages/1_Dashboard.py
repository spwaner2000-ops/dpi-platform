import streamlit as st
import pandas as pd
import altair as alt
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Engagement Maturity Dashboard", page_icon="📊", layout="wide")

# --- PASSWORD AUTHENTICATION ---
# Check if the user is already authenticated in this session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# If not authenticated, show the login screen and STOP the app
if not st.session_state.authenticated:
    st.title("🔒 Staff Login")
    st.markdown("Please enter the staff password to access the internal dashboard.")
    
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        # Check against the password saved in Streamlit Secrets
        if pwd == st.secrets["staff_password"]:
            st.session_state.authenticated = True
            st.rerun()  # Refresh the page to load the dashboard
        else:
            st.error("Incorrect password. Please try again.")
            
    st.stop()  # This prevents the rest of the code from running until logged in

# --- DASHBOARD CONTENT (Only runs if authenticated) ---
st.title("📊 Engagement Maturity Dashboard")
st.markdown("This view categorizes parent involvement to help staff identify which families are highly partnered and which might need targeted outreach.")
st.divider()

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the data
try:
    df = conn.read()
    df = df.dropna(how="all") 
except Exception as e:
    st.error("Could not read data from Google Sheets. Ensure your app.py is submitting data correctly.")
    st.stop()

if df.empty:
    st.info("No data available yet. Waiting for parents to submit the check-in form.")
    st.stop()

# --- CLASSIFICATION LOGIC ---
def calculate_tier(row):
    score = 0
    try:
        score += float(row.get("Reading Days", 0))
        score += float(row.get("Unplugged Play Days", 0))
    except:
        pass
        
    updates = str(row.get("Reviewed Updates", ""))
    if "read it thoroughly" in updates:
        score += 4
    elif "Skimmed" in updates:
        score += 2
        
    events = str(row.get("Event Participation", ""))
    if "in-person" in events:
        score += 4
    elif "asynchronously" in events:
        score += 2
        
    insight = str(row.get("Parent Insight", ""))
    if insight.strip() and insight.lower() != 'nan':
        score += 2
        
    if score >= 18:
        return "4 - Partner"
    elif score >= 12:
        return "3 - Engaged"
    elif score >= 6:
        return "2 - Involved"
    else:
        return "1 - Informed"

df["Maturity Tier"] = df.apply(calculate_tier, axis=1)

# --- DASHBOARD VISUALS ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Current Distribution")
    tier_counts = df["Maturity Tier"].value_counts().reset_index()
    tier_counts.columns = ["Tier", "Count"]
    tier_counts = tier_counts.sort_values("Tier")
    
    donut = alt.Chart(tier_counts).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Tier", type="nominal", 
                       scale=alt.Scale(domain=["1 - Informed", "2 - Involved", "3 - Engaged", "4 - Partner"],
                                     range=["#ff9999", "#ffcc99", "#99ccff", "#99ff99"])),
        tooltip=["Tier", "Count"]
    ).properties(height=300)
    
    st.altair_chart(donut, use_container_width=True)

with col2:
    st.subheader("Maturity by Class")
    class_tier = df.groupby(["Class", "Maturity Tier"]).size().reset_index(name="Count")
    
    bar_chart = alt.Chart(class_tier).mark_bar().encode(
        x=alt.X("sum(Count):Q", title="Number of Families"),
        y=alt.Y("Class:N", title="Class Group"),
        color=alt.Color("Maturity Tier:N", legend=None,
                       scale=alt.Scale(domain=["1 - Informed", "2 - Involved", "3 - Engaged", "4 - Partner"],
                                     range=["#ff9999", "#ffcc99", "#99ccff", "#99ff99"])),
        tooltip=["Class", "Maturity Tier", "Count"]
    ).properties(height=300)
    
    st.altair_chart(bar_chart, use_container_width=True)

st.divider()

# --- ACTIONABLE ROSTER ---
st.subheader("Targeted Outreach Roster")
st.markdown("Use this table to see exactly where families sit. **Tip:** Focus outreach on families in the 'Informed' tier to gently encourage more involvement.")

display_cols = ["Date", "Child Name", "Parent Name", "Class", "Maturity Tier"]
existing_cols = [col for col in display_cols if col in df.columns]

selected_class = st.selectbox("Filter by Class", ["All Classes"] + list(df["Class"].dropna().unique()))

if selected_class != "All Classes":
    filtered_df = df[df["Class"] == selected_class]
else:
    filtered_df = df

st.dataframe(
    filtered_df[existing_cols].sort_values(by="Maturity Tier"), 
    use_container_width=True,
    hide_index=True
)
