import streamlit as st
import json
import os
import datetime
import csv
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Startup Tracker", layout="wide")

# ---------- Utility Functions ----------
def load_json(filename, default=[]):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return default

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def export_to_csv(data, fields, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

def summarize_url(url):
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        if not paragraphs:
            return "No content found to summarize."
        text = ' '.join(p.get_text() for p in paragraphs[:5])
        summary = text[:300] + "..." if len(text) > 300 else text
        return summary or "Summary is empty."
    except Exception as e:
        return f"Error fetching content: {str(e)}"

# ---------- Sidebar Navigation ----------
st.sidebar.title("🚀 AI Startup Tracker")
page = st.sidebar.radio("Go to", ["Phase Tracker", "Ideas", "Testing Notes", "Roadmap", "Useful Links", "Upload Files", "Export Data"])

# ---------- Phase Tracker ----------
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

# ---------- Ideas Section ----------
elif page == "Ideas":
    st.title("💡 Idea Box")

    idea_file = "ideas.json"
    if "ideas" not in st.session_state:
        st.session_state.ideas = load_json(idea_file)

    st.subheader("Add New Idea")
    new_idea = st.text_area("Describe your idea here:")
    if st.button("Save Idea"):
        if new_idea.strip():
            st.session_state.ideas.append({
                "text": new_idea.strip(),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_json(idea_file, st.session_state.ideas)
            st.success("✅ Idea saved successfully!")
            st.experimental_rerun()

    st.subheader("Your Saved Ideas")
    for i, idea in enumerate(st.session_state.ideas):
        with st.expander(f"Idea {i+1} - {idea['timestamp']}"):
            edited_text = st.text_area(f"Edit Idea {i+1}", value=idea["text"], key=f"edit_idea_{i}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"💾 Update {i+1}"):
                    st.session_state.ideas[i]["text"] = edited_text
                    save_json(idea_file, st.session_state.ideas)
                    st.success("Updated!")
            with col2:
                if st.button(f"❌ Delete {i+1}"):
                    st.session_state.ideas.pop(i)
                    save_json(idea_file, st.session_state.ideas)
                    st.experimental_rerun()

# ---------- Testing Notes ----------
elif page == "Testing Notes":
    st.title("🧪 Testing Feedback Log")

    if "test_notes" not in st.session_state:
        st.session_state.test_notes = []

    feedback = st.text_area("Add testing feedback or user comments:")
    if st.button("Log Feedback"):
        if feedback.strip():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.test_notes.append({"note": feedback.strip(), "timestamp": timestamp})
            st.success("Feedback logged!")

    st.subheader("Past Notes:")
    for note in reversed(st.session_state.test_notes):
        st.markdown(f"- [{note['timestamp']}] {note['note']}")

# ---------- Roadmap ----------
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

# ---------- Useful Links ----------
elif page == "Useful Links":
    st.title("🔗 Useful Links and Resources")

    link_file = "links.json"
    if "links" not in st.session_state:
        st.session_state.links = load_json(link_file)

    st.subheader("Add a New Link")
    new_link = st.text_input("Enter the URL:")
    new_note = st.text_area("What is this link about?")
    if st.button("Add Link"):
        if new_link.strip():
            summary = summarize_url(new_link.strip())
            st.session_state.links.append({
                "url": new_link.strip(),
                "note": new_note.strip() or summary,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_json(link_file, st.session_state.links)
            st.success("🔗 Link added!")
            st.experimental_rerun()

    st.subheader("Saved Links:")
    for i, item in enumerate(st.session_state.links):
        with st.expander(f"{item['url']} ({item['timestamp']})"):
            edited_url = st.text_input(f"Edit URL {i+1}", value=item["url"], key=f"url_{i}")
            edited_note = st.text_area(f"Edit Note {i+1}", value=item["note"], key=f"note_{i}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"💾 Update Link {i+1}"):
                    st.session_state.links[i]["url"] = edited_url
                    st.session_state.links[i]["note"] = edited_note
                    save_json(link_file, st.session_state.links)
                    st.success("Link updated!")
            with col2:
                if st.button(f"❌ Delete Link {i+1}"):
                    st.session_state.links.pop(i)
                    save_json(link_file, st.session_state.links)
                    st.experimental_rerun()

# ---------- File Upload ----------
elif page == "Upload Files":
    st.title("📄 Upload Your Files")

    upload_file_path = "uploaded_files.json"
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = load_json(upload_file_path)

    uploaded_file = st.file_uploader("Upload a document or PDF")
    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.uploaded_files.append({
            "filename": uploaded_file.name,
            "path": file_path,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_json(upload_file_path, st.session_state.uploaded_files)
        st.success(f"Uploaded: {uploaded_file.name}")

    st.subheader("📚 Previously Uploaded Files")
    for file in st.session_state.uploaded_files:
        st.markdown(f"**{file['filename']}** uploaded at `{file['timestamp']}`")

# ---------- Export Data ----------
elif page == "Export Data":
    st.title("📤 Export Your Data")

    if st.button("Export Ideas to CSV"):
        export_to_csv(st.session_state.ideas, ["text", "timestamp"], "ideas_export.csv")
        st.success("ideas_export.csv saved")

    if st.button("Export Links to CSV"):
        export_to_csv(st.session_state.links, ["url", "note", "timestamp"], "links_export.csv")
        st.success("links_export.csv saved")
