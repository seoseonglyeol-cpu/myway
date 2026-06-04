import re
from datetime import date
import streamlit as st
from utils.session import load_session, clear_session, login_user, register_user

st.set_page_config(
    page_title="마이웨이",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
label, .stTextInput label, .stSelectbox label,
.stNumberInput label, .stTextArea label,
.stSlider label, .stRadio label,
.stCheckbox label, .stDateInput label,
p, span {
    color: #111827 !important;
}

/* 사이드바 안에서는 흰색 유지 */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {
    color: #FFFFFF !important;
}
.stApp {
    background-color: #F5F5F5;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── 기본 폰트 ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
    color: #111827;
}

/* ── 앱 배경 ── */
.stApp {
    background-color: #F5F5F5 !important;
}

/* ── 제목/본문 텍스트 (div는 제외 — Streamlit 내부 구조 깨짐 방지) ── */
h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
}
.stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #111827 !important;
}
[data-testid="stText"] {
    color: #111827 !important;
}

/* ── Metric 컴포넌트 텍스트 ── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 16px !important;
    border: 1px solid #E5E7EB !important;
}
[data-testid="stMetric"] label {
    color: #6B7280 !important;
    font-size: 13px !important;
}
[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: #6B7280 !important;
}

/* ── 프로그레스바 민트색 ── */
.stProgress > div > div > div > div {
    background-color: #02C39A !important;
}

/* ── 콘텐츠 여백 ── */
.main .block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 0.5rem !important;
}

