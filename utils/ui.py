import re
import streamlit as st

# AI 마크다운에서 떼어낼 요약 섹션 제목 키워드.
SUMMARY_KEYWORD = "한눈에 요약"


def pop_summary(text):
    """AI 마크다운에서 '## ⚡ 한눈에 요약' 섹션을 떼어내 (요약 본문, 나머지 텍스트)로 반환.
    요약이 없으면 (None, 원본)."""
    if not text:
        return None, text
    parts = re.split(r"\n(?=##\s)", text.strip())
    summary, rest = None, []
    for p in parts:
        head = p.strip().split("\n", 1)[0]
        if summary is None and head.startswith("##") and SUMMARY_KEYWORD in head:
            body = p.strip().split("\n", 1)
            summary = body[1].strip() if len(body) > 1 else ""
        else:
            rest.append(p)
    return summary, "\n".join(rest).strip()


def _md_bold_to_html(s):
    """마크다운 **굵게** → HTML <strong> (HTML 카드 안에서 렌더되도록)."""
    return re.sub(r"\*\*(.+?)\*\*", r'<strong style="color:#FFFFFF;">\1</strong>', s)


def render_summary(summary):
    """요약 본문(글머리 3줄)을 페이지 상단의 강조 카드로 렌더. 비어 있으면 아무것도 안 함."""
    if not summary:
        return
    lines = [re.sub(r"^[-*•]\s*", "", ln.strip()) for ln in summary.splitlines() if ln.strip()]
    lines = [_md_bold_to_html(ln) for ln in lines[:3]]
    items = "".join(
        '<div style="display:flex; gap:9px; align-items:flex-start; margin:5px 0;">'
        '<span style="color:#60a5fa; font-size:14px; line-height:1.5;">•</span>'
        f'<span style="color:rgba(255,255,255,0.88); font-size:14px; line-height:1.5;">{ln}</span>'
        "</div>"
        for ln in lines
    )
    st.markdown(
        '<div style="background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); '
        'border-radius:14px; padding:16px 18px; margin-bottom:18px;">'
        '<div style="color:#60a5fa; font-size:13px; font-weight:700; letter-spacing:0.5px; margin-bottom:8px;">'
        '⚡ 한눈에 요약</div>'
        f'{items}</div>',
        unsafe_allow_html=True,
    )
