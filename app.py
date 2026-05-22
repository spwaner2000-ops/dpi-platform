import streamlit as st
import streamlit as st
import pandas as pd
import pandas as pd

st.set_page_config(page_title="DPI Dashboard")
st.set_page_config(page_title="DPI Dashboard")

if "auth" not in st.session_state: st.session_state.auth = False
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = ""
if "role" not in st.session_state: st.session_state.role = ""
if "data" not in st.session_state: st.session_state.data = pd.DataFrame({"Student": ["Aarav", "Diya"], "Tier": ["Collaborative", "Engaged"]})
if "data" not in st.session_state: st.session_state.data = pd.DataFrame({"Student": ["Aarav", "Diya"], "Tier": ["Collaborative", "Engaged"]})

if not st.session_state.auth: st.title("DPI Login")
if not st.session_state.auth: st.title("DPI Login")
if not st.session_state.auth: st.write("teacher/admin123 OR parent/parent123")
if not st.session_state.auth: st.write("teacher/admin123 OR parent/parent123")
if not st.session_state.auth: form = st.form("login")
if not st.session_state.auth: form = st.form("login")
if not st.session_state.auth: u = form.text_input("User").strip().lower()
if not st.session_state.auth: u = form.text_input("User").strip().lower()
if not st.session_state.auth: p = form.text_input("Password", type="password")
if not st.session_state.auth: p = form.text_input("Password", type="password")
if not st.session_state.auth: s = form.form_submit_button("Login")
if not st.session_state.auth: s = form.form_submit_button("Login")
if not st.session_state.auth and s and u == "teacher": st.session_state.auth = True; st.session_state.role = "Educator"; st.rerun()
if not st.session_state.auth and s and u == "teacher": st.session_state.auth = True; st.session_state.role = "Educator"; st.rerun()
if not st.session_state.auth and s and u == "parent": st.session_state.auth = True; st.session_state.role = "Parent"; st.rerun()
if not st.session_state.auth and s and u == "parent": st.session_state.auth = True; st.session_state.role = "Parent"; st.rerun()
if not st.session_state.auth: st.stop()
if not st.session_state.auth: st.stop()

st.sidebar.write("Role: " + st.session_state.role)
st.sidebar.write("Role: " + st.session_state.role)
if st.sidebar.button("Logout"): st.session_state.auth = False; st.rerun()
if st.sidebar.button("Logout"): st.session_state.auth = False; st.rerun()

if st.session_state.role == "Educator": st.title("Analytics Dashboard")
if st.session_state.role == "Educator": st.title("Analytics Dashboard")
if st.session_state.role == "Educator": st.dataframe(st.session_state.data, use_container_width=True)
if st.session_state.role == "Educator": st.dataframe(st.session_state.data, use_container_width=True)
if st.session_state.role == "Educator": st.stop()
if st.session_state.role == "Educator": st.stop()

if st.session_state.role == "Parent": st.title("Log Observation")
if st.session_state.role == "Parent": st.title("Log Observation")
if st.session_state.role == "Parent": obs = st.form("obs")
if st.session_state.role == "Parent": obs = st.form("obs")
if st.session_state.role == "Parent": name = obs.text_input("Child Name")
if st.session_state.role == "Parent": name = obs.text_input("Child Name")
if st.session_state.role == "Parent": score = obs.slider("Routine Sync", 1, 10, 5)
if st.session_state.role == "Parent": score = obs.slider("Routine Sync", 1, 10, 5)
if st.session_state.role == "Parent": save = obs.form_submit_button("Save")
if st.session_state.role == "Parent": save = obs.form_submit_button("Save")
if st.session_state.role == "Parent" and save and name: st.success("Saved score " + str(score) + " for " + name)
if st.session_state.role == "Parent" and save and name: st.success("Saved score " + str(score) + " for " + name)
if st.session_state.role == "Parent": st.stop()
if st.session_state.role == "Parent": st.stop()
