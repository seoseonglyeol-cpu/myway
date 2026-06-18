import streamlit as st
from utils.crawler import search_jobs
from utils.nav import go_to


def _job_card(job):
    tags = "".join(
        f'<span style="background:rgba(59,130,246,0.12); color:#93c5fd; font-size:11px; font-weight:600; padding:3px 10px; border-radius:14px; border:1px solid rgba(59,130,246,0.3);">{t}</span>'
        for t in job.get("tags", [])
    )
    st.markdown(
        f'<div style="background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.1); border-radius:16px; padding:22px; margin-bottom:12px;">'
        f'<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; flex-wrap:wrap;">'
        f'<div style="flex:1; min-width:0;">'
        f'<div style="color:#FFFFFF; font-size:16px; font-weight:700; margin-bottom:6px;">{job["title"]}</div>'
        f'<div style="color:#60a5fa; font-size:13px; font-weight:600; margin-bottom:10px;">{job["company"]}</div>'
        f'<div style="display:flex; gap:14px; flex-wrap:wrap; margin-bottom:10px;">'
        f'<span style="color:rgba(255,255,255,0.6); font-size:12px;">📌 {job["type"]}</span>'
        f'<span style="color:rgba(255,255,255,0.6); font-size:12px;">📍 {job["location"]}</span>'
        f'</div>'
        f'<div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">{tags}</div>'
        f'<div style="color:rgba(255,255,255,0.45); font-size:12px;">{job.get("note","")}</div>'
        f'</div>'
        f'<a href="{job["url"]}" target="_blank" style="background:linear-gradient(135deg,#2563eb,#3b82f6); color:#FFFFFF; text-decoration:none; padding:10px 18px; border-radius:10px; font-size:13px; font-weight:600; white-space:nowrap;">공고 검색</a>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


def show():
    st.title("채용공고 탐색")
    st.caption("내 전공·목표에 맞는 실제 채용공고를 찾아드려요 (2026년 6월 기준 샘플 데이터)")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile
    major = profile.get("major") or ""

    st.info(f"**{major or '내 전공'}** 관련 공고를 우선으로 보여드려요. 키워드로 더 좁힐 수 있어요.")

    col1, col2 = st.columns([3, 1])
    with col1:
        keyword = st.text_input("검색 키워드 (자격증·회사·직무 등)", value="")
    with col2:
        count = st.selectbox("검색 수", [10, 20, 30], index=1)

    if st.button("공고 검색", type="primary", use_container_width=True):
        with st.spinner("채용공고를 찾고 있어요..."):
            st.session_state.jobs = search_jobs(keyword, count, major=major)

    # 처음 진입 시 자동으로 내 전공 공고 표시
    if "jobs" not in st.session_state:
        st.session_state.jobs = search_jobs("", count, major=major)

    jobs = st.session_state.get("jobs") or []
    if jobs:
        st.divider()
        st.caption(f"총 {len(jobs)}개 공고")
        for job in jobs:
            _job_card(job)
        st.caption("※ 정확한 접수 마감일·세부 요건은 '공고 검색'을 눌러 각 기관 채용 페이지에서 최종 확인하세요.")
    else:
        st.warning("조건에 맞는 공고가 없어요. 키워드를 바꿔보세요.")
