import streamlit as st


def go_to(page):
    """다른 페이지로 이동. 사이드바 라디오(key='nav_page')를 다음 런에서 바꾼다.
    위젯 인스턴스화 이후에는 직접 못 바꾸므로 중간 키(_nav_target)에 저장 후 rerun."""
    st.session_state["_nav_target"] = page
    st.rerun()


def apply_pending_nav():
    """라디오 생성 전에 호출. 대기 중인 이동 요청을 nav_page에 반영."""
    if "_nav_target" in st.session_state:
        st.session_state["nav_page"] = st.session_state.pop("_nav_target")
