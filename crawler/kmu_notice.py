"""Kookmin notice crawler."""

from crawler.base import BaseCrawler, SourcePage


class KMUNoticeCrawler(BaseCrawler):
    """Crawler adapter for KMU notices."""

    source_type = "notice"
    source_tier = 5
    pages = [
        SourcePage(
            doc_id="notice_course_registration_2026_1",
            title="2026-1학기 수강신청 일정안내",
            url="https://www.kookmin.ac.kr/user/kmuNews/notice/4/11139/view.do?currentPageNo=1",
            department="교무팀",
            published_at="2026-01-05",
            fallback_text=(
                "수강신청 후 수강신청시스템 '나의 시간표' 또는 ON국민 포털 '개인수업시간표 조회'에 "
                "표기되는 교과목만 수강신청 완료 및 수강 과목으로 인정된다. 폐강 이후에는 반드시 본인 "
                "수강신청 내역을 확인해야 한다. 교과목 거래, 매크로 사용 등 비정상적인 방식으로 수강신청을 "
                "진행하는 경우 적발된 학생의 모든 수강신청 내역이 삭제되며 학생 징계의 대상이 될 수 있다."
            ),
            keywords=["수강신청", "나의 시간표", "개인수업시간표", "폐강", "매크로"],
            search_hints=["수강신청 완료됐는지 어디서 확인해", "폐강 이후 해야 할 일", "수강신청 매크로"],
            issue_types=["course_registration"],
            application_path="수강신청시스템 나의 시간표 또는 ON국민 포털 개인수업시간표 조회",
            actions=["course_registration_checklist"],
        )
    ]
