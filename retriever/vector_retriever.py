"""Optional Chroma retriever facade.

The MVP runs without Chroma installed. This class reports availability and
keeps the backend shape ready for a real vector store.
"""

from __future__ import annotations


class VectorRetriever:
    """Optional vector retriever; gracefully disabled when Chroma is unavailable."""

    def __init__(self, *_args, **_kwargs):
        try:
            import chromadb  # noqa: F401

            self.available = True
        except Exception:
            self.available = False

    def search(self, _query: str, _issue_type: str | None = None, _limit: int = 6) -> list[dict]:
        """Return vector results when a real Chroma index is configured."""
        return []

