# 🎯 마이웨이 (My Way)
> 대학생 AI 취준 비서 플랫폼

## 🚀 실행 방법

### 1. 패키지 설치
```bash
pip install streamlit anthropic requests beautifulsoup4
```

### 2. API 키 설정
```bash
export ANTHROPIC_API_KEY="여기에_API_키_입력"
```

### 3. 앱 실행
```bash
cd myway
streamlit run app.py
```

## 📁 프로젝트 구조
```
myway/
├── app.py              # 메인 앱
├── pages/
│   ├── onboarding.py   # 스펙 입력
│   ├── analysis.py     # 스펙 분석
│   ├── roadmap.py      # 로드맵
│   ├── schedule.py     # 공부 스케줄러
│   ├── resources.py    # 교재·강의 추천
│   └── cost.py         # 비용 계산기
└── utils/
    └── claude_api.py   # Claude API 연동
```

## 🛠️ 기술 스택
- Python
- Streamlit (프론트엔드)
- Claude API (AI 엔진)
- BeautifulSoup (크롤링)
