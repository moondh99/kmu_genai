export default function ChatPanel({ examples, question, setQuestion, messages, loading, onAsk }) {
  return (
    <section className="chat shell">
      <div className="examples">
        {examples.map((item) => (
          <button key={item} type="button" onClick={() => { setQuestion(item); onAsk(item); }}>
            {item}
          </button>
        ))}
      </div>
      <div className="messages">
        {messages.length === 0 && <div className="message agent muted">예시 질문을 누르거나 직접 질문을 입력하세요.</div>}
        {messages.map((message, index) => (
          <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="composer">
        <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
        <button className="primary" type="button" disabled={loading} onClick={() => onAsk()}>
          {loading ? "처리 중" : "질문"}
        </button>
      </div>
    </section>
  );
}
