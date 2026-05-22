# --- CONFIGURATION ---
# --- CONFIGURATION ---
st.set_page_config(page_title="DPI Platform", layout="wide")
st.set_page_config(page_title="DPI Platform", layout="wide")


# --- MOCK DATABASE ---
# --- MOCK DATABASE ---
if "dpi" not in st.session_state:
if "dpi" not in st.session_state:
    st.session_state["dpi"] = pd.DataFrame({
    st.session_state["dpi"] = pd.DataFrame({
        "Date": ["2026-05-01", "2026-05-05"], 
        "Date": ["2026-05-01", "2026-05-05"], 
        "Student": ["Aarav", "Diya"], 
        "Student": ["Aarav", "Diya"], 
        "Routine": [8, 6], 
        "Routine": [8, 6], 
        "Scaffold": [7, 5], 
        "Scaffold": [7, 5], 
        "Goals": [8, 7], 
        "Goals": [8, 7], 
        "Tier": ["Collaborative", "Engaged"]
        "Tier": ["Collaborative", "Engaged"]
    })
    })


st.title("Developmental Partnership Index (DPI)")
st.title("Developmental Partnership Index (DPI)")


# --- PART 1: DATA ENTRY ---
# --- PART 1: DATA ENTRY ---
st.subheader("1. Log New Home Observation")
st.subheader("1. Log New Home Observation")


name = st.text_input("Child Name")
name = st.text_input("Child Name")
r = st.slider("Routine Sync", 1, 10, 5)
r = st.slider("Routine Sync", 1, 10, 5)
s = st.slider("Home Scaffolding", 1, 10, 5)
s = st.slider("Home Scaffolding", 1, 10, 5)
g = st.slider("Goal Alignment", 1, 10, 5)
g = st.slider("Goal Alignment", 1, 10, 5)


if st.button("Submit Data"):
if st.button("Submit Data"):
    if name != "":
    if name != "":
        total = r + s + g
        total = r + s + g
        tier = "Transactional"
        tier = "Transactional"
        if total >= 12: tier = "Engaged"
        if total >= 12: tier = "Engaged"
        if total >= 20: tier = "Collaborative"
        if total >= 20: tier = "Collaborative"
        if total >= 25: tier = "Synergistic"
        if total >= 25: tier = "Synergistic"
        
        
        new_row = pd.DataFrame({
        new_row = pd.DataFrame({
            "Date": [datetime.date.today().strftime("%Y-%m-%d")], 
            "Date": [datetime.date.today().strftime("%Y-%m-%d")], 
            "Student": [name.title()], 
            "Student": [name.title()], 
            "Routine": [r], 
            "Routine": [r], 
            "Scaffold": [s], 
            "Scaffold": [s], 
            "Goals": [g], 
            "Goals": [g], 
            "Tier": [tier]
            "Tier": [tier]
        })
        })
        st.session_state["dpi"] = pd.concat([st.session_state["dpi"], new_row], ignore_index=True)
        st.session_state["dpi"] = pd.concat([st.session_state["dpi"], new_row], ignore_index=True)
        st.success("Observation logged for " + name)
        st.success("Observation logged for " + name)
    else:
    else:
        st.error("Please enter a child name.")
        st.error("Please enter a child name.")


st.divider()
st.divider()


# --- PART 2: ANALYTICS ---
# --- PART 2: ANALYTICS ---
st.subheader("2. Kindergarten Cohort Analytics")
st.subheader("2. Kindergarten Cohort Analytics")


df = st.session_state["dpi"]
df = st.session_state["dpi"]


col1, col2, col3 = st.columns(3)
col1, col2, col3 = st.columns(3)
col1.metric("Assessments Logged", len(df))
col1.metric("Assessments Logged", len(df))
col2.metric("Active Families", df["Student"].nunique())
col2.metric("Active Families", df["Student"].nunique())
col3.metric("Most Common Tier", df["Tier"].mode()[0] if not df.empty else "N/A")
col3.metric("Most Common Tier", df["Tier"].mode()[0] if not df.empty else "N/A")


st.bar_chart(df["Tier"].value_counts())
st.bar_chart(df["Tier"].value_counts())
st.dataframe(df, use_container_width=True)
st.dataframe(df, use_container_width=True)
