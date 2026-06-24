import json
import os
import re
from groq import Groq

_client = None

# 한국어 전용 지시어 (모든 호출 system 프롬프트에 자동 주입).
# 한자/중국어/일본어/러시아어/태국어 등은 금지하되, 자격증명·회사명 등 고유명사 영문은 허용.
KOREAN_ONLY = (
    " [CRITICAL RULE] 반드시 한국어(한글)만 사용하세요. "
    "절대로 중국어(漢字), 일본어, 러시아어, 태국어, 아랍어 등 "
    "다른 언어의 문자를 섞지 마세요. "
    "예시: 잘못된 것 '경험을积累합니다' → 올바른 것 '경험을 쌓습니다'; "
    "잘못된 것 '능력을展示할' → 올바른 것 '능력을 보여줄'; "
    "잘못된 것 '자격증을เตรียม합니다' → 올바른 것 '자격증을 준비합니다'. "
    "모든 답변은 100% 순수 한국어로 작성하세요. "
    "자격증명·회사명·기술용어 등 고유명사만 영문 그대로 둬도 됩니다."
)

# 모든 생성 프롬프트에 주입하는 간결성 지침 (정보 과부하 방지).
BRIEF = (
    " [간결하게 써라] 사용자는 긴 글을 읽기 싫어한다. "
    "각 항목은 한 줄짜리 글머리(- )로, 가장 중요한 키워드만 **굵게** 강조. "
    "미사여구·반복·당연한 설명은 빼고 핵심만. 한 섹션당 글머리 최대 3개. "
    "한 글머리는 한 문장(40자 내외)을 넘기지 마라."
)

# 중국어/일본어 문자 감지 (한글 AC00-D7A3은 제외). CJK 한자 + 가나.
_NON_KOREAN_CJK = re.compile(r"[぀-ヿㇰ-ㇿｦ-ﾟ㐀-䶿一-鿿]")


def clean_foreign_chars(text):
    """한글·영문·숫자 외 외국 문자(중국어/일본어/러시아어/태국어/아랍어)를 제거하는 최종 안전망."""
    if not text:
        return text
    # 중국어 간체/번체 + CJK 확장 A
    text = re.sub(r"[一-鿿㐀-䶿]", "", text)
    # 일본어 히라가나/카타카나 (전각·반각·확장 포함)
    text = re.sub(r"[぀-ゟ゠-ヿㇰ-ㇿｦ-ﾟ]", "", text)
    # 일본어 반복/장음 부호 등 (々〆〇ー)
    text = re.sub(r"[々〻〆〇]", "", text)
    # 러시아어/키릴 문자
    text = re.sub(r"[Ѐ-ӿ]", "", text)
    # 태국어
    text = re.sub(r"[฀-๿]", "", text)
    # 아랍어
    text = re.sub(r"[؀-ۿ]", "", text)
    # 연속 공백 정리 (줄바꿈/표 구조는 보존)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text

# LLaMA가 한국어에 자주 섞는 중국어/한자 → 한글 치환 (최종 안전망).
# 여러 글자 단어를 먼저 치환하도록 순서 유지.
_KOREANIZE = {
    "阶段": "단계", "階段": "단계", "成功": "성공", "积累": "축적", "積累": "축적",
    "经验": "경험", "經驗": "경험", "经력": "경력", "时间": "시간", "技术": "기술",
    "开发": "개발", "项目": "프로젝트", "学生": "학생", "能力": "능력", "优势": "강점",
    "现": "현", "現": "현", "年": "년", "的": "",
}


def koreanize(text):
    """남은 흔한 중국어/한자 잔재를 한글로 치환 후, 그 외 외국 문자는 제거.
    캐시된 결과를 렌더할 때도 호출되어 옛 결과까지 정리된다."""
    if not text:
        return text
    for k, v in _KOREANIZE.items():
        text = text.replace(k, v)
    return clean_foreign_chars(text)


def _get_api_key():
    """API 키를 st.secrets → 환경변수 순으로 안전하게 읽는다. 코드에 하드코딩하지 않음."""
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY", "")


