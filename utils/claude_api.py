from groq import Groq

client = Groq(api_key="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")

def call_ai(prompt, system="", max_tokens=2000):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system or "당신은 대학생 취업 전문 AI 비서입니다. 한국어로 답변하세요."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
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

def _fmt_courses(courses):
    """과목 리스트(딕셔너리)를 사람이 읽기 좋은 문자열로."""
    if not courses:
        return "없음"
    parts = []
    for c in courses:
        if isinstance(c, dict):
            imp = f", {c.get('importance')}" if c.get("importance") else ""
            parts.append(f"{c.get('name','')}({c.get('category','')}, {c.get('grade','-')}{imp})")
        else:
            parts.append(str(c))
    return ", ".join(parts)


def _fmt_major_track(track, label):
    if track and track.get("has"):
        return f"{label}: {track.get('field','')} ({track.get('credits','')}, {track.get('status','')})"
    return f"{label}: 없음"


def compare_with_senior(profile, senior):
    user_specs = f"""- 전공: {profile.get('major', '미입력')} / {profile.get('grade', '')}
- 학점: {profile.get('gpa', '미입력')} / 4.5
- 어학: {profile.get('english') or '없음'}
- 보유 자격증: {profile.get('certificates') or '없음'}
- 경험(인턴/대외활동): {profile.get('activities') or '없음'}
- 수강 과목: {_fmt_courses(profile.get('courses'))}
- {_fmt_major_track(profile.get('double_major'), '복수전공')}
- {_fmt_major_track(profile.get('minor'), '부전공')}"""

    senior_specs = f"""- 전공: {senior['major']}
- 학점: {senior['gpa']} / 4.5
- 어학: {senior['english']}
- 자격증: {', '.join(senior['certificates'])}
- 경험(인턴/대외활동): {', '.join(senior['activities'])}
- 수강 과목: {_fmt_courses(senior.get('courses'))}
- {_fmt_major_track(senior.get('doubleMajor'), '복수전공')}
- {_fmt_major_track(senior.get('minor'), '부전공')}
- 선배의 핵심 조언: {senior.get('keyAdvice', '')}
- 선배 추천 과목: {', '.join(senior.get('courseRecommendation', []))}"""

    target = f"{senior['company']} · {senior['job']}"

    from utils.certs import cert_guide_text
    cert_guide = cert_guide_text(profile.get("major", ""))
    cert_block = f"\n\n[전공 자격증 가이드]\n{cert_guide}" if cert_guide else ""

    system = f"""너는 대학생 취업 준비 갭 분석 전문가야.

[분석 대상]
- 사용자 스펙:
{user_specs}
- 롤모델 선배 스펙 ({target} 합격):
{senior_specs}
- 목표 회사/직무: {target}{cert_block}

[분석 항목 - 반드시 모두 포함]
1. 수강 과목 갭 분석
   - 선배가 들었는데 내가 안 들은 과목 목록
   - 그 중 "핵심" 중요도 과목은 ⚠️ 경고 표시
   - 각 미이수 과목에 대해: 왜 들어야 하는지 1줄 이유
   - 우선순위: 이번 학기 / 다음 학기 / 여유 시 구분
2. 학점 갭 분석
   - 전체 학점 비교 (선배 vs 나)
   - 핵심 과목별 학점 비교 (선배 A+ → 내가 B+ 이면 개선 필요 표시)
   - "이 회사는 학점 컷이 있으므로 최소 X.X 이상 필요" 판단
3. 자격증 갭 분석
   - 선배가 가진 자격증 중 내가 없는 것
   - 각 자격증의 취득 난이도와 예상 준비 기간
   - 우선순위 정렬
4. 복수전공/부전공 분석
   - 선배의 복수전공이 취업에 미친 영향 분석
   - 나도 해야 하는지 / 안 해도 되는지 판단
   - 대안 제시 (복수전공 대신 이런 자격증/과목으로 대체 가능)
5. 경험 갭 분석
   - 인턴/대외활동/프로젝트 비교
   - 부족한 경험 유형과 구체적 추천
6. 종합 액션 플랜
   - 남은 학기별 구체적 행동 계획
   - "이번 학기에 반드시 해야 할 3가지"
   - "다음 학기까지 완료해야 할 5가지"

[출력 형식 - 반드시 지킬 것]
- 맨 첫 줄에 정확히 이 형식으로 전체 준비 완성도를 써라: `완성도: NN%`
- 각 분석 항목은 반드시 다음 마크다운 제목으로 시작: `## 📚 수강 과목 갭 분석`, `## 📊 학점 갭 분석`, `## 📜 자격증 갭 분석`, `## 🎓 복수전공/부전공 분석`, `## 💼 경험 갭 분석`, `## 🎯 종합 액션 플랜`
- 긴급도를 🔴(즉시) 🟡(다음 학기) 🟢(여유) 로 항목 앞에 표시
- 실행 가능한 구체적 행동 위주로 작성
- 격려와 현실적 조언의 밸런스 유지
- 한국어로만 작성"""

    return call_ai("위 정보를 바탕으로 갭 분석을 작성해줘.", system=system, max_tokens=3500)

def recommend_resources(profile, subject):
    prompt = f"""{profile['target_job']}를 목표로 하는 대학생에게 {subject} 관련 학습 리소스를 추천해주세요.

## 추천 교재 (입문/중급)
## 추천 강의 (무료/유료)
## 공부 팁 3가지"""
    return call_ai(prompt)
