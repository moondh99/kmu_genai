"""Draft action documents such as attendance recognition form text."""

from __future__ import annotations


ATTENDANCE_REQUIRED_SLOTS = [
    "event_date",
    "absence_reason",
    "course_name",
    "instructor_name_optional",
    "evidence_document_type",
    "planned_submission_date",
]


def missing_slots(action_id: str, slots: dict) -> list[str]:
    """Return missing slots for a supported action."""
    if action_id != "draft_attendance_recognition_form":
        return []
    return [slot for slot in ATTENDANCE_REQUIRED_SLOTS if not slots.get(slot)]


def slot_questions(action_id: str, missing: list[str]) -> list[str]:
    """Create user-facing questions for missing action slots."""
    labels = {
        "event_date": "결석일 또는 훈련일은 언제인가요? 예: 2026-05-15",
        "absence_reason": "결석 사유를 적어주세요. 예: 예비군 훈련",
        "course_name": "대상 수업명은 무엇인가요?",
        "instructor_name_optional": "담당 교강사명을 적어주세요. 모르면 '담당 교강사'라고 적어도 됩니다.",
        "evidence_document_type": "준비할 증빙서류는 무엇인가요? 예: 예비군 소집통지서 또는 훈련필증",
        "planned_submission_date": "제출 예정일은 언제인가요? 예: 2026-05-20",
    }
    return [labels[slot] for slot in missing]


def draft_action_document(action_id: str, slots: dict, policy_chunks: list[dict]) -> dict:
    """Draft a grounded action document from user-provided non-sensitive slots."""
    if action_id != "draft_attendance_recognition_form":
        return {"document": "지원하지 않는 action입니다.", "checklist": []}

    reason = slots.get("absence_reason", "예비군 훈련")
    event_date = slots.get("event_date", "")
    course = slots.get("course_name", "해당 교과목")
    instructor = slots.get("instructor_name_optional", "담당 교강사")
    evidence = slots.get("evidence_document_type", "증빙서류")
    planned = slots.get("planned_submission_date", "")

    document = f"""[출석인정신청서 초안]

신청 사유:
본인은 {reason}으로 인해 {event_date}에 {course} 수업에 출석하지 못하게 되어, 국민대학교 출석인정 안내에 따라 출석인정을 신청하고자 합니다.

대상 수업:
{course}

결석일 또는 사유 발생일:
{event_date}

제출 대상:
{instructor}

첨부 예정 증빙서류:
{evidence}

제출 예정일:
{planned}

확인 문구:
위 내용은 공식 근거를 바탕으로 작성한 초안이며, 실제 학교 양식과 담당 교강사 안내에 맞게 사용자가 직접 최종 확인 후 제출해야 합니다."""

    checklist = [
        "공식 출석인정신청서 양식이 있는지 확인합니다.",
        f"{evidence}를 준비합니다.",
        "사유 발생 7일 이내 제출 대상인지 확인합니다.",
        f"{instructor}에게 제출합니다.",
        "출석 인정 여부를 최종 확인합니다.",
    ]
    return {"document": document, "checklist": checklist}

