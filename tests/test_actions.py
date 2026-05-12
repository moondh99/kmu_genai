from agent.action_state import continue_action, start_action


def test_attendance_action_requests_missing_slots():
    result = start_action("draft_attendance_recognition_form")
    assert result["status"] == "needs_input"
    assert "event_date" in result["missing_slots"]


def test_attendance_action_drafts_document():
    slots = {
        "event_date": "2026-05-15",
        "absence_reason": "예비군 훈련",
        "course_name": "자료구조",
        "instructor_name_optional": "담당 교강사",
        "evidence_document_type": "예비군 소집통지서 또는 훈련필증",
        "planned_submission_date": "2026-05-20",
    }
    result = continue_action("draft_attendance_recognition_form", slots)
    assert result["status"] == "completed"
    assert "출석인정신청서 초안" in result["document"]
    assert "자료구조" in result["document"]

