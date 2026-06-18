from datetime import date
import streamlit as st
from utils.session import save_session
from utils.seniors import match_seniors, get_senior
from utils.claude_api import generate_semester_plan
from utils.nav import go_to

# =====================================================================
# 학기 플래너 — 1차: A(학기 정보 입력) + C(타임라인 UI), 더미 데이터
# =====================================================================

SEM_OPTIONS = [
    "1학년 1학기", "1학년 2학기", "2학년 1학기", "2학년 2학기",
    "3학년 1학기", "3학년 2학기", "4학년 1학기", "4학년 2학기",
]

# urgency: (배경, 글자색, 테두리, 이모지, 라벨)
URGENCY = {
    "critical": ("rgba(239,68,68,0.15)", "#fca5a5", "rgba(239,68,68,0.3)", "🔴", "필수"),
    "high":     ("rgba(234,179,8,0.15)", "#fde047", "rgba(234,179,8,0.3)", "🟡", "높음"),
    "medium":   ("rgba(34,197,94,0.15)", "#86efac", "rgba(34,197,94,0.3)", "🟢", "권장"),
    "low":      ("rgba(255,255,255,0.05)", "rgba(255,255,255,0.4)", "rgba(255,255,255,0.1)", "⚪", "여유"),
}

# ---- 더미 플랜 데이터 (AI 연동 전 UI 확인용) ----
DUMMY_PLAN = {
    "overview": {"totalReadiness": 45, "targetReadiness": 90, "criticalGaps": 3, "estimatedMonths": 18},
    "target": "네이버 · 백엔드 개발자",
    "immediateActions": [
        {"action": "알고리즘 수강신청", "deadline": "D-23", "urgency": "critical"},
        {"action": "SQLD 교재 구매 및 스터디 모집", "deadline": "D-30", "urgency": "high"},
        {"action": "GitHub 포트폴리오 정리 시작", "deadline": "D-14", "urgency": "medium"},
    ],
    "semesters": [
        {
            "id": "2025-2", "label": "2025년 2학기", "status": "current", "summary": "기초 역량 구축 학기",
            "readinessBefore": 45, "readinessAfter": 58,
            "courses": [
                {"name": "알고리즘", "category": "전공필수", "credits": 3, "urgency": "critical", "reason": "선배 전원 이수, 코딩테스트 핵심"},
                {"name": "운영체제", "category": "전공필수", "credits": 3, "urgency": "critical", "reason": "면접 단골 질문"},
                {"name": "데이터베이스", "category": "전공선택", "credits": 3, "urgency": "high", "reason": "백엔드 필수 지식"},
            ],
            "certifications": [{"name": "SQLD", "difficulty": "중", "prepMonths": 2, "urgency": "high", "reason": "IT기업 서류 가산점"}],
            "activities": [{"type": "인턴", "name": "하계 인턴 지원", "period": "7월~8월", "urgency": "medium", "reason": "경험 갭 해소"}],
            "goals": ["학점 4.0 이상 유지", "알고리즘 문제 주 5회 풀기", "SQLD 교재 1회독 완료"],
        },
        {
            "id": "2026-1", "label": "2026년 1학기", "status": "upcoming", "summary": "실무 지식 확장 학기",
            "readinessBefore": 58, "readinessAfter": 72,
            "courses": [
                {"name": "컴퓨터네트워크", "category": "전공필수", "credits": 3, "urgency": "high", "reason": "서버 통신 이해 필수"},
                {"name": "소프트웨어공학", "category": "전공선택", "credits": 3, "urgency": "medium", "reason": "협업/설계 역량"},
            ],
            "certifications": [{"name": "정보처리기사 필기", "difficulty": "중", "prepMonths": 2, "urgency": "high", "reason": "개발 직무 기본 자격증"}],
            "activities": [{"type": "프로젝트", "name": "사이드 프로젝트 1개 완성", "period": "학기 중", "urgency": "high", "reason": "포트폴리오 핵심"}],
            "goals": ["프로젝트 GitHub 공개", "정보처리기사 필기 합격", "학점 4.0 유지"],
        },
        {
            "id": "2026-2", "label": "2026년 2학기", "status": "upcoming", "summary": "심화/포트폴리오 학기",
            "readinessBefore": 72, "readinessAfter": 85,
            "courses": [
                {"name": "분산시스템", "category": "전공선택", "credits": 3, "urgency": "medium", "reason": "대규모 서비스 이해"},
                {"name": "캡스톤디자인", "category": "전공필수", "credits": 3, "urgency": "high", "reason": "팀 프로젝트 경험"},
            ],
            "certifications": [{"name": "정보처리기사 실기", "difficulty": "중상", "prepMonths": 2, "urgency": "high", "reason": "필기 후 실기 취득"}],
            "activities": [{"type": "포트폴리오", "name": "포트폴리오 완성", "period": "학기 말", "urgency": "high", "reason": "지원 필수 자료"}],
            "goals": ["캡스톤 우수상 도전", "정보처리기사 최종 취득", "포트폴리오 사이트 배포"],
        },
        {
            "id": "2027-1", "label": "2027년 1학기", "status": "upcoming", "summary": "취업 집중 학기",
            "readinessBefore": 85, "readinessAfter": 95,
            "courses": [],
            "certifications": [],
            "activities": [
                {"type": "취업준비", "name": "자소서 작성 + 면접 준비", "period": "학기 초", "urgency": "critical", "reason": "상반기 공채 대비"},
                {"type": "지원", "name": "상반기 공채 지원", "period": "3~4월", "urgency": "critical", "reason": "목표 취업"},
            ],
            "goals": ["자소서 5개 이상 완성", "모의 면접 10회", "상반기 공채 합격"],
        },
    ],
}

