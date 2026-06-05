import json, os, streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ACTIVE_FILE = os.path.join(BASE_DIR, "active_session.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)

def save_login(username):
    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        json.dump({"username": username}, f, ensure_ascii=False)

def load_login():
    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("username")
    return None

def clear_login():
    if os.path.exists(ACTIVE_FILE):
        os.remove(ACTIVE_FILE)

def save_session(username):
    data = {}
    for key in ["user_profile", "analysis_result", "roadmap_result",
                "schedule_result", "resources_result"]:
        if st.session_state.get(key):
            data[key] = st.session_state[key]
    with open(os.path.join(BASE_DIR, f"session_{username}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def load_session(username):
    fname = os.path.join(BASE_DIR, f"session_{username}.json")
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            st.session_state[key] = value

def clear_session():
    for key in ["user_profile", "analysis_result", "roadmap_result",
                "schedule_result", "resources_result", "jobs"]:
        if key in st.session_state:
            del st.session_state[key]
