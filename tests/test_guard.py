from agent.guard import inspect_privacy, require_sources


def test_privacy_guard_blocks_student_id_and_grades():
    result = inspect_privacy("내 학번이랑 성적으로 처리해줘.")
    assert result.blocked
    assert "student_id" in result.flags
    assert "grade_report" in result.flags


def test_requires_sources():
    result = require_sources([])
    assert result.blocked

