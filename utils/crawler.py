import urllib.parse

# =====================================================================
# 실제 채용공고 시드 데이터 (2026년 6월 기준)
# 출처: 사용자 제공 보고서 (Indeed / 잡코리아 / 사람인 / 자소설닷컴 / 링커리어 /
#       대한치과위생사협회 / 유디덴탈잡 / 각 기관 채용 페이지 등에서 확인된 실제 공고)
# 주의: 정확한 접수 마감일과 세부 요건은 각 기관 채용 페이지에서 최종 확인 필요.
#       (그래서 deadline 대신 유형/지역/관련 자격증을 보여주고, '공고 보기'는 검색으로 연결)
#
# major 분류: "전기전자" / "컴퓨터" / "기계" / "치위생"
#   (컴퓨터 = 컴퓨터공학과 + 응용정보공학과 공통)
# =====================================================================

JOBS = [
    # ===================== 전기전자공학과 =====================
    {"company": "한국전력공사(KEPCO)", "title": "2026년도 상반기 대졸수준 신입사원 채용", "type": "신입 정규직", "location": "전국", "major": "전기전자", "certs": ["전기기사", "전기공사기사"], "note": "사무·배전·송변전·ICT·토목·건축·SW특화전형 등, 기사 자격가점"},
    {"company": "한국수력원자력(한수원)", "title": "2026년도 제1차 신입사원(대졸수준) 선발", "type": "신입 정규직", "location": "전국", "major": "전기전자", "certs": ["전기기사", "전기공사기사"], "note": "총 210명 (전기전자 직렬 포함), 쌍기사 우대"},
    {"company": "한국수력원자력(한수원)", "title": "2026년도 제1차 체험형 청년인턴 선발", "type": "인턴", "location": "전국", "major": "전기전자", "certs": ["전기기사"], "note": "체험형 청년인턴 별도 선발"},
    {"company": "한전MCS(주)", "title": "2026년 상반기 시니어계약직 신규채용", "type": "계약직", "location": "전국", "major": "전기전자", "certs": ["전기기사"], "note": "15명 모집"},
    {"company": "광명도시공사", "title": "2026년도 제1회 일반직 공개경쟁", "type": "신입", "location": "경기 광명", "major": "전기전자", "certs": ["전기기사"], "note": "시설행정(전기) 전기기사 이상 자격증 소지자"},
    {"company": "선그로우", "title": "신재생에너지 ESS 기술엔지니어", "type": "경력", "location": "경기 안양", "major": "전기전자", "certs": ["전기기사"], "note": "신재생에너지/ESS"},
    {"company": "(주)아이센스", "title": "2026년 상반기 대규모 채용", "type": "신입/경력", "location": "인천 연수", "major": "전기전자", "certs": ["전기기사", "전자기사"], "note": "바이오센서 제조"},
    {"company": "비원이티에스(주)", "title": "태양광발전설비 공무 담당", "type": "신입/경력", "location": "경남 창원", "major": "전기전자", "certs": ["전기기사"], "note": "신입 지원 가능"},
    {"company": "(주)신세계푸드", "title": "오산공장 공무관리(전기 및 공조냉동)", "type": "경력", "location": "경기 오산", "major": "전기전자", "certs": ["전기기사", "공조냉동기계기사"], "note": "설비 공무"},
    {"company": "예스맨파워", "title": "2026년 전기소방공사분야 채용", "type": "정규직", "location": "수도권", "major": "전기전자", "certs": ["전기공사기사", "소방설비기사(전기)"], "note": "전기공사기사 필수"},
    {"company": "(주)인코리아 프로페셔널", "title": "전기기사·전장설계 외 경력 채용", "type": "경력", "location": "서울 강남", "major": "전기전자", "certs": ["전기기사"], "note": "전장설계"},
    {"company": "대구광역시행복진흥사회서비스원", "title": "2026년 제5차 직원 채용", "type": "신입/경력", "location": "대구", "major": "전기전자", "certs": ["전기기사", "산업안전기사"], "note": "안전보건 관련 자격증 우대"},

    # ===================== 컴퓨터공학과 · 응용정보공학과 =====================
    {"company": "신한은행", "title": "2026년 디지털/ICT 수시채용", "type": "신입", "location": "서울", "major": "컴퓨터", "certs": ["정보처리기사", "SQLD"], "note": "뱅킹서비스 개발·AI 앱 엔지니어링·정보보호"},
    {"company": "코스콤", "title": "2026년 상반기 IT 신입직원 채용", "type": "신입", "location": "서울", "major": "컴퓨터", "certs": ["정보처리기사", "SQLD"], "note": "SW 개발/운용, IT 인프라"},
    {"company": "아마존웹서비시즈코리아(AWS)", "title": "[아마존] 2026 신입/인턴 채용", "type": "신입/인턴", "location": "서울", "major": "컴퓨터", "certs": ["AWS"], "note": "Professional Services 인턴, Solutions Architect Intern 등"},
    {"company": "AWS Korea", "title": "Cloud Support Associate / Associate Solutions Architect 신입사원", "type": "신입", "location": "서울", "major": "컴퓨터", "certs": ["AWS"], "note": "한국 근무, 클라우드"},
    {"company": "AWS Korea", "title": "Data Center Operations Trainee", "type": "채용연계형 트레이니", "location": "서울", "major": "컴퓨터", "certs": ["AWS"], "note": "데이터센터, 채용 연계"},
    {"company": "한국사회보장정보원", "title": "2026년 제2차 직원 채용", "type": "신입/경력", "location": "서울", "major": "컴퓨터", "certs": ["정보처리기사"], "note": "전산직, 정보처리기사 우대"},
    {"company": "한국전력기술(KEPCO-ENC)", "title": "2026년도 상반기 전산직 정규직 채용", "type": "신입 정규직", "location": "경북 김천", "major": "컴퓨터", "certs": ["정보처리기사"], "note": "전산 직렬"},
    {"company": "코난테크놀로지", "title": "2026년 각부문 신입 및 경력 채용", "type": "신입/경력", "location": "서울", "major": "컴퓨터", "certs": ["정보처리기사", "빅데이터분석기사"], "note": "AI/검색/데이터"},
    {"company": "파수", "title": "2026년 1차 신입 공개 채용", "type": "신입", "location": "서울", "major": "컴퓨터", "certs": ["정보처리기사", "정보보안기사"], "note": "데이터 보안 SW"},
    {"company": "신한은행", "title": "정보보호 분야 수시채용", "type": "신입", "location": "서울", "major": "컴퓨터", "certs": ["정보보안기사"], "note": "160명 규모, 자소서"},
    {"company": "토스뱅크", "title": "시스템보안/네트워크보안 수시채용", "type": "신입/경력", "location": "서울", "major": "컴퓨터", "certs": ["정보보안기사"], "note": "보안 직무"},
    {"company": "메가존클라우드", "title": "보안컨설턴트/기술영업 상시채용", "type": "상시", "location": "서울", "major": "컴퓨터", "certs": ["정보보안기사", "AWS"], "note": "클라우드 보안"},
    {"company": "(주)윈스테크넷", "title": "윈스 클라우드 시큐리티 스쿨(2기) 교육생 모집", "type": "교육생", "location": "부산 해운대", "major": "컴퓨터", "certs": ["정보보안기사"], "note": "보안 교육 → 채용 연계"},
    {"company": "대한소방공제회", "title": "경력·신입직원 채용", "type": "신입/경력", "location": "서울", "major": "컴퓨터", "certs": ["정보처리기사", "빅데이터분석기사", "정보보안기사"], "note": "데이터/IT 자격증 우대"},
    {"company": "(주)강원랜드", "title": "2026년 하계 성수기 기간제 근로자", "type": "기간제", "location": "강원 정선", "major": "컴퓨터", "certs": ["정보처리기사"], "note": "정보처리기사 우대"},

    # ===================== 기계공학과 =====================
    {"company": "안산도시공사", "title": "2026년 제1차 신규직원(일반직)", "type": "신입", "location": "경기 안산", "major": "기계", "certs": ["일반기계기사", "공조냉동기계기사"], "note": "일반기계기사·공조냉동기계산업기사 이상 우대"},
    {"company": "한국선급", "title": "2026년도 제1차 직원", "type": "신입/경력", "location": "부산", "major": "기계", "certs": ["일반기계기사"], "note": "일반기계기사 자격 필수"},
    {"company": "동국제강", "title": "인천공장 설비관리(기계) 부문 신입사원", "type": "신입", "location": "인천", "major": "기계", "certs": ["일반기계기사"], "note": "기계 전공·일반기계기사 우대"},
    {"company": "부산항만공사", "title": "정규직(경력) 및 체험형 청년인턴 채용", "type": "인턴/경력", "location": "부산", "major": "기계", "certs": ["일반기계기사"], "note": "생애 첫 인턴 체험형"},
    {"company": "남양유업(주)", "title": "2026년 신입사원 수시채용(영업/기계)", "type": "신입", "location": "경북 경주", "major": "기계", "certs": ["일반기계기사"], "note": "제조업 기계 직무"},
    {"company": "대구경북과학기술원(DGIST)", "title": "2026년도 제1차 일반직원(정규직) 공개채용", "type": "신입/경력", "location": "대구 달성", "major": "기계", "certs": ["일반기계기사", "공조냉동기계기사"], "note": "시설/기계 직렬"},
    {"company": "(주)삼건이엔씨", "title": "AI 데이터센터 냉동공조 엔지니어", "type": "경력", "location": "서울 강남", "major": "기계", "certs": ["공조냉동기계기사"], "note": "AI 데이터센터 냉동공조"},
    {"company": "(주)피앤에이코리아", "title": "2026년 공조냉동기계기사/기능사 채용", "type": "경력무관", "location": "경기 용인", "major": "기계", "certs": ["공조냉동기계기사"], "note": "신입 지원 가능"},
    {"company": "바른기술(주)", "title": "에너지기사 및 공조냉동기계 자격증 보유자 모집", "type": "신입/경력", "location": "경기 평택", "major": "기계", "certs": ["에너지관리기사", "공조냉동기계기사"], "note": "연봉 3,300만 원~"},
    {"company": "경인엔지니어링", "title": "기계설계 담당자 채용", "type": "경력", "location": "수도권", "major": "기계", "certs": ["일반기계기사"], "note": "기계설계, 연봉 3,000~4,000만 원"},
    {"company": "광명도시공사", "title": "시설행정(에너지) 채용", "type": "신입", "location": "경기 광명", "major": "기계", "certs": ["에너지관리기사"], "note": "에너지관리기사/산업기사"},
    {"company": "동원건설산업(주)", "title": "고려대 메디사이언스파크 시설관리(기계설비)", "type": "경력", "location": "서울", "major": "기계", "certs": ["에너지관리기사", "공조냉동기계기사"], "note": "3교대 시설관리"},
    {"company": "대한안전보건기술협회", "title": "산업안전 전문지도 컨설턴트", "type": "경력", "location": "광주", "major": "기계", "certs": ["산업안전기사"], "note": "안전관리 컨설팅"},

    # ===================== 치위생(학)과 =====================
    {"company": "경북대학교치과병원", "title": "2026년 제11차 청년인턴(진료지원-치과위생사)", "type": "청년인턴", "location": "대구 중구", "major": "치위생", "certs": ["치과위생사 면허"], "note": "공공기관 인턴, 정규직 전환 루트"},
    {"company": "경북대학교치과병원", "title": "2026년 제8차 청년인턴(진료지원-치과교정과)", "type": "청년인턴", "location": "대구 중구", "major": "치위생", "certs": ["치과위생사 면허"], "note": "신입 지원 가능, 4대보험"},
    {"company": "분당서울대학교병원", "title": "2026년도 치과 인턴 모집", "type": "인턴", "location": "경기 성남", "major": "치위생", "certs": ["치과위생사 면허"], "note": "대학병원 수련직"},
    {"company": "연세대학교의료원", "title": "세브란스·치과대학병원 수련직(레지던트/인턴) 채용", "type": "인턴/정규직", "location": "서울", "major": "치위생", "certs": ["치과위생사 면허"], "note": "수시 채용"},
    {"company": "서울대학교치과병원", "title": "치과위생사 채용 공고", "type": "수시", "location": "서울", "major": "치위생", "certs": ["치과위생사 면허"], "note": "수시 채용"},
    {"company": "건국대학교병원", "title": "[계약직] 치과 치과위생사 채용", "type": "계약직", "location": "서울", "major": "치위생", "certs": ["치과위생사 면허"], "note": "기술직"},
    {"company": "단국대학교 세종치과병원", "title": "2026년 6월 치과위생사 계약직 모집", "type": "계약직", "location": "충남 세종", "major": "치위생", "certs": ["치과위생사 면허"], "note": "2026년 6월 공고"},
    {"company": "부천사과나무치과병원", "title": "2026년 치과위생사 신입 공채 3기", "type": "신입 공채", "location": "경기 부천", "major": "치위생", "certs": ["치과위생사 면허"], "note": "경조사·건강검진·기숙사 지원, 야근 없음"},
    {"company": "김해 드림플란트치과병원", "title": "치위생사 신입 모집", "type": "신입", "location": "경남 김해", "major": "치위생", "certs": ["치과위생사 면허"], "note": "기숙사 지원, 웰컴키트"},
    {"company": "부산WS치과병원", "title": "2026년 신규 치위생사 채용", "type": "신입", "location": "부산", "major": "치위생", "certs": ["치과위생사 면허"], "note": "신규 채용"},
    {"company": "서울특별시 광진구", "title": "일반임기제공무원(치과위생사) 채용", "type": "임기제공무원", "location": "서울 광진", "major": "치위생", "certs": ["치과위생사 면허"], "note": "광진구 보건소 보건의료과"},
    {"company": "군산시 보건소 구강보건센터", "title": "구강보건사업팀 치과위생사 채용", "type": "정규", "location": "전북 군산", "major": "치위생", "certs": ["치과위생사 면허"], "note": "상시 인력 운영"},
    {"company": "행정안전부 정부서울청사", "title": "의무실 치위생사 채용", "type": "계약직", "location": "서울", "major": "치위생", "certs": ["치과위생사 면허"], "note": "나라일터 공고"},
    {"company": "오스템임플란트(주)", "title": "치위생 전공 영업·교육·연구 수시채용", "type": "수시", "location": "서울", "major": "치위생", "certs": ["치과위생사 면허", "병원코디네이터"], "note": "치과 토털 솔루션 기업"},
    {"company": "(주)디오", "title": "치위생 전공 연구·영업직 채용", "type": "신입/경력", "location": "부산", "major": "치위생", "certs": ["치과위생사 면허"], "note": "임플란트 제조·연구"},
]