def _get_client():
    """Groq 클라이언트를 지연 생성. 키가 없으면 None."""
    global _client
    if _client is None:
        key = _get_api_key()
        if not key:
            return None
        _client = Groq(api_key=key)
    return _client


def call_ai(prompt, system="", max_tokens=2000):
    client = _get_client()
    if client is None:
        return "API 키가 설정되지 않았어요. .streamlit/secrets.toml에 GROQ_API_KEY를 넣어주세요."
    base = system or "당신은 대학생 취업 전문 AI 비서입니다."

    def _run(extra="", temperature=0.5):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": base + KOREAN_ONLY + extra},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content

    try:
        out = _run()
        # 중국어/일본어 문자가 섞이면 더 강한 지시 + 낮은 temperature로 최대 3회 재시도
        attempts = 0
        while out and _NON_KOREAN_CJK.search(out) and attempts < 3:
            out = _run(
                " 앞선 답변에 한자/외국 문자가 섞였습니다. 단 하나의 한자도 쓰지 말고 모든 문자를 한글로만 다시 작성하세요.",
                temperature=0.0,
            )
            attempts += 1
        # 한자는 한글로 치환, 그 외 외국 문자는 제거 (koreanize 안에서 clean_foreign_chars 호출)
        return koreanize(out)
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

맨 첫 줄에 정확히 이 형식으로 목표 직무 대비 준비도를 써라: `완성도: NN%`

완성도 줄 바로 다음에 아래 요약 섹션을 만들어라. 가장 중요한 3가지를 '- ' 글머리로 한 문장씩, 핵심 키워드는 **굵게**:
## ⚡ 한눈에 요약

## 준비도 분석
위 완성도 퍼센트의 이유를 설명해주세요.

## 잘하고 있는 부분
현재 스펙에서 강점 3가지

## 부족한 부분
보완이 필요한 스펙 3가지

## 합격자 평균 스펙
{profile['target_job']} 직무 합격자들의 평균적인 스펙

## 핵심 조언
가장 먼저 해야 할 일 1가지"""
    return call_ai(prompt + BRIEF)

def generate_roadmap(profile, senior=None):
    """선배 롤모델 + 내 스펙 + 자격증 가이드/2026 시험 일정을 근거로 4단계 로드맵 생성."""
    user_specs = f"""- 전공: {profile.get('major', '미입력')} / {profile.get('grade', '')}
- 학점: {profile.get('gpa', '미입력')} / 4.5
- 어학: {profile.get('english') or '없음'}
- 보유 자격증: {profile.get('certificates') or '없음'}
- 경험(인턴/대외활동): {profile.get('activities') or '없음'}
- 수강 과목: {_fmt_courses(profile.get('courses'))}
- {_fmt_major_track(profile.get('double_major'), '복수전공')}
- 공부 가능 시간: 평일 {profile.get('weekday_hours', '-')}시간, 주말 {profile.get('weekend_hours', '-')}시간"""

    if senior:
        target = f"{senior['company']} · {senior['job']}"
        senior_block = f"""
[롤모델 선배 스펙 ({target} 합격)]
- 전공: {senior['major']} / 학점 {senior['gpa']}
- 자격증: {', '.join(senior['certificates'])}
- 경험: {', '.join(senior['activities'])}
- 핵심 조언: {senior.get('keyAdvice', '')}"""
    else:
        target = f"{profile.get('target_company') or '목표 기업'} · {profile.get('target_job', '목표 직무')}"
        senior_block = ""

    from utils.certs import cert_guide_text
    cert_guide = cert_guide_text(profile.get("major", ""))
    cert_block = f"\n\n[자격증 가이드 + 2026 시험 일정 (이 날짜에 맞춰 단계 배치)]\n{cert_guide}" if cert_guide else ""

    system = f"""너는 대학생 취업 로드맵 전문가야. 사용자의 현재 스펙과 롤모델 선배를 비교해, 목표까지 가는 단계별 로드맵을 만든다.

[사용자 스펙]
{user_specs}
{senior_block}
[목표] {target}{cert_block}