STYLE = """
<style>
@keyframes currentPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.45); }
  50% { box-shadow: 0 0 0 12px rgba(59,130,246,0); }
}
@keyframes dotPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.6; }
}
.pl-node-current { animation: currentPulse 2s ease-in-out infinite; }
.pl-reddot { animation: dotPulse 1.4s ease-in-out infinite; }
</style>
"""


def _clean(html):
    """줄별 공백/빈 줄 제거 후 한 줄로 합쳐 마크다운 코드블록 오인을 방지."""
    return "".join(line.strip() for line in html.splitlines())


def _upcoming_semesters(remaining, today=None):
    """오늘(달력) 기준 현재 학기부터 remaining개 학기 라벨 생성.
    3~8월=1학기, 그 외=2학기. 반환: [{"id","label"}]"""
    today = today or date.today()
    year = today.year
    term = 1 if 3 <= today.month <= 8 else 2
    if today.month <= 2:  # 1,2월은 직전 연도 2학기 취급
        year -= 1
    out = []
    for _ in range(max(remaining, 1)):
        out.append({"id": f"{year}-{term}", "label": f"{year}년 {term}학기"})
        if term == 1:
            term = 2
        else:
            term, year = 1, year + 1
    return out


def _badge(urgency):
    bg, color, border, emoji, label = URGENCY.get(urgency, URGENCY["low"])
    return (f'<span style="background:{bg}; color:{color}; border:1px solid {border}; '
            f'font-size:11px; font-weight:600; padding:3px 9px; border-radius:12px; white-space:nowrap;">{emoji} {label}</span>')


def _overview_card(plan, remaining):
    ov = plan.get("overview", {})
    cur, tgt = ov.get("totalReadiness", 0), ov.get("targetReadiness", 90)
    return f"""
    <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.15); border-radius:16px; padding:24px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:10px;">
            <span style="color:rgba(255,255,255,0.6); font-size:13px; font-weight:600;">📊 전체 준비도</span>
            <span style="color:#93c5fd; font-size:13px; font-weight:700;">{cur}% <span style="color:rgba(255,255,255,0.4);">→ 목표 {tgt}%</span></span>
        </div>
        <div style="position:relative; background:rgba(148,163,184,0.18); border-radius:6px; height:14px; overflow:hidden; margin-bottom:6px;">
            <div style="background:linear-gradient(90deg,#1e40af,#3b82f6,#93c5fd); height:100%; width:{cur}%; border-radius:6px;"></div>
            <div style="position:absolute; top:-2px; left:{tgt}%; width:2px; height:18px; background:#93c5fd;"></div>
        </div>
        <div style="display:flex; gap:10px; margin-top:14px; flex-wrap:wrap;">
            <span style="background:rgba(59,130,246,0.12); color:#93c5fd; font-size:12px; font-weight:600; padding:5px 12px; border-radius:12px; border:1px solid rgba(59,130,246,0.25);">⏰ 남은 학기 {remaining}학기</span>
            <span style="background:rgba(59,130,246,0.12); color:#93c5fd; font-size:12px; font-weight:600; padding:5px 12px; border-radius:12px; border:1px solid rgba(59,130,246,0.25);">🎯 {plan.get('target','')}</span>
            <span style="background:rgba(239,68,68,0.12); color:#fca5a5; font-size:12px; font-weight:600; padding:5px 12px; border-radius:12px; border:1px solid rgba(239,68,68,0.25);">⚠️ 핵심 갭 {ov.get('criticalGaps',0)}개</span>
        </div>
    </div>
    """


