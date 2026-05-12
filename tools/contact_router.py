"""Contact routing tool for campus-life questions."""

from __future__ import annotations


DEFAULT_CONTACTS = {
    "attendance": [{"label": "1차 제출/확인", "name": "해당 교과목 교강사"}, {"label": "행정 확인", "name": "교무팀"}],
    "leave_return": [{"label": "행정 확인", "name": "교무팀"}, {"label": "소속 확인", "name": "소속 학과사무실 또는 단과대학 교학팀"}],
    "course_registration": [{"label": "수강신청/폐강 확인", "name": "교무팀"}, {"label": "전공 과목 확인", "name": "소속 학과사무실 또는 단과대학 교학팀"}],
    "certificate": [{"label": "학적 관련 문의", "name": "종합서비스센터", "phone": "02-910-4046, 4050"}],
    "military": [{"label": "병무/예비군 문의", "name": "병무지원팀"}, {"label": "출석 인정 제출", "name": "해당 교과목 교강사"}],
    "graduation": [{"label": "졸업요건 확인", "name": "소속 학과사무실 또는 단과대학 교학팀"}, {"label": "학사 행정 확인", "name": "교무팀"}],
}


def route_contact(issue_type: str, policy_chunks: list[dict]) -> list[dict]:
    """Recommend official contact destinations from chunks and defaults."""
    contacts: list[dict] = []
    for chunk in policy_chunks:
        for contact in chunk.get("contacts", []) or []:
            if contact not in contacts:
                contacts.append(contact)
    for contact in DEFAULT_CONTACTS.get(issue_type, []):
        if contact not in contacts:
            contacts.append(contact)
    return contacts

