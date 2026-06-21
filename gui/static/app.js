// === TAVOLAROTONDA GUI — Frontend logic ===

const state = {
  mode: "topic",
  sessionId: null,
  eventSource: null,
  eventCount: 0,
  htmlUrl: null,
  palaceUrl: null,
  models: [],
  selectedModel: "mock",
};

// === INIT ===
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupInputs();
  loadModels();
  loadCouncilPresets();
  loadAgents();
  setupButtons();
});

// === TABS ===
function setupTabs() {
  document.querySelectorAll("#mode-tabs .tab").forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode;
      state.mode = mode;
      document.querySelectorAll("#mode-tabs .tab").forEach(t => t.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById("field-topic").style.display = mode === "topic" ? "" : "none";
      document.getElementById("field-audit").style.display = mode === "audit" ? "" : "none";
      document.getElementById("field-qa").style.display = mode === "qa" ? "" : "none";
    });
  });
}

// === INPUTS ===
function setupInputs() {
  const slider = document.getElementById("rounds-slider");
  const val = document.getElementById("rounds-val");
  slider.addEventListener("input", () => val.textContent = slider.value);
}

// === BUTTONS ===
function setupButtons() {
  document.getElementById("run-btn").addEventListener("click", startRun);
  document.getElementById("stop-btn").addEventListener("click", stopRun);
  document.getElementById("clear-btn").addEventListener("click", clearStream);
  document.getElementById("download-html").addEventListener("click", () => {
    if (state.htmlUrl) window.open(state.htmlUrl, "_blank");
  });
  document.getElementById("download-palace").addEventListener("click", () => {
    if (state.palaceUrl) window.open(state.palaceUrl, "_blank");
  });
}

// === MODELS ===
async function loadModels() {
  const select = document.getElementById("model-select");
  const status = document.getElementById("model-status");
  const reason = document.getElementById("model-reason");
  select.innerHTML = '<option>Caricamento...</option>';
  status.innerHTML = '<span class="model-status-badge model-loading">Caricamento...</span>';

  try {
    const r = await fetch("/api/models");
    const data = await r.json();
    state.models = data.models;
    select.innerHTML = "";

    data.models.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m.key;
      opt.textContent = `${m.icon} ${m.label}`;
      opt.title = m.description;
      opt.dataset.status = m.state;
      select.appendChild(opt);
    });

    // Default: seleziona il primo "ok", o mock se tutti indisponibili
    const firstOk = data.models.find(m => m.state === "ok");
    if (firstOk) {
      select.value = firstOk.key;
      state.selectedModel = firstOk.key;
    } else {
      select.value = "mock";
      state.selectedModel = "mock";
    }

    updateModelStatus(state.selectedModel);
    select.addEventListener("change", () => {
      state.selectedModel = select.value;
      updateModelStatus(state.selectedModel);
    });
  } catch (e) {
    console.error("loadModels failed:", e);
    status.innerHTML = '<span class="model-status-badge model-error">⚠️ Errore caricamento modelli</span>';
  }
}

// === COUNCIL PRESETS ===
async function loadCouncilPresets() {
  try {
    const r = await fetch("/api/council-presets");
    const data = await r.json();
    state.councilPresets = data.presets;
    const select = document.getElementById("council-mode-select");
    select.innerHTML = "";
    data.presets.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.key;
      opt.textContent = `${p.icon} ${p.label}`;
      opt.title = p.description;
      select.appendChild(opt);
    });
    state.councilMode = "monolithic";
    updateCouncilPresetUI("monolithic");
    select.addEventListener("change", () => {
      state.councilMode = select.value;
      updateCouncilPresetUI(state.councilMode);
    });
  } catch (e) {
    console.error("loadCouncilPresets failed:", e);
  }
}

function updateCouncilPresetUI(key) {
  const preset = state.councilPresets?.find(p => p.key === key);
  const desc = document.getElementById("council-mode-desc");
  const preview = document.getElementById("routing-preview");
  if (!preset) return;

  desc.textContent = preset.description;

  if (!preset.routing) {
    preview.innerHTML = `<div class="routing-empty">Modalità monolitica: tutti i 18 agenti → <b>${state.selectedModel}</b></div>`;
    return;
  }

  // Costruisci tabella compatta: agente → provider
  // Raggruppa per provider per compattezza
  const byProvider = {};
  for (const [agentKey, provKey] of Object.entries(preset.routing)) {
    if (!byProvider[provKey]) byProvider[provKey] = [];
    byProvider[provKey].push(agentKey);
  }

  const providerColor = {
    "opus-4.8": "var(--purple)",
    "MiniMax-M3": "var(--accent)",
    "ollama-auto": "var(--success)",
    "mock": "var(--muted)",
  };

  let html = "";
  for (const [prov, agents] of Object.entries(byProvider)) {
    const color = providerColor[prov] || "var(--muted)";
    html += `<div class="routing-group">
      <div class="routing-prov" style="color:${color}">● ${prov} <span class="routing-count">(${agents.length})</span></div>
      <div class="routing-agents">${agents.map(a => `<span class="routing-agent">${a}</span>`).join(" ")}</div>
    </div>`;
  }
  preview.innerHTML = html;
}

