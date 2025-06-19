# app.py

import streamlit as st
import json
import os
import datetime

st.set_page_config(page_title="AI Startup Tracker", layout="wide")

IDEA_FILE = "ideas.json"

# Load ideas from file
def load_ideas():
    if os.path.exists(IDEA_FILE):
        with open(IDEA_FILE, "r") as f:
            return json.load(f)
    return []

# Save ideas to file
def save_ideas(ideas):
    with open(IDEA_FILE, "w") as f:
        json.dump(ideas, f, indent=2)

# Sidebar Navigation
st.sidebar.title("🚀 AI Startup Tracker")
page = st.sidebar.radio("Go to", ["Phase Tracker", "Ideas", "Testing Notes", "Roadmap"])

# ------------------ Phase Tracker ------------------
if page == "Phase Tracker":
    st.title("📌 Startup Phase Tracker")
    phases = [
        "Ideation & Learning (0-1 month)",
        "Market Research & Validation (1-2.5 months)",
        "Build MVP (2.5–4 months)",
        "Register Startup (4–5 months)",
        "Join Incubator / Apply Grants (5–7 months)",
        "First Customers & Feedback (6–9 months)",
        "Scale & Fundraise (9–12 months)"
    ]

    for phase in phases:
        if st.checkbox(phase, key=phase):
            st.success(f"✅ Completed: {phase}")

# ------------------ Idea Box with Edit/Delete ------------------
elif page == "Ideas":
    st.title("💡 Idea Box")

    # Load saved ideas into session state
    if "ideas" not in st.session_state:
        st.session_state.ideas = load_ideas()

    st.subheader("Add New Idea")
    new_idea = st.text_area("Describe your idea here:")
    if st.button("Save Idea"):
        if new_idea.strip():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.ideas.append({
                "text": new_idea.strip(),
                "timestamp": timestamp
            })
            save_ideas(st.session_state.ideas)
            st.success("✅ Idea saved successfully!")

    st.subheader("Your Saved Ideas")
    for i, idea in enumerate(st.session_state.ideas):
        with st.expander(f"Idea {i+1} - {idea['timestamp']}"):
            edited_text = st.text_area(f"Edit Idea {i+1}", value=idea["text"], key=f"edit_{i}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"💾 Update {i+1}"):
                    st.session_state.ideas[i]["text"] = edited_text
                    save_ideas(st.session_state.ideas)
                    st.success("Updated successfully!")
            with col2:
                if st.button(f"❌ Delete {i+1}"):
                    st.session_state.ideas.pop(i)
                    save_ideas(st.session_state.ideas)
                    st.experimental_rerun()

# ------------------ Testing Notes ------------------
elif page == "Testing Notes":
    st.title("🧪 Testing Feedback Log")

    if "test_notes" not in st.session_state:
        st.session_state.test_notes = []

    feedback = st.text_area("Add testing feedback or user comments:")
    if st.button("Log Feedback"):
        if feedback.strip():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.test_notes.append(f"[{timestamp}] {feedback.strip()}")
            st.success("Feedback logged!")

    st.subheader("Past Notes:")
    for note in reversed(st.session_state.test_notes):
        st.markdown(f"- {note}")

# ------------------ Roadmap ------------------
elif page == "Roadmap":
    st.title("🛣️ Roadmap Overview")
    roadmap_items = [
        "Month 0-1: Learn and Ideate",
        "Month 1-2.5: Market Research",
        "Month 2.5–4: Build MVP",
        "Month 4–5: Register Startup",
        "Month 5–7: Apply for Grants",
        "Month 6–9: Get Customers",
        "Month 9–12: Scale & Raise Funds"
    ]
    for step in roadmap_items:
        st.info(step)
