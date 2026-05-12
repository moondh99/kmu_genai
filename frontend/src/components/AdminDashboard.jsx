import React from "react";

export default function AdminDashboard({ apiBase }) {
  const [health, setHealth] = React.useState(null);
  const [ingest, setIngest] = React.useState(null);
  const [running, setRunning] = React.useState(false);

  async function loadHealth() {
    const response = await fetch(`${apiBase}/health`);
    setHealth(await response.json());
  }

  async function runIngest() {
    setRunning(true);
    try {
      const response = await fetch(`${apiBase}/ingest/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source: "all", limit: 20, force_rebuild: false })
      });
      const data = await response.json();
      setIngest(data);
      await loadHealth();
    } finally {
      setRunning(false);
    }
  }

  React.useEffect(() => {
    loadHealth();
  }, []);

  return (
    <section className="panel shell">
      <div className="panel-title">
        <h2>관리자</h2>
        <button type="button" onClick={loadHealth}>새로고침</button>
      </div>
      {!health && <p className="muted">상태를 불러오는 중입니다.</p>}
      {health && (
        <div className="metrics">
          <div><strong>{health.keyword_chunks}</strong><span>JSONL chunks</span></div>
          <div><strong>{health.vector_retriever_available ? "ON" : "OFF"}</strong><span>Chroma</span></div>
          <div><strong>{health.vector_indexed_count}</strong><span>Vector docs</span></div>
        </div>
      )}
      {health?.vector_error && <p className="status">Vector 상태: {health.vector_error}</p>}
      <button className="primary wide" type="button" disabled={running} onClick={runIngest}>
        {running ? "수집 중" : "공식자료 수집/인덱싱 실행"}
      </button>
      {ingest && (
        <div className="item">
          <strong>{ingest.status}</strong>
          <p>{ingest.message}</p>
          <p className="muted">
            문서 {ingest.documents_seen} · 신규 {ingest.new_documents} · 변경 {ingest.changed_documents} ·
            chunks {ingest.chunks_written} · vector {ingest.vector_indexed}
          </p>
          {(ingest.failures || []).map((failure) => (
            <p className="status" key={`${failure.source}-${failure.error}`}>{failure.source}: {failure.error}</p>
          ))}
        </div>
      )}
    </section>
  );
}