function updateModelStatus(key) {
  const m = state.models.find(x => x.key === key);
  if (!m) return;
  const status = document.getElementById("model-status");
  const reason = document.getElementById("model-reason");

  let badge = "";
  switch (m.state) {
    case "ok":
      badge = `<span class="model-status-badge model-ok">✅ ${m.model}</span>`;
      reason.textContent = m.reason;
      reason.style.color = "var(--muted)";
      break;
    case "missing_env":
      badge = `<span class="model-status-badge model-warn">⚠️ Config mancante</span>`;
      reason.textContent = m.reason;
      reason.style.color = "var(--warn)";
      break;
    case "unreachable":
    case "unavailable":
      badge = `<span class="model-status-badge model-error">❌ ${m.state}</span>`;
      reason.textContent = m.reason;
      reason.style.color = "var(--danger)";
      break;
    case "fallback_mock":
      badge = `<span class="model-status-badge model-warn">⚠️ Fallback mock</span>`;
      reason.textContent = m.reason;
      reason.style.color = "var(--warn)";
      break;
    default:
      badge = `<span class="model-status-badge model-loading">?</span>`;
      reason.textContent = m.reason || "";
  }
  status.innerHTML = badge;
}

// === AGENTS ===
async function loadAgents() {
  try {
    const r = await fetch("/api/agents");
    const data = await r.json();
    const list = document.getElementById("agents-list");
    list.innerHTML = "";
    data.agents.forEach(a => {
      const div = document.createElement("div");
      div.className = "agent";
      div.id = `agent-${a.key}`;
      const emojiMap = {
        aristotle: "🏛️", socrates: "🦉", sun_tzu: "⚔️", ada: "⚙️",
        aurelius: "👑", feynman: "🔬", torvalds: "🐧", karpathy: "🧠",
        kahneman: "🎯", meadows: "🌱", munger: "🧓", taleb: "🦢",
        rams: "✨", hadid: "📐", jobs: "🍎", skinner: "🧪",
        dijkstra: "∑", churchill: "🎖️"
      };
      const emoji = emojiMap[a.key] || "🤖";
      div.innerHTML = `
        <span class="emoji">${emoji}</span>
        <div class="info">
          <div class="name">${a.name}</div>
          <div class="meta">${a.domain}</div>
        </div>
      `;
      list.appendChild(div);
    });
  } catch (e) {
    console.error("loadAgents failed:", e);
  }
}

// === RUN ===
async function startRun() {
  clearStream();
  const topic = document.getElementById("topic-input").value.trim();
  const audit = document.getElementById("audit-input").value.trim();
  const qa = document.getElementById("qa-input").value.trim();
  const rounds = parseInt(document.getElementById("rounds-slider").value);
  const privacy = document.getElementById("privacy-select").value;
  const research = document.getElementById("research-check").checked;
  const model = state.selectedModel;
  const councilMode = state.councilMode || "monolithic";

  if (state.mode === "topic" && !topic) { alert("Inserisci un topic"); return; }
  if (state.mode === "audit" && !audit) { alert("Inserisci il path di un file"); return; }
  if (state.mode === "qa" && !qa) { alert("Inserisci almeno una domanda"); return; }

  const payload = {
    mode: state.mode,
    rounds,
    model,
    council_mode: councilMode,
    privacy,
    research,
  };
  if (state.mode === "topic") payload.topic = topic;
  if (state.mode === "audit") payload.audit_target = audit;
  if (state.mode === "qa") {
    payload.qa_questions = qa.split("\n").map(s => s.trim()).filter(Boolean);
  }

  setRunning(true);
  appendEvent({
    type: "info",
    msg: `▶ Avvio ${state.mode} con modello "${model}" (${rounds} round, privacy=${privacy})`,
  });

  try {
    const r = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await r.json();
    if (data.error) {
      appendEvent({ type: "error", msg: data.error });
      setRunning(false);
      return;
    }
    state.sessionId = data.session_id;
    state.htmlUrl = null;
    state.palaceUrl = null;
    document.getElementById("download-html").disabled = true;
    document.getElementById("download-palace").disabled = true;
    connectStream(data.session_id);
  } catch (e) {
    appendEvent({ type: "error", msg: `Errore di rete: ${e.message}` });
    setRunning(false);
  }
}

function stopRun() {
  if (state.eventSource) {
    state.eventSource.close();
    state.eventSource = null;
  }
  setRunning(false);
  appendEvent({ type: "warn", msg: "⏹ Stream interrotto manualmente" });
}

function connectStream(sid) {
  if (state.eventSource) state.eventSource.close();
  const es = new EventSource(`/api/stream/${sid}`);
  state.eventSource = es;

  es.onmessage = (msg) => {
    try {
      const ev = JSON.parse(msg.data);
      handleEvent(ev);
    } catch (e) {
      console.error("parse error:", e, msg.data);
    }
  };

  es.onerror = (err) => {
    console.warn("SSE error:", err);
  };
}

