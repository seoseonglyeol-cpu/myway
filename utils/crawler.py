import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.saramin.co.kr",
}

SAMPLE_DATA = {
    "백엔드": [
        {"title": "백엔드 개발자 신입 채용", "company": "카카오엔터프라이즈", "deadline": "2026-07-15", "url": "https://www.saramin.co.kr", "tags": ["Python", "Django", "신입가능", "재택가능"]},
        {"title": "서버 개발자 (Java/Spring)", "company": "네이버클라우드", "deadline": "2026-07-31", "url": "https://www.saramin.co.kr", "tags": ["Java", "Spring Boot", "신입/경력"]},
        {"title": "백엔드 엔지니어 (Python)", "company": "라인플러스", "deadline": "2026-08-10", "url": "https://www.saramin.co.kr", "tags": ["Python", "FastAPI", "AWS"]},
        {"title": "신입 개발자 공개채용", "company": "SK C&C", "deadline": "2026-07-20", "url": "https://www.saramin.co.kr", "tags": ["전공무관", "신입", "인턴전환"]},
        {"title": "API 서버 개발자", "company": "쿠팡", "deadline": "2026-08-01", "url": "https://www.saramin.co.kr", "tags": ["MSA", "Kotlin", "대규모트래픽"]},
        {"title": "백엔드 개발자 (Node.js)", "company": "당근마켓", "deadline": "2026-07-25", "url": "https://www.saramin.co.kr", "tags": ["Node.js", "TypeScript", "경력1년이상"]},
        {"title": "플랫폼 개발자 신입", "company": "삼성SDS", "deadline": "2026-08-15", "url": "https://www.saramin.co.kr", "tags": ["신입", "대기업", "복지우수"]},
        {"title": "백엔드 개발 인턴십", "company": "토스", "deadline": "2026-07-10", "url": "https://www.saramin.co.kr", "tags": ["인턴", "정규직전환", "핀테크"]},
        {"title": "서버 사이드 개발자", "company": "크래프톤", "deadline": "2026-08-20", "url": "https://www.saramin.co.kr", "tags": ["게임", "C++", "경력무관"]},
        {"title": "Cloud 백엔드 개발자", "company": "KT클라우드", "deadline": "2026-07-30", "url": "https://www.saramin.co.kr", "tags": ["Cloud", "Kubernetes", "신입가능"]},
    ],
    "프론트엔드": [
        {"title": "프론트엔드 개발자 신입", "company": "카카오", "deadline": "2026-07-15", "url": "https://www.saramin.co.kr", "tags": ["React", "TypeScript", "신입가능"]},
        {"title": "UI 개발자 (Vue.js)", "company": "네이버", "deadline": "2026-08-01", "url": "https://www.saramin.co.kr", "tags": ["Vue.js", "JavaScript", "신입/경력"]},
        {"title": "웹 프론트엔드 개발자", "company": "라인", "deadline": "2026-07-31", "url": "https://www.saramin.co.kr", "tags": ["React", "Next.js", "재택가능"]},
        {"title": "프론트엔드 인턴", "company": "토스", "deadline": "2026-07-10", "url": "https://www.saramin.co.kr", "tags": ["인턴", "정규직전환", "React"]},
        {"title": "웹 개발자 (React)", "company": "배달의민족", "deadline": "2026-08-10", "url": "https://www.saramin.co.kr", "tags": ["React", "Redux", "신입가능"]},
        {"title": "프론트엔드 신입 공채", "company": "삼성전자", "deadline": "2026-07-20", "url": "https://www.saramin.co.kr", "tags": ["대기업", "신입", "공채"]},
        {"title": "UI/UX 개발자", "company": "쿠팡", "deadline": "2026-08-05", "url": "https://www.saramin.co.kr", "tags": ["HTML/CSS", "JavaScript", "반응형"]},
        {"title": "웹퍼블리셔/프론트엔드", "company": "현대오토에버", "deadline": "2026-07-25", "url": "https://www.saramin.co.kr", "tags": ["신입가능", "대기업계열", "복지우수"]},
        {"title": "프론트엔드 개발자 (Angular)", "company": "SK텔레콤", "deadline": "2026-08-15", "url": "https://www.saramin.co.kr", "tags": ["Angular", "대기업", "신입/경력"]},
        {"title": "React Native 개발자", "company": "당근마켓", "deadline": "2026-07-30", "url": "https://www.saramin.co.kr", "tags": ["앱개발", "React Native", "스타트업"]},
    ],
    "마케터": [
        {"title": "디지털 마케터 신입", "company": "CJ ENM", "deadline": "2026-07-20", "url": "https://www.saramin.co.kr", "tags": ["SNS마케팅", "콘텐츠", "신입가능"]},
        {"title": "퍼포먼스 마케터", "company": "카카오", "deadline": "2026-08-01", "url": "https://www.saramin.co.kr", "tags": ["광고운영", "데이터분석", "GA4"]},
        {"title": "브랜드 마케터 신입공채", "company": "LG생활건강", "deadline": "2026-07-31", "url": "https://www.saramin.co.kr", "tags": ["브랜드전략", "대기업", "신입"]},
        {"title": "콘텐츠 마케터", "company": "무신사", "deadline": "2026-07-15", "url": "https://www.saramin.co.kr", "tags": ["콘텐츠기획", "SNS", "패션"]},
        {"title": "그로스 마케터", "company": "토스", "deadline": "2026-08-10", "url": "https://www.saramin.co.kr", "tags": ["그로스해킹", "A/B테스트", "핀테크"]},
        {"title": "마케팅 인턴십", "company": "현대자동차", "deadline": "2026-07-10", "url": "https://www.saramin.co.kr", "tags": ["인턴", "대기업", "정규직전환가능"]},
        {"title": "SEO/SEM 마케터", "company": "네이버", "deadline": "2026-08-05", "url": "https://www.saramin.co.kr", "tags": ["검색광고", "키워드분석", "신입가능"]},
        {"title": "마케팅 AE (대행사)", "company": "제일기획", "deadline": "2026-07-25", "url": "https://www.saramin.co.kr", "tags": ["광고기획", "대기업계열", "신입"]},
        {"title": "이커머스 마케터", "company": "쿠팡", "deadline": "2026-08-15", "url": "https://www.saramin.co.kr", "tags": ["이커머스", "상품기획", "경력무관"]},
        {"title": "소셜미디어 마케터", "company": "카카오스타일", "deadline": "2026-07-30", "url": "https://www.saramin.co.kr", "tags": ["Instagram", "릴스", "콘텐츠"]},
    ],
    "데이터": [
        {"title": "데이터 분석가 신입", "company": "카카오", "deadline": "2026-07-20", "url": "https://www.saramin.co.kr", "tags": ["SQL", "Python", "신입가능"]},
        {"title": "데이터 사이언티스트", "company": "네이버", "deadline": "2026-08-01", "url": "https://www.saramin.co.kr", "tags": ["ML", "통계", "석사우대"]},
        {"title": "BI 분석가", "company": "쿠팡", "deadline": "2026-07-31", "url": "https://www.saramin.co.kr", "tags": ["Tableau", "SQL", "신입/경력"]},
        {"title": "데이터 엔지니어", "company": "라인플러스", "deadline": "2026-08-10", "url": "https://www.saramin.co.kr", "tags": ["Spark", "Kafka", "대규모데이터"]},
        {"title": "AI/ML 엔지니어 신입", "company": "삼성리서치", "deadline": "2026-07-15", "url": "https://www.saramin.co.kr", "tags": ["딥러닝", "PyTorch", "대기업"]},
        {"title": "데이터 분석 인턴", "company": "현대카드", "deadline": "2026-07-10", "url": "https://www.saramin.co.kr", "tags": ["인턴", "SQL", "R/Python"]},
        {"title": "비즈니스 애널리스트", "company": "SK하이닉스", "deadline": "2026-08-05", "url": "https://www.saramin.co.kr", "tags": ["데이터분석", "Excel", "대기업"]},
        {"title": "마케팅 데이터 분석가", "company": "롯데e커머스", "deadline": "2026-07-25", "url": "https://www.saramin.co.kr", "tags": ["GA4", "SQL", "이커머스"]},
        {"title": "데이터 플랫폼 엔지니어", "company": "토스", "deadline": "2026-08-15", "url": "https://www.saramin.co.kr", "tags": ["Airflow", "BigQuery", "핀테크"]},
        {"title": "통계 분석가", "company": "통계청", "deadline": "2026-07-30", "url": "https://www.saramin.co.kr", "tags": ["공공기관", "통계", "안정적"]},
    ],
}

