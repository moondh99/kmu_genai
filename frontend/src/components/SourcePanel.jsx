export default function SourcePanel({ citations }) {
  return (
    <section className="panel shell">
      <h2>출처</h2>
      {citations.length === 0 && <p className="muted">답변의 [S1] 출처가 여기에 표시됩니다.</p>}
      {citations.map((source) => (
        <div className="item" key={source.id}>
          <div><span className="source-id">[{source.id}]</span> {source.title}</div>
          <div className="muted">Tier {source.source_tier} · {source.source_type} · {source.department || ""}</div>
          <p>{source.text}</p>
          <a href={source.url} target="_blank" rel="noreferrer">공식 문서 열기</a>
        </div>
      ))}
    </section>
  );
}