def _norm(s):
    return (s or "").replace(" ", "")


def _major_key(major):
    """사용자 전공명 → 데이터셋 major 분류. 못 찾으면 None(=전체)."""
    m = _norm(major)
    if not m:
        return None
    if "치위생" in m or "치기공" in m:
        return "치위생"
    if "전기" in m or "전자" in m:
        return "전기전자"
    if "기계" in m:
        return "기계"
    if "컴퓨터" in m or "응용정보" in m or "소프트" in m or "정보" in m or "software" in m.lower():
        return "컴퓨터"
    return None


def _search_url(company):
    """정확한 공고 URL이 없으므로 사람인 검색 결과로 연결(실데이터 한계 반영)."""
    q = urllib.parse.quote(company)
    return f"https://www.saramin.co.kr/zf_user/search?searchword={q}"


def _match_keyword(job, kw):
    if not kw:
        return True
    hay = " ".join([
        job.get("title", ""), job.get("company", ""), job.get("type", ""),
        job.get("location", ""), job.get("note", ""),
        " ".join(job.get("certs", [])),
    ])
    return kw.replace(" ", "") in hay.replace(" ", "")


def search_jobs(keyword="", count=20, major=""):
    """전공 우선으로 채용공고를 반환.
    major가 있으면 같은 전공 공고만 우선, 그 안에서 keyword로 필터.
    keyword 결과가 없으면 keyword를 무시하고 해당 전공 전체를 보여줌."""
    mk = _major_key(major)
    pool = [j for j in JOBS if j["major"] == mk] if mk else list(JOBS)

    filtered = [j for j in pool if _match_keyword(j, keyword)]
    if not filtered:  # 키워드로 좁혔는데 0건이면 전공 전체로 폴백
        filtered = pool

    results = []
    for j in filtered[:count]:
        results.append({
            "title": j["title"],
            "company": j["company"],
            "type": j["type"],
            "location": j["location"],
            "tags": j.get("certs", []),
            "note": j.get("note", ""),
            "url": _search_url(j["company"]),
        })
    return results
