import re
import streamlit as st
from utils.claude_api import generate_roadmap, koreanize
from utils.seniors import match_seniors, get_senior
from utils.session import save_session
from utils.nav import go_to

# 단계 헤더에 매칭할 색상/포인트
STAGE_ACCENTS = ["#3b82f6", "#60a5fa", "#f59e0b", "#22c55e", "#93c5fd", "#a78bfa"]


def _render_roadmap(text):
    """AI 마크다운(## 섹션)을 단계별 카드로 렌더. 본문은 st.markdown으로 정상 렌더."""
    text = koreanize(text)
    parts = re.split(r"\n(?=##\s)", text.strip())
    sections = [p.strip() for p in parts if p.strip().startswith("##")]
    if not sections:
        st.markdown(text)
        return
    for i, sec in enumerate(sections):
        split = sec.split("\n", 1)
        header = split[0].lstrip("#").strip()
        body = split[1].strip() if len(split) > 1 else ""
        accent = STAGE_ACCENTS[i % len(STAGE_ACCENTS)]
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:10px; margin:18px 0 8px;">'
            f'<div style="width:10px; height:10px; border-radius:50%; background:{accent}; box-shadow:0 0 10px {accent};"></div>'
            f'<span style="color:#FFFFFF; font-size:16px; font-weight:700;">{header}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.markdown(body)


def show():
    st.title("맞춤 로드맵")
    st.caption("시간 흐름(지금 → 6개월 이후)으로 무엇을 먼저 할지 한눈에 보여줘요")
    with st.expander("로드맵 vs 학기 플래너, 뭐가 달라요?"):
        st.markdown(
            "- **로드맵 (지금 여기)**: *시간 축* 단계별 우선순위 (지금 / 1~3개월 / 3~6개월 / 6개월+)\n"
            "- **학기 플래너**: *학기 축* (2026 2학기, 2027 1학기…)으로 과목·자격증을 시험 일정에 맞춰 배치"
        )
        if st.button("학기 플래너로 가기", key="rm_to_planner"):
            go_to("학기 플래너")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile
    major = profile.get("major") or "내 전공"
    target_job = profile.get("target_job", "목표 직무")

    seniors = match_seniors(profile)

    # 롤모델 선배 선택 (선배 매칭/플래너에서 고른 선배가 있으면 기본값)
    picked_id = None
    if seniors:
        labels = {f"{s['nickname']} · {s['company']} {s['job']}": s["id"] for s in seniors}
        default_idx = 0
        prev_id = st.session_state.get("planner_senior_id") or \
            (st.session_state.get("mentor_result") or {}).get("senior_id")
        if prev_id in labels.values():
            default_idx = list(labels.values()).index(prev_id)
        picked_label = st.selectbox("롤모델 선배 (선택)", list(labels.keys()), index=default_idx)
        picked_id = labels[picked_label]
        st.info(f"**{major}** · 목표 **{target_job}** 기준으로 선배와 비교해 로드맵을 만들어요")
    else:
        st.info(f"**{major}** · 목표 **{target_job}** 기준으로 로드맵을 만들어요 (매칭되는 선배 없음)")

    if st.button("로드맵 생성", type="primary", use_container_width=True):
        senior = get_senior(picked_id) if picked_id else None
        with st.spinner("AI가 선배 스펙과 시험 일정을 반영해 로드맵을 만들고 있어요..."):
            result = generate_roadmap(profile, senior)
            st.session_state.roadmap_result = result
            st.session_state.roadmap_senior_id = picked_id
            if st.session_state.get("current_user"):
                save_session(st.session_state.current_user)

    if st.session_state.get("roadmap_result"):
        st.divider()
        sr = get_senior(st.session_state.get("roadmap_senior_id"))
        if sr:
            st.success(f"**{sr['nickname']}** ({sr['company']} · {sr['job']}) 기준 로드맵이에요")
        _render_roadmap(st.session_state.roadmap_result)
