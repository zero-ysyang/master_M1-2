const API_BASE_URL = window.location.origin.includes("localhost") || window.location.origin.includes("127.0.0.1")
  ? "http://127.0.0.1:8000"
  : ""; // 배포 환경 동적 바인딩

let currentConversationId = null;

// DOM 로드 완료 후 초기화
document.addEventListener("DOMContentLoaded", () => {
  loadSummary();
  loadDataList();
  loadConversations();

  document.getElementById("data-form").addEventListener("submit", handleAddData);
  document.getElementById("chat-form").addEventListener("submit", handleSendChat);
  document.getElementById("btn-new-chat").addEventListener("click", startNewChat);
});

// 1. 데이터 요약 불러오기
async function loadSummary() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/data/summary`);
    const data = await res.json();
    document.getElementById("sum-period").innerText = data.period;
    document.getElementById("sum-count").innerText = data.count;
    document.getElementById("sum-avg").innerText = data.metrics.average;
    document.getElementById("sum-range").innerText = `${data.metrics.max} / ${data.metrics.min}`;
    document.getElementById("sum-trend").innerText = data.trend;
  } catch (err) {
    console.error("요약 정보 로드 실패:", err);
  }
}

// 2. 데이터 목록 및 CRUD
async function loadDataList() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/data`);
    const items = await res.json();
    const listEl = document.getElementById("data-list");
    listEl.innerHTML = "";

    // 최근 10개만 표시
    items.slice(-10).reverse().forEach(item => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span>${item.date}: <strong>${item.value}</strong> (${item.memo})</span>
        <button class="btn-del" onclick="deleteData('${item.id}')">삭제</button>
      `;
      listEl.appendChild(li);
    });
  } catch (err) {
    console.error("데이터 목록 로드 실패:", err);
  }
}

async function handleAddData(e) {
  e.preventDefault();
  const payload = {
    date: document.getElementById("input-date").value,
    value: parseFloat(document.getElementById("input-value").value),
    memo: document.getElementById("input-memo").value
  };

  await fetch(`${API_BASE_URL}/api/data`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  document.getElementById("data-form").reset();
  loadDataList();
  loadSummary(); // 데이터 추가 후 요약 정보 갱신
}

async function deleteData(id) {
  if (!confirm("삭제하시겠습니까?")) return;
  await fetch(`${API_BASE_URL}/api/data/${id}`, { method: "DELETE" });
  loadDataList();
  loadSummary();
}

// 3. AI 채팅 및 대화 불러오기
async function handleSendChat(e) {
  e.preventDefault();
  const inputEl = document.getElementById("chat-input");
  const message = inputEl.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputEl.value = "";
  toggleLoading(true);

  try {
    const res = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, conversation_id: currentConversationId })
    });
    const data = await res.json();

    currentConversationId = data.conversation_id;
    document.getElementById("current-conv-id").innerText = `ID: ${currentConversationId.substring(0, 8)}...`;
    
    appendMessage("assistant", data.reply);
    loadConversations(); // 대화 목록 갱신
  } catch (err) {
    appendMessage("assistant", "에러가 발생했습니다. 다시 시도해주세요.");
  } finally {
    toggleLoading(false);
  }
}

function appendMessage(role, text) {
  const container = document.getElementById("chat-messages");
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.innerText = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function toggleLoading(show) {
  document.getElementById("loading-spinner").classList.toggle("hidden", !show);
}

// 4. 대화 기록 연동
async function loadConversations() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/conversations`);
    const convs = await res.json();
    const listEl = document.getElementById("conv-list");
    listEl.innerHTML = "";

    convs.forEach(conv => {
      const li = document.createElement("li");
      li.innerText = conv.title || "대화 기록";
      if (conv.id === currentConversationId) li.classList.add("active");
      li.onclick = () => loadSingleConversation(conv.id);
      listEl.appendChild(li);
    });
  } catch (err) {
    console.error("대화 목록 로드 실패:", err);
  }
}

async function loadSingleConversation(id) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/conversations/${id}`);
    const conv = await res.json();
    currentConversationId = conv.id;
    document.getElementById("current-conv-id").innerText = `ID: ${id.substring(0, 8)}...`;
    
    const messagesEl = document.getElementById("chat-messages");
    messagesEl.innerHTML = "";
    
    conv.messages.forEach(msg => {
      appendMessage(msg.role, msg.content);
    });
    loadConversations();
  } catch (err) {
    console.error("대화 불러오기 실패:", err);
  }
}

function startNewChat() {
  currentConversationId = null;
  document.getElementById("current-conv-id").innerText = "새 대화 모드";
  document.getElementById("chat-messages").innerHTML = `
    <div class="message assistant">새 대화가 시작되었습니다. 질문을 입력하세요.</div>
  `;
  loadConversations();
}