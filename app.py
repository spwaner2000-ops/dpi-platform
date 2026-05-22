st.set_page_config(page_title="DPI Platform", layout="wide")
st.set_page_config(page_title="DPI Platform", layout="wide")


# Initialize mock database
# Initialize mock database
if "dpi_records" not in st.session_state:
if "dpi_records" not in st.session_state:
    st.session_state["dpi_records"] = pd.DataFrame({
    st.session_state["dpi_records"] = pd.DataFrame({
        "Date": pd.to_datetime(["2026-05-01", "2026-05-05", "2026-05-10"]),
        "Date": pd.to_datetime(["2026-05-01", "2026-05-05", "2026-05-10"]),
        "Student": ["Aarav", "Diya", "Kabir"],
        "Student": ["Aarav", "Diya", "Kabir"],
        "Routine_Sync": [8, 6, 4],
        "Routine_Sync": [8, 6, 4],
        "Home_Scaffolding": [7, 5, 3],
        "Home_Scaffolding": [7, 5, 3],
        "Goal_Alignment": [8, 7, 2],
        "Goal_Alignment": [8, 7, 2],
        "Tier": ["Collaborative", "Engaged", "Transactional"]
        "Tier": ["Collaborative", "Engaged", "Transactional"]
    })
    })


# Sidebar Navigation instead of Login
# Sidebar Navigation instead of Login
st.sidebar.title("Navigation")
st.sidebar.title("Navigation")
current_view = st.sidebar.radio("Select View:", ["Parent Input Form", "Educator Dashboard"])
current_view = st.sidebar.radio("Select View:", ["Parent Input Form", "Educator Dashboard"])


# --- PARENT VIEW ---
# --- PARENT VIEW ---
if current_view == "Parent Input Form":
if current_view == "Parent Input Form":
    st.title("Home Observation Log")
    st.title("Home Observation Log")
    st.write("Share your observations to help us align our strategies.")
    st.write("Share your observations to help us align our strategies.")
    
    
    student_name = st.text_input("Child Name", key="child_name")
    student_name = st.text_input("Child Name", key="child_name")
    routine = st.slider("Routine Sync (1-10)", 1, 10, 5, key="routine")
    routine = st.slider("Routine Sync (1-10)", 1, 10, 5, key="routine")
    scaffold = st.slider("Home Scaffolding (1-10)", 1, 10, 5, key="scaffold")
    scaffold = st.slider("Home Scaffolding (1-10)", 1, 10, 5, key="scaffold")
    goals = st.slider("Goal Alignment (1-10)", 1, 10, 5, key="goals")
    goals = st.slider("Goal Alignment (1-10)", 1, 10, 5, key="goals")
    
    
    if st.button("Submit Data", key="submit_btn"):
    if st.button("Submit Data", key="submit_btn"):
        if student_name != "":
        if student_name != "":
            total_score = routine + scaffold + goals
            total_score = routine + scaffold + goals
            tier = "Transactional"
            tier = "Transactional"
            if total_score >= 12:
            if total_score >= 12:
                tier = "Engaged"
                tier = "Engaged"
            if total_score >= 20:
            if total_score >= 20:
                tier = "Collaborative"
                tier = "Collaborative"
            if total_score >= 25:
            if total_score >= 25:
                tier = "Synergistic"
                tier = "Synergistic"
                
                
            new_row = pd.DataFrame({
            new_row = pd.DataFrame({
                "Date": [datetime.date.today()],
                "Date": [datetime.date.today()],
                "Student": [student_name.title()],
                "Student": [student_name.title()],
                "Routine_Sync": [routine],
                "Routine_Sync": [routine],
                "Home_Scaffolding": [scaffold],
                "Home_Scaffolding": [scaffold],
                "Goal_Alignment": [goals],
                "Goal_Alignment": [goals],
                "Tier": [tier]
                "Tier": [tier]
            })
            })
            st.session_state["dpi_records"] = pd.concat([st.session_state["dpi_records"], new_row], ignore_index=True)
            st.session_state["dpi_records"] = pd.concat([st.session_state["dpi_records"], new_row], ignore_index=True)
            st.success("Observation logged for " + student_name)
            st.success("Observation logged for " + student_name)
        else:
        else:
            st.error("Please enter a child name before submitting.")
            st.error("Please enter a child name before submitting.")


# --- EDUCATOR VIEW ---
# --- EDUCATOR VIEW ---
if current_view == "Educator Dashboard":
if current_view == "Educator Dashboard":
    st.title("Kindergarten Cohort Analytics")
    st.title("Kindergarten Cohort Analytics")
    st.write("Monitor the Developmental Partnership Index across the classrooms.")
    st.write("Monitor the Developmental Partnership Index across the classrooms.")
    
    
    df = st.session_state["dpi_records"]
    df = st.session_state["dpi_records"]
    
    
    col1, col2, col3 = st.columns(3)
    col1, col2, col3 = st.columns(3)
    col1.metric("Assessments Logged", len(df))
    col1.metric("Assessments Logged", len(df))
    col2.metric("Active Families", df["Student"].nunique())
    col2.metric("Active Families", df["Student"].nunique())
    col3.metric("Most Common Tier", df["Tier"].mode()[0])
    col3.metric("Most Common Tier", df["Tier"].mode()[0])
    
    
    st.divider()
    st.divider()
    st.subheader("Partnership Tier Distribution")
    st.subheader("Partnership Tier Distribution")
    st.bar_chart(df["Tier"].value_counts())
    st.bar_chart(df["Tier"].value_counts())
    
    
    st.subheader("Raw Data Extract")
    st.subheader("Raw Data Extract")
    st.dataframe(df, use_container_width=True)
    st.dataframe(df, use_container_width=True)
