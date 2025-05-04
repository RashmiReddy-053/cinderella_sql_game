import base64
import streamlit as st
import sqlite3
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="Finding Cinderella", layout="wide")

def get_base64_of_local_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background(image_path):
    if os.path.isfile(image_path):
        encoded = get_base64_of_local_image(image_path)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Background image file not found.")

# Set Background Image
set_background("cinderella4.jpg")

# Connect to DB
conn = sqlite3.connect('cinderella_mystery.db')
cursor = conn.cursor()

# --------------------- TITLE ------------------------
st.markdown("<h1 style='text-align: center;'> Finding Cinderella: A SQL Mystery Game</h1>", unsafe_allow_html=True)
st.markdown("Help Prince Leo find the mysterious guest who left the ball at midnight... by querying your way through clues.")

# Initialize session state
if "progress" not in st.session_state:
    st.session_state.progress = {"stage_1": False, "stage_2": False,  "final": False}

# ----------------------Sidebar-------------------------
with st.sidebar:
    st.title("🧭 Game Guide")
    st.markdown("**Hints:**")
    if not st.session_state.progress["stage_1"]:
        st.write("Look for guests who left before 10:30 PM.")
    elif not st.session_state.progress["stage_2"]:
        st.write("Find a glass slipper in the lost items.")
    else:
        st.write("You're close! Identify Cinderella by name.")

    st.markdown("**Progress:**")
    for key, value in st.session_state.progress.items():
        st.write(f"{'✅' if value else '⬜'} {key.replace('_', ' ').title()}")



# ------------------ Game Intro --------------------
st.header("📖 Introduction")
st.markdown("""
On the night of the Royal Ball, a mysterious guest vanished, leaving only a glass slipper behind.
Prince Leo needs your help to search through records — guests, messages, locations, and events — 
to find the one who captured his heart.

Your only tools? SQL queries and your sharp mind.
""")

# ------------------ Objective ----------------------
st.header("🎯 Objective")
st.markdown("Find the name of the guest who left the slipper. Use clues from the tables to help Prince Leo reunite with Cinderella.")

# ------------------ Table Schema -------------------
st.header("🧾 Tables Overview")
with st.expander("📊 Click to View Table Structures"):
    st.markdown("""
    **`people`**  
    - `id`, `name`, `gender`, `age`, `occupation`  

    **`event_attendance`**  
    - `id`, `person_id`, `event_name`, `timestamp`, `dress_color`  

    **`lost_items`**  
    - `id`, `item_name`, `owner_id`, `location`, `found_time`  

    **`messages`**  
    - `id`, `sender_id`, `receiver_id`, `message`, `sent_time`  

    **`travel_logs`**  
    - `id`, `person_id`, `from_location`, `to_location`, `travel_time`
    """)

# ------------------ STAGE 1 ------------------
st.subheader("🔎 Stage 1: Who left the ball early?")
query_1 = st.text_area("Enter your SQL query to find guests who left before 10:30 PM:", key="q1")
if st.button("Run Stage 1 Query"):
    try:
        df1 = pd.read_sql_query(query_1, conn)
        st.dataframe(df1)

        # Validate
        expected = pd.read_sql_query("""
            SELECT p.name
            FROM people p
            JOIN event_attendance ea ON p.id = ea.person_id
            WHERE ea.timestamp < '22:00'
        """, conn)

        user_res = df1[["name"]].drop_duplicates().sort_values("name").reset_index(drop=True)
        expected_res = expected[["name"]].drop_duplicates().sort_values("name").reset_index(drop=True)

        if user_res.equals(expected_res):
            st.success("Correct! You found the early leaver.")
            st.session_state.progress["stage_1"] = True
        else:
            st.warning("Close, but not correct. Make sure you're selecting guests who left before 10 PM.")
    except Exception as e:
        st.error(f"SQL Error: {e}")

# ------------------ STAGE 2 ------------------
if st.session_state.progress["stage_1"]:
    st.subheader("🔍 Stage 2: Who left the glass slipper?")
    query_2 = st.text_area("Enter your SQL query to find the glass slipper:", key="q2")
    if st.button("Run Stage 2 Query"):
        try:
            df2 = pd.read_sql_query(query_2, conn)
            st.dataframe(df2)

            # Basic validation
            if "slipper" in query_2.lower() and "lost_items" in query_2.lower():
                st.success("Correct! You found the person who lost their slipper.")
                st.session_state.progress["stage_2"] = True
            else:
                st.warning("Hint: Look in the `lost_items` table for 'slipper'.")
        except Exception as e:
            st.error(f"SQL Error: {e}")

# ------------------ STAGE 3 ------------------

# ------------------ FINAL STEP ------------------
if st.session_state.progress["stage_1"] and st.session_state.progress["stage_2"]:
    st.subheader("👑 Final Step: Who is Cinderella?")
    with st.form("final_guess"):
        final_name = st.text_input("Enter Cinderella's real name:")
        submit = st.form_submit_button("Submit")
        if submit:
            if final_name.lower().strip() == "ella":  # You can change the correct name here
                st.balloons()
                st.success("🎉 You did it! Prince Leo and Cinderella are reunited.")
            else:
                st.warning("That's not quite right. Check all the clues again carefully.")

