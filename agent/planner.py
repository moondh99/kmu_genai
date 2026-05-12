"""Plan tool calls and next actions for a classified query."""

from __future__ import annotations


NEXT_ACTIONS = {
    "attendance": [
        {
            "action_id": "draft_attendance_recognition_form",
            "label": "출석인정신청서 초안 작성",
            "description": "결석일, 수업명, 증빙서류 등 필요한 항목을 받아 신청서 초안을 작성합니다.",
        }
    ],
    "leave_return": [
        {
            "action_id": "draft_leave_checklist",
            "label": "휴학/복학 준비 체크리스트 생성",
            "description": "신청 경로, 기간, 서류 확인 항목을 정리합니다.",
        }
    ],
    "course_registration": [
        {
            "action_id": "course_registration_checklist",
            "label": "수강신청/폐강 확인 체크리스트 생성",
            "description": "나의 시간표, 개인수업시간표, 폐강 후 내역 확인 항목을 정리합니다.",
        }
    ],
    "certificate": [
        {
            "action_id": "certificate_issue_guide",
            "label": "증명서 발급 경로 확인",
            "description": "발급 가능한 증명서와 문의처를 확인합니다.",
        }
    ],
    "graduation": [
        {
            "action_id": "graduation_audit",
            "label": "졸업요건 간이 진단",
            "description": "비식별 이수학점 요약을 바탕으로 부족 학점을 계산합니다.",
        }
    ],
}


def suggest_actions(issue_type: str, chunks: list[dict]) -> list[dict]:
    """Suggest next actions suitable for the issue type and retrieved chunks."""
    actions = list(NEXT_ACTIONS.get(issue_type, []))
    chunk_actions = []
    for chunk in chunks:
        for action_id in chunk.get("actions", []) or []:
            chunk_actions.append(action_id)
    if "draft_attendance_recognition_form" in chunk_actions and issue_type != "attendance":
        actions.insert(0, NEXT_ACTIONS["attendance"][0])
    return actions

