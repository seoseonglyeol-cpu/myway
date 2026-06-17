import streamlit as st
from utils.claude_api import generate_roadmap
from utils.session import save_session

def show():
    st.title("맞춤 로드맵")
    st.caption("AI가 취준 단계별 로드맵을 짜드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        return

    profile = st.session_state.user_profile
    st.info(f"{profile['name']}님의 {profile['target_job']} 취준 로드맵")

    if st.button("로드맵 생성", type="primary", use_container_width=True):
        with st.spinner("AI가 로드맵을 만들고 있습니다..."):
            result = generate_roadmap(profile)
            st.session_state.roadmap_result = result
            if st.session_state.get("current_user"):
                save_session(st.session_state.current_user)

    if st.session_state.get("roadmap_result"):
        st.divider()

        profile = st.session_state.user_profile
        job = profile.get("target_job", "")

        st.markdown(f"""
        <div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:32px;
             border:1px solid rgba(59,130,246,0.2); margin-bottom:24px; overflow-x:auto;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:24px;">
                <div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>
                <span style="color:#60a5fa; font-size:13px; font-weight:700;">{job} 취준 로드맵</span>
            </div>
            <div style="display:grid; grid-template-columns:120px 1fr 1fr 1fr 1fr; gap:2px; margin-bottom:4px;">
                <div style="background:#0a1628; padding:12px; border-radius:8px 0 0 0;">
                    <span style="color:#FFFFFF; font-size:12px; font-weight:700;">단계</span>
                </div>
                <div style="background:#0a1628; padding:12px; text-align:center;">
                    <span style="color:#FFFFFF; font-size:12px; font-weight:700;">지금</span>
                </div>
                <div style="background:#0a1628; padding:12px; text-align:center;">
                    <span style="color:#FFFFFF; font-size:12px; font-weight:700;">1~3개월</span>
                </div>
                <div style="background:#0a1628; padding:12px; text-align:center;">
                    <span style="color:#FFFFFF; font-size:12px; font-weight:700;">3~6개월</span>
                </div>
                <div style="background:#0a1628; padding:12px; text-align:center; border-radius:0 8px 0 0;">
                    <span style="color:#FFFFFF; font-size:12px; font-weight:700;">6개월~</span>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:120px 1fr 1fr 1fr 1fr; gap:2px; margin-bottom:2px;">
                <div style="background:rgba(15,27,46,0.45); padding:12px; display:flex; align-items:center;">
                    <span style="color:#E2E8F0; font-size:13px; font-weight:600;">자격증</span>
                </div>
                <div style="background:rgba(59,130,246,0.1); padding:12px; grid-column: span 2;">
                    <div style="background:linear-gradient(135deg,#2563eb,#3b82f6); border-radius:6px; padding:6px 12px;">
                        <span style="color:#FFF; font-size:11px; font-weight:600;">필수 자격증 취득</span>
                    </div>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;">
                    <div style="background:rgba(148,163,184,0.2); border-radius:6px; padding:6px 12px;">
                        <span style="color:#CBD5E1; font-size:11px;">심화 자격증</span>
                    </div>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;"></div>
            </div>
            <div style="display:grid; grid-template-columns:120px 1fr 1fr 1fr 1fr; gap:2px; margin-bottom:2px;">
                <div style="background:rgba(15,27,46,0.45); padding:12px; display:flex; align-items:center;">
                    <span style="color:#E2E8F0; font-size:13px; font-weight:600;">스킬</span>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;">
                    <div style="background:#DBEAFE; border-radius:6px; padding:6px 12px;">
                        <span style="color:#1D4ED8; font-size:11px; font-weight:600;">기초 학습</span>
                    </div>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px; grid-column: span 2;">
                    <div style="background:#1D4ED8; border-radius:6px; padding:6px 12px;">
                        <span style="color:#FFF; font-size:11px; font-weight:600;">실무 스킬 향상</span>
                    </div>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;"></div>
            </div>
            <div style="display:grid; grid-template-columns:120px 1fr 1fr 1fr 1fr; gap:2px; margin-bottom:2px;">
                <div style="background:rgba(15,27,46,0.45); padding:12px; display:flex; align-items:center;">
                    <span style="color:#E2E8F0; font-size:13px; font-weight:600;">경험</span>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;"></div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;">
                    <div style="background:#FEF3C7; border-radius:6px; padding:6px 12px;">
                        <span style="color:#92400E; font-size:11px; font-weight:600;">공모전/프로젝트</span>
                    </div>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px; grid-column: span 2;">
                    <div style="background:#F59E0B; border-radius:6px; padding:6px 12px;">
                        <span style="color:#FFF; font-size:11px; font-weight:600;">인턴십 + 포트폴리오</span>
                    </div>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:120px 1fr 1fr 1fr 1fr; gap:2px;">
                <div style="background:rgba(15,27,46,0.45); padding:12px; display:flex; align-items:center; border-radius:0 0 0 8px;">
                    <span style="color:#E2E8F0; font-size:13px; font-weight:600;">취업준비</span>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;"></div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;"></div>
                <div style="background:rgba(15,27,46,0.45); padding:12px;">
                    <div style="background:#FEE2E2; border-radius:6px; padding:6px 12px;">
                        <span style="color:#DC2626; font-size:11px; font-weight:600;">서류 준비</span>
                    </div>
                </div>
                <div style="background:rgba(15,27,46,0.45); padding:12px; border-radius:0 0 8px 0;">
                    <div style="background:#DC2626; border-radius:6px; padding:6px 12px;">
                        <span style="color:#FFF; font-size:11px; font-weight:600;">면접 + 입사</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(15,27,46,0.6); border-radius:16px; padding:32px;
             border:1px solid rgba(59,130,246,0.2);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:24px;">
                <div style="width:8px; height:8px; border-radius:50%; background:#3b82f6;"></div>
                <span style="color:#60a5fa; font-size:13px; font-weight:700;">상세 로드맵</span>
            </div>
            <div style="color:#CBD5E1; font-size:15px; line-height:1.8;">
                {st.session_state.roadmap_result}
            </div>
        </div>
        """, unsafe_allow_html=True)
