import streamlit as st
from utils.session import save_session
from utils.nav import go_to

# 카테고리별 좌측 컬러 바 (다크 블루 테마)
CATEGORIES = ["전공필수", "전공선택", "교양필수", "교양선택", "자유선택"]
CAT_COLORS = {
    "전공필수": "#3b82f6",
    "전공선택": "#60a5fa",
    "교양필수": "#8b5cf6",
    "교양선택": "#a78bfa",
    "자유선택": "#6b7280",
}
GRADES = ["A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F"]


# ===== A) 수강 과목 입력 (태그형) =====
def _add_course():
    """추가 버튼 콜백 — 위젯 재생성 전에 실행되어 입력칸 비우기가 허용됨."""
    name = (st.session_state.get("onb_course_name") or "").strip()
    if name:
        st.session_state.onb_courses.append({
            "name": name,
            "category": st.session_state.get("onb_course_cat", CATEGORIES[0]),
            "grade": st.session_state.get("onb_course_grade", GRADES[0]),
        })
        st.session_state["onb_course_name"] = ""  # 입력칸 비우기 (콜백 내부라 OK)


def _course_manager():
    st.subheader("수강 과목")
    st.caption("과목명·카테고리·학점을 입력하고 '추가'를 누르면 태그로 쌓여요")

    ac1, ac2, ac3, ac4 = st.columns([3, 2, 1.5, 1])
    with ac1:
        st.text_input("과목명", key="onb_course_name", placeholder="예: 자료구조")
    with ac2:
        st.selectbox("카테고리", CATEGORIES, key="onb_course_cat")
    with ac3:
        st.selectbox("학점", GRADES, key="onb_course_grade")
    with ac4:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.button("추가", use_container_width=True, on_click=_add_course)

    if st.session_state.onb_courses:
        for i, c in enumerate(st.session_state.onb_courses):
            color = CAT_COLORS.get(c["category"], "#6b7280")
            dc1, dc2 = st.columns([9, 1])
            with dc1:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; background:rgba(59,130,246,0.12);
                     border:1px solid rgba(59,130,246,0.3); border-left:4px solid {color};
                     border-radius:8px; padding:7px 12px; margin-bottom:6px;">
                    <span style="color:#FFFFFF; font-size:13px; font-weight:600;">{c['name']}</span>
                    <span style="color:#93c5fd; font-size:11px;">· {c['category']} · {c['grade']}</span>
                </div>
                """, unsafe_allow_html=True)
            with dc2:
                if st.button("✕", key=f"del_course_{i}"):
                    st.session_state.onb_courses.pop(i)
                    st.rerun()
    else:
        st.caption("아직 추가한 과목이 없어요")


# ===== B) 복수전공 / 부전공 (토글) =====
def _double_minor_manager():
    st.subheader("복수전공 / 부전공")
    has_double = st.toggle("복수전공 있음", key="onb_has_double")
    if has_double:
        d1, d2, d3 = st.columns([2, 1, 1])
        with d1:
            st.text_input("복수전공 분야", key="onb_double_field", placeholder="예: 통계학")
        with d2:
            st.text_input("이수 학점", key="onb_double_credits", placeholder="예: 39/42")
        with d3:
            st.selectbox("진행 상태", ["이수중", "완료"], key="onb_double_status")

    has_minor = st.toggle("부전공 있음", key="onb_has_minor")
    if has_minor:
        m1, m2, m3 = st.columns([2, 1, 1])
        with m1:
            st.text_input("부전공 분야", key="onb_minor_field", placeholder="예: 심리학")
        with m2:
            st.text_input("이수 학점 ", key="onb_minor_credits", placeholder="예: 21/21")
        with m3:
            st.selectbox("진행 상태 ", ["이수중", "완료"], key="onb_minor_status")


def show():
    st.title("스펙 입력")
    st.caption("한 번만 입력하면 마이웨이가 알아서 챙겨드려요")
    st.divider()

    # 기존 프로필이 있으면 초기값으로 한 번만 로드
    _existing = st.session_state.get("user_profile") or {}
    if "onb_courses" not in st.session_state:
        st.session_state.onb_courses = list(_existing.get("courses", []))
    _dm = _existing.get("double_major") or {}
    _mn = _existing.get("minor") or {}
    st.session_state.setdefault("onb_has_double", bool(_dm.get("has")))
    st.session_state.setdefault("onb_double_field", _dm.get("field", ""))
    st.session_state.setdefault("onb_double_credits", _dm.get("credits", ""))
    st.session_state.setdefault("onb_double_status", _dm.get("status") or "이수중")
    st.session_state.setdefault("onb_has_minor", bool(_mn.get("has")))
    st.session_state.setdefault("onb_minor_field", _mn.get("field", ""))
    st.session_state.setdefault("onb_minor_credits", _mn.get("credits", ""))
    st.session_state.setdefault("onb_minor_status", _mn.get("status") or "이수중")

    # 동적 섹션 (폼 밖 — 추가/삭제/토글이 즉시 반영되도록)
    _course_manager()
    st.divider()
    _double_minor_manager()
    st.divider()

    # 정적 섹션 (폼 안)
    with st.form("profile_form"):
        st.subheader("기본 정보")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름", value=_existing.get("name", ""), placeholder="홍길동")
            university = st.text_input("학교", value=_existing.get("university", ""), placeholder="OO대학교")
        with col2:
            _grades = ["1학년", "2학년", "3학년", "4학년", "졸업생"]
            grade = st.selectbox(
                "학년", _grades,
                index=_grades.index(_existing["grade"]) if _existing.get("grade") in _grades else 0,
            )
            major = st.text_input("전공", value=_existing.get("major", ""), placeholder="컴퓨터공학과")

        st.divider()
        st.subheader("목표")
        col3, col4 = st.columns(2)
        with col3:
            target_job = st.text_input("목표 직무", value=_existing.get("target_job", ""), placeholder="예: 백엔드 개발자")
        with col4:
            target_company = st.text_input("목표 회사", value=_existing.get("target_company", ""), placeholder="예: 카카오, 네이버")

        st.divider()
        st.subheader("현재 스펙")
        col5, col6 = st.columns(2)
        with col5:
            gpa = st.number_input("학점 (4.5 기준)", min_value=0.0, max_value=4.5, step=0.01, value=float(_existing.get("gpa", 3.5)))
            english = st.text_input("어학점수", value=_existing.get("english", ""), placeholder="예: 토익 850")
        with col6:
            certificates = st.text_area("보유 자격증", value=_existing.get("certificates", ""), placeholder="예: 정보처리기사", height=100)
            activities = st.text_area("대외활동 / 인턴", value=_existing.get("activities", ""), placeholder="예: OO회사 인턴 6개월", height=100)

        st.divider()
        st.subheader("가용 시간")
        col7, col8 = st.columns(2)
        with col7:
            weekday_hours = st.slider("평일 하루 공부 가능 시간", 0, 12, int(_existing.get("weekday_hours", 2)))
        with col8:
            weekend_hours = st.slider("주말 하루 공부 가능 시간", 0, 12, int(_existing.get("weekend_hours", 4)))

        st.divider()
        submitted = st.form_submit_button("저장하고 분석 시작", use_container_width=True, type="primary")

        if submitted:
            if not name or not target_job:
                st.error("이름과 목표 직무는 필수입니다")
            else:
                double_major = {
                    "has": st.session_state.get("onb_has_double", False),
                    "field": st.session_state.get("onb_double_field", ""),
                    "credits": st.session_state.get("onb_double_credits", ""),
                    "status": st.session_state.get("onb_double_status", ""),
                }
                minor = {
                    "has": st.session_state.get("onb_has_minor", False),
                    "field": st.session_state.get("onb_minor_field", ""),
                    "credits": st.session_state.get("onb_minor_credits", ""),
                    "status": st.session_state.get("onb_minor_status", ""),
                }
                st.session_state.user_profile = {
                    "name": name,
                    "university": university,
                    "grade": grade,
                    "major": major,
                    "target_job": target_job,
                    "target_company": target_company,
                    "gpa": gpa,
                    "english": english,
                    "certificates": certificates,
                    "activities": activities,
                    "courses": list(st.session_state.onb_courses),
                    "double_major": double_major,
                    "minor": minor,
                    "weekday_hours": weekday_hours,
                    "weekend_hours": weekend_hours,
                }
                if st.session_state.get("current_user"):
                    save_session(st.session_state.current_user)
                st.success(f"{name}님의 스펙이 저장됐어요!")
                st.balloons()

    # 저장된 프로필이 있으면 다음 단계로 이동 버튼 (폼 밖)
    if st.session_state.get("user_profile"):
        st.divider()
        st.markdown('<p style="color:#94A3B8; font-size:13px;">입력이 끝났다면 바로 다음 단계로 가보세요</p>', unsafe_allow_html=True)
        o1, o2, o3 = st.columns(3)
        with o1:
            if st.button("스펙 분석 받기", use_container_width=True, key="onb_to_analysis"):
                go_to("스펙 분석")
        with o2:
            if st.button("선배 매칭 보기", use_container_width=True, key="onb_to_mentor"):
                go_to("선배 매칭")
        with o3:
            if st.button("채용공고 보기", use_container_width=True, key="onb_to_jobs"):
                go_to("채용공고 탐색")
