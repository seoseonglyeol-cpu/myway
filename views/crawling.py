import streamlit as st
from utils.crawler import search_jobs

def show():
    st.title("채용공고 탐색")
    st.caption("내 스펙에 맞는 채용공고를 찾아드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        return

    profile = st.session_state.user_profile

    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("검색 키워드", value=profile["target_job"])
    with col2:
        count = st.selectbox("검색 수", [5, 10, 20], index=1)

    if st.button("공고 검색", type="primary", use_container_width=True):
        with st.spinner("채용공고를 검색하고 있습니다..."):
            jobs = search_jobs(keyword, count)
            st.session_state.jobs = jobs

    if st.session_state.get("jobs"):
        st.divider()
        st.caption(f"총 {len(st.session_state.jobs)}개 공고 검색됨")
        st.divider()

        for job in st.session_state.jobs:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{job['title']}**")
                st.caption(f"{job['company']}  |  마감: {job['deadline']}")
                if job.get("tags"):
                    st.caption(" · ".join(job["tags"]))
            with col2:
                st.link_button("공고 보기", job["url"])
            st.divider()