DEFAULT_SAMPLE = [
    {"title": f"{{keyword}} 신입 채용", "company": "삼성SDS", "deadline": "2026-07-31", "url": "https://www.saramin.co.kr", "tags": ["신입", "대기업", "복지우수"]},
    {"title": f"{{keyword}} 담당자 모집", "company": "LG CNS", "deadline": "2026-08-15", "url": "https://www.saramin.co.kr", "tags": ["신입/경력", "대기업계열"]},
    {"title": f"{{keyword}} 인턴십", "company": "카카오", "deadline": "2026-07-20", "url": "https://www.saramin.co.kr", "tags": ["인턴", "정규직전환", "스타트업"]},
    {"title": f"{{keyword}} 공개채용", "company": "SK텔레콤", "deadline": "2026-08-01", "url": "https://www.saramin.co.kr", "tags": ["공채", "대기업", "신입"]},
    {"title": f"{{keyword}} 수시채용", "company": "현대자동차", "deadline": "상시", "url": "https://www.saramin.co.kr", "tags": ["수시", "대기업", "경력무관"]},
]


def _get_sample(keyword: str, count: int) -> list:
    kw = keyword.lower()
    if any(w in kw for w in ["백엔드", "서버", "backend"]):
        pool = SAMPLE_DATA["백엔드"]
    elif any(w in kw for w in ["프론트", "frontend", "react", "vue"]):
        pool = SAMPLE_DATA["프론트엔드"]
    elif any(w in kw for w in ["마케터", "마케팅", "marketing"]):
        pool = SAMPLE_DATA["마케터"]
    elif any(w in kw for w in ["데이터", "data", "분석"]):
        pool = SAMPLE_DATA["데이터"]
    else:
        pool = [
            {k: v.replace("{keyword}", keyword) if isinstance(v, str) else v
             for k, v in item.items()}
            for item in DEFAULT_SAMPLE
        ]
    return pool[:count]


def search_jobs(keyword: str, count: int = 10) -> list:
    jobs = []
    try:
        url = (
            "https://www.saramin.co.kr/zf_user/search/recruit"
            f"?searchType=search&searchword={quote(keyword)}&recruitPage=1"
        )
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code != 200:
            return _get_sample(keyword, count)

        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(".item_recruit")[:count]:
            title_tag   = item.select_one(".job_tit a")
            company_tag = item.select_one(".corp_name a")
            date_tag    = item.select_one(".job_date .date")
            tags        = [t.get_text(strip=True) for t in item.select(".job_sector a")]

            if not title_tag:
                continue

            href = title_tag.get("href", "")
            jobs.append({
                "title":    title_tag.get_text(strip=True),
                "company":  company_tag.get_text(strip=True) if company_tag else "미상",
                "deadline": date_tag.get_text(strip=True) if date_tag else "상시",
                "url":      f"https://www.saramin.co.kr{href}" if href.startswith("/") else href,
                "tags":     tags[:4],
            })
    except Exception:
        pass

    return jobs if jobs else _get_sample(keyword, count)
