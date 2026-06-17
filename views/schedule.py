import streamlit as st
from datetime import date
from utils.claude_api import generate_schedule
from utils.certs import next_exam_date
from utils.session import save_session


def _sync_deadline():
    """목표 선택이 바뀌면 다음 시험일로 마감일 자동 설정."""
    nd = next_exam_date(st.session_state.get("sched_goal", ""))
    if nd:
        st.session_state["sched_deadline"] = nd


def show():
    st.title("공부 스케줄")
    st.caption("마감일과 가용시간을 입력하면 AI가 공부 계획을 자동으로 짜드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        return

    profile = st.session_state.user_profile

    col1, col2 = st.columns(2)
    with col1:
        profile = st.session_state.user_profile
        job = profile.get("target_job", "")
        certs = profile.get("certificates", "")

        recommendations = {
            "개발": ["정보처리기사 필기", "정보처리기사 실기", "SQLD", "토익", "코딩테스트 준비", "AWS 자격증", "직접 입력"],
            "설계": ["CAD 자격증", "기계설계산업기사", "3D프린팅 자격증", "AutoCAD", "SolidWorks", "토익", "직접 입력"],
            "생산": ["품질경영기사", "생산자동화기사", "ERP 정보관리사", "6시그마", "토익", "안전기사", "직접 입력"],
            "마케팅": ["구글 애널리틱스(GAIQ)", "ADsP", "사회조사분석사 2급", "토익스피킹", "컴활 1급", "직접 입력"],
            "회계": ["전산세무 2급", "전산회계 1급", "CPA 1차", "ERP 정보관리사", "토익", "직접 입력"],
            "데이터": ["ADsP", "빅데이터분석기사", "SQLD", "토익", "파이썬 자격증", "직접 입력"],
        }

        matched = ["토익", "직접 입력"]
        for key, vals in recommendations.items():
            if key in job:
                matched = vals
                break

        # 마감일 초기값: 첫 목표의 다음 시험일 (없으면 오늘)
        if "sched_deadline" not in st.session_state:
            st.session_state["sched_deadline"] = next_exam_date(matched[0]) or date.today()

        selected = st.selectbox("목표 (AI 추천)", matched, key="sched_goal", on_change=_sync_deadline)

        if selected == "직접 입력":
            target = st.text_input("직접 입력", placeholder="예: 정보처리기사 필기")
        else:
            target = selected

    with col2:
        deadline = st.date_input("마감일", min_value=date.today(), key="sched_deadline")
        _nd = next_exam_date(selected) if selected != "직접 입력" else None
        if _nd:
            st.caption(f"🗓️ {selected} 다음 시험일({_nd})로 자동 설정했어요. 직접 바꿔도 돼요.")
        elif selected not in ("직접 입력",):
            st.caption("이 목표는 등록된 시험일이 없어요. 마감일을 직접 정해주세요.")

    if target:
        days_left = (deadline - date.today()).days
        if days_left >= 30:
            color = "정상"
        elif days_left >= 14:
            color = "주의"
        else:
            color = "긴박"
        st.metric("남은 일수", f"D-{days_left}", delta=color)

    st.divider()
    if st.button("공부 스케줄 생성", type="primary", use_container_width=True, disabled=not target):
        with st.spinner("AI가 공부 계획을 만들고 있습니다..."):
            result = generate_schedule(profile, target, str(deadline))
            st.session_state.schedule_result = result
            st.session_state.schedule_dday = (deadline - date.today()).days
            if st.session_state.get("current_user"):
                save_session(st.session_state.current_user)

    if st.session_state.get("schedule_result"):
        st.divider()
        result = st.session_state.schedule_result
        st.markdown(f"""
        <div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:32px;
             border:1px solid rgba(59,130,246,0.2); margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:24px;">
                <div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>
                <span style="color:#60a5fa; font-size:13px; font-weight:700; letter-spacing:1px;">AI 분석 완료</span>
            </div>
            <div style="color:#CBD5E1; font-size:15px; line-height:1.8;">
                {result}
            </div>
        </div>
        """, unsafe_allow_html=True)
