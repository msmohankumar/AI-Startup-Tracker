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
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default  # Return default if JSON is invalid
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

# ---------- Sidebar ----------
st.sidebar.title("🚀 AI Startup Tracker")
page = st.sidebar.radio("Go to", [
    "Phase Tracker", "Ideas", "Testing Notes", "Roadmap",
    "Useful Links", "Upload Files", "Export Data"
])

# ---------- Pages ----------
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

elif page == "Ideas":
    st.title("💡 Idea Box")
    idea_file = "ideas.json"
    if "ideas" not in st.session_state:
        st.session_state.ideas = load_json(idea_file)

    name = st.text_input("Your Name:")
    title = st.text_input("Idea Title:")
    new_idea = st.text_area("Describe your idea here:")
    
    if st.button("Save Idea"):
        if name.strip() and title.strip():  # Allow saving even if description is empty
            new_idea_entry = {
                "name": name.strip(),
                "title": title.strip(),
                "description": new_idea.strip(),  # Can be empty
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.ideas.append(new_idea_entry)
            save_json(idea_file, st.session_state.ideas)
            st.success("✅ Idea saved successfully!")
            st.experimental_rerun()
        else:
            st.error("Please fill in your name and title before saving.")

    st.subheader("Your Saved Ideas")
    for i, idea in enumerate(st.session_state.ideas):
        # Check if the required keys exist
        if "title" in idea and "name" in idea and "timestamp" in idea:
            with st.expander(f"{idea['title']} by {idea['name']} - {idea['timestamp']}"):
                st.markdown(f"**Name:** {idea['name']}")
                st.markdown(f"**Title:** {idea['title']}")
                st.markdown(f"**Description:** {idea['description'] if idea['description'] else 'No description provided.'}")
                edited_name = st.text_input(f"Edit Name {i+1}", value=idea["name"], key=f"edit_name_{i}")
                edited_title = st.text_input(f"Edit Title {i+1}", value=idea["title"], key=f"edit_title_{i}")
                edited_description = st.text_area(f"Edit Idea Description {i+1}", value=idea["description"], key=f"edit_idea_{i}")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"💾 Update {i+1}", key=f"update_{i}"):
                        st.session_state.ideas[i]["name"] = edited_name
                        st.session_state.ideas[i]["title"] = edited_title
                        st.session_state.ideas[i]["description"] = edited_description
                        save_json(idea_file, st.session_state.ideas)
                        st.success("Updated!")
                with col2:
                    if st.button(f"❌ Delete {i+1}", key=f"delete_{i}"):
                        st.session_state.ideas.pop(i)
                        save_json(idea_file, st.session_state.ideas)
                        st.success("Idea deleted!")
                        st.experimental_rerun()
        else:
            st.warning("One of the saved ideas is missing required fields.")

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

    st.subheader("📘 Helpful Links")
    st.markdown("- [Startup India Guide](https://www.startupindia.gov.in)")
    st.markdown("- [MVP Tools & Platforms](https://nocode.tech/tools)")
    st.markdown("- [Grant Application Guide](https://www.msins.in)")

    st.subheader("🧩 Key Actions")
    st.checkbox("Have you defined your target market?")
    st.checkbox("Do you have a working prototype?")
    st.checkbox("Have you registered your startup officially?")
    st.checkbox("Have you pitched to any incubators?")
    st.checkbox("Have you reached out to any early adopters?")

    st.subheader("📊 Quick Poll")
    st.radio("How confident are you about your startup progress?", ["Very confident", "Somewhat confident", "Need support"], key="progress_poll")

elif page == "Useful Links":
    st.title("🔗 Useful Links and Resources")
    link_file = "links.json"
    if "links" not in st.session_state:
        st.session_state.links = load_json(link_file)

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
    for i, file in enumerate(st.session_state.uploaded_files):
        with st.expander(f"{file['filename']} ({file['timestamp']})"):
            if os.path.exists(file['path']):
                with open(file['path'], "rb") as f:
                    st.download_button(
                        label=f"📥 Download {file['filename']}",
                        data=f.read(),
                        file_name=file['filename'],
                        key=f"download_{i}"
                    )
            else:
                st.warning("⚠️ File not found on disk.")

            col1, col2 = st.columns([1, 1])
            with col1:
                new_filename = st.text_input(f"Rename File {i+1}", value=file['filename'], key=f"rename_{i}")
                if st.button(f"💾 Update File {i+1}", key=f"update_{i}"):
                    new_path = os.path.join("uploads", new_filename)
                    if os.path.exists(file['path']):
                        os.rename(file['path'], new_path)
                        st.session_state.uploaded_files[i]['filename'] = new_filename
                        st.session_state.uploaded_files[i]['path'] = new_path
                        save_json(upload_file_path, st.session_state.uploaded_files)
                        st.success("File renamed!")
                        st.experimental_rerun()
                    else:
                        st.error("Original file missing. Cannot rename.")
            with col2:
                if st.button(f"❌ Delete File {i+1}", key=f"delete_{i}"):
                    if os.path.exists(file['path']):
                        os.remove(file['path'])
                    st.session_state.uploaded_files.pop(i)
                    save_json(upload_file_path, st.session_state.uploaded_files)
                    st.success("File entry removed!")
                    st.experimental_rerun()

elif page == "Export Data":
    st.title("📤 Export Your Data")
    if st.button("Export Ideas to CSV"):
        export_to_csv(st.session_state.ideas, ["name", "title", "description", "timestamp"], "ideas_export.csv")
        st.success("ideas_export.csv saved")
    if st.button("Export Links to CSV"):
        export_to_csv(st.session_state.links, ["url", "note", "timestamp"], "links_export.csv")
        st.success("links_export.csv saved")
