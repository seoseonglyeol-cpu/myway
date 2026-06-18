import streamlit as st
from datetime import date, timedelta
from utils.claude_api import generate_schedule, koreanize
from utils.certs import next_exam_date, cert_options
from utils.session import save_session
from utils.nav import go_to


def _default_deadline(goal):
    """목표의 다음 시험일, 없으면 약 한 달 뒤로."""
    return next_exam_date(goal) or (date.today() + timedelta(days=30))


def _sync_deadline():
    """목표 선택이 바뀌면 마감일 자동 설정 (시험일 없으면 +30일)."""
    st.session_state["sched_deadline"] = _default_deadline(st.session_state.get("sched_goal", ""))


def show():
    st.title("공부 스케줄")
    st.caption("마감일과 가용시간을 입력하면 AI가 공부 계획을 자동으로 짜드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile

    col1, col2 = st.columns(2)
    with col1:
        # 전공 기반 목표(자격증) 추천 목록
        matched = cert_options(profile.get("major", ""))

        # 마감일 초기값: 첫 목표의 다음 시험일 (없으면 +30일)
        if "sched_deadline" not in st.session_state:
            st.session_state["sched_deadline"] = _default_deadline(matched[0])

        selected = st.selectbox("목표 (전공 맞춤)", matched, key="sched_goal", on_change=_sync_deadline)

        if selected == "직접 입력":
            target = st.text_input("직접 입력", placeholder="예: 정보처리기사 필기")
        else:
            target = selected

    with col2:
        deadline = st.date_input("마감일", min_value=date.today(), key="sched_deadline")
        _nd = next_exam_date(selected) if selected != "직접 입력" else None
        if _nd:
            st.caption(f"🗓️ {selected} 다음 시험일({_nd})로 자동 설정했어요. 직접 바꿔도 돼요.")
        elif selected != "직접 입력":
            st.caption("정확한 시험일이 없어 약 한 달 뒤로 자동 설정했어요. 직접 바꿔도 돼요.")

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
        result = koreanize(st.session_state.schedule_result)
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">'
            '<div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>'
            '<span style="color:#60a5fa; font-size:13px; font-weight:700; letter-spacing:1px;">AI 분석 완료</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.markdown(result)
