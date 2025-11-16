import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="EduTrack", page_icon="🎓", layout="centered")

DATA_FILE = "data/marks.csv"

os.makedirs("data", exist_ok=True)

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Subject", "Mark", "Semester"])
    df.to_csv(DATA_FILE, index=False)

# Sidebar
st.sidebar.title("📘 EduTrack Menu")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Add Marks", "View Marks", "Performance Trend", "Semester Comparison"]
)

# -----------------------------
# HOME
# -----------------------------
if page == "Home":
    st.title("🎓 Welcome to EduTrack")
    st.markdown("""
    <div style='text-align:center; margin-top:30px;'>
        <img src='https://cdn-icons-png.flaticon.com/512/3135/3135755.png' width='180'>
        <h3>Your Study Progress Starts Here</h3>
        <p>Use the menu on the left to add marks, track progress, and compare semesters.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# ADD MARKS (FIXED: ONE LINE INPUT)
# -----------------------------
elif page == "Add Marks":
    st.title("📝 Add Your Marks")

    col1, col2 = st.columns([2, 1])

    with col1:
        subject = st.text_input("Subject")

    with col2:
        mark = st.number_input("Mark", min_value=0, max_value=100)

    semester = st.selectbox("Semester", ["Semester 1", "Semester 2", "Semester 3", "Semester 4"])

    if st.button("Save Mark"):
        new_row = pd.DataFrame({"Subject": [subject], "Mark": [mark], "Semester": [semester]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Mark saved successfully!")

# -----------------------------
# VIEW MARKS
# -----------------------------
elif page == "View Marks":
    st.title("📄 Your Marks")
    if df.empty:
        st.info("No marks added yet.")
    else:
        st.dataframe(df)

# -----------------------------
# PERFORMANCE TREND
# -----------------------------
elif page == "Performance Trend":
    st.title("📊 Performance Trend")

    if df.empty:
        st.info("No marks added yet.")
    else:
        chart = alt.Chart(df).mark_line(point=True).encode(
            x="Subject",
            y="Mark",
            color="Semester"
        ).properties(width=600, height=350)

        st.altair_chart(chart, use_container_width=True)

# -----------------------------
# SEMESTER COMPARISON
# -----------------------------
elif page == "Semester Comparison":
    st.title("📈 Semester Comparison")

    if df.empty:
        st.info("No data to compare.")
    else:
        comparison_chart = alt.Chart(df).mark_bar().encode(
            x="Subject",
            y="Mark",
            color="Semester"
        ).properties(width=600, height=350)

        st.altair_chart(comparison_chart, use_container_width=True)
