import re
import streamlit as st
from utils.session import save_session
from utils.nav import go_to

SOURCE_COLORS = {
    "학기 플래너": "#3b82f6",
    "로드맵": "#22c55e",
    "직접": "#a78bfa",
}


def _save():
    if st.session_state.get("current_user"):
        save_session(st.session_state.current_user)


def _ensure_state():
    st.session_state.setdefault("todos", [])
    st.session_state.setdefault("todo_seq", 0)


def _add_id():
    st.session_state.todo_seq += 1
    return st.session_state.todo_seq


def _add_todo():
    """직접 추가 콜백 (위젯 재생성 전 실행되어 입력칸 비우기 허용)."""
    txt = (st.session_state.get("todo_new") or "").strip()
    if txt:
        st.session_state.todos.append(
            {"id": _add_id(), "text": txt, "done": False, "source": "직접", "deadline": ""}
        )
        st.session_state["todo_new"] = ""
        _save()


def _toggle(tid):
    for t in st.session_state.todos:
        if t["id"] == tid:
            t["done"] = st.session_state.get(f"todo_chk_{tid}", t["done"])
    _save()


def _collect_suggestions():
    """학기 플래너/로드맵에서 실행 항목 자동 수집. (text, source, deadline) 목록."""
    items = []
    plan = st.session_state.get("planner_plan")
    if isinstance(plan, dict):
        for a in plan.get("immediateActions", []):
            items.append((a.get("action", ""), "학기 플래너", a.get("deadline", "")))
        sems = plan.get("semesters", [])
        if sems:
            cur = sems[0]
            for c in cur.get("certifications", []):
                items.append((f"{c.get('name','')} 준비", "학기 플래너", ""))
            for ac in cur.get("activities", []):
                items.append((ac.get("name", ""), "학기 플래너", ac.get("period", "")))
            for g in cur.get("goals", []):
                items.append((g, "학기 플래너", ""))

    rm = st.session_state.get("roadmap_result")
    if isinstance(rm, str):
        m = re.search(r"##[^\n]*1단계[^\n]*\n(.*?)(?:\n##|\Z)", rm, re.S)
        if m:
            for line in m.group(1).splitlines():
                line = line.strip()
                if line.startswith("-") or line.startswith("*"):
                    items.append((line.lstrip("-* ").strip(), "로드맵", ""))

    return [(t, s, d) for (t, s, d) in items if t]


def _import_suggestions():
    existing = {t["text"] for t in st.session_state.todos}
    added = 0
    for text, source, deadline in _collect_suggestions():
        if text not in existing:
            st.session_state.todos.append(
                {"id": _add_id(), "text": text, "done": False, "source": source, "deadline": deadline}
            )
            existing.add(text)
            added += 1
    _save()
    return added


def show():
    _ensure_state()
    st.title("내 할 일")
    st.caption("AI가 추천한 행동을 모아서 체크하고, 직접 할 일도 추가하세요")
    st.divider()

    todos = st.session_state.todos
    total = len(todos)
    done = sum(1 for t in todos if t["done"])

    # 진행 요약
    if total:
        pct = int(done / total * 100)
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("완료", f"{done}/{total}")
        with c2:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.progress(pct / 100, text=f"{pct}% 완료")
        st.divider()

    # 자동 불러오기 / 직접 추가
    n_sugg = len(_collect_suggestions())
    top1, top2 = st.columns([1, 1])
    with top1:
        label = f"AI 추천 행동 불러오기 ({n_sugg}개)" if n_sugg else "AI 추천 행동 불러오기"
        if st.button(label, use_container_width=True, disabled=not n_sugg):
            added = _import_suggestions()
            st.toast(f"{added}개 항목을 추가했어요" if added else "이미 모두 추가돼 있어요")
            st.rerun()
    with top2:
        if not n_sugg:
            if st.button("학기 플래너에서 계획 만들기", use_container_width=True):
                go_to("학기 플래너")

    ac1, ac2 = st.columns([4, 1])
    with ac1:
        st.text_input("직접 할 일 추가", key="todo_new", placeholder="예: 알고리즘 문제 하루 2개 풀기", label_visibility="collapsed")
    with ac2:
        st.button("추가", use_container_width=True, on_click=_add_todo)

    st.divider()

    if not todos:
        st.info("아직 할 일이 없어요. 위에서 'AI 추천 행동 불러오기'를 누르거나 직접 추가해보세요.")
        return

    # 진행 중 → 완료 순으로 정렬해 표시
    for t in sorted(todos, key=lambda x: x["done"]):
        tid = t["id"]
        color = SOURCE_COLORS.get(t["source"], "#6b7280")
        meta = f'<span style="background:{color}22; color:{color}; font-size:10px; font-weight:700; padding:2px 8px; border-radius:10px; border:1px solid {color}55;">{t["source"]}</span>'
        if t.get("deadline"):
            meta += f' <span style="color:#94A3B8; font-size:11px;">⏰ {t["deadline"]}</span>'

        col_chk, col_meta, col_del = st.columns([8, 3, 1])
        with col_chk:
            st.checkbox(
                t["text"], value=t["done"], key=f"todo_chk_{tid}",
                on_change=_toggle, args=(tid,),
            )
        with col_meta:
            st.markdown(f'<div style="padding-top:6px;">{meta}</div>', unsafe_allow_html=True)
        with col_del:
            if st.button("✕", key=f"todo_del_{tid}"):
                st.session_state.todos = [x for x in todos if x["id"] != tid]
                _save()
                st.rerun()

    # 완료 항목 정리
    if done:
        st.divider()
        if st.button(f"완료한 {done}개 항목 지우기"):
            st.session_state.todos = [x for x in todos if not x["done"]]
            _save()
            st.rerun()
