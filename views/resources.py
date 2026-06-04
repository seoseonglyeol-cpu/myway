import streamlit as st
from utils.claude_api import recommend_resources

def show():
    st.title("교재 · 강의 추천")
    st.caption("목표에 맞는 교재와 강의를 AI가 추천해드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        return

    profile = st.session_state.user_profile
    subject = st.text_input("어떤 과목 · 자격증을 공부하려고 해요?", placeholder="예: 정보처리기사, 토익, SQL")

    if st.button("추천 받기", type="primary", use_container_width=True, disabled=not subject):
        with st.spinner("AI가 최적의 리소스를 찾고 있습니다..."):
            result = recommend_resources(profile, subject)
            st.session_state.resources_result = result

    if st.session_state.get("resources_result"):
        st.divider()
        st.markdown(st.session_state.resources_result)
