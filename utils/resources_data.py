# 자격증별 실제 교재·강의 추천 데이터 (2026년 기준).
# 출처: 사용자 제공 보고서 (교보문고/인프런/Udemy/YouTube/각 출판사·학원 등 실제 정보).
# 주의: 가격/구성은 시기에 따라 바뀔 수 있으니 구매 전 최종 확인 필요.
#
# 스키마: STUDY_RESOURCES[키] = {
#   "label", "books":[{name,publisher,note}], "lectures":[{name,platform,price,note}],
#   "free":[str], "tip": str }

STUDY_RESOURCES = {
    "SQLD": {
        "label": "SQLD (SQL 개발자)",
        "books": [
            {"name": "2026 이지패스 SQLD", "publisher": "위키북스", "note": "SQL 초보자용 친절한 설명 (비전공자·입문)"},
            {"name": "2026 빠르게 따는 SQLD", "publisher": "골든래빗", "note": "2권 구성(이론+족보/기출/모의고사), 단기 합격"},
            {"name": "2026 이기적 SQLD 기본서", "publisher": "영진닷컴", "note": "동영상 강의 무료 + SQL 실습문제 (독학)"},
            {"name": "2026 박문각 SQLD 기출원스톱 400제", "publisher": "박문각", "note": "무료 YouTube 강의, 기출 중심"},
        ],
        "lectures": [
            {"name": "SQL 개발자(SQLD) 자격증 따기", "platform": "인프런", "price": "무료", "note": "환경설정~예제풀이 핵심만"},
            {"name": "2026 SQLD 무료 강의", "platform": "YouTube(박문각)", "price": "무료", "note": "핵심이론+실전모의고사 전 강의"},
            {"name": "노베이스도 한번에 합격하는 SQLD", "platform": "Udemy", "price": "유료", "note": "이론+모의고사 PDF 제공"},
            {"name": "SQLD 합격 패키지", "platform": "데이터에듀", "price": "유료", "note": "Live SQL 실습, 합격 시 응시료 5만원 지원"},
        ],
        "free": ["SQLD SQLP 문제은행(sqld.kr): 2026 MASTERBOOK 핵심요약 + 무한문제/모의고사 무료"],
        "tip": "난이도 ⭐⭐ · 준비 2~4주 · 교재비 2~2.5만원 · CBT 50문항/90분 · IT 전 직무 가산점. 입문이면 무료 강의로 시작해 기출 반복을 추천.",
    },
    "정보처리기사": {
        "label": "정보처리기사",
        "books": [
            {"name": "2026 시나공 정보처리기사 필기 기본서", "publisher": "길벗", "note": "157섹션 정리, QR 저자 직강 (필기 전체)"},
            {"name": "2026 시나공 정보처리기사 실기 총정리", "publisher": "길벗", "note": "실기 전용 총정리"},
            {"name": "2026 해커스 정보처리기사", "publisher": "해커스", "note": "인강+교재 단기 합격 (체계적)"},
        ],
        "lectures": [
            {"name": "정보처리기사 실기 단번에 합격", "platform": "인프런", "price": "유료", "note": "핵심+기출 완벽 정복, 수상 강의"},
            {"name": "흥달쌤 2026 정보처리기사", "platform": "N잡러", "price": "유료", "note": "필기+실기 합격 패키지"},
            {"name": "해커스 정보처리기사", "platform": "해커스자격증", "price": "유료", "note": "최대 300% 환급, 기출 무료 배포"},
            {"name": "알기사 정보처리기사", "platform": "지안에듀", "price": "유료", "note": "C언어 등 코딩 보충 강의 포함"},
        ],
        "free": [],
        "tip": "난이도 ⭐⭐⭐⭐ · 준비 2~4개월 · 3~3.5만원 · 필기 CBT + 실기 서술형 · 공기업/대기업 필수. 실기 합격률 10~20%로 낮고 신유형이 늘어 교재+강의 병행이 필수.",
    },
    "AWS": {
        "label": "AWS 자격증 (Cloud Practitioner)",
        "books": [
            {"name": "AWS Cloud Practitioner Essentials (한국어)", "publisher": "AWS Training", "note": "무료, 클라우드 개념·서비스·보안·요금 학습"},
            {"name": "AWS Skill Builder", "publisher": "AWS 공식", "note": "무료/유료, Exam Prep Plan 제공"},
            {"name": "Exam Prep Official Practice Question Set", "publisher": "AWS 공식", "note": "무료 공식 연습 문제 세트"},
        ],
        "lectures": [
            {"name": "AWS Certified Cloud Practitioner CLF-C02 (한글자막)", "platform": "Udemy(Stephane Maarek)", "price": "유료", "note": "최신 CLF-C02, 퀴즈·실습 포함"},
            {"name": "AWS Certified Cloud Practitioner 준비하기", "platform": "인프런(코드바나나)", "price": "유료", "note": "이론+실습+문제풀이"},
            {"name": "AWS Cloud Practitioner 모의고사 4회 (한국어)", "platform": "Udemy", "price": "유료", "note": "해설 포함 4회 모의고사"},
        ],
        "free": ["AWS Free Tier로 직접 실습하는 경험이 매우 중요"],
        "tip": "난이도 ⭐⭐ · 준비 2~4주 · 무료~2만원 · 상시 시험(피어슨뷰) · 글로벌 IT 우대. 암기형이 아니라 클라우드 이해도 평가 → CP로 구조 이해 후 Associate로 확장.",
    },
    "ADsP": {
        "label": "ADsP (데이터분석 준전문가)",
        "books": [
            {"name": "2026 ADsP 데이터분석 준전문가 (민트책)", "publisher": "데이터에듀", "note": "11년 베스트셀러, 기출 1~47회, 모의 3회+기출복원 18회, 앱 연동 (가장 인기)"},
            {"name": "2026 시나공 ADsP 기출문제의 재구성", "publisher": "길벗", "note": "기출 중심 재구성"},
        ],
        "lectures": [
            {"name": "데이터에듀 이론정복강의", "platform": "데이터에듀", "price": "교재포함", "note": "48시간 강의 요약, 16시간 무료 제공"},
            {"name": "에이치데이터랩 ADsP", "platform": "YouTube", "price": "무료", "note": "전체 커리큘럼 무료"},
            {"name": "해커스 2주 합격! ADsP", "platform": "해커스HRD", "price": "유료", "note": "단기 합격 집중 코스"},
        ],
        "free": [],
        "tip": "난이도 ⭐⭐⭐ · 준비 3~4주 · 2.5~3만원 · PBT 50문항 객관식 · 데이터 직무 가산점. 고정 문제 유형이 60% 이상이라 기출 유형 암기가 중요.",
    },
    "빅데이터분석기사": {
        "label": "빅데이터분석기사",
        "books": [
            {"name": "수제비 빅데이터분석기사 필기/실기", "publisher": "건기원", "note": "기출 분석 + 실기 작업형 대비"},
            {"name": "이기적 빅데이터분석기사 필기/실기", "publisher": "영진닷컴", "note": "동영상 강의 연계, 실기 파이썬/R"},
        ],
        "lectures": [
            {"name": "빅데이터분석기사 실기", "platform": "인프런", "price": "유료", "note": "파이썬 기반 작업형 실습"},
            {"name": "데이터에듀 빅데이터분석기사", "platform": "데이터에듀", "price": "유료", "note": "필기+실기 패키지"},
        ],
        "free": ["dataq.or.kr 공식 예시문항 + 파이썬/판다스 무료 강의(YouTube) 활용"],
        "tip": "ADsP→SQLD 이후 단계로 추천 · 실기는 파이썬(판다스/사이킷런) 코딩이 핵심 · 데이터 직무·공공기관 가산점.",
    },
    "전기기사": {
        "label": "전기기사",
        "books": [
            {"name": "2026 전기기사 필기 한권끝장 + 무료특강", "publisher": "에듀윌", "note": "200키워드 핵심 + 20회 기출, 베스트셀러 1위 (38,000원)"},
            {"name": "2026 전기기사 필기 기본서 시리즈(전7종)", "publisher": "김앤북(엔지니어랩)", "note": "KEC 최신 개정 반영, 한전 양성교재 채택"},
            {"name": "2026 전기기사 필기 5주완성", "publisher": "한솔아카데미", "note": "핵심포켓북 + 무료 동영상 강좌 (43,000원)"},
            {"name": "2026 해커스 전기기사 필기 한권완성", "publisher": "해커스자격증", "note": "기출 3개년 + CBT 모의고사 (과목별 23,000원)"},
        ],
        "lectures": [
            {"name": "엔지니어랩 (김상훈·조경필)", "platform": "엔지니어랩", "price": "유료", "note": "합격률 92%, 종로 오프라인 병행 가능"},
            {"name": "에듀윌 전기기사", "platform": "에듀윌", "price": "유료", "note": "KEC 개정 특강 무료, 대학생 5만원 할인"},
            {"name": "다산에듀 속전속결", "platform": "다산에듀", "price": "유료", "note": "오프라인 다산전기학원 병행"},
            {"name": "엔트미디어 무료강의", "platform": "ent1.co.kr", "price": "무료", "note": "도서별 무료 동영상 (유튜브/홈페이지)"},
        ],
        "free": ["엔트미디어(ent1.co.kr) 도서별 무료 동영상", "에듀윌 KEC 개정·CBT 복원 무료 특강"],
        "tip": "회로이론·전력공학 계산 비중이 높고 전기설비기술기준은 암기 중심. '이론 1 : 기출 3' 비율로 기출 최소 3회 반복하면 70점 안정권. 공기업이면 전기공사기사와 '쌍기사' 전략.",
    },
    "전기공사기사": {
        "label": "전기공사기사",
        "books": [
            {"name": "2026 전기공사(산업)기사 필기 기본서", "publisher": "김앤북(엔지니어랩)", "note": "전기응용 및 공사재료 등 과목별"},
            {"name": "2026 전기공사기사 실기", "publisher": "김앤북", "note": "KEC 최신 개정안 반영"},
        ],
        "lectures": [
            {"name": "엔지니어랩 종합 패키지", "platform": "엔지니어랩", "price": "유료", "note": "속전속결 종합 패키지(619,000원)"},
            {"name": "에듀윌 전기+공사 쌍기사", "platform": "에듀윌", "price": "유료", "note": "쌍기사 평생 패스 상품"},
            {"name": "다산에듀 필기 패키지", "platform": "다산에듀", "price": "유료", "note": "속전속결 필기 패키지(320,000원)"},
        ],
        "free": [],
        "tip": "전기기사와 묶어 '전기 쌍기사'로 준비하면 공기업 자격 가산점 2개 인정. 과목이 겹쳐 함께 준비하는 게 효율적.",
    },
    "소방설비기사": {
        "label": "소방설비기사 (전기/기계분야)",
        "books": [
            {"name": "소방설비기사 필기/실기 기본서", "publisher": "성안당/예문사 등", "note": "전기분야·기계분야 분리 선택"},
        ],
        "lectures": [
            {"name": "엔지니어랩 소방설비기사", "platform": "엔지니어랩", "price": "유료", "note": "전기분야/기계분야 과정 운영"},
            {"name": "모아바", "platform": "모아바", "price": "유료", "note": "소방/안전/전기/기계 분야 수강 만족도 1위"},
            {"name": "올배움(KISA)", "platform": "올배움", "price": "유료", "note": "다수 자격증 과정 운영"},
        ],
        "free": [],
        "tip": "전기전자·기계 공통 자격증. 소방 분야 취업을 진지하게 본다면 전기+기계 '소방 쌍기사'가 사실상 필수.",
    },
    "일반기계기사": {
        "label": "일반기계기사",
        "books": [
            {"name": "2026 해커스 일반기계기사 필기 한권합격", "publisher": "해커스자격증", "note": "실기 작업형 도면집과 세트 구성 가능"},
            {"name": "2026 스마트 7개년 과년도 일반기계기사 필기", "publisher": "성안당(허원회)", "note": "CBT 실전 모의고사 수록, 단기 합격용"},
            {"name": "2026 일반기계기사 실기(필답형+작업형)", "publisher": "구민사(김영기)", "note": "2차 실기 완전 분석"},
            {"name": "2026 일반기계기사 실기 필답형 과년도", "publisher": "명인북스", "note": "14개년(2011~2025) 상세풀이 (28,000원)"},
        ],
        "lectures": [
            {"name": "성안당 e러닝 (허원회)", "platform": "성안당", "price": "유료", "note": "기계분야 시그니처, 필기+실기 패키지"},
            {"name": "스터디채널 초단기", "platform": "스터디채널", "price": "유료", "note": "초단기 필기+실기 (321,500~462,000원)"},
            {"name": "올배움(KISA, 조형철)", "platform": "올배움", "price": "유료", "note": "실기 솔리드웍스&인벤터 인강"},
            {"name": "홍인 설계·디자인 원격학원", "platform": "홍인학원", "price": "유료", "note": "CBT 복원 PDF, 무료 오리엔테이션"},
        ],
        "free": ["홍인학원 무료 오리엔테이션 + 2024~2025 CBT 복원문제 PDF"],
        "tip": "4대 역학(재료·열·유체·동역학)이 기본. 작업형(CAD)은 솔리드웍스/인벤터 실습 필요. 공기업이면 공조냉동기계기사와 '쌍기사' 전략.",
    },
    "공조냉동기계기사": {
        "label": "공조냉동기계기사",
        "books": [
            {"name": "2026 공조냉동기계기사 필기 5주완성", "publisher": "한솔아카데미", "note": "2025부터 5→4과목 통폐합 반영"},
            {"name": "2026 에듀윌 공조냉동기계기사 필기 한권끝장", "publisher": "에듀윌", "note": "4과목 + 최신 8개년 기출, 무료특강"},
        ],
        "lectures": [
            {"name": "한솔아카데미", "platform": "한솔아카데미", "price": "유료", "note": "필기+실기 과정 운영"},
            {"name": "배울학 공조냉동기계기사", "platform": "배울학", "price": "유료", "note": "All in One 프리패스, 단기합격반"},
            {"name": "성안당 e러닝 (허원회)", "platform": "성안당", "price": "유료", "note": "개정 출제기준 반영 핵심이론"},
        ],
        "free": [],
        "tip": "2025년부터 출제기준이 5과목→4과목으로 통폐합 → 반드시 2026년판 교재를 사용. 데이터센터·시설관리 수요 증가로 활용도 높음.",
    },
    "에너지관리기사": {
        "label": "에너지관리기사",
        "books": [
            {"name": "에너지관리기사 필기/실기 기본서", "publisher": "성안당/한솔 등", "note": "보일러/열설비/시설관리 대비"},
        ],
        "lectures": [
            {"name": "올배움(KISA) 에너지관리기사", "platform": "올배움", "price": "유료", "note": "환급반, 평생학습보장반"},
            {"name": "배울학 2 in 1 공조 에너지", "platform": "배울학", "price": "유료", "note": "공조냉동과 병행 수강 가능"},
        ],
        "free": [],
        "tip": "기계설비법 도입으로 시설관리에서 급부상. 공조냉동기계기사와 함께 준비하면 시너지.",
    },
    "산업안전기사": {
        "label": "산업안전기사",
        "books": [
            {"name": "산업안전기사 필기/실기 기본서", "publisher": "성안당/예문사 등", "note": "안전관리/위험관리 대비"},
        ],
        "lectures": [
            {"name": "올배움(KISA, 최병환)", "platform": "올배움", "price": "유료", "note": "환급반, 평생학습보장반"},
            {"name": "에듀윌·해커스 산업안전기사", "platform": "에듀윌/해커스", "price": "유료", "note": "2026 대비 과정 운영"},
        ],
        "free": [],
        "tip": "제조·건설·시설 안전관리 직무에 두루 우대. 다른 기사와 묶어 안전 직무 경쟁력 강화 가능.",
    },
    "치과위생사": {
        "label": "치과위생사 국가시험 (국가면허)",
        "books": [
            {"name": "2026 파워 치과위생사 국가시험 핵심요약집", "publisher": "군자출판사", "note": "12년 최다 합격, 기출치트키 제공 (52,000원)"},
            {"name": "POWER 치과위생사 국가시험 예상문제집 1,2 + 심화", "publisher": "군자출판사", "note": "시간·장소 무관 학습 구성 (45,000원)"},
            {"name": "2026 치과위생학개론(제10판)", "publisher": "고문사", "note": "국시 기초이론 전공 교재"},
            {"name": "2026 치과보험 파워정복", "publisher": "군자출판사", "note": "치과보험 실무·시험 대비 (38,000원)"},
        ],
        "lectures": [
            {"name": "스마트에듀K (온라인)", "platform": "smarteduk.com", "price": "유료", "note": "실시간 피드백, 과목별 취약점 분석"},
            {"name": "대학 자체 국시 대비 프로그램", "platform": "소속 대학", "price": "무료", "note": "3~4학년 특강·모의시험 운영"},
            {"name": "기출유형문제집 + 무료 동영상 해설(QR)", "platform": "시중 교재", "price": "교재포함", "note": "독학용 QR 무료 해설 강의"},
        ],
        "free": ["대부분의 치위생(학)과에서 운영하는 자체 국시 대비 특강·모의시험 적극 활용"],
        "tip": "매년 12월 시행 · 필기 매과목 40%+총점 60% 이상, 실기 60% 이상 합격. 교재는 해당 연도 개정판(보통 2~3월 출간) 확인 후 구매.",
    },
    "치과보험청구사": {
        "label": "치과보험청구사",
        "books": [
            {"name": "2026 치과보험 파워정복", "publisher": "군자출판사", "note": "치과보험 청구 실무·시험 대비"},
        ],
        "lectures": [
            {"name": "대한치과경영관리자협회 주관 대비 과정", "platform": "협회/온라인", "price": "유료", "note": "협회 주관 시험 대비"},
        ],
        "free": [],
        "tip": "대형병원·치과의원 보험청구 전담 및 실장 승진에 유리. 치과위생사 면허와 함께 준비하면 실무 경쟁력 상승.",
    },
    "병원코디네이터": {
        "label": "병원코디네이터",
        "books": [
            {"name": "대한병원코디네이터협회 지정 교재", "publisher": "협회", "note": "환자상담·병원경영·마케팅"},
        ],
        "lectures": [
            {"name": "협회 온라인 자격시험 대비", "platform": "협회/온라인", "price": "유료", "note": "온라인 자격시험 응시 가능"},
        ],
        "free": [],
        "tip": "대형 치과병원 데스크·상담·경영지원 직무에 유리. 치과위생사 면허 + 코디네이터로 현장 경쟁력 강화.",
    },
}


def _norm(s):
    return (s or "").replace(" ", "").lower()


def get_resources(subject):
    """과목/자격증명으로 교재·강의 데이터를 찾는다(부분 일치). 없으면 None."""
    q = _norm(subject)
    if not q:
        return None
    # 더 구체적인(긴) 키부터 매칭해 오탐 방지
    for key in sorted(STUDY_RESOURCES, key=len, reverse=True):
        nk = _norm(key)
        if nk in q or q in nk:
            return STUDY_RESOURCES[key]
    return None


def list_certs():
    """등록된 자격증 라벨 목록."""
    return [v["label"] for v in STUDY_RESOURCES.values()]
