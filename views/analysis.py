import streamlit as st
from utils.claude_api import analyze_spec
from utils.session import save_session

def show():
    st.title("스펙 분석")
    st.caption("목표 직무 대비 내 스펙을 AI가 분석해드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
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
        result = st.session_state.analysis_result
        st.markdown(f"""
        <div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:32px;
             border:1px solid rgba(59,130,246,0.2); margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:24px;">
                <div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>
                <span style="color:#60a5fa; font-size:13px; font-weight:700; letter-spacing:1px;">AI 분석 완료</span>
            </div>
            <div style="color:#CBD5E1; font-size:15px; line-height:1.8;">
                {result}
            </div>
        </div>
        """, unsafe_allow_html=True)
