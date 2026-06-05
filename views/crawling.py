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

        for job in st.session_state.jobs:
            st.markdown(f"""
            <div style="background:#FFFFFF; border-radius:14px; padding:24px;
                 border:1px solid #E5E7EB; margin-bottom:12px;
                 display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <p style="color:#111827; font-size:17px; font-weight:700;
                       margin:0 0 6px 0;">{job['title']}</p>
                    <p style="color:#6B7280; font-size:13px; margin:0 0 8px 0;">
                       {job['company']}  |  마감: {job['deadline']}</p>
                    <div style="display:flex; gap:8px;">
                        {"".join(f'<span style="background:#F0FDF9; color:#02C39A; font-size:12px; font-weight:600; padding:4px 10px; border-radius:20px; border:1px solid #A7F3D0;">{tag}</span>' for tag in job.get('tags', []))}
                    </div>
                </div>
                <a href="{job['url']}" target="_blank" style="background:#1C1C1E;
                   color:#FFFFFF; text-decoration:none; padding:10px 20px;
                   border-radius:10px; font-size:13px; font-weight:600;
                   white-space:nowrap;">공고 보기</a>
            </div>
            """, unsafe_allow_html=True)
