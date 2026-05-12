"""Rule-based issue classifier for the MVP agent."""

from __future__ import annotations


ISSUE_KEYWORDS: dict[str, list[str]] = {
    "attendance": ["출석", "출석인정", "결석", "예비군", "훈련", "공결"],
    "leave_return": ["휴학", "복학", "질병휴학", "가사휴학", "군휴학"],
    "course_registration": ["수강신청", "폐강", "시간표", "장바구니", "매크로", "교과목 거래"],
    "certificate": ["증명서", "졸업예정증명서", "성적증명서", "재학증명서", "발급"],
    "graduation": ["졸업요건", "졸업", "이수학점", "요람", "전공필수", "전공선택"],
    "schedule": ["언제", "기간", "일정", "마감", "신청기간"],
    "contact": ["문의", "어디에", "어디로", "부서", "전화", "연락"],
    "military": ["예비군", "병무", "군", "훈련"],
    "student_support": ["학생증", "보험", "상담", "IT", "기숙사", "도서관"],
}


def classify_issue(query: str) -> dict:
    """Classify a user query into a campus-life issue type."""
    normalized = (query or "").lower()
    scores: dict[str, int] = {}
    for issue, keywords in ISSUE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in normalized)
        if score:
            scores[issue] = score

    if not scores:
        return {"issue_type": "other", "confidence": 0.0, "scores": {}}

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    issue_type, score = ranked[0]
    return {
        "issue_type": issue_type,
        "confidence": min(1.0, 0.35 + score * 0.2),
        "scores": scores,
    }