// === EVENT HANDLER ===
function handleEvent(ev) {
  state.eventCount++;
  document.getElementById("event-counter").textContent = `${state.eventCount} eventi`;

  if (ev.type === "connected") return;

  if (ev.type === "closed") {
    setRunning(false);
    setStatus(ev.status === "done" ? "done" : "error",
              ev.status === "done" ? "✅ Completato" : "❌ Errore");
    if (state.eventSource) {
      state.eventSource.close();
      state.eventSource = null;
    }
    return;
  }

  if (ev.type === "done") {
    state.htmlUrl = ev.html_url;
    state.palaceUrl = ev.palace_url;
    document.getElementById("download-html").disabled = false;
    document.getElementById("download-palace").disabled = false;
    const modelUsed = ev.model_used || "?";
    appendEvent({ type: "done", msg: `🎉 Dibattito concluso con modello: ${modelUsed}. Scarica HTML o Palace JSON.` });
    return;
  }

  appendEvent(ev);

  // Highlight active agent
  if (ev.agent) {
    document.querySelectorAll(".agent").forEach(a => a.classList.remove("active"));
    const el = document.getElementById(`agent-${slugify(ev.agent)}`);
    if (el) {
      el.classList.add("active");
      setTimeout(() => el.classList.remove("active"), 3000);
    }
  }
}

function slugify(s) {
  return s.toLowerCase().replace(/[^a-z0-9]/g, "");
}

// === APPEND EVENT TO STREAM ===
function appendEvent(ev) {
  document.getElementById("empty-state").style.display = "none";
  const stream = document.getElementById("stream");
  const div = document.createElement("div");
  div.className = `event event-${ev.type || "info"}`;

  const header = document.createElement("div");
  header.className = "event-header";
  const ts = ev.ts ? new Date(ev.ts * 1000).toLocaleTimeString() : new Date().toLocaleTimeString();

  let badge = "";
  if (ev.agent) {
    badge = `<span class="agent-badge">${escapeHtml(ev.agent)}</span>`;
  } else if (ev.role === "director") {
    badge = `<span class="agent-badge">🎬 Direttore</span>`;
  } else if (ev.role === "secretary") {
    badge = `<span class="agent-badge">📝 Segretario</span>`;
  } else if (ev.phase) {
    badge = `<span class="agent-badge">⚙ ${ev.phase}</span>`;
  }
  const roundTxt = ev.round ? `<span class="round">R${ev.round}</span>` : "";
  header.innerHTML = `${badge}${roundTxt}<span class="ts">${ts}</span>`;
  div.appendChild(header);

  const content = document.createElement("div");
  content.className = "event-content";

  if (ev.type === "research") {
    content.innerHTML = formatResearch(ev);
  } else if (ev.text || ev.msg) {
    const text = ev.text || ev.msg;
    content.innerHTML = formatText(text);
  }
  div.appendChild(content);

  stream.appendChild(div);
  stream.parentElement.scrollTop = stream.parentElement.scrollHeight;
}

function formatResearch(ev) {
  const sup = (ev.supporting || []).map(r =>
    `<li><b>${escapeHtml(r.title || r.url || "?")}</b> — ${escapeHtml(r.snippet || "")}</li>`
  ).join("");
  const ctr = (ev.counter || []).map(r =>
    `<li><b>${escapeHtml(r.title || r.url || "?")}</b> — ${escapeHtml(r.snippet || "")}</li>`
  ).join("");
  return `<b>🔍 Ricerca avversariale</b><br>
    <details open><summary>✅ A favore (${ev.supporting?.length || 0})</summary><ul>${sup}</ul></details>
    <details><summary>❌ Contro (${ev.counter?.length || 0})</summary><ul>${ctr}</ul></details>`;
}

function formatText(t) {
  return escapeHtml(t)
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^- (.+)$/gm, '• $1')
    .replace(/\n/g, '<br>');
}

function escapeHtml(s) {
  if (typeof s !== "string") return JSON.stringify(s);
  return s.replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[c]);
}

// === UI STATE ===
function setRunning(running) {
  document.getElementById("run-btn").disabled = running;
  document.getElementById("stop-btn").disabled = !running;
  const bar = document.getElementById("progress-bar");
  const fill = document.getElementById("progress-fill");
  if (running) {
    bar.style.display = "";
    fill.classList.add("indeterminate");
    setStatus("running", "⏳ Dibattito in corso...");
  } else {
    fill.classList.remove("indeterminate");
    setTimeout(() => bar.style.display = "none", 500);
  }
}

function setStatus(state, text) {
  const dot = document.querySelector("#status .dot");
  dot.className = `dot dot-${state}`;
  document.getElementById("status-text").textContent = text;
}

function clearStream() {
  document.getElementById("stream").innerHTML = "";
  document.getElementById("empty-state").style.display = "";
  state.eventCount = 0;
  document.getElementById("event-counter").textContent = "0 eventi";
  state.htmlUrl = null;
  state.palaceUrl = null;
  document.getElementById("download-html").disabled = true;
  document.getElementById("download-palace").disabled = true;
}
