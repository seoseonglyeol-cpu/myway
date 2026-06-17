import streamlit as st
from datetime import date, datetime

def render_progress_cards(data, show_subjects=True):
    """진행률 대시보드 카드 렌더링."""
    # 학점 진행률
    credit_pct = min(int((data["completed_credits"] / data["total_credits"]) * 100), 100)
    remaining_credits = data["total_credits"] - data["completed_credits"]

    # 학기 진행률
    remaining_semesters = data["total_semesters"] - data["completed_semesters"]

    # D-day 계산
    today = date.today()
    semester_end = datetime.strptime(data["semester_end"], "%Y-%m-%d").date()
    vacation_start = datetime.strptime(data["vacation_start"], "%Y-%m-%d").date()
    days_to_end = (semester_end - today).days
    days_to_vacation = (vacation_start - today).days

    # 메인 카드 - 학점 진행률
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, rgba(30,58,95,0.55), rgba(10,22,40,0.65)); border:1px solid rgba(59,130,246,0.2); border-radius:16px; padding:28px; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="color:#94A3B8; font-size:13px; font-weight:600; letter-spacing:1px;">학점 이수율</span>
            <span style="color:#60a5fa; font-size:14px; font-weight:700;">{data['completed_credits']} / {data['total_credits']} 학점</span>
        </div>
        <div style="font-size:48px; font-weight:900; color:#60a5fa; margin-bottom:12px;">{credit_pct}%</div>
        <div style="background:rgba(148,163,184,0.2); border-radius:4px; height:8px; overflow:hidden;">
            <div style="background:linear-gradient(90deg,#2563eb,#3b82f6); height:100%; width:{credit_pct}%; border-radius:4px;"></div>
        </div>
        <div style="color:#94A3B8; font-size:12px; margin-top:8px;">남은 학점: {remaining_credits}학점</div>
    </div>
    """, unsafe_allow_html=True)

    # 서브 카드 4개
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("현재 학점", f"{data['current_gpa']}")
    with col2:
        st.metric("목표 학점", f"{data['target_gpa']}")
    with col3:
        st.metric("종강까지", f"D-{days_to_end}" if days_to_end >= 0 else "종강!")
    with col4:
        st.metric("방학까지", f"D-{days_to_vacation}" if days_to_vacation >= 0 else "방학!")

    st.markdown("<br>", unsafe_allow_html=True)

    # 학기 진행률 바
    st.markdown(f"""
    <div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:24px;
         border:1px solid rgba(59,130,246,0.2); margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
            <span style="color:#F1F5F9; font-size:15px; font-weight:700;">학기 진행률</span>
            <span style="color:#94A3B8; font-size:13px;">{data['completed_semesters']} / {data['total_semesters']} 학기</span>
        </div>
        <div style="display:flex; gap:4px;">
            {"".join(f'<div style="flex:1; height:24px; border-radius:6px; background:{"#3b82f6" if i < data["completed_semesters"] else "#93c5fd" if i == data["completed_semesters"] else "rgba(148,163,184,0.2)"};"></div>' for i in range(data["total_semesters"]))}
        </div>
        <div style="color:#94A3B8; font-size:12px; margin-top:8px;">남은 학기: {remaining_semesters}학기</div>
    </div>
    """, unsafe_allow_html=True)

    # 이번 학기 과목
    if show_subjects and data.get("subjects"):
        subjects_list = [s.strip() for s in data["subjects"].split(",") if s.strip()]
        st.markdown(f"""
        <div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:24px;
             border:1px solid rgba(59,130,246,0.2); margin-bottom:16px;">
            <span style="color:#F1F5F9; font-size:15px; font-weight:700;">이번 학기 수강 과목</span>
            <span style="color:#94A3B8; font-size:13px; margin-left:8px;">({data['this_semester_credits']}학점)</span>
            <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">
                {"".join(f'<span style="background:rgba(59,130,246,0.15); color:#93c5fd; font-size:13px; font-weight:600; padding:6px 14px; border-radius:20px; border:1px solid rgba(59,130,246,0.35);">{s}</span>' for s in subjects_list)}
            </div>
        </div>
        """, unsafe_allow_html=True)


def _input_form():
    """진행률 정보 입력 폼."""
    with st.form("progress_form"):
        st.subheader("학점 정보")
        col1, col2 = st.columns(2)
        with col1:
            total_credits = st.number_input("졸업 필요 학점", min_value=100, max_value=200, value=130)
            completed_credits = st.number_input("현재 이수 학점", min_value=0, max_value=200, value=0)
        with col2:
            current_gpa = st.number_input("현재 평균 학점 (4.5 기준)", min_value=0.0, max_value=4.5, step=0.01, value=0.0)
            target_gpa = st.number_input("목표 학점", min_value=0.0, max_value=4.5, step=0.01, value=4.0)

        st.divider()
        st.subheader("학기 정보")
        col3, col4 = st.columns(2)
        with col3:
            total_semesters = st.number_input("총 학기 수", min_value=6, max_value=12, value=8)
            completed_semesters = st.number_input("완료한 학기 수", min_value=0, max_value=12, value=0)
        with col4:
            semester_end = st.date_input("이번 학기 종강일")
            vacation_start = st.date_input("방학 시작일")

        st.divider()
        st.subheader("이번 학기 수강 과목")
        subjects = st.text_area("수강 과목 (쉼표로 구분)",
            placeholder="예: 공학수학, 재료역학, 영어회화, 프로그래밍")
        this_semester_credits = st.number_input("이번 학기 수강 학점", min_value=0, max_value=24, value=18)

        if st.form_submit_button("저장", use_container_width=True, type="primary"):
            st.session_state.progress_data = {
                "total_credits": total_credits,
                "completed_credits": completed_credits,
                "current_gpa": current_gpa,
                "target_gpa": target_gpa,
                "total_semesters": total_semesters,
                "completed_semesters": completed_semesters,
                "semester_end": str(semester_end),
                "vacation_start": str(vacation_start),
                "subjects": subjects,
                "this_semester_credits": this_semester_credits,
            }
            if st.session_state.get("current_user"):
                from utils.session import save_session
                save_session(st.session_state.current_user)
            st.rerun()


def home_block():
    """홈 화면 진행률 섹션: 데이터 있으면 대시보드, 없으면 입력 폼."""
    st.markdown('<p style="color:#F1F5F9; font-size:18px; font-weight:700; margin:8px 0 16px 0;">대학생활 진행률</p>', unsafe_allow_html=True)
    data = st.session_state.get("progress_data")
    if not data:
        st.info("대학생활 정보를 입력하면 진행률 대시보드가 표시돼요")
        _input_form()
        return
    render_progress_cards(data, show_subjects=True)
    if st.button("정보 수정", use_container_width=True):
        del st.session_state.progress_data
        st.rerun()
