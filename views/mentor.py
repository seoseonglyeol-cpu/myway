import re
import streamlit as st
from utils.seniors import match_seniors, get_senior
from utils.claude_api import compare_with_senior, koreanize
from utils.session import save_session
from utils.nav import go_to


def _track_text(track):
    """복수전공/부전공 딕셔너리 → 표시 문자열."""
    if isinstance(track, dict) and track.get("has"):
        return f"{track.get('field','')} ({track.get('status','')})"
    return "없음"


# ===== 선배 카드 =====
def _senior_card(s):
    certs = "".join(
        f'<span style="background:rgba(59,130,246,0.12); color:#93c5fd; font-size:11px; font-weight:600; padding:3px 10px; border-radius:14px; border:1px solid rgba(59,130,246,0.3);">{c}</span>'
        for c in s["certificates"]
    )
    top_courses = ", ".join(c["name"] for c in s["courses"][:4])
    dm = s.get("doubleMajor", {})
    dm_text = dm.get("field") if dm.get("has") else "없음"
    st.markdown(f"""
    <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.1); border-radius:16px; padding:22px; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="width:44px; height:44px; border-radius:50%; background:linear-gradient(135deg,#2563eb,#3b82f6); display:flex; align-items:center; justify-content:center; flex-shrink:0; box-shadow:0 0 16px rgba(59,130,246,0.35);">
                <span style="color:#FFFFFF; font-size:18px; font-weight:700;">{s['nickname'][0]}</span>
            </div>
            <div style="flex:1;">
                <div style="color:#FFFFFF; font-size:16px; font-weight:700;">{s['nickname']}</div>
                <div style="color:#60a5fa; font-size:13px; font-weight:600;">{s['company']} · {s['job']}</div>
            </div>
            <span style="background:rgba(59,130,246,0.12); color:#93c5fd; font-size:11px; font-weight:600; padding:4px 10px; border-radius:12px; border:1px solid rgba(59,130,246,0.3);">{s.get('field','')}</span>
        </div>
        <div style="display:flex; gap:18px; margin-bottom:10px; flex-wrap:wrap;">
            <div><span style="color:rgba(255,255,255,0.5); font-size:11px;">학점</span><div style="color:#FFFFFF; font-size:15px; font-weight:700;">{s['gpa']}</div></div>
            <div><span style="color:rgba(255,255,255,0.5); font-size:11px;">전공</span><div style="color:#FFFFFF; font-size:15px; font-weight:700;">{s['major']}</div></div>
            <div><span style="color:rgba(255,255,255,0.5); font-size:11px;">복수전공</span><div style="color:#FFFFFF; font-size:15px; font-weight:700;">{dm_text}</div></div>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">{certs}</div>
        <div style="color:rgba(255,255,255,0.5); font-size:12px; margin-bottom:8px;">핵심 수업: {top_courses} 외</div>
        <div style="background:rgba(59,130,246,0.08); border-left:3px solid #3b82f6; border-radius:0 8px 8px 0; padding:10px 14px;">
            <span style="color:#93c5fd; font-size:12px;">💬 {s.get('keyAdvice','')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ===== 나 vs 선배 비교표 =====
def _compare_table(profile, s):
    rows = [
        ("학점", f"{profile.get('gpa', '-')}", f"{s['gpa']}"),
        ("어학", profile.get("english") or "없음", s["english"]),
        ("복수전공", _track_text(profile.get("double_major")), _track_text(s.get("doubleMajor"))),
        ("부전공", _track_text(profile.get("minor")), _track_text(s.get("minor"))),
        ("자격증", profile.get("certificates") or "없음", ", ".join(s["certificates"])),
        ("수강 과목 수", str(len(profile.get("courses") or [])), str(len(s.get("courses") or []))),
    ]
    body = "".join(
        f'<tr style="border-bottom:1px solid rgba(59,130,246,0.1);">'
        f'<td style="padding:10px 14px; color:rgba(255,255,255,0.5); font-size:13px; font-weight:600;">{label}</td>'
        f'<td style="padding:10px 14px; color:rgba(255,255,255,0.85); font-size:13px;">{me}</td>'
        f'<td style="padding:10px 14px; color:#93c5fd; font-size:13px; font-weight:600;">{sr}</td>'
        f'</tr>'
        for label, me, sr in rows
    )
    st.markdown(f"""
    <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.1); border-radius:16px; padding:8px; margin-bottom:16px; overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse;">
            <thead><tr style="background:linear-gradient(135deg,#1e3a5f,#1e40af);">
                <th style="padding:12px 14px; text-align:left; color:#FFF; font-size:12px;">항목</th>
                <th style="padding:12px 14px; text-align:left; color:#FFF; font-size:12px;">나</th>
                <th style="padding:12px 14px; text-align:left; color:#FFF; font-size:12px;">{s['nickname']}</th>
            </tr></thead>
            <tbody>{body}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ===== AI 갭 분석 결과 렌더 (완성도 게이지 + 아코디언) =====
