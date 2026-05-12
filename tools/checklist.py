"""Checklist generation from grounded policy chunks."""

from __future__ import annotations


def generate_checklist(issue_type: str, policy_chunks: list[dict]) -> dict:
    """Generate action items and required documents from official chunks."""
    documents: list[str] = []
    tasks: list[str] = []
    paths: list[str] = []
    submit_to: list[str] = []

    for chunk in policy_chunks:
        for document in chunk.get("required_documents", []) or []:
            if document not in documents:
                documents.append(document)
        path = chunk.get("application_path")
        if path and path not in paths:
            paths.append(path)
        target = chunk.get("submit_to")
        if target and target not in submit_to:
            submit_to.append(target)

    if issue_type == "attendance":
        tasks.extend(["결석 사유와 날짜를 확인합니다.", "출석인정신청서와 증빙서류를 준비합니다.", "기한 내 담당 교강사에게 제출합니다."])
    elif issue_type == "leave_return":
        tasks.extend(["휴학/복학 유형과 신청 기간을 확인합니다.", "ON국민 포털 신청 경로를 확인합니다.", "필요 서류가 있는 경우 제출 전 원본/사본 요건을 확인합니다."])
    elif issue_type == "course_registration":
        tasks.extend(["수강신청시스템 나의 시간표 또는 ON국민 개인수업시간표를 확인합니다.", "폐강 공지가 있는 경우 본인 수강신청 내역을 다시 확인합니다."])
    elif issue_type == "certificate":
        tasks.extend(["필요한 증명서 종류를 고릅니다.", "인터넷 증명 발급신청 페이지에서 발급 가능 여부를 확인합니다.", "수수료 및 원본확인 방법을 확인합니다."])
    elif issue_type == "graduation":
        tasks.extend(["요람/규정집에서 소속 학과 졸업요건을 확인합니다.", "총 이수학점, 전공 이수학점, 필수과목, 교양영역을 나누어 점검합니다.", "최종 졸업 판정은 소속 학과사무실 또는 교무팀에 확인합니다."])
    elif issue_type == "contact":
        tasks.extend(["문의 주제에 맞는 담당 부서를 고릅니다.", "개인정보를 제외한 질문 요약을 준비합니다.", "공식 포털 또는 담당 부서 안내에 따라 후속 확인을 진행합니다."])
    else:
        tasks.append("공식 근거와 담당 부서를 확인합니다.")

    return {
        "tasks": tasks,
        "required_documents": documents,
        "application_paths": paths,
        "submit_to": submit_to,
    }
