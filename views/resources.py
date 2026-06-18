import streamlit as st
from utils.claude_api import recommend_resources, koreanize
from utils.session import save_session
from utils.nav import go_to
from utils.resources_data import get_resources, list_certs


def _md_table(headers, rows):
    """데이터로 마크다운 표 생성 (전역 CSS가 예쁘게 렌더)."""
    out = "| " + " | ".join(headers) + " |\n"
    out += "| " + " | ".join("---" for _ in headers) + " |\n"
    for r in rows:
        cells = [str(c).replace("|", "/").replace("\n", " ") for c in r]
        out += "| " + " | ".join(cells) + " |\n"
    return out


def _render_curated(data):
    st.success(f"**{data['label']}** 추천 교재·강의예요 (2026년 기준)")
    if data.get("books"):
        st.markdown("#### 📖 추천 교재")
        st.markdown(_md_table(
            ["교재명", "출판사", "특징"],
            [(b["name"], b.get("publisher", ""), b.get("note", "")) for b in data["books"]],
        ))
    if data.get("lectures"):
        st.markdown("#### 🎬 추천 강의")
        st.markdown(_md_table(
            ["강의", "플랫폼", "가격", "특징"],
            [(l["name"], l.get("platform", ""), l.get("price", ""), l.get("note", "")) for l in data["lectures"]],
        ))
    if data.get("free"):
        st.markdown("#### 🔧 무료 자료")
        for f in data["free"]:
            st.markdown(f"- {f}")
    if data.get("tip"):
        st.info("💡 " + data["tip"])


def show():
    st.title("교재 · 강의 추천")
    st.caption("목표 자격증의 실제 교재·강의를 정리해드려요 (없으면 AI가 추천)")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile

    # 공부 스케줄에서 정한 목표가 있으면 기본값으로
    default_subject = st.session_state.get("sched_goal", "")
    if default_subject in ("직접 입력", ""):
        default_subject = ""

    subject = st.text_input(
        "어떤 과목 · 자격증을 공부하려고 해요?",
        value=default_subject,
        placeholder="예: SQLD, 정보처리기사, 전기기사, 치과위생사",
    )

    data = get_resources(subject) if subject else None

    if data:
        # ===== 실제 큐레이션 데이터 =====
        _render_curated(data)
        st.divider()
        st.markdown('<p style="color:#94A3B8; font-size:13px;">내 스펙에 맞춘 추가 팁이 필요하면 AI에게 물어보세요</p>', unsafe_allow_html=True)
        if st.button("AI 맞춤 추가 추천", use_container_width=True, disabled=not subject):
            with st.spinner("AI가 추가 리소스를 찾고 있어요..."):
                st.session_state.resources_result = recommend_resources(profile, subject)
                if st.session_state.get("current_user"):
                    save_session(st.session_state.current_user)
    else:
        # ===== 등록 안 된 자격증 → AI =====
        if subject:
            st.caption("등록된 자격증이 아니어서 AI가 추천해드려요.")
        st.caption("바로 보기: " + ", ".join(list_certs()[:8]) + " 등")
        if st.button("AI 추천 받기", type="primary", use_container_width=True, disabled=not subject):
            with st.spinner("AI가 최적의 리소스를 찾고 있어요..."):
                st.session_state.resources_result = recommend_resources(profile, subject)
                if st.session_state.get("current_user"):
                    save_session(st.session_state.current_user)

    if st.session_state.get("resources_result"):
        st.divider()
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">'
            '<div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>'
            '<span style="color:#60a5fa; font-size:13px; font-weight:700; letter-spacing:1px;">AI 추가 추천</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.markdown(koreanize(st.session_state.resources_result))
