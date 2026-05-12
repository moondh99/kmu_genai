export default function ActionForm({ actions, actionState, slots, setSlots, onStart, onContinue }) {
  return (
    <section className="panel shell">
      <h2>다음 행동</h2>
      {actions.length === 0 && <p className="muted">질문 후 action이 표시됩니다.</p>}
      {actions.map((action) => (
        <div className="item" key={action.action_id}>
          <strong>{action.label}</strong>
          <p className="muted">{action.description}</p>
          <button className="action" type="button" onClick={() => onStart(action.action_id)}>시작</button>
        </div>
      ))}
      {actionState && (
        <div className="item action-box">
          <h3>{actionState.label || "Action"}</h3>
          {actionState.message && <p className="status">{actionState.message}</p>}
          {actionState.privacy_notice && <p className="status">{actionState.privacy_notice}</p>}
          <div className="action-form">
            {(actionState.missing_slots || []).map((slot, index) => (
              <label key={slot}>
                <span>{actionState.questions?.[index] || slot}</span>
                <input
                  value={slots[slot] || ""}
                  onChange={(event) => setSlots({ ...slots, [slot]: event.target.value })}
                />
              </label>
            ))}
            {actionState.status !== "unsupported" && (
              <button className="primary" type="button" onClick={onContinue}>초안 생성</button>
            )}
          </div>
        </div>
      )}
    </section>
  );
}
