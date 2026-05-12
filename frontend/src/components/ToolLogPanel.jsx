export default function ToolLogPanel({ logs }) {
  return (
    <section className="panel shell">
      <h2>Tool Calling 로그</h2>
      {logs.length === 0 && <p className="muted">질문 처리 과정이 표시됩니다.</p>}
      {logs.map((log, index) => <div className="item" key={`${log}-${index}`}>{index + 1}. {log}</div>)}
    </section>
  );
}
