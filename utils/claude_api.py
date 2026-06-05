from groq import Groq

client = Groq(api_key="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")

def call_ai(prompt, system=""):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system or "당신은 대학생 취업 전문 AI 비서입니다. 한국어로 답변하세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했어요: {str(e)}"

def analyze_spec(profile):
    prompt = f"""다음은 대학생의 취준 스펙입니다. 분석해주세요.

[기본 정보]
- 이름: {profile['name']}
- 학교: {profile['university']} {profile['grade']} {profile['major']}
- 목표 직무: {profile['target_job']}
- 목표 회사: {profile.get('target_company', '미정')}

[현재 스펙]
- 학점: {profile['gpa']} / 4.5
- 어학점수: {profile.get('english', '없음')}
- 보유 자격증: {profile.get('certificates', '없음')}
- 대외활동/인턴: {profile.get('activities', '없음')}

다음 형식으로 분석해주세요:

## 준비도 분석
목표 직무 대비 현재 준비도를 퍼센트로 표시하고 이유를 설명해주세요.

## 잘하고 있는 부분
현재 스펙에서 강점 3가지

## 부족한 부분
보완이 필요한 스펙 3가지

## 합격자 평균 스펙
{profile['target_job']} 직무 합격자들의 평균적인 스펙

## 핵심 조언
가장 먼저 해야 할 일 1가지"""
    return call_ai(prompt)

def generate_roadmap(profile):
    prompt = f"""{profile['name']}님의 취준 로드맵을 만들어주세요.

- 목표 직무: {profile['target_job']}
- 학년: {profile['grade']}
- 현재 자격증: {profile.get('certificates', '없음')}
- 평일 {profile['weekday_hours']}시간, 주말 {profile['weekend_hours']}시간 공부 가능

한국어만 사용해주세요. 다른 언어(중국어, 태국어 등) 절대 섞지 마세요.
각 단계별로 구체적인 행동을 3가지씩 제시해주세요.

## 단계별 로드맵
### 1단계 (지금 당장)
### 2단계 (1~3개월)
### 3단계 (3~6개월)
### 4단계 (6개월 이후)
## 필수 자격증 목록 (우선순위 순)
## 인턴십/공모전 추천"""
    return call_ai(prompt)

def generate_schedule(profile, target, deadline):
    prompt = f"""{profile['name']}님의 맞춤 공부 스케줄을 만들어주세요.

- 목표: {target}
- 마감일: {deadline}
- 평일 가능 시간: {profile['weekday_hours']}시간
- 주말 가능 시간: {profile['weekend_hours']}시간

## 주차별 공부 계획
| 주차 | 학습 내용 | 목표 분량 |
|------|----------|----------|

## 추천 교재
## 추천 강의
## 하루 공부 루틴
## 예상 총 비용"""
    return call_ai(prompt)

def recommend_resources(profile, subject):
    prompt = f"""{profile['target_job']}를 목표로 하는 대학생에게 {subject} 관련 학습 리소스를 추천해주세요.

## 추천 교재 (입문/중급)
## 추천 강의 (무료/유료)
## 공부 팁 3가지"""
    return call_ai(prompt)
