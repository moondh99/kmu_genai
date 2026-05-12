"""FastAPI server for KMU Campus Life Action Agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agent.action_state import continue_action, start_action
from agent.answer_builder import build_final_answer
from agent.classifier import classify_issue
from agent.guard import inspect_privacy, require_sources
from agent.planner import suggest_actions
from retriever.hybrid_retriever import HybridRetriever


class AskRequest(BaseModel):
    """Request body for a user question."""

    question: str = Field(..., min_length=1)
    student_context: dict[str, Any] = Field(default_factory=dict)


class ActionStartRequest(BaseModel):
    """Request body for starting a follow-up action."""

    action_id: str


class ActionContinueRequest(BaseModel):
    """Request body for continuing a follow-up action."""

    action_id: str
    slots: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    """Request body for an ingestion run."""

    source: str = "seed"
    limit: int = 20
    force_rebuild: bool = False


app = FastAPI(title="KMU Campus Life Action Agent", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = HybridRetriever()

frontend_path = Path("frontend")
if frontend_path.exists():
    app.mount("/frontend", StaticFiles(directory=str(frontend_path)), name="frontend")


@app.get("/", response_model=None)
def index():
    """Serve the local demo UI when available."""
    html = Path("frontend/index.html")
    if html.exists():
        return FileResponse(html)
    return {"message": "KMU Campus Life Action Agent API"}


@app.get("/health")
def health() -> dict:
    """Return service health and optional vector-store availability."""
    return {
        "status": "ok",
        "keyword_chunks": len(retriever.all_sources()),
        "vector_retriever_available": retriever.vector.available,
    }


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    """Answer a campus-life question with grounded sources and next actions."""
    tool_logs: list[str] = []
    privacy = inspect_privacy(request.question)
    tool_logs.append("guard.inspect_privacy 호출됨")
    if privacy.blocked:
        return {
            "answer": privacy.message,
            "issue_type": "privacy_blocked",
            "tool_logs": tool_logs,
            "sources": [],
            "citations": [],
            "next_actions": [],
            "safety_flags": privacy.flags,
        }

    classification = classify_issue(request.question)
    issue_type = classification["issue_type"]
    tool_logs.append("classify_issue 호출됨")

    chunks = retriever.search(request.question, issue_type=issue_type, limit=8)
    tool_logs.append("search_official_sources 호출됨")

    source_guard = require_sources(chunks)
    tool_logs.append("guard.require_sources 호출됨")
    if source_guard.blocked:
        return {
            "answer": (
                f"{source_guard.message}\n"
                "국민대학교 공식 포털, 관련 부서, 학과사무실 또는 담당 교강사에게 확인해 주세요."
            ),
            "issue_type": issue_type,
            "tool_logs": tool_logs,
            "sources": [],
            "citations": [],
            "next_actions": [],
            "safety_flags": source_guard.flags,
        }

    actions = suggest_actions(issue_type, chunks)
    tool_logs.append("suggest_actions 호출됨")
    built = build_final_answer(request.question, issue_type, chunks, actions)
    tool_logs.extend(["generate_checklist 호출됨", "route_contact 호출됨", "build_final_answer 호출됨"])

    return {
        "answer": built["answer"],
        "issue_type": issue_type,
        "classification": classification,
        "tool_logs": tool_logs,
        "sources": chunks,
        "citations": built["citations"],
        "next_actions": actions,
        "safety_flags": [],
    }


@app.post("/actions/start")
def action_start(request: ActionStartRequest) -> dict:
    """Start a document/action drafting flow."""
    return start_action(request.action_id)


@app.post("/actions/continue")
def action_continue(request: ActionContinueRequest) -> dict:
    """Continue a document/action drafting flow with user-provided non-sensitive slots."""
    privacy_text = " ".join(str(value) for value in request.slots.values())
    privacy = inspect_privacy(privacy_text)
    if privacy.blocked:
        return {
            "status": "blocked",
            "message": privacy.message,
            "safety_flags": privacy.flags,
        }
    chunks = retriever.search("출석인정 예비군", issue_type="attendance", limit=4)
    return continue_action(request.action_id, request.slots, chunks)


@app.post("/ingest/run")
def ingest_run(request: IngestRequest) -> dict:
    """Run a placeholder ingestion job for demo/admin visibility."""
    _ = request
    return {
        "status": "completed",
        "message": "MVP는 seed JSONL 데이터와 crawler adapter 구조를 사용합니다. 실제 주기 크롤링은 crawler 모듈을 확장해 연결하세요.",
        "indexed_chunks": len(retriever.all_sources()),
    }


@app.get("/sources")
def sources() -> dict:
    """List available official source chunks."""
    chunks = retriever.all_sources()
    return {"count": len(chunks), "sources": chunks}
