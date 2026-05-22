import streamlit as st
import streamlit as st
import pandas as pd
import pandas as pd
import datetime
import datetime

st.set_page_config(page_title="DPI Platform", layout="wide")
st.set_page_config(page_title="DPI Platform", layout="wide")

if "dpi" not in st.session_state: st.session_state["dpi"] = pd.DataFrame({"Date": ["2026-05-01", "2026-05-05"], "Student": ["Aarav", "Diya"], "Routine": [8, 6], "Scaffold": [7, 5], "Goals": [8, 7], "Tier": ["Collaborative", "Engaged"]})
if "dpi" not in st.session_state: st.session_state["dpi"] = pd.DataFrame({"Date": ["2026-05-01", "2026-05-05"], "Student": ["Aarav", "Diya"], "Routine": [8, 6], "Scaffold": [7, 5], "Goals": [8, 7], "Tier": ["Collaborative", "Engaged"]})

st.sidebar.title("Navigation")
st.sidebar.title("Navigation")
view = st.sidebar.radio("Select View:", ["Parent Input", "Educator Dashboard"], key="view_radio")
view = st.sidebar.radio("Select View:", ["Parent Input", "Educator Dashboard"], key="view_radio")

if view == "Parent Input": st.title("Home Observation Log")
if view == "Parent Input": st.title("Home Observation Log")
if view == "Parent Input": name = st.text_input("Child Name", key="n")
if view == "Parent Input": name = st.text_input("Child Name", key="n")
if view == "Parent Input": r = st.slider("Routine Sync", 1, 10, 5, key="r")
if view == "Parent Input": r = st.slider("Routine Sync", 1, 10, 5, key="r")
if view == "Parent Input": s = st.slider("Home Scaffolding", 1, 10, 5, key="s")
if view == "Parent Input": s = st.slider("Home Scaffolding", 1, 10, 5, key="s")
if view == "Parent Input": g = st.slider("Goal Alignment", 1, 10, 5, key="g")
if view == "Parent Input": g = st.slider("Goal Alignment", 1, 10, 5, key="g")
if view == "Parent Input": btn = st.button("Submit Data", key="b")
if view == "Parent Input": btn = st.button("Submit Data", key="b")

if view == "Parent Input" and btn and name != "": total = r + s + g
if view == "Parent Input" and btn and name != "": total = r + s + g
if view == "Parent Input" and btn and name != "": tier = "Transactional" if total < 12 else "Engaged" if total < 20 else "Collaborative" if total < 25 else "Synergistic"
if view == "Parent Input" and btn and name != "": tier = "Transactional" if total < 12 else "Engaged" if total < 20 else "Collaborative" if total < 25 else "Synergistic"
if view == "Parent Input" and btn and name != "": new_row = pd.DataFrame({"Date": [datetime.date.today().strftime("%Y-%m-%d")], "Student": [name.title()], "Routine": [r], "Scaffold": [s], "Goals": [g], "Tier": [tier]})
if view == "Parent Input" and btn and name != "": new_row = pd.DataFrame({"Date": [datetime.date.today().strftime("%Y-%m-%d")], "Student": [name.title()], "Routine": [r], "Scaffold": [s], "Goals": [g], "Tier": [tier]})
if view == "Parent Input" and btn and name != "": st.session_state["dpi"] = pd.concat([st.session_state["dpi"], new_row], ignore_index=True)
if view == "Parent Input" and btn and name != "": st.session_state["dpi"] = pd.concat([st.session_state["dpi"], new_row], ignore_index=True)
if view == "Parent Input" and btn and name != "": st.success("Observation logged for " + name)
if view == "Parent Input" and btn and name != "": st.success("Observation logged for " + name)
if view == "Parent Input" and btn and name == "": st.error("Please enter a child name.")
if view == "Parent Input" and btn and name == "": st.error("Please enter a child name.")
if view == "Parent Input": st.stop()
if view == "Parent Input": st.stop()

st.title("Kindergarten Cohort Analytics")
st.title("Kindergarten Cohort Analytics")
df = st.session_state["dpi"]
df = st.session_state["dpi"]
c1, c2, c3 = st.columns(3)
c1, c2, c3 = st.columns(3)
c1.metric("Assessments Logged", len(df))
c1.metric("Assessments Logged", len(df))
c2.metric("Active Families", df["Student"].nunique())
c2.metric("Active Families", df["Student"].nunique())
c3.metric("Most Common Tier", df["Tier"].mode()[0] if not df.empty else "N/A")
c3.metric("Most Common Tier", df["Tier"].mode()[0] if not df.empty else "N/A")
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
