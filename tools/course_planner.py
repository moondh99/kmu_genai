"""Course planning MVP placeholder."""

from __future__ import annotations


def recommend_course_plan(interests: list[str], gaps: dict) -> list[str]:
    """Recommend a coarse course-plan direction from interests and graduation gaps."""
    recommendations = []
    if gaps.get("major_credit_gap", 0) > 0:
        recommendations.append("전공 부족 학점을 우선 채울 수 있는 전공선택/전공필수 과목을 확인하세요.")
    if gaps.get("total_credit_gap", 0) > 0:
        recommendations.append("총 졸업학점 부족분을 고려해 교양 또는 일반선택 과목을 함께 배치하세요.")
    if interests:
        recommendations.append(f"관심 분야({', '.join(interests)})와 관련된 강의계획서를 우선 비교하세요.")
    return recommendations or ["공식 요람과 수업시간표를 기준으로 다음 학기 계획을 확인하세요."]

