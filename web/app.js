export function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

export function createActivationApp({
  documentRef = globalThis.document,
  fetchImpl = globalThis.fetch,
  now = () => new Date(),
} = {}) {
  const queueEl = documentRef.getElementById("queue");
  const emptyEl = documentRef.getElementById("empty");
  const statusEl = documentRef.getElementById("status");

  async function loadQueue() {
    const res = await fetchImpl("/api/queue");
    if (!res.ok) throw new Error("queue unavailable");
    const payload = await res.json();
    render(payload.relationships || []);
  }

  function render(rows) {
    queueEl.innerHTML = "";
    emptyEl.hidden = rows.length > 0;
    for (const row of rows) {
      const li = documentRef.createElement("li");
      li.className = "card";
      li.innerHTML = `
        <p class="kind">${escapeHtml(row.kind)} · due ${escapeHtml(row.due)}</p>
        <p class="parties"><strong>${escapeHtml(row.from_party)}</strong> → ${escapeHtml(row.to_party)}</p>
        <p class="move">${escapeHtml(row.next_move)}</p>
        <p class="why">${escapeHtml(row.why_now)}</p>
        <div class="actions">
          <button data-relationship-id="${escapeHtml(row.relationship_id)}" data-action="activate">Activate</button>
          <button class="secondary" data-relationship-id="${escapeHtml(row.relationship_id)}" data-action="reschedule">Reschedule +7d</button>
          <button class="secondary" data-relationship-id="${escapeHtml(row.relationship_id)}" data-action="dismiss">Dismiss</button>
        </div>`;
      queueEl.appendChild(li);
    }
  }

  async function handleQueueClick(event) {
    const btn = event.target.closest("button");
    if (!btn) return;
    const action = btn.dataset.action;
    const relationshipId = btn.dataset.relationshipId;
    const body = { action };
    if (action === "reschedule") {
      const due = now();
      due.setUTCDate(due.getUTCDate() + 7);
      body.due = due.toISOString().slice(0, 10);
    }
    btn.disabled = true;
    try {
      const res = await fetchImpl(
        `/api/queue/${encodeURIComponent(relationshipId)}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        },
      );
      if (!res.ok) {
        statusEl.hidden = false;
        statusEl.textContent = "Could not record that move.";
        return;
      }
      const done = await res.json();
      statusEl.hidden = false;
      statusEl.textContent = `${done.from_party} → ${done.to_party} is now ${done.status}.`;
      await loadQueue();
    } catch (_error) {
      statusEl.hidden = false;
      statusEl.textContent = "Could not record that move.";
    } finally {
      btn.disabled = false;
    }
  }

  queueEl.addEventListener("click", handleQueueClick);
  const ready = loadQueue().catch((error) => {
    statusEl.hidden = false;
    statusEl.textContent = error.message;
  });

  return { handleQueueClick, loadQueue, ready, render };
}