def _immediate_card(plan):
    items = ""
    for a in plan.get("immediateActions", []):
        bg, color, border, emoji, _ = URGENCY.get(a.get("urgency"), URGENCY["low"])
        items += f"""
        <div style="display:flex; align-items:center; gap:10px; background:rgba(15,23,42,0.5); border:1px solid {border}; border-radius:10px; padding:11px 14px; margin-bottom:8px;">
            <span style="color:{color}; font-size:16px;">☐</span>
            <span style="color:#FFFFFF; font-size:13px; font-weight:500; flex:1;">{a.get('action','')}</span>
            <span style="color:{color}; font-size:12px; font-weight:700;">{emoji} {a.get('deadline','')}</span>
        </div>
        """
    return f"""
    <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(239,68,68,0.25); border-radius:16px; padding:20px; margin-bottom:24px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
            <span class="pl-reddot" style="width:9px; height:9px; border-radius:50%; background:#ef4444; display:inline-block;"></span>
            <span style="color:#FFFFFF; font-size:15px; font-weight:700;">⚡ 이번 주 액션</span>
        </div>
        {items}
    </div>
    """


def _semester_node(sem, is_last):
    is_current = sem.get("status") == "current"
    # 노드 점
    if is_current:
        dot = ('<div class="pl-node-current" style="width:16px; height:16px; border-radius:50%; '
               'background:#3b82f6; border:2px solid #93c5fd;"></div>')
    else:
        dot = ('<div style="width:12px; height:12px; border-radius:50%; background:transparent; '
               'border:2px solid #3b82f6; margin:2px;"></div>')
    line = "" if is_last else '<div style="flex:1; width:2px; background:linear-gradient(#3b82f6,#1e40af); margin:4px 0; min-height:24px;"></div>'

    # 카드 본문 섹션들
    def section(title, rows_html):
        if not rows_html:
            return ""
        return f"""
        <div style="background:rgba(10,22,40,0.5); border:1px solid rgba(59,130,246,0.12); border-radius:10px; padding:12px 14px; margin-top:10px;">
            <div style="color:#93c5fd; font-size:12px; font-weight:700; margin-bottom:8px;">{title}</div>
            {rows_html}
        </div>
        """

    courses_html = "".join(
        f'<div style="display:flex; align-items:center; gap:8px; padding:5px 0;">'
        f'<span style="color:#FFFFFF; font-size:13px; font-weight:600; flex:1;">{c.get("name","")}</span>'
        f'<span style="color:rgba(255,255,255,0.4); font-size:11px;">{c.get("category","")} · {c.get("credits","-")}학점</span>'
        f'{_badge(c.get("urgency"))}</div>'
        f'<div style="color:rgba(255,255,255,0.35); font-size:11px; padding-bottom:6px;">{c.get("reason","")}</div>'
        for c in sem.get("courses", [])
    )
    certs_html = "".join(
        f'<div style="display:flex; align-items:center; gap:8px; padding:5px 0;">'
        f'<span style="color:#FFFFFF; font-size:13px; font-weight:600; flex:1;">{c.get("name","")}</span>'
        f'<span style="color:rgba(255,255,255,0.4); font-size:11px;">난이도 {c.get("difficulty","-")} · {c.get("prepMonths","-")}개월</span>'
        f'{_badge(c.get("urgency"))}</div>'
        for c in sem.get("certifications", [])
    )
    acts_html = "".join(
        f'<div style="display:flex; align-items:center; gap:8px; padding:5px 0;">'
        f'<span style="color:#FFFFFF; font-size:13px; font-weight:600; flex:1;">{a.get("name","")}</span>'
        f'<span style="color:rgba(255,255,255,0.4); font-size:11px;">{a.get("period","")}</span>'
        f'{_badge(a.get("urgency"))}</div>'
        for a in sem.get("activities", [])
    )
    goals_html = "".join(
        f'<div style="color:rgba(255,255,255,0.75); font-size:13px; padding:4px 0;">☐ {g}</div>'
        for g in sem.get("goals", [])
    )

    growth = sem.get("readinessAfter", 0) - sem.get("readinessBefore", 0)
    cur_tag = '<span style="color:#3b82f6; font-size:12px; font-weight:700; margin-left:6px;">(현재)</span>' if is_current else ""

    card = f"""
    <div style="flex:1; background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.15); border-radius:16px; padding:20px; margin-bottom:18px;">
        <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:6px;">
            <div style="color:#FFFFFF; font-size:16px; font-weight:700;">{sem.get('label','')}{cur_tag}</div>
            <div style="color:#93c5fd; font-size:13px; font-weight:700;">준비도 {sem.get('readinessBefore',0)}% → {sem.get('readinessAfter',0)}% <span style="color:#86efac;">(+{growth}%)</span></div>
        </div>
        <div style="color:rgba(255,255,255,0.5); font-size:13px; margin-top:4px;">{sem.get('summary','')}</div>
        {section("📚 수강 과목", courses_html)}
        {section("📜 자격증", certs_html)}
        {section("💼 활동", acts_html)}
        {section("🎯 이 학기 목표", goals_html)}
        <div style="margin-top:14px;">
            <div style="background:rgba(148,163,184,0.18); border-radius:5px; height:8px; overflow:hidden;">
                <div style="background:linear-gradient(90deg,#1e40af,#3b82f6); height:100%; width:{sem.get('readinessAfter',0)}%; border-radius:5px;"></div>
            </div>
            <div style="color:rgba(255,255,255,0.4); font-size:11px; margin-top:5px;">이 학기 달성 시 준비도 {sem.get('readinessAfter',0)}%</div>
        </div>
    </div>
    """

    return f"""
    <div style="display:flex; gap:16px; align-items:stretch;">
        <div style="display:flex; flex-direction:column; align-items:center; padding-top:6px;">
            {dot}
            {line}
        </div>
        {card}
    </div>
    """


