import json
import os
import hashlib
import streamlit as st

SESSION_FILE = "session_data.json"
PROFILES_FILE = "profiles.json"
USERS_FILE = "users.json"


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── 세션 저장/불러오기 ────────────────────────────────────────

def save_session():
    data = {}
    for key in ["user_profile", "analysis_result", "roadmap_result",
                "schedule_result", "resources_result"]:
        if st.session_state.get(key):
            data[key] = st.session_state[key]
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            if key not in st.session_state or st.session_state[key] is None:
                st.session_state[key] = value


def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    for key in ["user_profile", "analysis_result", "roadmap_result",
                "schedule_result", "resources_result", "jobs",
                "logged_in", "current_user"]:
        if key in st.session_state:
            del st.session_state[key]


# ── 프로필 관리 ──────────────────────────────────────────────

def save_profile(name: str, profile: dict):
    profiles = load_all_profiles()
    profiles[name] = profile
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False)


def load_all_profiles() -> dict:
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def delete_profile(name: str):
    profiles = load_all_profiles()
    if name in profiles:
        del profiles[name]
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False)


# ── 유저 관리 ────────────────────────────────────────────────

def _load_users() -> dict:
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)


def register_user(username: str, password: str) -> tuple:
    if not username or not password:
        return False, "아이디와 비밀번호를 입력해주세요."
    users = _load_users()
    if username in users:
        return False, "이미 존재하는 아이디입니다."
    users[username] = {"password": _hash(password)}
    _save_users(users)
    return True, "회원가입이 완료됐어요!"


def login_user(username: str, password: str) -> tuple:
    if not username or not password:
        return False, "아이디와 비밀번호를 입력해주세요."
    users = _load_users()
    if username not in users:
        return False, "존재하지 않는 아이디입니다."
    if users[username]["password"] != _hash(password):
        return False, "비밀번호가 틀렸습니다."
    st.session_state.logged_in = True
    st.session_state.current_user = username
    return True, f"{username}님, 환영합니다!"
