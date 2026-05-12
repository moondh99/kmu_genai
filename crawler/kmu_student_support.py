"""Kookmin student-support guide crawler."""

from crawler.base import BaseCrawler, SourcePage


class KMUStudentSupportCrawler(BaseCrawler):
    """Crawler adapter for student-support guide pages."""

    source_type = "student_support"
    source_tier = 3
    pages = [
        SourcePage(
            doc_id="student_support_certificate",
            title="국민대학교 증명서 발급",
            url="https://www.kookmin.ac.kr/comm/menu/user/00078abe6af76fde00965b928c8c9067/content/index.do",
            department="종합서비스센터",
            fallback_text=(
                "인터넷 증명 발급 신청을 통해 제 증명서를 출력할 수 있으며, 성적, 재학, 휴학, 수료, 제적, "
                "졸업예정, 졸업 등 증명서가 안내되어 있다. 졸업예정증명서는 학사과정 수료생 또는 일정 차수 "
                "등록을 필하고 총취득학점과 최종학기 수강신청학점의 합이 졸업에 필요한 최저이수학점수 이상인 "
                "자에게 발급되는 것으로 안내되어 있다."
            ),
            keywords=["증명서", "인터넷신청", "졸업예정증명서", "성적증명서", "재학증명서"],
            search_hints=["졸업예정증명서 어디서 뽑아", "성적증명서 발급", "증명서 인터넷 발급"],
            issue_types=["certificate", "graduation"],
            application_path="국민대학교 인터넷 증명 발급신청 페이지",
            contacts=[
                {"label": "학적 관련 문의", "name": "종합서비스센터", "phone": "02-910-4046, 4050"},
                {"label": "증명발급 시스템/수수료 결제 문의", "name": "한국정보인증(주)", "phone": "1644-2378"},
            ],
            actions=["certificate_issue_guide"],
        )
    ]
