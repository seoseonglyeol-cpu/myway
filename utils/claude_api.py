import json
import anthropic
import streamlit as st

client = anthropic.Anthropic()

def call_claude(prompt: str, system: str = "") -> str:
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system if system else "당신은 대학생 취업 전문 AI 비서입니다. 한국어로 답변하세요.",
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"오류가 발생했어요: {str(e)}"

def analyze_spec(profile: dict) -> str:
    prompt = f"""
다음은 대학생의 취준 스펙입니다. 분석해주세요.

[기본 정보]
- 이름: {profile['name']}
- 학교: {profile['university']} {profile['grade']} {profile['major']}
- 목표 직무: {profile['target_job']}
- 목표 회사: {profile.get('target_company', '미정')}

[현재 스펙]
- 학점: {profile['gpa']} / 4.5
- 어학점수: {profile.get('english', '없음')}
- 보유 자격증: {profile.get('certificates', '없음')}
- 대외활동·인턴: {profile.get('activities', '없음')}

다음 형식으로 분석해주세요:

## 📊 준비도 분석
목표 직무({profile['target_job']}) 대비 현재 준비도를 퍼센트(%)로 표시하고 이유를 설명해주세요.

## ✅ 잘하고 있는 부분
현재 스펙에서 강점 3가지

## ⚠️ 부족한 부분
보완이 필요한 스펙 3가지 (구체적으로)

## 🏆 합격자 평균 스펙
{profile['target_job']} 직무 합격자들의 평균적인 스펙을 알려주세요.

## 💡 핵심 조언
가장 먼저 해야 할 일 1가지
"""
    return call_claude(prompt)

def generate_roadmap(profile: dict) -> str:
    prompt = f"""
{profile['name']}님의 취준 로드맵을 만들어주세요.

[정보]
- 목표 직무: {profile['target_job']}
- 학년: {profile['grade']}
- 현재 자격증: {profile.get('certificates', '없음')}
- 평일 {profile['weekday_hours']}시간, 주말 {profile['weekend_hours']}시간 공부 가능

다음 형식으로 작성해주세요:

## 🗺️ 단계별 로드맵

### 1단계 (지금 당장)
해야 할 일과 이유

### 2단계 (1~3개월)
해야 할 일과 이유

### 3단계 (3~6개월)
해야 할 일과 이유

### 4단계 (6개월 이후)
해야 할 일과 이유

## 🎯 필수 자격증 목록
{profile['target_job']}에 필요한 자격증 3~5개 (우선순위 순)

## 📌 인턴십·공모전 추천
지원하면 좋을 인턴십이나 공모전 종류
"""
    return call_claude(prompt)

def generate_schedule(profile: dict, target: str, deadline: str) -> str:
    prompt = f"""
{profile['name']}님의 맞춤 공부 스케줄을 만들어주세요.

[정보]
- 목표: {target}
- 마감일: {deadline}
- 평일 가능 시간: {profile['weekday_hours']}시간
- 주말 가능 시간: {profile['weekend_hours']}시간

다음 형식으로 작성해주세요:

## 📅 주차별 공부 계획

| 주차 | 기간 | 학습 내용 | 목표 분량 |
|------|------|----------|----------|
(표 형식으로 작성)

## 📚 추천 교재
1. (교재명) - (이유)
2. (교재명) - (이유)

## 🎥 추천 강의
1. (강의명/플랫폼) - 무료/유료 여부
2. (강의명/플랫폼) - 무료/유료 여부

## ⏰ 하루 공부 루틴
평일과 주말 각각 어떻게 공부하면 좋은지

## 💰 예상 총 비용
- 응시료: 원
- 교재비: 원
- 강의비: 원
- **총합: 원**
"""
    return call_claude(prompt)

def recommend_resources(profile: dict, subject: str) -> str:
    prompt = f"""
{profile['target_job']}를 목표로 하는 대학생에게 {subject} 관련 학습 리소스를 추천해주세요.

## 📚 추천 교재 (난이도별)

### 입문자용
- 교재명: 
- 특징: 
- 가격: 약 원

### 중급자용
- 교재명:
- 특징:
- 가격: 약 원

## 🎥 추천 강의

### 무료 강의
- 플랫폼/채널명:
- 강의명:
- 특징:

### 유료 강의
- 플랫폼:
- 강의명:
- 가격: 약 원
- 특징:

## 💡 공부 팁
{subject} 공부할 때 효율적인 방법 3가지
"""
    return call_claude(prompt)


def match_jobs(profile: dict, jobs: list) -> list:
    if not jobs:
        return []

    # 최대 10개만 분석 (프롬프트 길이 제한)
    target = jobs[:10]
    jobs_text = "\n".join([
        f"{i+1}. 제목: {j['title']} | 회사: {j['company']} | 내용: {j.get('description', '')}"
        for i, j in enumerate(target)
    ])

    prompt = f"""취준생 스펙과 채용공고를 비교해 매칭 분석해주세요.

[취준생 정보]
목표직무: {profile['target_job']} | 전공: {profile['major']} | 학년: {profile['grade']}
학점: {profile['gpa']}/4.5 | 어학: {profile.get('english', '없음')}
자격증: {profile.get('certificates', '없음')} | 활동: {profile.get('activities', '없음')}

[채용공고 {len(target)}개]
{jobs_text}

아래 JSON 배열만 출력하세요 (다른 텍스트, 마크다운 코드블록 없이):
[{{"index":1,"recommend":true,"possibility":"상","reason":"이유를 한 문장으로"}},...]

possibility는 반드시 상/중/하 중 하나."""

    raw = call_claude(prompt, system="JSON 배열만 출력하세요. ```json 같은 마크다운 없이 순수 JSON만.")

    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError
        matches = json.loads(raw[start:end])

        order = {"상": 0, "중": 1, "하": 2}
        result = []
        for m in matches:
            idx = m.get("index", 0) - 1
            if 0 <= idx < len(target):
                job = dict(target[idx])
                job["recommend"] = m.get("recommend", False)
                job["possibility"] = m.get("possibility", "중")
                job["reason"] = m.get("reason", "")
                result.append(job)

        result.sort(key=lambda x: order.get(x.get("possibility", "하"), 2))
        return result
    except Exception:
        for job in target:
            job.setdefault("recommend", False)
            job.setdefault("possibility", "중")
            job.setdefault("reason", "AI 분석을 불러오지 못했어요.")
        return target
