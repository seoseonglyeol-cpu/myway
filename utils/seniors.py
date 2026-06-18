# 데모용 가짜(seed) 선배 스펙 데이터.
# 실제 서비스에서는 설문/사용자 기여/외부 데이터로 교체 예정.
#
# 과목(courses) 스키마: {"name", "category", "grade", "importance"}
#   - category: 전공필수 / 전공선택 / 교양필수 / 교양선택 / 자유선택
#   - grade: A+, A0, B+, B0, C+, C0, D+, D0, F
#   - importance: 핵심 / 권장 / 일반

SENIORS = [
    # ===== 응용정보공학과 (사용자 학과) =====
    {
        "id": 1, "nickname": "민준 선배", "major": "응용정보공학과", "field": "IT/개발",
        "gpa": 3.8, "english": "토익 900",
        "company": "네이버", "job": "백엔드 개발자",
        "certificates": ["정보처리기사", "SQLD"],
        "activities": ["네이버 인턴 3개월", "교내 알고리즘 동아리", "오픈소스 컨트리뷰션"],
        "courses": [
            {"name": "정보프로그래밍기초", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "객체지향정보프로그래밍", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "응용자료구조", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "알고리즘응용", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "데이터베이스개론", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "응용정보컴퓨팅시스템", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "웹프로그래밍", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "정보SW공학", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "응용자료구조와 알고리즘응용은 반드시 A 이상 받으세요. 코딩테스트와 면접에서 직접 물어봅니다.",
        "courseRecommendation": ["응용자료구조", "알고리즘응용", "데이터베이스개론", "응용정보컴퓨팅시스템"],
    },
    {
        "id": 2, "nickname": "하은 선배", "major": "응용정보공학과", "field": "데이터",
        "gpa": 4.0, "english": "토익 920",
        "company": "쿠팡", "job": "데이터 분석가",
        "certificates": ["ADsP", "SQLD", "빅데이터분석기사"],
        "activities": ["데이터 분석 공모전 수상", "교내 데이터 학회", "쿠팡 인턴 2개월"],
        "courses": [
            {"name": "데이터분석개론", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "고급데이터분석", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "인공지능개론", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "응용자료구조", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "데이터베이스개론", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "인공지능기초수학", "category": "전공필수", "grade": "A0", "importance": "권장"},
            {"name": "시각정보분석", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "정보프로그래밍기초", "category": "전공필수", "grade": "A0", "importance": "권장"},
        ],
        "doubleMajor": {"has": True, "field": "응용통계학과", "credits": "42/42", "status": "완료"},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "데이터 직무는 'SQL+통계+분석 프로젝트'가 핵심이에요. 고급데이터분석에서 실데이터 프로젝트를 꼭 해보세요.",
        "courseRecommendation": ["데이터분석개론", "고급데이터분석", "인공지능개론", "시각정보분석"],
    },
    {
        "id": 3, "nickname": "준서 선배", "major": "응용정보공학과", "field": "스타트업",
        "gpa": 3.5, "english": "토익 830",
        "company": "토스(비바리퍼블리카)", "job": "백엔드 개발자",
        "certificates": ["정보처리기사", "SQLD"],
        "activities": ["스타트업 인턴 6개월", "사이드 프로젝트 2개 출시", "오픈소스 SW 동아리"],
        "courses": [
            {"name": "정보프로그래밍기초", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "응용자료구조", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "알고리즘응용", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "데이터베이스개론", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "응용정보컴퓨팅시스템", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "오픈소스SW응용", "category": "전공선택", "grade": "A+", "importance": "권장"},
            {"name": "정보SW공학", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "데이터분석개론", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": True, "field": "경영학", "credits": "21/21", "status": "이수중"},
        "keyAdvice": "스타트업은 실제로 배포한 프로젝트가 최고의 스펙이에요. 오픈소스SW응용에서 만든 걸 GitHub에 공개하세요.",
        "courseRecommendation": ["응용자료구조", "알고리즘응용", "데이터베이스개론", "오픈소스SW응용"],
    },

    {
        "id": 14, "nickname": "지안 선배", "major": "응용정보공학과", "field": "정보보안",
        "gpa": 3.7, "english": "토익 860",
        "company": "신한은행", "job": "정보보안 담당(디지털/ICT)",
        "certificates": ["정보처리기사", "정보보안기사", "리눅스마스터 2급"],
        "activities": ["금융보안 동아리", "CTF 보안대회 입상", "보안관제 인턴 3개월"],
        "courses": [
            {"name": "정보프로그래밍기초", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "응용자료구조", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "컴퓨터네트워크", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "정보보안개론", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "운영체제", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "시스템보안", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "암호학", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "데이터베이스개론", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "금융권 보안은 정보보안기사 + 실전 감각이 핵심이에요. CTF나 보안관제 인턴으로 실전 경험을 쌓고 네트워크·운영체제 기초를 단단히 하세요. 정보보안기사는 난이도가 높으니 일찍 시작하세요.",
        "courseRecommendation": ["정보보안개론", "시스템보안", "컴퓨터네트워크", "암호학"],
    },

    # ===== 컴퓨터과학 =====
    {
        "id": 4, "nickname": "서연 선배", "major": "컴퓨터과학과", "field": "IT/개발",
        "gpa": 4.1, "english": "오픽 IH",
        "company": "카카오", "job": "프론트엔드 개발자",
        "certificates": ["정보처리기사"],
        "activities": ["프론트엔드 부트캠프 수료", "개인 포트폴리오 사이트 5개", "사이드 프로젝트 출시"],
        "courses": [
            {"name": "컴퓨터프로그래밍", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "객체지향프로그래밍", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "자료구조", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "인터넷프로그래밍", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "인간과컴퓨터인터페이스", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "컴퓨터그래픽스", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "알고리즘분석", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "소프트웨어공학", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": True, "field": "산업디자인학과", "credits": "39/42", "status": "이수중"},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "프론트는 포트폴리오가 학점보다 중요해요. 인터넷프로그래밍에서 배운 걸로 실제 사이트를 3개 이상 배포하세요.",
        "courseRecommendation": ["인터넷프로그래밍", "인간과컴퓨터인터페이스", "객체지향프로그래밍", "알고리즘분석"],
    },
    {
        "id": 5, "nickname": "지후 선배", "major": "컴퓨터과학과", "field": "AI/ML",
        "gpa": 4.2, "english": "토익 920",
        "company": "네이버", "job": "AI/ML 엔지니어",
        "certificates": ["빅데이터분석기사", "TensorFlow Developer"],
        "activities": ["AI 논문 스터디", "캐글 메달 2개", "연구실 인턴 6개월"],
        "courses": [
            {"name": "인공지능", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "기계학습", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "딥러닝기초수학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "심층신경망", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "자연어처리", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "컴퓨터비전", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "자료구조", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "알고리즘분석", "category": "전공선택", "grade": "A0", "importance": "권장"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": True, "field": "수학", "credits": "21/21", "status": "완료"},
        "keyAdvice": "AI는 수학이 기본입니다. 딥러닝기초수학과 기계학습은 A+ 받고, 캐글이나 논문 구현으로 증명하세요.",
        "courseRecommendation": ["인공지능", "기계학습", "딥러닝기초수학", "심층신경망"],
    },
    {
        "id": 6, "nickname": "수아 선배", "major": "컴퓨터과학과", "field": "대기업",
        "gpa": 3.6, "english": "토익 850",
        "company": "삼성SDS", "job": "백엔드/클라우드 엔지니어",
        "certificates": ["정보처리기사", "AWS SAA", "SQLD"],
        "activities": ["삼성 SW 역량테스트 B형", "클라우드 스터디 운영", "교내 IT 봉사"],
        "courses": [
            {"name": "운영체제", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "컴퓨터네트워크", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "시스템프로그래밍", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "데이터베이스", "category": "전공선택", "grade": "B+", "importance": "핵심"},
            {"name": "자료구조", "category": "전공필수", "grade": "B+", "importance": "핵심"},
            {"name": "컴퓨터아키텍처", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "컴퓨터보안", "category": "전공선택", "grade": "B0", "importance": "권장"},
            {"name": "알고리즘분석", "category": "전공선택", "grade": "A0", "importance": "권장"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "백엔드는 OS·네트워크·DB 'CS 3대 과목'이 면접 핵심이에요. AWS 자격증으로 실무 감각을 보여주세요.",
        "courseRecommendation": ["운영체제", "컴퓨터네트워크", "시스템프로그래밍", "데이터베이스"],
    },

    # ===== 전기전자공학부 =====
    {
        "id": 7, "nickname": "도윤 선배", "major": "전기전자공학부", "field": "반도체",
        "gpa": 3.7, "english": "토익 870",
        "company": "삼성전자", "job": "반도체 회로설계",
        "certificates": ["반도체설계산업기사", "한국사능력검정 1급"],
        "activities": ["반도체 아카데미 수료", "산학협력 프로젝트", "교내 연구실 인턴"],
        "courses": [
            {"name": "기초회로이론", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "전자회로(1)", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "디지털논리회로", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "전자기학1", "category": "전공필수", "grade": "B+", "importance": "핵심"},
            {"name": "시스템반도체설계", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "신호및시스템", "category": "전공필수", "grade": "B+", "importance": "권장"},
            {"name": "디지털전자회로", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "물리전자", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "반도체는 전공 깊이가 핵심이에요. 전자회로와 디지털논리회로, 시스템반도체설계 학점을 꼭 챙기세요.",
        "courseRecommendation": ["기초회로이론", "전자회로(1)", "디지털논리회로", "시스템반도체설계"],
    },
    {
        "id": 8, "nickname": "유나 선배", "major": "전기전자공학부", "field": "공기업",
        "gpa": 3.6, "english": "토익 780",
        "company": "한국전력공사", "job": "전기직",
        "certificates": ["전기기사", "한국사능력검정 1급"],
        "activities": ["NCS 스터디 1년", "전기 관련 봉사활동", "공기업 취업 동아리"],
        "courses": [
            {"name": "기초회로이론", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "전력공학", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "전자기학1", "category": "전공필수", "grade": "B+", "importance": "핵심"},
            {"name": "신호및시스템", "category": "전공필수", "grade": "A0", "importance": "권장"},
            {"name": "제어공학", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "디지털논리회로", "category": "전공필수", "grade": "A0", "importance": "권장"},
            {"name": "전기전자재료", "category": "전공선택", "grade": "A0", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "전기기사는 공기업 전기직의 필수예요. NCS와 전공 필기(회로·전력)를 병행 준비하세요.",
        "courseRecommendation": ["기초회로이론", "전력공학", "전자기학1", "제어공학"],
    },

    {
        "id": 15, "nickname": "건우 선배", "major": "전기전자공학부", "field": "신재생에너지",
        "gpa": 3.5, "english": "토익 800",
        "company": "선그로우(Sungrow)", "job": "신재생에너지 ESS 엔지니어",
        "certificates": ["전기기사", "전기공사기사"],
        "activities": ["태양광 발전 산학 프로젝트", "전기 동아리", "신재생에너지 기업 인턴 3개월"],
        "courses": [
            {"name": "기초회로이론", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "전력공학", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "전력전자", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "제어공학", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "전자기학1", "category": "전공필수", "grade": "B+", "importance": "핵심"},
            {"name": "에너지변환공학", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "신호및시스템", "category": "전공필수", "grade": "B+", "importance": "권장"},
            {"name": "디지털논리회로", "category": "전공필수", "grade": "A0", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "신재생/ESS는 전력공학·전력전자가 핵심이에요. 전기기사+전기공사기사 쌍기사를 갖추고 태양광·ESS 산학 프로젝트로 실무 경험을 보여주세요.",
        "courseRecommendation": ["전력공학", "전력전자", "제어공학", "에너지변환공학"],
    },

    # ===== 기계공학 =====
    {
        "id": 9, "nickname": "시우 선배", "major": "기계공학부", "field": "대기업",
        "gpa": 3.7, "english": "토익 840",
        "company": "LG전자", "job": "기구설계 엔지니어",
        "certificates": ["일반기계기사", "3D프린팅운용기능사"],
        "activities": ["사내 캡스톤 산학과제", "자작 자동차 동아리", "현대차 인턴 2개월"],
        "courses": [
            {"name": "고체역학", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "열역학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "유체역학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "동역학", "category": "전공필수", "grade": "B+", "importance": "핵심"},
            {"name": "기계요소설계", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "컴퓨터응용기계설계", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "기계공학실험(1)", "category": "전공필수", "grade": "A0", "importance": "권장"},
            {"name": "생산공학", "category": "전공선택", "grade": "B+", "importance": "권장"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "기구설계는 '4대 역학 + CAD'가 기본이에요. 컴퓨터응용기계설계로 3D 모델링 포트폴리오를 만드세요.",
        "courseRecommendation": ["고체역학", "기계요소설계", "컴퓨터응용기계설계", "동역학"],
    },

    {
        "id": 16, "nickname": "재윤 선배", "major": "기계공학부", "field": "발전/공기업",
        "gpa": 3.6, "english": "토익 820",
        "company": "한국남부발전", "job": "기계직",
        "certificates": ["일반기계기사", "공조냉동기계기사", "한국사능력검정 1급"],
        "activities": ["NCS 스터디 1년", "발전공기업 취업 동아리", "기계설비 현장 실습"],
        "courses": [
            {"name": "고체역학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "열역학", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "유체역학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "열전달", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "동역학", "category": "전공필수", "grade": "B+", "importance": "핵심"},
            {"name": "기계요소설계", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "유체기계", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "발전공학", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "발전·공기업 기계직은 '쌍기사(일반기계+공조냉동)' + NCS가 기본이에요. 4대 역학 학점을 챙기고 열전달·유체기계로 발전설비 이해를 보여주세요.",
        "courseRecommendation": ["열역학", "열전달", "유체역학", "유체기계"],
    },
    {
        "id": 17, "nickname": "한별 선배", "major": "기계공학부", "field": "시설/데이터센터",
        "gpa": 3.4, "english": "토익 760",
        "company": "삼건이엔씨", "job": "데이터센터 냉동공조 엔지니어",
        "certificates": ["공조냉동기계기사", "에너지관리기사"],
        "activities": ["건물 기계설비 인턴 4개월", "HVAC 설계 스터디", "캡스톤 공조 설계 프로젝트"],
        "courses": [
            {"name": "열역학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "열전달", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "공조냉동공학", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "유체역학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "유체기계", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "기계요소설계", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "자동제어", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "에너지시스템공학", "category": "전공선택", "grade": "A0", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "AI 데이터센터·시설 분야는 공조냉동기계기사+에너지관리기사가 강력해요. 공조냉동공학·열전달을 챙기고 HVAC 설계 프로젝트로 실무를 보여주세요.",
        "courseRecommendation": ["공조냉동공학", "열전달", "유체기계", "에너지시스템공학"],
    },

    # ===== 치위생학과 (단국대) =====
    {
        "id": 10, "nickname": "지원 선배", "major": "치위생학과", "field": "의료/임상",
        "gpa": 3.9, "english": "토익 720",
        "company": "연세대학교치과병원", "job": "치과위생사",
        "certificates": ["치과위생사 면허", "BLS(기본소생술)", "의료 코디네이터"],
        "activities": ["치과병원 임상 실습 6개월", "구강보건 봉사단", "대한치과위생사협회 세미나 참여"],
        "courses": [
            {"name": "치위생학1", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "치위생학실습1", "category": "전공필수", "grade": "A+", "importance": "핵심"},
            {"name": "임상치위생학실습1", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "구강해부학", "category": "전공기초", "grade": "A0", "importance": "핵심"},
            {"name": "구강생리학", "category": "전공기초", "grade": "B+", "importance": "권장"},
            {"name": "치과방사선학", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "치과임상학1(보존,소치)", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "치아형태학", "category": "전공기초", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "임상은 전문 술기 능력 + 환자와의 의사소통 능력을 함께 봐요. 치위생학실습·임상치위생학실습 학점과 병원 실습 경험이 핵심이고, 면허는 기본입니다.",
        "courseRecommendation": ["치위생학실습1", "임상치위생학실습1", "치과방사선학", "구강해부학"],
    },
    {
        "id": 11, "nickname": "민서 선배", "major": "치위생학과", "field": "공공/보건",
        "gpa": 3.8, "english": "토익 750",
        "company": "보건소(지자체)", "job": "치위생 보건직",
        "certificates": ["치과위생사 면허", "보건교육사 3급"],
        "activities": ["보건소 실습", "지역사회 구강보건 캠페인", "공공기관 취업 스터디", "대한치과위생사협회 보수교육 이수"],
        "courses": [
            {"name": "공중보건학", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "지역사회구강보건학", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "구강보건교육학", "category": "전공필수", "grade": "A0", "importance": "핵심"},
            {"name": "보건통계학", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "보건의료법규", "category": "전공선택", "grade": "A0", "importance": "권장"},
            {"name": "치위생윤리", "category": "전공필수", "grade": "B+", "importance": "권장"},
            {"name": "디지털치위생관리", "category": "전공선택", "grade": "B+", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "공공기관은 공중보건학·지역사회구강보건학 같은 사회치위생 과목이 핵심이에요. 보건직 공무원 시험도 병행 준비하세요.",
        "courseRecommendation": ["공중보건학", "지역사회구강보건학", "구강보건교육학", "보건통계학"],
    },
    {
        "id": 12, "nickname": "하늘 선배", "major": "치위생학과", "field": "의료기업",
        "gpa": 3.7, "english": "토익 800",
        "company": "오스템임플란트", "job": "임상지원/교육 직무",
        "certificates": ["치과위생사 면허", "치과방사선 안전관리", "컴퓨터활용능력 1급"],
        "activities": ["치과 의료기기 기업 인턴", "임플란트 임상 세미나 참여", "캡스톤 산학 프로젝트"],
        "courses": [
            {"name": "치과임상학4(외과,임플란트)", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "치과임상학3(교정,보철)", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "첨단치과생체재료학", "category": "전공선택", "grade": "A0", "importance": "핵심"},
            {"name": "치과의료관리학", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "임상치위생학실습2", "category": "전공필수", "grade": "A0", "importance": "권장"},
            {"name": "스마트건강보험실무", "category": "전공선택", "grade": "B+", "importance": "권장"},
            {"name": "캡스톤디자인1(치위생)", "category": "전공선택", "grade": "A0", "importance": "일반"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "임플란트/의료기기 기업은 임상 지식 + 제품 교육 역량이 차별점이에요. 치과임상학·생체재료학을 챙기세요.",
        "courseRecommendation": ["치과임상학4(외과,임플란트)", "첨단치과생체재료학", "치과임상학3(교정,보철)", "치과의료관리학"],
    },
    {
        "id": 13, "nickname": "예린 선배", "major": "치위생학과", "field": "연구/교육",
        "gpa": 4.2, "english": "토익 880",
        "company": "치위생 대학원 / 연구소", "job": "연구·교육직 (대학원 진학)",
        "certificates": ["치과위생사 면허", "보건교육사 2급"],
        "activities": ["학부 연구생 1년", "치위생 연구방법론 학회 발표", "캡스톤 우수상", "대학원 진학(석사)"],
        "courses": [
            {"name": "치위생연구방법론", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "보건통계학", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "구강병리학", "category": "전공기초", "grade": "A0", "importance": "핵심"},
            {"name": "치위생학연구(캡스톤디자인2)", "category": "전공선택", "grade": "A+", "importance": "핵심"},
            {"name": "영양생화학", "category": "전공기초", "grade": "A0", "importance": "권장"},
            {"name": "구강미생물학", "category": "전공기초", "grade": "A0", "importance": "권장"},
            {"name": "지역사회구강보건학", "category": "전공선택", "grade": "B+", "importance": "권장"},
        ],
        "doubleMajor": {"has": False, "field": "", "credits": "", "status": ""},
        "minor": {"has": False, "field": "", "credits": "", "status": ""},
        "keyAdvice": "연구·교육 진로는 학점과 연구 경험이 핵심이에요. 치위생연구방법론·보건통계학을 챙기고 학부 연구생으로 논문 경험을 쌓은 뒤 대학원에 진학하세요.",
        "courseRecommendation": ["치위생연구방법론", "보건통계학", "구강병리학", "치위생학연구(캡스톤디자인2)"],
    },
]


def _norm(s):
    return (s or "").replace(" ", "")


def _major_match(user_major, senior):
    """전공이 같은(또는 거의 같은) 선배인지."""
    um, sm = _norm(user_major), _norm(senior["major"])
    return bool(um and sm and (um in sm or sm in um))


def match_seniors(profile):
    """전공 우선으로 선배를 매칭. 같은 전공 선배가 있으면 그들만,
    없으면 직무/회사 매칭으로 폴백, 그래도 없으면 전체."""
    target_job = (profile.get("target_job") or "").strip()
    target_company = (profile.get("target_company") or "").strip()
    user_major = profile.get("major") or ""

    def jc_score(senior):
        s = 0
        if target_job:
            tj, sj = _norm(target_job), _norm(senior["job"])
            if tj and (tj in sj or sj in tj):
                s += 3
            elif any(tok and tok in sj for tok in target_job.split()):
                s += 2
        if target_company:
            companies = [c.strip() for c in target_company.replace(",", " ").split() if c.strip()]
            if any(c and (c in senior["company"] or senior["company"] in c) for c in companies):
                s += 2
        return s

    # 1순위: 같은 전공 선배 (직무/회사 점수로 정렬)
    major_matched = [s for s in SENIORS if _major_match(user_major, s)]
    if major_matched:
        return sorted(major_matched, key=jc_score, reverse=True)

    # 2순위: 직무/회사 매칭
    scored = sorted(SENIORS, key=jc_score, reverse=True)
    jc_matched = [s for s in scored if jc_score(s) > 0]
    return jc_matched if jc_matched else scored


def get_senior(senior_id):
    for s in SENIORS:
        if s["id"] == senior_id:
            return s
    return None
