import streamlit as st
from utils.claude_api import generate_roadmap
from utils.session import save_session

def show():
    st.title("맞춤 로드맵")
    st.caption("AI가 취준 단계별 로드맵을 짜드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        return

    profile = st.session_state.user_profile
    st.info(f"{profile['name']}님의 {profile['target_job']} 취준 로드맵")

    if st.button("로드맵 생성", type="primary", use_container_width=True):
        with st.spinner("AI가 로드맵을 만들고 있습니다..."):
            result = generate_roadmap(profile)
            st.session_state.roadmap_result = result
            save_session()

    if st.session_state.get("roadmap_result"):
        st.divider()
        st.markdown(st.session_state.roadmap_result)
