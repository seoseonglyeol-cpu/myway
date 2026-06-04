import streamlit as st
from datetime import date
from utils.claude_api import generate_schedule
from utils.session import save_session

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
        target = st.text_input("목표", placeholder="예: 정보처리기사 필기, 토익")
    with col2:
        deadline = st.date_input("마감일", min_value=date.today())

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
            save_session()

    if st.session_state.get("schedule_result"):
        st.divider()
        st.markdown(st.session_state.schedule_result)