def _render_result(text):
    text = koreanize(text)
    # 완성도 파싱
    pct = None
    m = re.search(r"완성도[^\d]*(\d{1,3})\s*%", text)
    if m:
        pct = max(0, min(100, int(m.group(1))))

    if pct is not None:
        st.markdown(f"""
        <div style="display:flex; justify-content:center; margin:4px 0 20px;">
            <div style="width:150px; height:150px; border-radius:50%;
                 background:conic-gradient(#3b82f6 {pct}%, rgba(59,130,246,0.12) 0);
                 display:flex; align-items:center; justify-content:center;">
                <div style="width:116px; height:116px; border-radius:50%; background:#0a1628; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                    <span style="color:#60a5fa; font-size:34px; font-weight:900;">{pct}%</span>
                    <span style="color:rgba(255,255,255,0.5); font-size:11px; letter-spacing:1px;">준비 완성도</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # 게이지 위에 쓴 완성도 줄은 본문에서 제거
        text = re.sub(r".*완성도[^\d]*\d{1,3}\s*%.*\n?", "", text, count=1)

    # 섹션을 아코디언으로 분리 (## 헤더 기준)
    parts = re.split(r'\n(?=##\s)', text.strip())
    sections = [p.strip() for p in parts if p.strip().startswith("##")]
    if sections:
        for i, sec in enumerate(sections):
            split = sec.split("\n", 1)
            header = split[0].lstrip("#").strip()
            body = split[1].strip() if len(split) > 1 else ""
            with st.expander(header, expanded=(i == 0)):
                st.markdown(body)
    else:
        # 헤더 분리 실패 시 통째로 카드에 표시
        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.1); border-radius:16px; padding:28px;">
            <div style="color:rgba(255,255,255,0.85); font-size:15px; line-height:1.8;">{text}</div>
        </div>
        """, unsafe_allow_html=True)


def show():
    st.title("선배 매칭")
    st.caption("내 목표에 취업한 선배를 찾아, 롤모델과 내 스펙을 AI가 비교해드려요")
    st.divider()

    if not st.session_state.get("user_profile"):
        st.warning("먼저 스펙 입력을 완료해주세요")
        if st.button("스펙 입력하러 가기", type="primary"):
            go_to("스펙 입력")
        return

    profile = st.session_state.user_profile
    target_job = profile.get("target_job", "미정")
    target_company = profile.get("target_company") or "전체"
    major = profile.get("major") or "내 전공"
    st.info(f"**{major}** 선배 중 목표(**{target_company} · {target_job}**)에 가까운 순서로 보여드려요")

    seniors = match_seniors(profile)
    if not seniors:
        st.warning("매칭되는 선배 데이터가 아직 없어요")
        return

    for s in seniors:
        _senior_card(s)

    st.divider()

    labels = {f"{s['nickname']} · {s['company']} {s['job']}": s["id"] for s in seniors}
    picked_label = st.selectbox("비교할 선배(롤모델)를 선택하세요", list(labels.keys()))
    picked_id = labels[picked_label]

    if st.button("이 선배와 내 스펙 비교 (AI)", type="primary", use_container_width=True):
        senior = get_senior(picked_id)
        with st.spinner("AI가 수강 과목·학점·자격증·복수전공까지 비교하고 있어요..."):
            result = compare_with_senior(profile, senior)
            st.session_state.mentor_result = {"senior_id": picked_id, "text": result}
            if st.session_state.get("current_user"):
                save_session(st.session_state.current_user)

    mr = st.session_state.get("mentor_result")
    if mr:
        senior = get_senior(mr["senior_id"])
        if senior:
            st.divider()
            st.markdown(f'<p style="color:#FFFFFF; font-size:18px; font-weight:700; margin-bottom:12px;">{senior["nickname"]} vs 나 · 갭 분석</p>', unsafe_allow_html=True)
            _compare_table(profile, senior)
            _render_result(mr["text"])

            st.divider()
            st.markdown('<p style="color:#94A3B8; font-size:13px;">이 선배 기준으로 다음 단계를 이어가 보세요</p>', unsafe_allow_html=True)
            n1, n2 = st.columns(2)
            with n1:
                if st.button("이 선배로 로드맵 만들기", use_container_width=True, key="mentor_to_roadmap"):
                    st.session_state.planner_senior_id = mr["senior_id"]
                    go_to("로드맵")
            with n2:
                if st.button("학기 플래너로 이어가기", use_container_width=True, key="mentor_to_planner"):
                    st.session_state.planner_senior_id = mr["senior_id"]
                    go_to("학기 플래너")