def _timeline(plan):
    sems = plan.get("semesters", [])
    nodes = "".join(
        _semester_node(s, is_last=(i == len(sems) - 1))
        for i, s in enumerate(sems)
    )
    return f'<div style="margin-top:8px;">{nodes}</div>'


def show():
    st.title("학기 플래너")
    st.caption("남은 학기별(2026 2학기, 2027 1학기…)로 과목·자격증·활동을 시험 일정에 맞춰 배치해요")
    with st.expander("학기 플래너 vs 로드맵, 뭐가 달라요?"):
        st.markdown(
            "- **학기 플래너 (지금 여기)**: *학기 축* 으로 과목·자격증을 시험 일정에 맞춰 배치 (수강 학점 고려)\n"
            "- **로드맵**: *시간 축* (지금 / 1~3개월 / 3~6개월 / 6개월+)으로 큰 흐름과 우선순위만 빠르게"
        )
        if st.button("로드맵으로 가기", key="pl_to_roadmap"):
            go_to("로드맵")
    st.divider()

    # ===== A. 내 학기 정보 입력 =====
    st.markdown('<p style="color:#FFFFFF; font-size:16px; font-weight:700;">🎓 내 학기 정보</p>', unsafe_allow_html=True)

    info = st.session_state.get("semester_info", {})
    a1, a2, a3 = st.columns(3)
    with a1:
        cur_sem = st.selectbox("현재 학년/학기", SEM_OPTIONS,
                               index=SEM_OPTIONS.index(info["currentSemester"]) if info.get("currentSemester") in SEM_OPTIONS else 4)
    with a2:
        grad_year = st.selectbox("졸업 예정 연도", list(range(2025, 2031)),
                                 index=(info.get("graduationYear", 2027) - 2025))
    with a3:
        grad_sem = st.selectbox("졸업 학기", ["1학기 (2월 졸업)", "2학기 (8월 졸업)"],
                                index=(info.get("graduationSemester", 2) - 1))

    b1, b2 = st.columns(2)
    with b1:
        target_timing = st.selectbox("목표 취업 시기", ["졸업 전", "졸업 후 3개월", "졸업 후 6개월", "미정"],
                                     index=["졸업 전", "졸업 후 3개월", "졸업 후 6개월", "미정"].index(info.get("targetTiming", "졸업 전")))
    with b2:
        max_credits = st.number_input("이번 학기 수강 가능 학점", min_value=0, max_value=24,
                                      value=int(info.get("maxCredits", 18)))
        st.caption("최대 21학점까지 가능")

    # 남은 학기 자동 계산 (현재 학기 ~ 4학년 2학기 기준, 현재 포함)
    idx = SEM_OPTIONS.index(cur_sem) + 1
    remaining = max(8 - idx + 1, 1)
    st.markdown(
        f'<div style="margin:6px 0 4px 0;">남은 학기: '
        f'<span style="color:#93c5fd; font-size:18px; font-weight:800;">{remaining}학기</span></div>',
        unsafe_allow_html=True)

    # 저장
    st.session_state.semester_info = {
        "currentSemester": cur_sem,
        "graduationYear": grad_year,
        "graduationSemester": 1 if grad_sem.startswith("1") else 2,
        "remainingSemesters": remaining,
        "targetTiming": target_timing,
        "maxCredits": max_credits,
    }
    if st.session_state.get("current_user"):
        save_session(st.session_state.current_user)

    st.divider()

    # ===== B. AI 학기 플랜 생성 =====
    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료하면 AI가 맞춤 학기 플랜을 만들어드려요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile
    seniors = match_seniors(profile)
    if not seniors:
        st.warning("매칭되는 선배가 없어 플랜을 만들 수 없어요")
        return

    st.markdown('<p style="color:#FFFFFF; font-size:16px; font-weight:700;">🤖 AI 학기 플랜 생성</p>', unsafe_allow_html=True)
    st.caption("롤모델 선배를 기준으로, 내 스펙 갭과 2026 시험 일정을 반영해 학기별 계획을 만들어요")

    labels = {f"{s['nickname']} · {s['company']} {s['job']}": s["id"] for s in seniors}
    # 선배 매칭에서 이미 고른 선배가 있으면 기본 선택
    default_idx = 0
    prev_id = st.session_state.get("planner_senior_id") or \
        (st.session_state.get("mentor_result") or {}).get("senior_id")
    if prev_id in labels.values():
        default_idx = list(labels.values()).index(prev_id)

    picked_label = st.selectbox("롤모델 선배", list(labels.keys()), index=default_idx)
    picked_id = labels[picked_label]

    def _run_generation():
        senior = get_senior(picked_id)
        sem_labels = _upcoming_semesters(remaining)
        gap_text = (st.session_state.get("mentor_result") or {}).get("text", "")
        with st.spinner("AI가 선배 스펙과 시험 일정을 비교해 학기별 계획을 짜고 있어요..."):
            plan = generate_semester_plan(profile, senior, st.session_state.semester_info, sem_labels, gap_text)
        if plan and plan.get("semesters"):
            st.session_state.planner_plan = plan
            st.session_state.planner_senior_id = picked_id
            if st.session_state.get("current_user"):
                save_session(st.session_state.current_user)
            st.rerun()
        else:
            st.error("플랜 생성에 실패했어요. 다시 시도해주세요.")

    has_plan = bool(st.session_state.get("planner_plan"))
    if not has_plan:
        if st.button("AI 학기 플랜 생성", type="primary", use_container_width=True):
            _run_generation()
    else:
        # 선택한 선배가 현재 플랜의 선배와 다르면 안내
        if picked_id != st.session_state.get("planner_senior_id"):
            st.caption("선배를 바꿨어요. '다시 생성'을 누르면 새 선배 기준으로 플랜을 다시 만들어요.")
        g1, g2 = st.columns([2, 1])
        with g1:
            if st.button("🔄 플랜 다시 생성", type="primary", use_container_width=True):
                _run_generation()
        with g2:
            if st.button("🗑️ 플랜 지우기", use_container_width=True):
                st.session_state.pop("planner_plan", None)
                st.session_state.pop("planner_senior_id", None)
                if st.session_state.get("current_user"):
                    save_session(st.session_state.current_user)
                st.rerun()

    st.divider()

    # ===== C. 타임라인 렌더 (실제 플랜 우선, 없으면 예시) =====
    plan = st.session_state.get("planner_plan")
    if plan:
        sr = get_senior(st.session_state.get("planner_senior_id"))
        if sr:
            st.success(f"**{sr['nickname']}** ({sr['company']} · {sr['job']}) 기준으로 만든 맞춤 플랜이에요")
    else:
        plan = DUMMY_PLAN
        st.info("아래는 **예시 미리보기**예요. 위에서 선배를 고르고 'AI 학기 플랜 생성'을 누르면 내 맞춤 플랜으로 바뀌어요")

    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(_clean(_overview_card(plan, remaining)), unsafe_allow_html=True)
    st.markdown(_clean(_immediate_card(plan)), unsafe_allow_html=True)
    st.markdown('<p style="color:#FFFFFF; font-size:16px; font-weight:700; margin-bottom:8px;">🗓️ 학기별 타임라인</p>', unsafe_allow_html=True)
    st.markdown(_clean(_timeline(plan)), unsafe_allow_html=True)