/* ── Sidebar 배경 ── */
section[data-testid="stSidebar"] > div:first-child {
    background: #1C1C1E !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span:not([data-testid]),
section[data-testid="stSidebar"] .stMarkdown p {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* ── 사이드바 라디오 — 동그라미 제거, 텍스트만 ── */
div[data-testid="stSidebarContent"] .stRadio > div {
    gap: 0px !important;
}
div[data-testid="stSidebarContent"] .stRadio > div > label {
    padding: 10px 16px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-size: 15px !important;
    color: #AAAAAA !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: color 0.15s !important;
}
div[data-testid="stSidebarContent"] .stRadio > div > label:hover {
    color: #FFFFFF !important;
}
/* 선택된 메뉴 민트색 */
div[data-testid="stSidebarContent"] .stRadio [data-baseweb="radio"][aria-checked="true"] ~ div label,
div[data-testid="stSidebarContent"] .stRadio [aria-checked="true"] label {
    color: #02C39A !important;
    font-weight: 700 !important;
}
/* 라디오 동그라미 숨기기 */
.stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── Card classes (view 파일용) ── */
.dark-card {
    background: #1C1C1E;
    border-radius: 16px;
    padding: 20px;
    color: white;
    margin-bottom: 12px;
}
.light-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #E5E7EB;
    margin-bottom: 12px;
}
.big-number { font-size: 36px; font-weight: 700; color: #02C39A; line-height: 1.1; }
.mint-tag {
    display: inline-block;
    background: #02C39A;
    color: white !important;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 13px;
    font-weight: 700;
}

/* ── Primary buttons (mint) ── */
div.stButton > button[kind="primary"],
div.stFormSubmitButton > button {
    background: #02C39A !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition: opacity 0.15s !important;
}
div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button:hover {
    opacity: 0.85 !important;
}

/* ── Secondary buttons ── */
div.stButton > button:not([kind="primary"]) {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    background: white !important;
    font-weight: 600 !important;
    color: #1C1C1E !important;
}
div.stButton > button:not([kind="primary"]):hover {
    border-color: #02C39A !important;
    color: #02C39A !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: transparent !important;
    border-bottom: 1px solid #E5E7EB !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    color: #888 !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #1C1C1E !important;
    color: #fff !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    background: #FFFFFF !important;
    color: #111827 !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #02C39A !important;
    box-shadow: 0 0 0 2px rgba(2,195,154,0.12) !important;
}

/* ── Alert boxes ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    color: #111827 !important;
}

hr { border-color: #E5E7EB !important; }

/* ── Press Enter to submit 텍스트 숨기기 ── */
.stTextInput > div > div > div > div {
    display: none !important;
}

/* ── 인풋 포커스 테두리 민트색 ── */
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #02C39A !important;
    box-shadow: 0 0 0 1px #02C39A !important;
    outline: none !important;
}

/* ── 에러 테두리 제거 ── */
.stTextInput > div[data-baseweb="input"] {
    border-color: #E5E7EB !important;
}

/* ── 셀렉트박스, 인풋 배경 흰색 ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #E5E7EB !important;
}

/* ── 셀렉트박스 드롭다운 ── */
.stSelectbox > div > div > div {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

/* ── 드롭다운 옵션 리스트 ── */
[data-baseweb="select"] * {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

[data-baseweb="popover"] * {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)


# ── helpers ──────────────────────────────────────────────────
def _extract_pct(text: str):
    for m in re.findall(r'(\d{1,3})\s*%', text):
        v = int(m)
        if 10 <= v <= 100:
            return v
    return None


def _count_certs(raw: str) -> int:
    if not raw or raw.strip().lower() in ('없음', 'none', ''):
        return 0
    items = [c.strip() for c in raw.replace('\n', ',').split(',') if c.strip()]
    return len([i for i in items if i.lower() not in ('없음', 'none', '')])


def _thin_bar(pct: float, bg: str = "#2C2C2E", fg: str = "#02C39A") -> str:
    return (
        f'<div style="background:{bg};border-radius:2px;height:4px;'
        f'margin:12px 0 4px;overflow:hidden;">'
        f'<div style="background:{fg};width:{min(pct,100):.1f}%;height:4px;border-radius:2px;"></div>'
        f'</div>'
    )


# ── 세션 초기화 + 파일에서 복원 ─────────────────────────────
for _k in ["user_profile", "analysis_result"]:
    if _k not in st.session_state:
        st.session_state[_k] = None

load_session()

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size:28px; font-weight:900;
             color:#FFFFFF;">마이웨이</div>
        <div style="font-size:11px; font-weight:600;
             color:#02C39A; letter-spacing:3px;">MY WAY</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio("", [
        "홈", "스펙 입력", "스펙 분석", "로드맵",
        "공부 스케줄", "교재·강의 추천", "비용 계산기", "채용공고 탐색"
    ], key="main_nav", label_visibility="collapsed")

    st.divider()

    if st.session_state.get("logged_in"):
        # 프로필 카드
        current_user = st.session_state.get("current_user", "")
        profile = st.session_state.get("user_profile")
        st.markdown(f"""
        <div style="background:#2D2D2D; border-radius:12px;
             padding:16px; margin-top:4px;">
            <div style="font-size:10px; color:#02C39A;
                 font-weight:700; letter-spacing:1px;">PROFILE</div>
            <div style="font-size:16px; font-weight:700;
                 color:#FFFFFF; margin-top:4px;">{current_user}</div>
            <div style="font-size:12px; color:#AAAAAA; margin-top:2px;">
                 {profile['target_job'] if profile else ''}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("로그아웃", use_container_width=True):
            clear_session()
            st.rerun()
    else:
        # 로그인 / 회원가입
        mode = st.radio("", ["로그인", "회원가입"], horizontal=True,
                        label_visibility="collapsed", key="auth_mode")
        username = st.text_input("아이디", key="auth_user", label_visibility="collapsed",
                                 placeholder="아이디")
        password = st.text_input("비밀번호", type="password", key="auth_pw",
                                 label_visibility="collapsed", placeholder="비밀번호")
        if mode == "로그인":
            if st.button("로그인", use_container_width=True, type="primary"):
                ok, msg = login_user(username, password)
                if ok:
                    st.rerun()
                else:
                    st.error(msg)
        else:
            if st.button("회원가입", use_container_width=True, type="primary"):
                ok, msg = register_user(username, password)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)


# ── 로그인 필요 페이지 잠금 ──────────────────────────────────
PROTECTED = {"스펙 입력", "스펙 분석", "로드맵", "공부 스케줄",
             "교재·강의 추천", "비용 계산기", "채용공고 탐색"}

if page in PROTECTED and not st.session_state.get("logged_in"):
    st.title(page)
    st.divider()
    st.warning("로그인이 필요한 서비스입니다.")
    st.info("왼쪽 사이드바에서 로그인 또는 회원가입해주세요.")
    st.stop()

# ── 홈 ───────────────────────────────────────────────────────
if page == "홈":
    profile  = st.session_state.user_profile
    analysis = st.session_state.analysis_result

    # ── 데이터 수집 ──
    pct = _extract_pct(analysis) if analysis else 0

    if profile:
        name           = profile['name']
        target_job     = profile['target_job']
        target_company = profile.get('target_company') or '미정'
        cert_count     = _count_certs(profile.get('certificates', ''))
        is_weekend     = date.today().weekday() >= 5
        today_h        = profile['weekend_hours'] if is_weekend else profile['weekday_hours']
        today_str      = f"{today_h}h"
    else:
        name, target_job, target_company = "-", "미설정", "-"
        cert_count, today_str = 0, "-"

    dday_val = st.session_state.get("schedule_dday")
    dday_str = f"D-{dday_val}" if dday_val is not None else "-"

    matched  = st.session_state.get("matched_jobs") or []
    top_jobs = len([j for j in matched if j.get("possibility") == "상"])
    jobs_str = str(top_jobs) if matched else "-"

    steps_done = sum([
        bool(analysis),
        bool(st.session_state.get("roadmap_result")),
        bool(st.session_state.get("schedule_result")),
        bool(st.session_state.get("resources_result")),
    ])
    remaining = max(0, 4 - steps_done)

    # 다음 추천 단계
    if not analysis:
        next_step = "스펙 분석"
    elif not st.session_state.get("roadmap_result"):
        next_step = "로드맵"
    elif not st.session_state.get("schedule_result"):
        next_step = "공부 스케줄"
    else:
        next_step = "채용공고 탐색"

    # ── 1. 헤더 ──
    col_title, col_job = st.columns([2, 1])
    with col_title:
        st.title("마이웨이")
        st.caption("대학생 AI 취준 비서")
    with col_job:
        st.markdown("####")
        st.markdown(f"**목표 직무** · {target_job}")
        st.markdown(f"**목표 회사** · {target_company}")

    st.divider()

    # ── 2. 준비도 metric + progress ──
    pct_display = pct if pct else 0
    st.metric(
        label="취준 준비도",
        value=f"{pct_display}%",
        delta=f"{name} · {target_job}" if profile else "스펙 입력 후 분석을 시작하세요",
        delta_color="off",
    )
    st.progress(pct_display / 100)

    st.divider()

    # ── 3. 서브 지표 4개 ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("자격증 현황", f"{cert_count}개", "보유")
    with c2:
        st.metric("남은 할 일", f"{remaining}단계", f"완료 {steps_done}/4")
    with c3:
        st.metric("오늘 공부 목표", today_str)
    with c4:
        st.metric("추천 공고", jobs_str, "합격가능성 상" if matched else "공고 탐색 전")

    st.divider()

    # ── 4. 빠른 이동 버튼 4개 ──
    b1, b2, b3, b4 = st.columns(4)
    btn_map = [
        (b1, "스펙 분석",   "스펙 분석"),
        (b2, "로드맵",     "로드맵"),
        (b3, "공부 스케줄", "공부 스케줄"),
        (b4, "공고 탐색",  "채용공고 탐색"),
    ]
    for col, label, nav_target in btn_map:
        with col:
            is_primary = (label == next_step or nav_target == next_step)
            if st.button(label, use_container_width=True,
                         type="primary" if is_primary else "secondary"):
                st.session_state.main_nav = nav_target
                st.rerun()


# ── 페이지 라우팅 ────────────────────────────────────────────
elif page == "스펙 입력":
    from views.onboarding import show; show()

elif page == "스펙 분석":
    from views.analysis import show; show()

elif page == "로드맵":
    from views.roadmap import show; show()

elif page == "공부 스케줄":
    from views.schedule import show; show()

elif page == "교재·강의 추천":
    from views.resources import show; show()

elif page == "비용 계산기":
    from views.cost import show; show()

elif page == "채용공고 탐색":
    from views.crawling import show; show()
