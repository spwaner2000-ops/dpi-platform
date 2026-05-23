import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

# Set page configuration
st.set_page_config(page_title="Center for Collaborative Learning - A Lilmod Initiative", page_icon="🌱", layout="centered")

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Header Section
st.title("🌱 Center for Collaborative Development - A Lilmod Initiative")
st.markdown("""
Welcome! We believe early childhood development is a true partnership between school and home. 
This quick check-in helps us understand how we are working together to support your child's growth.
""")
st.divider()

with st.form("partnership_form"):
    
    st.subheader("1. The Basics")
    # Updated to a 3-column layout to fit the new Parent Name field smoothly
    col1, col2, col3 = st.columns(3)
    with col1:
        parent_name = st.text_input("Your Name (Parent/Guardian)")
    with col2:
        child_name = st.text_input("Child's First Name")
    with col3:
        class_group = st.selectbox("Class / Group", ["Playgroup", "Nursery", "LKG", "UKG"])
        
    st.subheader("2. Learning & Play at Home")
    reading_days = st.slider("How many days did you read a story together this week?", 0, 7, 0)
    play_days = st.slider("How many days did you engage in unplugged play?", 0, 7, 0)
    writing_days = st.slider("Were you able to assist or assess drawing, writing skills?", 0, 7, 0)
    reasoning_days = st.slider("Did you try to quiz the child randomly to check knowledge level?", 0, 7, 0)
    
    st.subheader("3. Collaborating with School")
    updates = st.radio("Were you able to review this week's school communication?",
        ["Yes, read it thoroughly", "Skimmed the highlights", "Haven't had a chance yet"])
    events = st.radio("Did you participate in any school activities this week?",
        ["Attended an in-person event", "Supported asynchronously", "Not this week"])
    
    st.subheader("4. Your Insights")
    insight = st.text_area("Did you notice any new milestones or interests this week? (Optional)")
    
    # Submit Button
    submitted = st.form_submit_button("Share Weekly Update")
    
   if submitted:
        if not parent_name.strip() or not child_name.strip():
            st.error("Please enter both your name and your child's name so we can update their portfolio.")
        else:
            # Pull the existing data from Google Sheets
            existing_data = conn.read(ttl=0)
            
            # --- DUPLICATE CHECK LOGIC ---
            if not existing_data.empty and "Date" in existing_data.columns and "Child Name" in existing_data.columns:
                # Convert Date column to actual datetime objects
                existing_data["Date"] = pd.to_datetime(existing_data["Date"], errors='coerce')
                
                # Get current month and year
                current_month = date.today().month
                current_year = date.today().year
                
                # Check if this child already has an entry this month
                child_matches = existing_data[existing_data["Child Name"].str.strip().str.lower() == child_name.strip().lower()]
                month_matches = child_matches[(child_matches["Date"].dt.month == current_month) & (child_matches["Date"].dt.year == current_year)]
                
                if not month_matches.empty:
                    st.warning(f"Thank you! We already have a check-in for {child_name.strip().title()} this month. We look forward to your next update in {date.today().replace(month=(current_month%12)+1).strftime('%B')}!")
                    st.stop() # This halts the script so no data is saved
            # -----------------------------

            # Create the new row
            new_data = pd.DataFrame([{
                "Date": date.today().strftime("%Y-%m-%d"),
                "Parent Name": parent_name.strip(),
                "Child Name": child_name.strip(),
                "Class": class_group,
                "Reading Days": reading_days,
                "Unplugged Play Days": play_days,
                "Reviewed Updates": updates,
                "Event Participation": events,
                "Parent Insight": insight
            }])
            
            # Combine and push back to the Sheet
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success("Thank you for sharing! Your involvement at home is the foundation of their growth.")
st.balloons()
