import streamlit as st

CERT_FEES = {
    "정보처리기사": {"필기": 19400, "실기": 22600},
    "컴퓨터활용능력 1급": {"필기": 19000, "실기": 25000},
    "컴퓨터활용능력 2급": {"필기": 19000, "실기": 25000},
    "SQLD": {"단일": 50000},
    "ADsP": {"단일": 50000},
    "토익": {"단일": 55000},
    "오픽": {"단일": 84000},
    "직접 입력": {"단일": 0},
}

def show():
    st.title("비용 계산기")
    st.caption("자격증 준비에 드는 총 비용을 자동으로 계산해드려요")
    st.divider()

    cert = st.selectbox("자격증 선택", list(CERT_FEES.keys()))
    exam_fee = 0
    fees = CERT_FEES[cert]

    if cert == "직접 입력":
        exam_fee = st.number_input("응시료 (원)", min_value=0, step=1000)
    elif "필기" in fees:
        col1, col2 = st.columns(2)
        with col1:
            written = st.checkbox(f"필기 ({fees['필기']:,}원)", value=True)
        with col2:
            practical = st.checkbox(f"실기 ({fees['실기']:,}원)", value=True)
        exam_fee = (fees["필기"] if written else 0) + (fees["실기"] if practical else 0)
    else:
        exam_fee = fees["단일"]
        st.info(f"응시료: {exam_fee:,}원")

    st.divider()
    col3, col4 = st.columns(2)
    with col3:
        book_count = st.number_input("교재 수", min_value=0, max_value=10, value=1)
        book_price = st.number_input("교재 평균 가격 (원)", min_value=0, step=1000, value=25000)
    with col4:
        lecture_type = st.radio("강의 유형", ["무료", "유료"])
        lecture_fee = 0
        if lecture_type == "유료":
            lecture_fee = st.number_input("강의 가격 (원)", min_value=0, step=1000, value=99000)

    etc_fee = st.number_input("기타 비용 (원)", min_value=0, step=1000, value=10000)

    total = exam_fee + (book_count * book_price) + lecture_fee + etc_fee

    st.divider()
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("응시료", f"{exam_fee:,}원")
    with col6:
        st.metric("교재비", f"{book_count * book_price:,}원")
    with col7:
        st.metric("강의비", f"{lecture_fee:,}원")
    with col8:
        st.metric("기타", f"{etc_fee:,}원")

    st.divider()
    st.metric("총 예상 비용", f"{total:,}원")

    if total < 50000:
        st.success("비용이 매우 저렴해요. 부담 없이 도전해보세요!")
    elif total < 150000:
        st.info("합리적인 비용이에요. 무료 강의를 활용하면 더 절약할 수 있어요.")
    else:
        st.warning("유튜브 무료 강의나 도서관 교재를 활용해보세요.")