[작성 규칙]
- 맨 처음에 `## ⚡ 한눈에 요약` 섹션을 만들고, 가장 중요한 3가지를 '- ' 글머리로 한 문장씩 (핵심 키워드 **굵게**)
- 그 다음 반드시 아래 6개 섹션을 정확한 마크다운 제목으로 작성:
  `## 🚀 1단계 · 지금 당장`
  `## 📈 2단계 · 1~3개월`
  `## 🎯 3단계 · 3~6개월`
  `## 🏆 4단계 · 6개월 이후`
  `## 📜 추천 자격증 (우선순위)`
  `## 💼 인턴십·공모전 추천`
- 1~4단계는 각각 자격증/스킬/경험/취업준비 관점에서 구체적 행동 2~3개를 '- ' 글머리로 작성
- 선배 대비 부족한 부분을 우선 배치하고, 자격증은 2026 시험 일정에 맞춰 어느 단계에 딸지 명시
- 추천 자격증은 우선순위 순으로, 난이도와 예상 준비 기간 포함
- 실행 가능한 구체적 행동 위주, 격려와 현실적 조언의 균형
- 한국어로만 작성{BRIEF}"""

    return call_ai("위 정보를 바탕으로 단계별 로드맵을 작성해줘.", system=system, max_tokens=2800)

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
- 완성도 줄 다음에 `## ⚡ 한눈에 요약` 섹션을 만들고, 가장 중요한 3가지를 '- ' 글머리로 한 문장씩 (핵심 키워드 **굵게**)
- 그 다음 각 분석 항목은 반드시 다음 마크다운 제목으로 시작: `## 📚 수강 과목 갭 분석`, `## 📊 학점 갭 분석`, `## 📜 자격증 갭 분석`, `## 🎓 복수전공/부전공 분석`, `## 💼 경험 갭 분석`, `## 🎯 종합 액션 플랜`
- 긴급도를 🔴(즉시) 🟡(다음 학기) 🟢(여유) 로 항목 앞에 표시
- 실행 가능한 구체적 행동 위주로 작성
- 격려와 현실적 조언의 밸런스 유지
- 한국어로만 작성{BRIEF}"""

    return call_ai("위 정보를 바탕으로 갭 분석을 작성해줘.", system=system, max_tokens=3500)

def _extract_json(text):
    """AI 응답에서 JSON 객체만 안전하게 추출. 실패 시 None."""
    if not text:
        return None
    t = text.strip()
    # 코드펜스 제거
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t).strip()
    start, end = t.find("{"), t.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    chunk = t[start:end + 1]
    try:
        return json.loads(chunk)
    except Exception:
        # 후행 콤마 등 흔한 오류 1회 보정 시도
        fixed = re.sub(r",\s*([}\]])", r"\1", chunk)
        try:
            return json.loads(fixed)
        except Exception:
            return None


