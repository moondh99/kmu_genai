"""Crawler adapter base classes."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class RawDocument:
    """A raw official document collected from a source."""

    doc_id: str
    title: str
    url: str
    source_type: str
    text: str
    metadata: dict

    @property
    def content_hash(self) -> str:
        """Return a stable content hash for incremental updates."""
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


class BaseCrawler:
    """Base class for official-source crawler adapters."""

    source_type = "base"

    def crawl(self, limit: int = 20) -> list[RawDocument]:
        """Collect raw documents. Subclasses should override this."""
        _ = limit
        return []

