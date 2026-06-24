import re
import streamlit as st
from utils.claude_api import analyze_spec, koreanize
from utils.session import save_session
from utils.nav import go_to
from utils.ui import pop_summary, render_summary

def show():
    st.title("스펙 분석")
    st.caption("목표 직무 대비 내 스펙을 AI가 분석해드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("이름", profile["name"])
    with col2:
        st.metric("학교", profile["university"])
    with col3:
        st.metric("목표 직무", profile["target_job"])

    st.divider()
    if st.button("AI 스펙 분석 시작", type="primary", use_container_width=True):
        with st.spinner("AI가 분석 중입니다..."):
            result = analyze_spec(profile)
            st.session_state.analysis_result = result
            if st.session_state.get("current_user"):
                save_session(st.session_state.current_user)

    if st.session_state.get("analysis_result"):
        st.divider()
        result = koreanize(st.session_state.analysis_result)
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">'
            '<div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>'
            '<span style="color:#60a5fa; font-size:13px; font-weight:700; letter-spacing:1px;">AI 분석 완료</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        # 완성도 줄은 본문에서 제거하고, 수치는 전역 준비도(compute_readiness)로 통일
        result = re.sub(r".*완성도[^\d]*\d{1,3}\s*%.*\n?", "", result, count=1)
        from utils.metrics import compute_readiness
        readiness = compute_readiness(st.session_state)
        if readiness is not None:
            st.metric("준비도", f"{readiness}%")

        # 상단 '한눈에 요약' 카드 — 본문에서 떼어내 강조 렌더
        summary, result = pop_summary(result)
        render_summary(summary)

        # ## 섹션을 아코디언으로 분리 — 첫 섹션만 펼치고 나머지는 접어 한눈에 보이게
        parts = re.split(r"\n(?=##\s)", result.strip())
        sections = [p.strip() for p in parts if p.strip().startswith("##")]
        if sections:
            for i, sec in enumerate(sections):
                split = sec.split("\n", 1)
                header = split[0].lstrip("#").strip()
                body = split[1].strip() if len(split) > 1 else ""
                with st.expander(header, expanded=(i == 0)):
                    st.markdown(body)
        else:
            with st.container(border=True):
                st.markdown(result)

        st.markdown('<p style="color:#94A3B8; font-size:13px;">다음 단계로 이어가 보세요</p>', unsafe_allow_html=True)
        n1, n2 = st.columns(2)
        with n1:
            if st.button("선배와 비교하기", use_container_width=True, key="analysis_to_mentor"):
                go_to("선배 매칭")
        with n2:
            if st.button("로드맵 만들기", use_container_width=True, key="analysis_to_roadmap"):
                go_to("로드맵")