def generate_semester_plan(profile, senior, semester_info, sem_labels, gap_text=""):
    """선배 롤모델 + 내 스펙 + 시험 일정을 근거로 학기별 실행 계획(JSON)을 생성.
    sem_labels: [{"id","label"}] 남은 학기 목록(현재 학기부터, 달력 기준).
    반환: planner.py가 렌더하는 dict (overview/target/immediateActions/semesters). 실패 시 None."""
    user_specs = f"""- 전공: {profile.get('major', '미입력')} / {profile.get('grade', '')}
- 학점: {profile.get('gpa', '미입력')} / 4.5
- 어학: {profile.get('english') or '없음'}
- 보유 자격증: {profile.get('certificates') or '없음'}
- 경험(인턴/대외활동): {profile.get('activities') or '없음'}
- 수강 과목: {_fmt_courses(profile.get('courses'))}
- {_fmt_major_track(profile.get('double_major'), '복수전공')}
- {_fmt_major_track(profile.get('minor'), '부전공')}
- 목표 직무: {profile.get('target_job', '미정')}
- 목표 회사: {profile.get('target_company') or '미정'}"""

    senior_specs = f"""- 닉네임: {senior['nickname']}
- 전공: {senior['major']}
- 학점: {senior['gpa']} / 4.5
- 어학: {senior['english']}
- 자격증: {', '.join(senior['certificates'])}
- 경험: {', '.join(senior['activities'])}
- 수강 과목: {_fmt_courses(senior.get('courses'))}
- {_fmt_major_track(senior.get('doubleMajor'), '복수전공')}
- 선배 핵심 조언: {senior.get('keyAdvice', '')}
- 선배 추천 과목: {', '.join(senior.get('courseRecommendation', []))}"""

    target = f"{senior['company']} · {senior['job']}"
    max_credits = semester_info.get("maxCredits", 18)

    sem_list = "\n".join(f'  {i+1}. id="{s["id"]}", label="{s["label"]}"'
                         for i, s in enumerate(sem_labels))

    from utils.certs import cert_guide_text
    cert_guide = cert_guide_text(profile.get("major", ""))
    cert_block = f"\n\n[전공 자격증 가이드 + 2026 시험 일정 (이 날짜 기준으로 학기 배치)]\n{cert_guide}" if cert_guide else ""
    gap_block = f"\n\n[참고: 이미 수행된 AI 갭 분석 요약]\n{gap_text[:1500]}" if gap_text else ""

    system = f"""너는 대학생 취업 준비 학기 플래너 AI다. 사용자의 현재 스펙과 롤모델 선배의 합격 스펙을 비교해, 남은 학기 동안 무엇을 해야 하는지 학기별 실행 계획을 만든다.

[사용자 스펙]
{user_specs}

[롤모델 선배 스펙 ({target} 합격)]
{senior_specs}

[남은 학기 목록 (반드시 이 id/label 그대로 사용, 첫 학기 status는 "current")]
{sem_list}

[제약]
- 각 학기 수강 과목 학점 합계는 {max_credits}학점을 넘지 마라.
- 선배가 듣고 내가 안 들은 과목, 선배가 가졌고 내가 없는 자격증을 우선 배치하라.
- 자격증은 위 2026 시험 일정에 맞는 학기에 배치하라 (예: 8월 시험이면 그 직전 학기).
- urgency는 정확히 "critical", "high", "medium", "low" 중 하나만 사용.
- readinessBefore/After는 0~100 정수, 학기를 거치며 점진적으로 상승, 마지막 학기 After는 targetReadiness 근처.
- 모든 텍스트는 한국어. em dash(—) 쓰지 말 것.{cert_block}{gap_block}

[출력 형식 - 오직 아래 JSON 한 개만 출력. 설명/마크다운/코드펜스 금지]
{{
  "overview": {{"totalReadiness": 정수, "targetReadiness": 정수, "criticalGaps": 정수, "estimatedMonths": 정수}},
  "target": "{target}",
  "immediateActions": [
    {{"action": "이번 주에 할 구체적 행동", "deadline": "D-NN", "urgency": "critical|high|medium|low"}}
  ],
  "semesters": [
    {{
      "id": "위 목록의 id",
      "label": "위 목록의 label",
      "status": "current 또는 upcoming",
      "summary": "이 학기 한 줄 테마",
      "readinessBefore": 정수,
      "readinessAfter": 정수,
      "courses": [{{"name": "과목명", "category": "전공필수|전공선택|교양", "credits": 정수, "urgency": "...", "reason": "왜 이 학기에 듣는지 1줄"}}],
      "certifications": [{{"name": "자격증명", "difficulty": "하|중|중상|상", "prepMonths": 정수, "urgency": "...", "reason": "1줄 이유 (시험일 언급)"}}],
      "activities": [{{"type": "인턴|프로젝트|공모전|포트폴리오|취업준비", "name": "활동명", "period": "시기", "urgency": "...", "reason": "1줄"}}],
      "goals": ["이 학기 목표 1", "목표 2", "목표 3"]
    }}
  ]
}}
- immediateActions는 2~4개. semesters는 위 학기 목록과 동일한 개수.
- 마지막 학기는 보통 취업 지원/면접 준비 중심."""

    raw = call_ai("위 정보를 바탕으로 학기별 실행 계획 JSON을 생성해줘.", system=system, max_tokens=4000)
    return _extract_json(raw)


def recommend_resources(profile, subject):
    prompt = f"""{profile['target_job']}를 목표로 하는 대학생에게 {subject} 관련 학습 리소스를 추천해주세요.

## 추천 교재 (입문/중급)
## 추천 강의 (무료/유료)
## 공부 팁 3가지"""
    return call_ai(prompt)
