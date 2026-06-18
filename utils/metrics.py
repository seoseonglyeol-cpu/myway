import re


def compute_readiness(session):
    """준비도(%)를 실제 데이터에서 계산. 우선순위: 학기 플래너 > 선배 갭 분석 > 스펙 분석.
    아무 분석도 없으면 None."""
    # 1. 학기 플래너 플랜의 전체 준비도
    plan = session.get("planner_plan")
    if isinstance(plan, dict):
        v = plan.get("overview", {}).get("totalReadiness")
        if isinstance(v, (int, float)):
            return max(0, min(100, int(v)))

    # 2. 선배 갭 분석의 '완성도: NN%'
    mr = session.get("mentor_result")
    if isinstance(mr, dict) and mr.get("text"):
        m = re.search(r"완성도[^\d]*(\d{1,3})\s*%", mr["text"])
        if m:
            return max(0, min(100, int(m.group(1))))

    # 3. 스펙 분석의 '완성도/준비도 ... NN%'
    ar = session.get("analysis_result")
    if isinstance(ar, str):
        m = re.search(r"(?:완성도|준비도)[^\d]*(\d{1,3})\s*%", ar)
        if m:
            return max(0, min(100, int(m.group(1))))

    return None
