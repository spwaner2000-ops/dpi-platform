import streamlit as st
import streamlit as st
import pandas as pd
import pandas as pd

if "auth" not in st.session_state: st.session_state.auth = False
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = ""
if "role" not in st.session_state: st.session_state.role = ""

if not st.session_state.auth: st.title("DPI Login")
if not st.session_state.auth: st.title("DPI Login")
if not st.session_state.auth: st.write("Use teacher/admin123 OR parent/parent123")
if not st.session_state.auth: st.write("Use teacher/admin123 OR parent/parent123")
if not st.session_state.auth: u = st.text_input("Username").strip().lower()
if not st.session_state.auth: u = st.text_input("Username").strip().lower()
if not st.session_state.auth: p = st.text_input("Password", type="password")
if not st.session_state.auth: p = st.text_input("Password", type="password")
if not st.session_state.auth: s = st.button("Login")
if not st.session_state.auth: s = st.button("Login")

if not st.session_state.auth and s and u == "teacher": st.session_state.auth = True; st.session_state.role = "Educator"; st.rerun()
if not st.session_state.auth and s and u == "teacher": st.session_state.auth = True; st.session_state.role = "Educator"; st.rerun()
if not st.session_state.auth and s and u == "parent": st.session_state.auth = True; st.session_state.role = "Parent"; st.rerun()
if not st.session_state.auth and s and u == "parent": st.session_state.auth = True; st.session_state.role = "Parent"; st.rerun()
if not st.session_state.auth and s: st.error("Invalid credentials")
if not st.session_state.auth and s: st.error("Invalid credentials")
if not st.session_state.auth: st.stop()
if not st.session_state.auth: st.stop()

st.sidebar.write("Role: " + st.session_state.role)
st.sidebar.write("Role: " + st.session_state.role)
if st.sidebar.button("Logout"): st.session_state.auth = False; st.rerun()
if st.sidebar.button("Logout"): st.session_state.auth = False; st.rerun()

if st.session_state.role == "Educator": st.title("Kindergarten Analytics Dashboard")
if st.session_state.role == "Educator": st.title("Kindergarten Analytics Dashboard")
if st.session_state.role == "Educator": st.write("Student observation metrics will sync here.")
if st.session_state.role == "Educator": st.write("Student observation metrics will sync here.")

if st.session_state.role == "Parent": st.title("Home Observation")
if st.session_state.role == "Parent": st.title("Home Observation")
if st.session_state.role == "Parent": st.write("Record your child's weekly scaffolding progress here.")
if st.session_state.role == "Parent": st.write("Record your child's weekly scaffolding progress here.")
