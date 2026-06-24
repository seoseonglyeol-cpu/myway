import streamlit as st
from utils.nav import go_to

# 취준 여정 단계: (제목, 완료를 판단할 session_state 키, 한 줄 설명, 이동할 메뉴)
STEPS = [
    ("스펙 입력", "user_profile", "학교·학점·목표 직무 등 기본 정보를 입력해요", "스펙 입력"),
    ("AI 스펙 분석", "analysis_result", "목표 직무 대비 내 준비도를 분석받아요", "스펙 분석"),
    ("선배 매칭", "mentor_result", "롤모델 선배와 내 스펙을 비교해 갭을 찾아요", "선배 매칭"),
    ("맞춤 로드맵", "roadmap_result", "지금부터 할 일을 시간 순서로 받아요", "로드맵"),
    ("학기 플래너", "planner_plan", "학기별로 과목·자격증을 시험 일정에 맞춰 배치해요", "학기 플래너"),
]


def _is_done(key):
    return bool(st.session_state.get(key))


def quick_start():
    """홈 '빠른 시작' — 진행 상태를 읽어 '지금 할 일' 하나를 강조하고, 전체 체크리스트를 보여준다."""
    done_flags = [_is_done(key) for _, key, _, _ in STEPS]
    done_count = sum(done_flags)
    total = len(STEPS)

    # 다음 할 일 = 아직 안 끝난 첫 단계
    next_idx = next((i for i, d in enumerate(done_flags) if not d), None)

    pct = int(done_count / total * 100)
    st.markdown(
        f'<div style="display:flex; align-items:baseline; justify-content:space-between; margin:8px 0 12px 0;">'
        f'<span style="color:#F1F5F9; font-size:18px; font-weight:700;">나의 취준 여정</span>'
        f'<span style="color:#60a5fa; font-size:14px; font-weight:700;">{done_count} / {total} 완료</span>'
        f'</div>'
        f'<div style="background:rgba(148,163,184,0.18); border-radius:5px; height:8px; overflow:hidden; margin-bottom:18px;">'
        f'<div style="background:linear-gradient(90deg,#2563eb,#3b82f6,#93c5fd); height:100%; width:{pct}%; border-radius:5px;"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if next_idx is not None:
        title, _, desc, menu = STEPS[next_idx]
        st.markdown(
            f'<div style="background:linear-gradient(135deg, rgba(37,99,235,0.18), rgba(59,130,246,0.08)); '
            f'border:1px solid rgba(59,130,246,0.4); border-radius:16px; padding:24px; margin-bottom:14px;">'
            f'<div style="color:#60a5fa; font-size:12px; font-weight:700; letter-spacing:2px;">⚡ 지금 할 일 · STEP {next_idx + 1}</div>'
            f'<div style="color:#FFFFFF; font-size:22px; font-weight:800; margin:8px 0 6px 0;">{title}</div>'
            f'<div style="color:#94A3B8; font-size:14px;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(f"{title} 하러 가기", use_container_width=True, type="primary", key="home_next_step"):
            go_to(menu)
    else:
        # 모든 단계 완료 — 실행/관리 단계로 안내
        st.markdown(
            '<div style="background:linear-gradient(135deg, rgba(34,197,94,0.15), rgba(59,130,246,0.08)); '
            'border:1px solid rgba(34,197,94,0.4); border-radius:16px; padding:24px; margin-bottom:14px;">'
            '<div style="color:#86efac; font-size:12px; font-weight:700; letter-spacing:2px;">🎉 준비 완료</div>'
            '<div style="color:#FFFFFF; font-size:22px; font-weight:800; margin:8px 0 6px 0;">계획은 끝났어요. 이제 실행만 남았어요</div>'
            '<div style="color:#94A3B8; font-size:14px;">할 일과 공부 스케줄로 매일의 실행을 챙겨보세요</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        e1, e2 = st.columns(2)
        with e1:
            if st.button("내 할 일 관리", use_container_width=True, type="primary", key="home_done_todo"):
                go_to("내 할 일")
        with e2:
            if st.button("공부 스케줄 보기", use_container_width=True, key="home_done_sched"):
                go_to("공부 스케줄")

    # 전체 체크리스트 (완료/대기 한눈에)
    rows = ""
    for i, (title, _, _, _) in enumerate(STEPS):
        if done_flags[i]:
            icon, color, weight = "✓", "#86efac", "600"
            badge = '<span style="color:#86efac; font-size:11px; font-weight:700;">완료</span>'
        elif i == next_idx:
            icon, color, weight = "▶", "#60a5fa", "700"
            badge = '<span style="color:#60a5fa; font-size:11px; font-weight:700;">지금</span>'
        else:
            icon, color, weight = "○", "rgba(255,255,255,0.35)", "500"
            badge = '<span style="color:rgba(255,255,255,0.3); font-size:11px;">대기</span>'
        rows += (
            f'<div style="display:flex; align-items:center; gap:12px; padding:9px 0; '
            f'border-bottom:1px solid rgba(59,130,246,0.08);">'
            f'<span style="color:{color}; font-size:15px; width:18px; text-align:center;">{icon}</span>'
            f'<span style="color:{color}; font-size:14px; font-weight:{weight}; flex:1;">STEP {i + 1}. {title}</span>'
            f'{badge}</div>'
        )
    st.markdown(
        f'<div style="background:rgba(15,27,46,0.5); border:1px solid rgba(59,130,246,0.15); '
        f'border-radius:14px; padding:8px 18px; margin-top:16px;">{rows}</div>',
        unsafe_allow_html=True,
    )
