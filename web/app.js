const queueEl = document.getElementById("queue");
const emptyEl = document.getElementById("empty");
const statusEl = document.getElementById("status");

async function loadQueue() {
  const res = await fetch("/api/queue");
  if (!res.ok) throw new Error("queue unavailable");
  const payload = await res.json();
  render(payload.relationships || []);
}

function render(rows) {
  queueEl.innerHTML = "";
  emptyEl.hidden = rows.length > 0;
  for (const row of rows) {
    const li = document.createElement("li");
    li.className = "card";
    li.innerHTML = `
      <p class="kind">${escapeHtml(row.kind)} · due ${escapeHtml(row.due)}</p>
      <p class="parties"><strong>${escapeHtml(row.from_party)}</strong> → ${escapeHtml(row.to_party)}</p>
      <p class="move">${escapeHtml(row.next_move)}</p>
      <p class="why">${escapeHtml(row.why_now)}</p>
      <div class="actions">
        <button data-id="${escapeHtml(row.id)}" data-action="activate">Activate</button>
        <button class="secondary" data-id="${escapeHtml(row.id)}" data-action="reschedule">Reschedule +7d</button>
        <button class="secondary" data-id="${escapeHtml(row.id)}" data-action="dismiss">Dismiss</button>
      </div>`;
    queueEl.appendChild(li);
  }
}

queueEl.addEventListener("click", async (event) => {
  const btn = event.target.closest("button");
  if (!btn) return;
  const action = btn.dataset.action;
  const id = btn.dataset.id;
  const body = { action };
  if (action === "reschedule") {
    const due = new Date();
    due.setUTCDate(due.getUTCDate() + 7);
    body.due = due.toISOString().slice(0, 10);
  }
  btn.disabled = true;
  const res = await fetch(`/api/queue/${encodeURIComponent(id)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    statusEl.hidden = false;
    statusEl.textContent = "Could not record that move.";
    btn.disabled = false;
    return;
  }
  const done = await res.json();
  statusEl.hidden = false;
  statusEl.textContent = `${done.from_party} → ${done.to_party} is now ${done.status}.`;
  await loadQueue();
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

loadQueue().catch((err) => {
  statusEl.hidden = false;
  statusEl.textContent = err.message;
});
