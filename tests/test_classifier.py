from agent.classifier import classify_issue


def test_classifies_core_issues():
    assert classify_issue("예비군 때문에 결석하는데 출석인정 어떻게 해?")["issue_type"] == "attendance"
    assert classify_issue("질병휴학 하려면 뭐 필요해?")["issue_type"] == "leave_return"
    assert classify_issue("수강신청 완료됐는지 어디서 확인해?")["issue_type"] == "course_registration"
    assert classify_issue("졸업예정증명서 어디서 뽑아?")["issue_type"] == "certificate"

