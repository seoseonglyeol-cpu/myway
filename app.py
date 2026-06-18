import streamlit as st
import streamlit.components.v1 as components
import os
from utils.session import (load_users, save_users, load_session, save_session,
                           clear_session, save_login, load_login, clear_login)

st.set_page_config(
    page_title="마이웨이",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif; }
/* ===== 다크 블루 코스믹 테마 ===== */
.stApp {
    background:
        radial-gradient(ellipse at 20% 0%, rgba(30, 64, 175, 0.18) 0%, transparent 45%),
        radial-gradient(ellipse at 90% 100%, rgba(59, 130, 246, 0.10) 0%, transparent 45%),
        linear-gradient(180deg, #030712 0%, #020617 40%, #0a1628 100%) !important;
    background-attachment: fixed !important;
}
section[data-testid="stSidebar"] {
    display: block !important;
    background: linear-gradient(180deg, #020617 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.15) !important;
    min-width: 280px !important;
    width: 280px !important;
    transform: none !important;
}
section[data-testid="stSidebar"] > div:first-child { width: 280px !important; }
section[data-testid="stSidebar"] * { color: #E5E7EB; }
button[kind="header"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }
label, .stTextInput label, .stSelectbox label,
.stNumberInput label, .stTextArea label,
.stSlider label, .stRadio label { color: #CBD5E1 !important; }
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: rgba(15, 27, 46, 0.8) !important;
    color: #E5E7EB !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] * { background-color: rgba(15, 27, 46, 0.95) !important; color: #E5E7EB !important; }
[data-baseweb="popover"] * { background-color: #0f1b2e !important; color: #E5E7EB !important; }
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important; color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    box-shadow: 0 4px 18px rgba(59,130,246,0.25) !important;
}
.stButton > button:hover { box-shadow: 0 6px 26px rgba(59,130,246,0.45) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0px; border-bottom: 1px solid rgba(59,130,246,0.2); }
.stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #64748B; padding: 12px 24px; }
.stTabs [aria-selected="true"] { color: #93c5fd !important; border-bottom: 2px solid #3b82f6 !important; }
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important; color: white !important;
    border: none !important;
    border-radius: 10px !important; height: 48px !important;
    font-size: 16px !important; font-weight: 600 !important;
    box-shadow: 0 4px 18px rgba(59,130,246,0.3) !important;
}
.stFormSubmitButton > button:hover { background: linear-gradient(135deg, #1d4ed8, #60a5fa) !important; }
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio > div > label {
    padding: 10px 16px !important; border-radius: 10px !important;
    cursor: pointer !important; font-size: 14px !important; font-weight: 500 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover { background: rgba(59,130,246,0.12) !important; }
/* 현재 페이지(선택된 메뉴) 강조 */
section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
    background: linear-gradient(135deg, rgba(37,99,235,0.30), rgba(59,130,246,0.14)) !important;
    box-shadow: inset 3px 0 0 #3b82f6 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) p,
section[data-testid="stSidebar"] .stRadio > div > label:has(input:checked) div {
    color: #93c5fd !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; border: 1px solid rgba(148,163,184,0.25) !important;
    color: #94A3B8 !important; font-size: 13px !important; height: 40px !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #FF6B6B !important; color: #FF6B6B !important;
}
h1, h2, h3, h4 { color: #F1F5F9 !important; }
.stCaption, .stCaption p { color: #94A3B8 !important; }
input::placeholder, textarea::placeholder { color: #64748B !important; }
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 16px !important; color: #E5E7EB; }
.stDeployButton { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
/* AI 결과 카드 안 스타일 */
.stMarkdown h2 {
    color: #F1F5F9 !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    margin-top: 32px !important;
    margin-bottom: 16px !important;
    padding-bottom: 8px !important;
    border-bottom: 2px solid #3b82f6 !important;
}
.stMarkdown h3 {
    color: #E2E8F0 !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    margin-top: 24px !important;
    margin-bottom: 12px !important;
}
.stMarkdown table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 16px 0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
}
.stMarkdown thead tr {
    background: linear-gradient(135deg, #1e3a5f, #1e40af) !important;
}
.stMarkdown thead th {
    color: #FFFFFF !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-align: left !important;
}
.stMarkdown tbody tr {
    border-bottom: 1px solid rgba(59,130,246,0.12) !important;
}
.stMarkdown tbody tr:nth-child(even) {
    background: rgba(30, 58, 95, 0.18) !important;
}
.stMarkdown tbody td {
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #CBD5E1 !important;
}
.stMarkdown ul {
    margin: 12px 0 !important;
    padding-left: 0 !important;
    list-style: none !important;
}
.stMarkdown ul li {
    padding: 8px 0 8px 20px !important;
    position: relative !important;
    color: #CBD5E1 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
.stMarkdown ul li::before {
    content: "" !important;
    position: absolute !important;
    left: 0 !important;
    top: 16px !important;
    width: 6px !important;
    height: 6px !important;
    border-radius: 50% !important;
    background: #3b82f6 !important;
}
.stMarkdown ol li {
    padding: 8px 0 !important;
    color: #CBD5E1 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
.stMarkdown strong {
    color: #93c5fd !important;
    font-weight: 700 !important;
}
.stMarkdown blockquote {
    border-left: 3px solid #3b82f6 !important;
    padding: 12px 16px !important;
    background: rgba(59,130,246,0.08) !important;
    border-radius: 0 8px 8px 0 !important;
    margin: 16px 0 !important;
}
.block-container > div:first-child {
    color: inherit;
}
/* info/success/warning/error 박스 */
.stAlert {
    background: rgba(15, 27, 46, 0.7) !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
}
.stAlert p, .stAlert span {
    color: #E5E7EB !important;
}
/* 체크박스 텍스트 */
.stCheckbox label span,
.stCheckbox label p,
.stCheckbox label {
    color: #CBD5E1 !important;
}
/* metric 카드 - 다크 글래스 */
[data-testid="stMetric"] {
    background: rgba(15, 27, 46, 0.6) !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}
[data-testid="stMetric"] label {
    color: #94A3B8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}
hr { border-color: rgba(59,130,246,0.15) !important; }

/* ===== 모바일 반응형 (<=768px) ===== */
@media (max-width: 768px) {
    /* 사이드바: 강제 고정 해제 → 햄버거로 접고 펴기 복원 */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] { display: block !important; }
    section[data-testid="stSidebar"] { min-width: 75vw !important; width: 75vw !important; }
    section[data-testid="stSidebar"] > div:first-child { width: 75vw !important; }
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: translateX(-100%) !important;
        min-width: 0 !important; width: 0 !important;
    }
    /* 컬럼을 세로로 쌓기 (폼·메트릭·카드) */
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 8px !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 100% !important; min-width: 100% !important; width: 100% !important;
    }
    .block-container { padding: 12px 14px !important; }
    h1 { font-size: 24px !important; }
    /* 준비도 배너 줄바꿈 */
    .rd-banner { flex-wrap: wrap !important; gap: 10px 16px !important; padding: 12px 16px !important; }
    .rd-banner .rd-div { display: none !important; }
    /* 메트릭 카드 패딩 축소 */
    [data-testid="stMetric"] { padding: 14px !important; }
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    saved_user = load_login()
    if saved_user:
        st.session_state.logged_in = True
        st.session_state.current_user = saved_user
        load_session(saved_user)
    else:
        st.session_state.logged_in = False
        st.session_state.current_user = None

if not st.session_state.logged_in:
    # 로그인 화면: 사이드바 숨기고 풀스크린 클린 레이아웃
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    .block-container {
        max-width: 100% !important;
        padding-left: 0 !important; padding-right: 0 !important;
        padding-top: 0 !important;
    }
    .block-container iframe { width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

    # 코스믹 히어로 (애니메이션 — components.html 안에서 JS 실행)
    _hero_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "hero.html")
    with open(_hero_path, "r", encoding="utf-8") as _f:
        components.html(_f.read(), height=720, scrolling=False)

    # 마이웨이 소개 (로그인 전 인트로 — 이름 없는 일반 문구)
    _about_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "about.html")
    with open(_about_path, "r", encoding="utf-8") as _f:
        _intro_html = _f.read().replace(
            '{{NAME}}님이 <span class="accent">잘 해내고 있어요</span>',
            '나의 길을 <span class="accent">AI와 함께</span>')
    components.html(_intro_html, height=620, scrolling=False)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:24px 0 8px 0;">
            <div style="font-size:14px; color:#93c5fd; letter-spacing:3px; font-weight:600;">시작하기</div>
            <div style="font-size:15px; color:#94A3B8; margin-top:10px;">대학생 취준의 모든 것을 AI가 알아서 챙겨준다</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        tab1, tab2 = st.tabs(["로그인", "회원가입"])
        with tab1:
            with st.form("login_form"):
                st.markdown("<br>", unsafe_allow_html=True)
                username = st.text_input("아이디", placeholder="아이디를 입력하세요")
                password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("로그인", use_container_width=True, type="primary"):
                    users = load_users()
                    if username in users and users[username] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        save_login(username)
                        load_session(username)
                        st.rerun()
                    else:
                        st.error("아이디 또는 비밀번호가 틀렸어요")
        with tab2:
            with st.form("register_form"):
                st.markdown("<br>", unsafe_allow_html=True)
                new_u = st.text_input("아이디", placeholder="사용할 아이디를 입력하세요")
                new_p = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
                new_p2 = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호를 다시 입력하세요")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("회원가입", use_container_width=True, type="primary"):
                    if not new_u or not new_p:
                        st.error("아이디와 비밀번호를 입력해주세요")
                    elif new_p != new_p2:
                        st.error("비밀번호가 일치하지 않아요")
                    else:
                        users = load_users()
                        if new_u in users:
                            st.error("이미 존재하는 아이디예요")
                        else:
                            users[new_u] = new_p
                            save_users(users)
                            st.success("가입 완료! 로그인하세요")
    st.stop()

display_name = st.session_state.current_user.split("@")[0] if "@" in st.session_state.current_user else st.session_state.current_user
profile = st.session_state.get("user_profile")
profile_job = profile["target_job"] if profile else "미설정"

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:24px 0 8px 0;">
        <div style="font-size:24px; font-weight:900; color:#FFFFFF; letter-spacing:-1px;">마이웨이</div>
        <div style="font-size:10px; font-weight:600; color:#93c5fd; letter-spacing:4px; margin-top:4px;">MY WAY</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #1e3a5f, #0a1628); border-radius:14px; padding:20px; margin:16px 0; border:1px solid rgba(59,130,246,0.25);">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg,#2563eb,#3b82f6); display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 0 18px rgba(59,130,246,0.4);">
                <span style="color:#FFFFFF; font-size:16px; font-weight:700;">{display_name[0].upper()}</span>
            </div>
            <div>
                <div style="color:#FFFFFF; font-size:15px; font-weight:700;">{display_name}</div>
                <div style="color:#94A3B8; font-size:12px; margin-top:2px;">{profile_job}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="color:#64748B; font-size:11px; font-weight:600; letter-spacing:2px; padding:8px 16px 4px 16px;">MENU</div>', unsafe_allow_html=True)
    from utils.nav import apply_pending_nav
    apply_pending_nav()
    page = st.radio("메뉴", [
        "홈", "내 할 일", "스펙 입력", "스펙 분석", "선배 매칭", "학기 플래너", "로드맵",
        "공부 스케줄", "교재·강의 추천", "비용 계산기", "채용공고 탐색"
    ], label_visibility="collapsed", key="nav_page")
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    if st.button("로그아웃", use_container_width=True):
        save_session(st.session_state.current_user)
        clear_login()
        st.session_state.logged_in = False
        st.session_state.current_user = None
        clear_session()
        st.rerun()

from utils.metrics import compute_readiness
_readiness = compute_readiness(st.session_state)
_readiness_txt = f"{_readiness}%" if _readiness is not None else "분석 전"
st.markdown(f"""
<div class="rd-banner" style="background:linear-gradient(135deg, rgba(30,58,95,0.6), rgba(10,22,40,0.6)); border:1px solid rgba(59,130,246,0.2); border-radius:12px; padding:14px 24px; margin-bottom:20px; display:flex; align-items:center; flex-wrap:wrap; gap:24px;">
    <span style="color:#94A3B8; font-size:12px; font-weight:600; letter-spacing:1px;">준비도</span>
    <span style="color:#60a5fa; font-size:20px; font-weight:900;">{_readiness_txt}</span>
    <div class="rd-div" style="width:1px; height:20px; background:rgba(59,130,246,0.25);"></div>
    <span style="color:#94A3B8; font-size:12px; font-weight:600; letter-spacing:1px;">목표</span>
    <span style="color:#F1F5F9; font-size:14px; font-weight:600;">{profile_job}</span>
    <div class="rd-div" style="width:1px; height:20px; background:rgba(59,130,246,0.25);"></div>
    <span style="color:#94A3B8; font-size:13px; margin-left:auto;">{display_name}님</span>
</div>
""", unsafe_allow_html=True)

if page == "홈":
    job = profile["target_job"] if profile else "미설정"
    company = profile.get("target_company", "미설정") if profile else "미설정"
    grade = profile["grade"] if profile else "미설정"

    # 홈 인사
    st.markdown(f'<div style="padding:8px 0 4px 0;"><p style="color:#94A3B8; font-size:14px; margin:0;">안녕하세요,</p><h1 style="color:#F1F5F9; font-size:30px; font-weight:800; margin:4px 0 0 0;">{display_name}님 👋</h1></div>', unsafe_allow_html=True)
    st.divider()

    # 대학생활 진행률 요약
    from views.progress import home_block
    home_block()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("준비도", _readiness_txt)
    with col2:
        st.metric("목표 직무", job)
    with col3:
        st.metric("목표 회사", company)
    with col4:
        st.metric("학년", grade)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="color:#F1F5F9; font-size:18px; font-weight:700; margin-bottom:16px;">빠른 시작</p>', unsafe_allow_html=True)
    from utils.nav import go_to
    c5, c6, c7 = st.columns(3)
    with c5:
        st.markdown('<div style="background:rgba(59,130,246,0.12); border-radius:16px; padding:24px; border:1px solid rgba(59,130,246,0.35); height:120px;"><p style="color:#60a5fa; font-size:14px; font-weight:700; margin:0;">STEP 1</p><p style="color:#F1F5F9; font-size:18px; font-weight:700; margin:8px 0 4px 0;">스펙 입력</p><p style="color:#94A3B8; font-size:13px; margin:0;">학교, 학점, 목표 직무 등 기본 정보를 입력하세요</p></div>', unsafe_allow_html=True)
        if st.button("스펙 입력하러 가기", use_container_width=True, key="home_go_onb"):
            go_to("스펙 입력")
    with c6:
        st.markdown('<div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:24px; border:1px solid rgba(59,130,246,0.15); height:120px;"><p style="color:#94A3B8; font-size:14px; font-weight:700; margin:0;">STEP 2</p><p style="color:#F1F5F9; font-size:18px; font-weight:700; margin:8px 0 4px 0;">AI 분석</p><p style="color:#94A3B8; font-size:13px; margin:0;">AI가 목표 직무 대비 준비도를 분석해드려요</p></div>', unsafe_allow_html=True)
        if st.button("스펙 분석 받기", use_container_width=True, key="home_go_analysis"):
            go_to("스펙 분석")
    with c7:
        st.markdown('<div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:24px; border:1px solid rgba(59,130,246,0.15); height:120px;"><p style="color:#94A3B8; font-size:14px; font-weight:700; margin:0;">STEP 3</p><p style="color:#F1F5F9; font-size:18px; font-weight:700; margin:8px 0 4px 0;">로드맵 받기</p><p style="color:#94A3B8; font-size:13px; margin:0;">맞춤 로드맵과 공부 스케줄을 자동으로 받으세요</p></div>', unsafe_allow_html=True)
        if st.button("로드맵 만들러 가기", use_container_width=True, key="home_go_roadmap"):
            go_to("로드맵")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="background:linear-gradient(135deg, #0a1628, #1e3a5f); border:1px solid rgba(59,130,246,0.25); border-radius:16px; padding:32px; text-align:center;"><p style="color:#60a5fa; font-size:14px; font-weight:600; margin:0; letter-spacing:2px;">MY WAY</p><p style="color:#FFFFFF; font-size:20px; font-weight:700; margin:8px 0 0 0;">기존 서비스는 정보를 보여주지만, 마이웨이는 판단하고 행동한다</p></div>', unsafe_allow_html=True)
elif page == "내 할 일":
    from views.todo import show
    show()
elif page == "스펙 입력":
    from views.onboarding import show
    show()
elif page == "스펙 분석":
    from views.analysis import show
    show()
elif page == "선배 매칭":
    from views.mentor import show
    show()
elif page == "학기 플래너":
    from views.planner import show
    show()
elif page == "로드맵":
    from views.roadmap import show
    show()
elif page == "공부 스케줄":
    from views.schedule import show
    show()
elif page == "교재·강의 추천":
    from views.resources import show
    show()
elif page == "비용 계산기":
    from views.cost import show
    show()
elif page == "채용공고 탐색":
    from views.crawling import show
    show()
