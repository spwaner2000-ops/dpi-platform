import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Admin & Finance", page_icon="💼", layout="wide")

# --- PASSWORD AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Admin Login")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == st.secrets["staff_password"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# --- FINANCIAL DASHBOARD ---
st.title("💼 School Administration & Finance")
st.markdown("Track admissions, fee collections, and operational expenses.")
st.divider()

conn = st.connection("gsheets", type=GSheetsConnection)

# --- ENTRY FORM ---
with st.expander("➕ Add New Record", expanded=True):
    with st.form("finance_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            record_type = st.radio("Record Type", ["Income (Fees)", "Expense (Opex/Capex)"])
            student_name = st.text_input("Student/Vendor Name")
        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.0, step=500.0)
            class_group = st.selectbox("Class (if applicable)", ["N/A", "Playgroup", "Nursery", "LKG", "UKG"])
        with col3:
            category = st.selectbox("Category", ["Tuition Fee", "Admission Fee", "Opex (Rent/Utilities)", "Opex (Salaries)", "Capex (Equipment/Furniture)", "Other"])
            notes = st.text_input("Notes")
            
        submit_finance = st.form_submit_button("Save Record")
        
        if submit_finance:
            # TARGET THE FINANCES TAB SPECIFICALLY
            existing_finances = conn.read(worksheet="Finances", ttl=0)
            
            # Make expenses negative for easy math
            final_amount = -amount if "Expense" in record_type else amount
            
            new_record = pd.DataFrame([{
                "Date": date.today().strftime("%Y-%m-%d"),
                "Student Name": student_name.strip(),
                "Class": class_group,
                "Admission Status": "Enrolled" if "Fee" in category else "N/A",
                "Fee Amount": final_amount,
                "Capex/Opex Category": category,
                "Notes": notes
            }])
            
            updated_finances = pd.concat([existing_finances, new_record], ignore_index=True)
            conn.update(worksheet="Finances", data=updated_finances)
            st.success("Record saved successfully.")

# --- DATA VIEW ---
st.subheader("Recent Ledger")
try:
    df_finances = conn.read(worksheet="Finances", ttl=0)
    df_finances = df_finances.dropna(how="all")
    
    if not df_finances.empty:
        # Create metric cards for quick tracking
        total_income = df_finances[df_finances["Fee Amount"] > 0]["Fee Amount"].sum()
        total_expense = df_finances[df_finances["Fee Amount"] < 0]["Fee Amount"].sum()
        
        colA, colB, colC = st.columns(3)
        colA.metric("Total Income collected", f"₹{total_income:,.2f}")
        colB.metric("Total Expenses (Capex/Opex)", f"₹{abs(total_expense):,.2f}")
        colC.metric("Net Balance", f"₹{(total_income + total_expense):,.2f}")
        
        st.dataframe(df_finances.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("No financial records found.")
except Exception as e:
st.warning("Could not load the Finances tab. Did you create it in your Google Sheet?")
