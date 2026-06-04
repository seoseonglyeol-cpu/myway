SAMPLE_DATA = [
    {"title": "백엔드 개발자 신입 채용", "company": "카카오엔터프라이즈", "deadline": "2026-07-31", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "서버 개발자 (Java/Spring)", "company": "네이버클라우드", "deadline": "2026-08-15", "url": "https://www.work.go.kr", "tags": ["성남", "정규직", "대졸"]},
    {"title": "데이터 분석가 신입", "company": "SK하이닉스", "deadline": "2026-07-20", "url": "https://www.work.go.kr", "tags": ["이천", "정규직", "대졸이상"]},
    {"title": "마케터 신입 공개채용", "company": "LG생활건강", "deadline": "2026-08-01", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "프론트엔드 개발자", "company": "라인플러스", "deadline": "2026-07-25", "url": "https://www.work.go.kr", "tags": ["성남", "정규직", "대졸"]},
    {"title": "AI 엔지니어 신입", "company": "삼성리서치", "deadline": "2026-08-10", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "석사우대"]},
    {"title": "경영기획 담당자", "company": "현대자동차", "deadline": "2026-07-30", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸이상"]},
    {"title": "콘텐츠 마케터", "company": "무신사", "deadline": "2026-08-05", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "경력무관"]},
    {"title": "인사 담당자 (HR)", "company": "쿠팡", "deadline": "2026-07-15", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "재무회계 신입", "company": "롯데그룹", "deadline": "2026-08-20", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸이상"]},
    {"title": "UX 디자이너 신입", "company": "카카오", "deadline": "2026-07-28", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "영업 관리자", "company": "삼성전자", "deadline": "2026-08-12", "url": "https://www.work.go.kr", "tags": ["수원", "정규직", "대졸"]},
    {"title": "클라우드 엔지니어", "company": "KT클라우드", "deadline": "2026-07-22", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "콘텐츠 기획자", "company": "CJ ENM", "deadline": "2026-08-03", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "보안 엔지니어 신입", "company": "SK인포섹", "deadline": "2026-07-18", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸이상"]},
    {"title": "iOS 개발자", "company": "토스", "deadline": "2026-08-08", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "경력무관"]},
    {"title": "빅데이터 분석가", "company": "KT", "deadline": "2026-07-26", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "브랜드 마케터", "company": "아모레퍼시픽", "deadline": "2026-08-14", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "DevOps 엔지니어", "company": "배달의민족", "deadline": "2026-07-24", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸"]},
    {"title": "회계·세무 담당자", "company": "신한금융그룹", "deadline": "2026-08-18", "url": "https://www.work.go.kr", "tags": ["서울", "정규직", "대졸이상"]},
]


def search_jobs(keyword: str, count: int = 10) -> list:
    kw = keyword.lower()
    matched = [j for j in SAMPLE_DATA if kw in j["title"].lower() or kw in j["company"].lower()]
    result = matched if matched else SAMPLE_DATA
    return result[:count]
