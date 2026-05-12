"""Safety guardrails for privacy, unsupported sources, and grounded answers."""

from __future__ import annotations

import re
from dataclasses import dataclass


PRIVACY_PATTERNS = {
    "student_id": re.compile(r"\b20\d{6,8}\b|학번", re.IGNORECASE),
    "resident_number": re.compile(r"\d{6}-\d{7}|주민"),
    "portal_password": re.compile(r"비밀번호|패스워드|password|pw", re.IGNORECASE),
    "grade_report": re.compile(r"성적표|성적|평점|gpa", re.IGNORECASE),
    "phone": re.compile(r"01[016789]-?\d{3,4}-?\d{4}|연락처|전화번호"),
}


@dataclass(frozen=True)
class GuardResult:
    """Result of a safety inspection."""

    blocked: bool
    flags: list[str]
    message: str | None = None


def inspect_privacy(text: str) -> GuardResult:
    """Detect requests or content involving personal data that the agent must not collect."""
    flags = [name for name, pattern in PRIVACY_PATTERNS.items() if pattern.search(text or "")]
    if not flags:
        return GuardResult(blocked=False, flags=[])

    return GuardResult(
        blocked=True,
        flags=flags,
        message=(
            "실제 학번, 성적, 주민번호, 연락처, 포털 ID/PW 등 개인정보는 입력받지 않습니다. "
            "가상 사례나 사용자가 직접 요약한 비식별 정보로만 안내할 수 있습니다."
        ),
    )


def require_sources(chunks: list[dict]) -> GuardResult:
    """Block grounded answers when no official source chunks are available."""
    if chunks:
        return GuardResult(blocked=False, flags=[])
    return GuardResult(
        blocked=True,
        flags=["no_official_source"],
        message="공식 문서 근거가 부족하므로 확인이 필요합니다.",
    )
