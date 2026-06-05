import streamlit as st
from utils.session import save_session

def show():
    st.title("스펙 입력")
    st.caption("한 번만 입력하면 마이웨이가 알아서 챙겨드려요")
    st.divider()

    with st.form("profile_form"):
        st.subheader("기본 정보")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름", placeholder="홍길동")
            university = st.text_input("학교", placeholder="OO대학교")
        with col2:
            grade = st.selectbox("학년", ["1학년","2학년","3학년","4학년","졸업생"])
            major = st.text_input("전공", placeholder="컴퓨터공학과")

        st.divider()
        st.subheader("목표")
        col3, col4 = st.columns(2)
        with col3:
            target_job = st.text_input("목표 직무", placeholder="예: 백엔드 개발자")
        with col4:
            target_company = st.text_input("목표 회사", placeholder="예: 카카오, 네이버")

        st.divider()
        st.subheader("현재 스펙")
        col5, col6 = st.columns(2)
        with col5:
            gpa = st.number_input("학점 (4.5 기준)", min_value=0.0, max_value=4.5, step=0.01, value=3.5)
            english = st.text_input("어학점수", placeholder="예: 토익 850")
        with col6:
            certificates = st.text_area("보유 자격증", placeholder="예: 정보처리기사", height=100)
            activities = st.text_area("대외활동 / 인턴", placeholder="예: OO회사 인턴 6개월", height=100)

        st.divider()
        st.subheader("가용 시간")
        col7, col8 = st.columns(2)
        with col7:
            weekday_hours = st.slider("평일 하루 공부 가능 시간", 0, 12, 2)
        with col8:
            weekend_hours = st.slider("주말 하루 공부 가능 시간", 0, 12, 4)

        st.divider()
        submitted = st.form_submit_button("저장하고 분석 시작", use_container_width=True, type="primary")

        if submitted:
            if not name or not target_job:
                st.error("이름과 목표 직무는 필수입니다")
            else:
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
                    "weekday_hours": weekday_hours,
                    "weekend_hours": weekend_hours,
                }
                if st.session_state.get("current_user"):
                    save_session(st.session_state.current_user)
                st.success(f"{name}님의 스펙이 저장됐어요!")
                st.balloons()
