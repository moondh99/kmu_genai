"""Graduation audit MVP placeholder."""

from __future__ import annotations


def audit_graduation_requirements(student_summary: dict, requirements: dict | None = None) -> dict:
    """Audit graduation requirements from user-provided non-sensitive summaries."""
    requirements = requirements or {"total_credits": 130, "major_credits": 60}
    total = int(student_summary.get("total_credits", 0))
    major = int(student_summary.get("major_credits", 0))
    return {
        "total_credit_gap": max(0, requirements["total_credits"] - total),
        "major_credit_gap": max(0, requirements["major_credits"] - major),
        "note": "MVP 데모용 진단입니다. 실제 졸업 판정은 요람, 학과 기준, 교무팀/학과사무실 확인이 필요합니다.",
    }

