def search_jobs(keyword, count=10):
    sample_jobs = [
        {
            "title": f"{keyword} 신입 채용",
            "company": "카카오",
            "deadline": "2024.07.15",
            "url": "https://careers.kakao.com",
            "tags": ["서울", "정규직", "대졸"]
        },
        {
            "title": f"{keyword} 인턴십",
            "company": "네이버",
            "deadline": "2024.07.20",
            "url": "https://recruit.navercorp.com",
            "tags": ["성남", "인턴", "대졸"]
        },
        {
            "title": f"주니어 {keyword}",
            "company": "라인플러스",
            "deadline": "2024.07.31",
            "url": "https://careers.linecorp.com",
            "tags": ["서울", "정규직", "대졸"]
        },
        {
            "title": f"{keyword} 개발자 모집",
            "company": "쿠팡",
            "deadline": "2024.08.05",
            "url": "https://www.coupang.jobs",
            "tags": ["서울", "정규직", "무관"]
        },
        {
            "title": f"신입 {keyword} 채용공고",
            "company": "토스",
            "deadline": "2024.08.10",
            "url": "https://toss.im/career",
            "tags": ["서울", "정규직", "대졸"]
        },
        {
            "title": f"{keyword} 스타트업 채용",
            "company": "당근마켓",
            "deadline": "2024.08.15",
            "url": "https://team.daangn.com",
            "tags": ["서울", "정규직", "무관"]
        },
        {
            "title": f"{keyword} 경력/신입",
            "company": "배달의민족",
            "deadline": "2024.08.20",
            "url": "https://career.woowahan.com",
            "tags": ["서울", "정규직", "대졸"]
        },
        {
            "title": f"글로벌 {keyword} 채용",
            "company": "삼성전자",
            "deadline": "2024.09.01",
            "url": "https://www.samsung.com/careers",
            "tags": ["수원", "정규직", "대졸"]
        },
        {
            "title": f"{keyword} 공채",
            "company": "LG전자",
            "deadline": "2024.09.05",
            "url": "https://careers.lg.com",
            "tags": ["서울", "정규직", "대졸"]
        },
        {
            "title": f"{keyword} 수시채용",
            "company": "현대자동차",
            "deadline": "2024.09.10",
            "url": "https://talent.hyundai.com",
            "tags": ["서울", "정규직", "대졸"]
        },
    ]
    return sample_jobs[:count]
