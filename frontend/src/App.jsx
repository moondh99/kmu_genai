import React from "react";
import { createRoot } from "react-dom/client";
import ActionForm from "./components/ActionForm.jsx";
import AdminDashboard from "./components/AdminDashboard.jsx";
import ChatPanel from "./components/ChatPanel.jsx";
import SourcePanel from "./components/SourcePanel.jsx";
import ToolLogPanel from "./components/ToolLogPanel.jsx";
import "./styles.css";

const API_BASE = window.location.port === "5173" ? "http://127.0.0.1:8000" : window.location.origin;

const examples = [
  "예비군 때문에 결석하는데 뭐 해야 해?",
  "질병휴학 하려면 뭐 필요해?",
  "수강신청 완료됐는지 어디서 확인해?",
  "졸업예정증명서 어디서 뽑아?",
  "졸업요건 부족한지 확인하고 다음 학기 수강계획 짜줘",
  "내 학번이랑 성적으로 처리해줘."
];

function App() {
  const [question, setQuestion] = React.useState(examples[0]);
  const [messages, setMessages] = React.useState([]);
  const [toolLogs, setToolLogs] = React.useState([]);
  const [citations, setCitations] = React.useState([]);
  const [actions, setActions] = React.useState([]);
  const [actionState, setActionState] = React.useState(null);
  const [slots, setSlots] = React.useState({});
  const [loading, setLoading] = React.useState(false);

  async function ask(text = question) {
    if (!text.trim() || loading) return;
    setLoading(true);
    setMessages((prev) => [...prev, { role: "user", text }]);
    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { role: "agent", text: data.answer || "응답을 생성하지 못했습니다." }]);
      setToolLogs(data.tool_logs || []);
      setCitations(data.citations || []);
      setActions(data.next_actions || []);
      setActionState(null);
      setSlots({});
    } catch (error) {
      setMessages((prev) => [...prev, { role: "agent", text: `요청 실패: ${error.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  async function startAction(actionId) {
    const response = await fetch(`${API_BASE}/actions/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action_id: actionId })
    });
    const data = await response.json();
    setActionState(data);
    setSlots({});
  }

  async function continueAction() {
    if (!actionState) return;
    const response = await fetch(`${API_BASE}/actions/continue`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action_id: actionState.action_id, slots })
    });
    const data = await response.json();
    if (data.status === "completed") {
      const checklist = (data.checklist || []).map((item, index) => `${index + 1}. ${item}`).join("\n");
      setMessages((prev) => [...prev, { role: "agent", text: `${data.document}\n\n[제출 전 체크리스트]\n${checklist}` }]);
      setActionState(null);
      setSlots({});
    } else {
      setActionState(data);
    }
  }

  return (
    <>
      <header className="topbar">
        <div>
          <h1>KMU Campus Life Action Agent</h1>
          <p>공식자료 수집, Chroma hybrid 검색, 출처 기반 답변, 다음 행동까지 한 화면에서 확인합니다.</p>
        </div>
      </header>
      <main className="layout">
        <ChatPanel
          examples={examples}
          question={question}
          setQuestion={setQuestion}
          messages={messages}
          loading={loading}
          onAsk={ask}
        />
        <aside className="side">
          <ActionForm
            actions={actions}
            actionState={actionState}
            slots={slots}
            setSlots={setSlots}
            onStart={startAction}
            onContinue={continueAction}
          />
          <SourcePanel citations={citations} />
          <ToolLogPanel logs={toolLogs} />
          <AdminDashboard apiBase={API_BASE} />
        </aside>
      </main>
    </>
  );
}

createRoot(document.getElementById("root")).render(<App />);
