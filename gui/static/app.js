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
      // Tronca SOLO nel select (full label nel info panel sotto)
      const label = `${m.icon} ${m.label}`;
      opt.textContent = label.length > 35 ? label.slice(0, 33) + "…" : label;
      opt.title = `${m.label}\n${m.description}`;
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

    renderModelInfo(state.selectedModel);
    select.addEventListener("change", () => {
      state.selectedModel = select.value;
      renderModelInfo(state.selectedModel);
      // Aggiorna anche routing preview se council mode è attivo
      if (state.councilMode && state.councilMode !== "monolithic") {
        updateRoutingPreview();
      }
    });
  } catch (e) {
    console.error("loadModels failed:", e);
    status.innerHTML = '<span class="model-status-badge model-error">⚠️ Errore caricamento modelli</span>';
  }
}

// Render info panel dettagliato del modello selezionato (descrizione + env + sub-provider)
function renderModelInfo(key) {
  const m = state.models.find(x => x.key === key);
  if (!m) return;

  // Status badge (inline)
  const status = document.getElementById("model-status");
  const reason = document.getElementById("model-reason");
  let badge = "";
  switch (m.state) {
    case "ok":
      badge = `<span class="model-status-badge model-ok">✅ ${escapeHtml(m.model || "ok")}</span>`;
      reason.textContent = m.reason || "";
      reason.style.color = "var(--muted)";
      break;
    case "missing_env":
      badge = `<span class="model-status-badge model-warn">⚠️ Config mancante</span>`;
      reason.textContent = m.reason || "";
      reason.style.color = "var(--warn)";
      break;
    case "unreachable":
    case "unavailable":
      badge = `<span class="model-status-badge model-error">❌ ${escapeHtml(m.state)}</span>`;
      reason.textContent = m.reason || "";
      reason.style.color = "var(--danger)";
      break;
    case "fallback_mock":
      badge = `<span class="model-status-badge model-warn">⚠️ Fallback mock</span>`;
      reason.textContent = m.reason || "";
      reason.style.color = "var(--warn)";
      break;
    default:
      badge = `<span class="model-status-badge model-loading">?</span>`;
      reason.textContent = m.reason || "";
  }
  status.innerHTML = badge;

  // Info panel dettagliato (sempre visibile, full text)
  const info = document.getElementById("model-info");
  let envHtml = "";
  if (m.env_required && m.env_required.length > 0) {
    const cmds = m.env_required.map(k =>
      `<code class="model-info-env-cmd" title="Clicca per selezionare, poi copia">export ${escapeHtml(k)}=&lt;your-key&gt;</code>`
    ).join("");
    envHtml = `<div class="model-info-env">
      <div class="model-info-env-label">🔑 Env richieste</div>
      ${cmds}
    </div>`;
  }

  let providersHtml = "";
  if (m.providers && Object.keys(m.providers).length > 0) {
    const rows = Object.entries(m.providers).map(([pname, pst]) => {
      const icon = pst.state === "ok" ? "✅" : "⚠️";
      const modelInfo = state.models.find(x => x.key === pname);
      const pIcon = modelInfo ? modelInfo.icon : "🤖";
      return `<div class="model-info-provider">
        <span class="model-info-provider-icon">${pIcon}</span>
        <div class="model-info-provider-info">
          <div class="model-info-provider-name">${escapeHtml(pname)} <span style="color:var(--muted);font-weight:400">→ ${escapeHtml(pst.model || "?")}</span></div>
          <div class="model-info-provider-reason">${icon} ${escapeHtml(pst.state)} · ${escapeHtml((pst.reason || "").slice(0, 100))}</div>
        </div>
      </div>`;
    }).join("");
    providersHtml = `<div class="model-info-providers">
      <div class="model-info-providers-title">🎭 Sub-provider attivi</div>
      ${rows}
    </div>`;
  }

  info.innerHTML = `
    <div class="model-info-header">
      <span class="model-info-icon">${escapeHtml(m.icon || "🤖")}</span>
      <span class="model-info-label">${escapeHtml(m.label)}</span>
    </div>
    <div class="model-info-desc">${escapeHtml(m.description)}</div>
    ${m.model && m.model !== "mock" ? `<div class="model-info-model">model: ${escapeHtml(m.model)}</div>` : ""}
    ${envHtml}
    ${providersHtml}
  `;
  info.style.display = "";
}

// === COUNCIL PRESETS (radio cards) ===
async function loadCouncilPresets() {
  try {
    const r = await fetch("/api/council-presets");
    const data = await r.json();
    state.councilPresets = data.presets;
    renderCouncilCards();
    state.councilMode = "monolithic";
    updateRoutingPreview();
  } catch (e) {
    console.error("loadCouncilPresets failed:", e);
    document.getElementById("council-cards").innerHTML =
      '<div class="routing-empty">⚠️ Errore caricamento preset</div>';
  }
}

function renderCouncilCards() {
  const container = document.getElementById("council-cards");
  if (!container || !state.councilPresets) return;
  container.innerHTML = "";
  state.councilPresets.forEach(p => {
    const card = document.createElement("label");
    card.className = "council-card" + (state.councilMode === p.key ? " active" : "");
    card.dataset.key = p.key;
    card.innerHTML = `
      <input type="radio" name="council-mode" value="${escapeHtml(p.key)}" ${state.councilMode === p.key ? "checked" : ""}>
      <div class="council-card-header">
        <span class="council-card-icon">${escapeHtml(p.icon || "🎭")}</span>
        <span class="council-card-label">${escapeHtml(p.label)}</span>
      </div>
      <div class="council-card-desc">${escapeHtml(p.description)}</div>
    `;
    card.addEventListener("click", () => {
      state.councilMode = p.key;
      document.querySelectorAll(".council-card").forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      const radio = card.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
      updateRoutingPreview();
    });
    container.appendChild(card);
  });
}

function updateRoutingPreview() {
  const preset = state.councilPresets?.find(p => p.key === state.councilMode);
  const preview = document.getElementById("routing-preview");
  if (!preset || !preview) return;

  if (!preset.routing) {
    const mLabel = state.models.find(x => x.key === state.selectedModel)?.label || state.selectedModel;
    preview.innerHTML = `<div class="routing-empty">Modalità monolitica: tutti i 18 agenti → <b>${escapeHtml(mLabel)}</b></div>`;
    return;
  }

  // Raggruppa per provider
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
    const provLabel = state.models.find(x => x.key === prov)?.label || prov;
    html += `<div class="routing-group">
      <div class="routing-prov" style="color:${color}">● ${escapeHtml(provLabel)} <span class="routing-count">(${agents.length})</span></div>
      <div class="routing-agents">${agents.map(a => `<span class="routing-agent" title="${escapeHtml(a)}">${escapeHtml(a)}</span>`).join(" ")}</div>
    </div>`;
  }
  preview.innerHTML = html;
}

// Backward-compat alias (era la firma precedente)
function updateCouncilPresetUI(key) {
  state.councilMode = key;
  renderCouncilCards();
  updateRoutingPreview();
}

function updateModelStatus(key) {
  // Retrocompat: delega a renderModelInfo
  renderModelInfo(key);
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
