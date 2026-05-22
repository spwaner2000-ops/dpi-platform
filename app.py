import streamlit as st
import pandas as pd
import os
from datetime import date

# Set page configuration and styling
st.set_page_config(page_title="Parent Partnership Check-In", page_icon="🌱", layout="centered")

# Initialize the CSV file if it doesn't exist
DATA_FILE = "engagement_data.csv"
if not os.path.exists(DATA_FILE):
    df_empty = pd.DataFrame(columns=[
        "Date", "Child Name", "Class", "Reading Days", 
        "Unplugged Play Days", "Reviewed Updates", 
        "Event Participation", "Parent Insight"
    ])
    df_empty.to_csv(DATA_FILE, index=False)

# Header Section
st.title("🌱 Weekly Partnership Check-In")
st.markdown("""
Welcome! We believe early childhood development is a true partnership between school and home. 
This quick check-in helps us understand how we are working together to support your child's growth this week.
""")
st.divider()

# The Form
with st.form("partnership_form"):
    
    st.subheader("1. The Basics")
    col1, col2 = st.columns(2)
    with col1:
        child_name = st.text_input("Child's First Name")
    with col2:
        class_group = st.selectbox("Class / Group", ["Playgroup", "Nursery", "LKG", "UKG"])
        
    st.subheader("2. Learning & Play at Home")
    st.markdown("*Even 15 minutes of dedicated interaction makes a profound impact.*")
    
    reading_days = st.slider(
        "How many days did you read a story together this week?", 
        min_value=0, max_value=7, value=0
    )
    
    play_days = st.slider(
        "How many days did you engage in unplugged play (e.g., building blocks, puzzles, drawing)?", 
        min_value=0, max_value=7, value=0
    )
    
    st.subheader("3. Connecting with School")
    updates = st.radio(
        "Were you able to review this week's school communication?",
        ["Yes, read it thoroughly", "Skimmed the highlights", "Haven't had a chance yet"]
    )
    
    events = st.radio(
        "Did you participate in any school activities this week?",
        ["Attended an in-person event", "Supported asynchronously (e.g., sent requested materials from home)", "Not this week"]
    )
    
    st.subheader("4. Your Insights")
    insight = st.text_area(
        "Did you notice any new milestones or interests this week? (Optional)", 
        placeholder="e.g., 'They showed a lot of interest in counting their toys...'"
    )
    
    # Submit Button
    submitted = st.form_submit_button("Share Weekly Update")
    
    if submitted:
        if not child_name.strip():
            st.error("Please enter your child's name so we can update their portfolio.")
        else:
            # Prepare data for saving
            new_data = pd.DataFrame([{
                "Date": date.today().strftime("%Y-%m-%d"),
                "Child Name": child_name.strip(),
                "Class": class_group,
                "Reading Days": reading_days,
                "Unplugged Play Days": play_days,
                "Reviewed Updates": updates,
                "Event Participation": events,
                "Parent Insight": insight
            }])
            
            # Append to CSV
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
            
            st.success("Thank you for sharing! Your involvement at home is the foundation of their growth.")
            st.balloons()
