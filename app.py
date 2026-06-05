import streamlit as st
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
.stApp { background-color: #F5F5F5; }
section[data-testid="stSidebar"] {
    display: block !important;
    background-color: #1C1C1E !important;
    min-width: 280px !important;
    width: 280px !important;
    transform: none !important;
}
section[data-testid="stSidebar"] > div:first-child { width: 280px !important; }
section[data-testid="stSidebar"] * { color: #FFFFFF; }
button[kind="header"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] { display: none !important; }
label, .stTextInput label, .stSelectbox label,
.stNumberInput label, .stTextArea label,
.stSlider label, .stRadio label { color: #111827 !important; }
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] * { background-color: #FFFFFF !important; color: #111827 !important; }
[data-baseweb="popover"] * { background-color: #FFFFFF !important; color: #111827 !important; }
.stButton > button {
    background: #02C39A !important; color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-list"] { gap: 0px; border-bottom: 2px solid #E5E7EB; }
.stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #6B7280; padding: 12px 24px; }
.stTabs [aria-selected="true"] { color: #1C1C1E !important; border-bottom: 2px solid #02C39A !important; }
.stFormSubmitButton > button {
    background: #1C1C1E !important; color: white !important;
    border-radius: 10px !important; height: 48px !important;
    font-size: 16px !important; font-weight: 600 !important;
}
.stFormSubmitButton > button:hover { background: #02C39A !important; }
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] .stRadio > div > label {
    padding: 10px 16px !important; border-radius: 10px !important;
    cursor: pointer !important; font-size: 14px !important; font-weight: 500 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover { background: rgba(255,255,255,0.08) !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; border: 1px solid #333 !important;
    color: #999 !important; font-size: 13px !important; height: 40px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #FF6B6B !important; color: #FF6B6B !important;
}
h1, h2, h3, h4 { color: #111827 !important; }
.stCaption, .stCaption p { color: #6B7280 !important; }
input::placeholder, textarea::placeholder { color: #9CA3AF !important; }
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 16px !important; color: #111827; }
.stDeployButton { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
/* AI 결과 카드 안 스타일 */
.stMarkdown h2 {
    color: #1C1C1E !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    margin-top: 32px !important;
    margin-bottom: 16px !important;
    padding-bottom: 8px !important;
    border-bottom: 2px solid #02C39A !important;
}
.stMarkdown h3 {
    color: #1C1C1E !important;
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
}
.stMarkdown thead tr {
    background: #1C1C1E !important;
}
.stMarkdown thead th {
    color: #FFFFFF !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-align: left !important;
}
.stMarkdown tbody tr {
    border-bottom: 1px solid #E5E7EB !important;
}
.stMarkdown tbody tr:nth-child(even) {
    background: #F9FAFB !important;
}
.stMarkdown tbody td {
    padding: 12px 16px !important;
    font-size: 14px !important;
    color: #111827 !important;
}
.stMarkdown ul {
    margin: 12px 0 !important;
    padding-left: 0 !important;
    list-style: none !important;
}
.stMarkdown ul li {
    padding: 8px 0 8px 20px !important;
    position: relative !important;
    color: #111827 !important;
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
    background: #02C39A !important;
}
.stMarkdown ol li {
    padding: 8px 0 !important;
    color: #111827 !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
.stMarkdown strong {
    color: #1C1C1E !important;
    font-weight: 700 !important;
}
.stMarkdown blockquote {
    border-left: 3px solid #02C39A !important;
    padding: 12px 16px !important;
    background: #F0FDF9 !important;
    border-radius: 0 8px 8px 0 !important;
    margin: 16px 0 !important;
}
/* 메인 영역 기본 텍스트 색상 */
.block-container > div:first-child {
    color: inherit;
}
/* 하단 다크 배너 텍스트 */
.block-container div[style*="background:#1C1C1E"] p,
.block-container div[style*="background:#1C1C1E"] span {
    color: inherit !important;
}
/* info/success/warning/error 박스 */
.stAlert {
    background: #F5F5F5 !important;
    border: 1px solid #E5E7EB !important;
}
.stAlert p, .stAlert span {
    color: #111827 !important;
}
/* 사이드바 텍스트 흰색 */
section[data-testid="stSidebar"] {
    color: #FFFFFF;
}
/* 체크박스 텍스트 */
.stCheckbox label span,
.stCheckbox label p,
.stCheckbox label {
    color: #111827 !important;
}
/* metric 카드 기본 스타일 - 흰 배경 */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 16px !important;
    padding: 20px !important;
}
[data-testid="stMetric"] label {
    color: #6B7280 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
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
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <div style="font-size:28px; font-weight:900; color:#FFFFFF;">마이웨이</div>
            <div style="font-size:11px; color:#02C39A; letter-spacing:3px;">MY WAY</div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:40px 0 20px 0;">
            <div style="font-size:48px; font-weight:900; color:#1C1C1E; letter-spacing:-2px;">마이웨이</div>
            <div style="font-size:14px; color:#6B7280; margin-top:8px; letter-spacing:2px;">MY WAY</div>
            <div style="font-size:15px; color:#6B7280; margin-top:16px;">대학생 취준의 모든 것을 AI가 알아서 챙겨준다</div>
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
        <div style="font-size:10px; font-weight:600; color:#02C39A; letter-spacing:4px; margin-top:4px;">MY WAY</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #1a3a2a, #1C1C1E); border-radius:14px; padding:20px; margin:16px 0; border:1px solid rgba(2,195,154,0.2);">
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:40px; height:40px; border-radius:50%; background:#02C39A; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <span style="color:#FFFFFF; font-size:16px; font-weight:700;">{display_name[0].upper()}</span>
            </div>
            <div>
                <div style="color:#FFFFFF; font-size:15px; font-weight:700;">{display_name}</div>
                <div style="color:#6B7280; font-size:12px; margin-top:2px;">{profile_job}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="color:#6B7280; font-size:11px; font-weight:600; letter-spacing:2px; padding:8px 16px 4px 16px;">MENU</div>', unsafe_allow_html=True)
    page = st.radio("", [
        "홈", "스펙 입력", "스펙 분석", "로드맵",
        "공부 스케줄", "비용 계산기", "채용공고 탐색"
    ], label_visibility="collapsed")
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    if st.button("로그아웃", use_container_width=True):
        save_session(st.session_state.current_user)
        clear_login()
        st.session_state.logged_in = False
        st.session_state.current_user = None
        clear_session()
        st.rerun()

st.markdown(f"""
<div style="background:#1C1C1E; border-radius:12px; padding:14px 24px; margin-bottom:20px; display:flex; align-items:center; gap:24px;">
    <span style="color:#6B7280; font-size:12px; font-weight:600; letter-spacing:1px;">준비도</span>
    <span style="color:#02C39A; font-size:20px; font-weight:900;">0%</span>
    <div style="width:1px; height:20px; background:#333;"></div>
    <span style="color:#6B7280; font-size:12px; font-weight:600; letter-spacing:1px;">목표</span>
    <span style="color:#FFFFFF; font-size:14px; font-weight:600;">{profile_job}</span>
    <div style="width:1px; height:20px; background:#333;"></div>
    <span style="color:#6B7280; font-size:13px; margin-left:auto;">{display_name}님</span>
</div>
""", unsafe_allow_html=True)

if page == "홈":
    job = profile["target_job"] if profile else "미설정"
    company = profile.get("target_company", "미설정") if profile else "미설정"
    grade = profile["grade"] if profile else "미설정"
    st.markdown(f'<div style="padding:16px 0;"><p style="color:#6B7280; font-size:14px; margin:0;">안녕하세요,</p><h1 style="color:#111827; font-size:32px; font-weight:800; margin:4px 0 0 0;">{display_name}님</h1></div>', unsafe_allow_html=True)
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("준비도", "0%")
    with col2:
        st.metric("목표 직무", job)
    with col3:
        st.metric("목표 회사", company)
    with col4:
        st.metric("학년", grade)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="color:#111827; font-size:18px; font-weight:700; margin-bottom:16px;">빠른 시작</p>', unsafe_allow_html=True)
    c5, c6, c7 = st.columns(3)
    with c5:
        st.markdown('<div style="background:#F0FDF9; border-radius:16px; padding:24px; border:1px solid #A7F3D0; height:120px;"><p style="color:#02C39A; font-size:14px; font-weight:700; margin:0;">STEP 1</p><p style="color:#111827; font-size:18px; font-weight:700; margin:8px 0 4px 0;">스펙 입력</p><p style="color:#6B7280; font-size:13px; margin:0;">학교, 학점, 목표 직무 등 기본 정보를 입력하세요</p></div>', unsafe_allow_html=True)
    with c6:
        st.markdown('<div style="background:#F5F5F5; border-radius:16px; padding:24px; border:1px solid #E5E7EB; height:120px;"><p style="color:#6B7280; font-size:14px; font-weight:700; margin:0;">STEP 2</p><p style="color:#111827; font-size:18px; font-weight:700; margin:8px 0 4px 0;">AI 분석</p><p style="color:#6B7280; font-size:13px; margin:0;">AI가 목표 직무 대비 준비도를 분석해드려요</p></div>', unsafe_allow_html=True)
    with c7:
        st.markdown('<div style="background:#F5F5F5; border-radius:16px; padding:24px; border:1px solid #E5E7EB; height:120px;"><p style="color:#6B7280; font-size:14px; font-weight:700; margin:0;">STEP 3</p><p style="color:#111827; font-size:18px; font-weight:700; margin:8px 0 4px 0;">로드맵 받기</p><p style="color:#6B7280; font-size:13px; margin:0;">맞춤 로드맵과 공부 스케줄을 자동으로 받으세요</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="background:#1C1C1E; border-radius:16px; padding:32px; text-align:center;"><p style="color:#02C39A; font-size:14px; font-weight:600; margin:0; letter-spacing:2px;">MY WAY</p><p style="color:#FFFFFF; font-size:20px; font-weight:700; margin:8px 0 0 0;">기존 서비스는 정보를 보여주지만, 마이웨이는 판단하고 행동한다</p></div>', unsafe_allow_html=True)
elif page == "스펙 입력":
    from views.onboarding import show
    show()
elif page == "스펙 분석":
    from views.analysis import show
    show()
elif page == "로드맵":
    from views.roadmap import show
    show()
elif page == "공부 스케줄":
    from views.schedule import show
    show()
elif page == "비용 계산기":
    from views.cost import show
    show()
elif page == "채용공고 탐색":
    from views.crawling import show
    show()
