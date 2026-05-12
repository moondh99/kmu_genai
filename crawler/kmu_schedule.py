"""Kookmin academic schedule crawler."""

from crawler.base import BaseCrawler, SourcePage


class KMUScheduleCrawler(BaseCrawler):
    """Crawler adapter for academic schedule pages."""

    source_type = "schedule"
    source_tier = 4
    pages = [
        SourcePage(
            doc_id="schedule_2026_leave_return",
            title="국민대학교 학사일정 - 2026학년도 휴학/복학",
            url="https://www.kookmin.ac.kr/user/scGuid/scSchedule/index.do",
            department="교무팀",
            fallback_text="2026학년도 2학기 휴학, 복학 신청 기간은 2026.07.06부터 2026.07.24까지이다.",
            keywords=["학사일정", "휴학", "복학", "신청기간", "2026"],
            search_hints=["2학기 휴학 복학 신청 기간", "복학 언제 신청", "휴학 신청 기간"],
            issue_types=["leave_return", "schedule"],
            schedule={"start_date": "2026-07-06", "end_date": "2026-07-24", "label": "2026학년도 2학기 휴학, 복학 신청 기간"},
        ),
        SourcePage(
            doc_id="schedule_2026_course_registration",
            title="국민대학교 학사일정 - 2026학년도 수강신청",
            url="https://www.kookmin.ac.kr/user/scGuid/scSchedule/index.do",
            department="교무팀",
            fallback_text="2026학년도 2학기 수강신청 기간은 2026.08.12부터 2026.08.26까지이다.",
            keywords=["학사일정", "수강신청", "2026", "2학기"],
            search_hints=["2학기 수강신청 기간", "수강신청 언제"],
            issue_types=["course_registration", "schedule"],
            schedule={"start_date": "2026-08-12", "end_date": "2026-08-26", "label": "2026학년도 2학기 수강신청 기간"},
        ),
    ]
