"""Public SWELL crawler placeholder."""

from crawler.base import BaseCrawler


class SWELLPublicCrawler(BaseCrawler):
    """Crawler adapter for public SWELL pages only."""

    source_type = "swell_public"

