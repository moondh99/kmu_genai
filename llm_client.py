"""Guarded LLM interface.

MVP uses deterministic template fallback. Replace this class with an Ollama,
Qwen, or Llama adapter later while preserving the same method shape.
"""

from __future__ import annotations


class GuardedLLMClient:
    """Minimal guarded LLM facade."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def generate(self, prompt: str, grounded_context: list[dict]) -> str:
        """Generate text only from grounded context.

        The current implementation intentionally returns an empty string so the
        deterministic answer builder remains the source of truth.
        """
        _ = prompt, grounded_context
        return ""

