import assert from "node:assert/strict";
import test from "node:test";

const appModule = await import(new URL("../web/app.js", import.meta.url));
const { createActivationApp, escapeHtml } = appModule;

function response(payload, { ok = true, jsonError = null } = {}) {
  return {
    ok,
    async json() {
      if (jsonError) throw jsonError;
      return payload;
    },
  };
}

function createDocumentHarness() {
  let clickHandler;
  const rendered = [];
  const queueEl = {
    innerHTML: "preexisting",
    appendChild(node) {
      rendered.push(node);
    },
    addEventListener(type, handler) {
      assert.equal(type, "click");
      clickHandler = handler;
    },
  };
  const emptyEl = { hidden: true };
  const statusEl = { hidden: true, textContent: "" };
  const documentRef = {
    getElementById(elementId) {
      return { queue: queueEl, empty: emptyEl, status: statusEl }[elementId];
    },
    createElement(tagName) {
      assert.equal(tagName, "li");
      return { className: "", innerHTML: "" };
    },
  };
  return {
    documentRef,
    emptyEl,
    getClickHandler: () => clickHandler,
    queueEl,
    rendered,
    statusEl,
  };
}

function button(action = "activate") {
  return {
    dataset: { action, relationshipId: "rel-001" },
    disabled: false,
  };
}

function clickEvent(targetButton) {
  return { target: { closest: () => targetButton } };
}

test("module exposes a testable activation app and HTML escaping", () => {
  assert.equal(typeof createActivationApp, "function");
  assert.equal(
    escapeHtml('&<>"'),
    "&amp;&lt;&gt;&quot;",
  );
});

test("initial load renders escaped relationship cards with semantic identity", async () => {
  const harness = createDocumentHarness();
  const row = {
    relationship_id: 'rel-"1',
    kind: "partner&ally",
    due: "2026-09-01",
    from_party: "A <Team>",
    to_party: "B > Team",
    next_move: 'Say "hello"',
    why_now: "Now & next",
  };
  const fetchCalls = [];
  const app = createActivationApp({
    documentRef: harness.documentRef,
    fetchImpl: async (...args) => {
      fetchCalls.push(args);
      return response({ relationships: [row] });
    },
  });
  await app.ready;

  assert.deepEqual(fetchCalls, [["/api/queue"]]);
  assert.equal(harness.queueEl.innerHTML, "");
  assert.equal(harness.emptyEl.hidden, true);
  assert.equal(harness.rendered.length, 1);
  assert.equal(harness.rendered[0].className, "card");
  assert.match(harness.rendered[0].innerHTML, /partner&amp;ally/);
  assert.match(harness.rendered[0].innerHTML, /A &lt;Team&gt;/);
  assert.match(harness.rendered[0].innerHTML, /B &gt; Team/);
  assert.match(harness.rendered[0].innerHTML, /Say &quot;hello&quot;/);
  assert.match(harness.rendered[0].innerHTML, /Now &amp; next/);
  assert.match(harness.rendered[0].innerHTML, /data-relationship-id="rel-&quot;1"/);
  assert.doesNotMatch(harness.rendered[0].innerHTML, /data-id=/);
  assert.equal(typeof harness.getClickHandler(), "function");
});

test("initial load treats a missing relationships field as an empty queue", async () => {
  const harness = createDocumentHarness();
  const app = createActivationApp({
    documentRef: harness.documentRef,
    fetchImpl: async () => response({}),
  });
  await app.ready;
  assert.equal(harness.emptyEl.hidden, false);
  assert.deepEqual(harness.rendered, []);
});

test("initial load exposes a readable error state", async () => {
  const harness = createDocumentHarness();
  const app = createActivationApp({
    documentRef: harness.documentRef,
    fetchImpl: async () => response({}, { ok: false }),
  });
  await app.ready;
  assert.equal(harness.statusEl.hidden, false);
  assert.equal(harness.statusEl.textContent, "queue unavailable");
});

test("clicks outside queue buttons are ignored", async () => {
  const harness = createDocumentHarness();
  const app = createActivationApp({
    documentRef: harness.documentRef,
    fetchImpl: async () => response({ relationships: [] }),
  });
  await app.ready;
  await harness.getClickHandler()({ target: { closest: () => null } });
  assert.equal(harness.statusEl.hidden, true);
});

test("reschedule records a seven-day UTC date, reports success, and reloads", async () => {
  const harness = createDocumentHarness();
  const calls = [];
  let call = 0;
  const fetchImpl = async (...args) => {
    calls.push(args);
    call += 1;
    if (call === 1 || call === 3) return response({ relationships: [] });
    return response({ from_party: "A", to_party: "B", status: "rescheduled" });
  };
  const app = createActivationApp({
    documentRef: harness.documentRef,
    fetchImpl,
    now: () => new Date("2026-08-29T23:30:00Z"),
  });
  await app.ready;
  const selected = button("reschedule");
  await harness.getClickHandler()(clickEvent(selected));

  const [url, options] = calls[1];
  assert.equal(url, "/api/queue/rel-001");
  assert.equal(options.method, "POST");
  assert.deepEqual(options.headers, { "Content-Type": "application/json" });
  assert.deepEqual(JSON.parse(options.body), {
    action: "reschedule",
    due: "2026-09-05",
  });
  assert.equal(calls[2][0], "/api/queue");
  assert.equal(selected.disabled, false);
  assert.equal(harness.statusEl.hidden, false);
  assert.equal(harness.statusEl.textContent, "A → B is now rescheduled.");
});

test("a non-OK action response shows the existing error state", async () => {
  const harness = createDocumentHarness();
  let call = 0;
  const app = createActivationApp({
    documentRef: harness.documentRef,
    fetchImpl: async () => {
      call += 1;
      return call === 1
        ? response({ relationships: [] })
        : response({}, { ok: false });
    },
  });
  await app.ready;
  const selected = button();
  await harness.getClickHandler()(clickEvent(selected));
  assert.equal(selected.disabled, false);
  assert.equal(harness.statusEl.textContent, "Could not record that move.");
});

for (const stage of ["fetch", "response-json", "reload"]) {
  test(`queue action recovers when ${stage} rejects`, async () => {
    const harness = createDocumentHarness();
    let call = 0;
    const app = createActivationApp({
      documentRef: harness.documentRef,
      fetchImpl: async () => {
        call += 1;
        if (call === 1) return response({ relationships: [] });
        if (stage === "fetch" && call === 2) throw new Error("network unavailable");
        if (call === 2) {
          return response(
            { from_party: "A", to_party: "B", status: "activated" },
            stage === "response-json"
              ? { jsonError: new Error("invalid response JSON") }
              : {},
          );
        }
        if (stage === "reload" && call === 3) throw new Error("reload unavailable");
        return response({ relationships: [] });
      },
    });
    await app.ready;
    const selected = button();
    await harness.getClickHandler()(clickEvent(selected));

    assert.equal(selected.disabled, false);
    assert.equal(harness.statusEl.hidden, false);
    assert.equal(harness.statusEl.textContent, "Could not record that move.");
  });
}

test("browser auto-start uses global dependencies and the default clock", async () => {
  const harness = createDocumentHarness();
  const calls = [];
  let call = 0;
  const RealDate = globalThis.Date;
  class FixedDate extends RealDate {
    constructor(...args) {
      super(...(args.length ? args : ["2026-08-29T23:30:00Z"]));
    }
  }
  globalThis.document = harness.documentRef;
  globalThis.fetch = async (...args) => {
    calls.push(args);
    call += 1;
    if (call === 1 || call === 3) return response({ relationships: [] });
    return response({ from_party: "A", to_party: "B", status: "rescheduled" });
  };
  globalThis.Date = FixedDate;
  try {
    await import(new URL("../web/bootstrap.js", import.meta.url));
    await new Promise((resolve) => setImmediate(resolve));
    const selected = button("reschedule");
    await harness.getClickHandler()(clickEvent(selected));
    assert.deepEqual(JSON.parse(calls[1][1].body), {
      action: "reschedule",
      due: "2026-09-05",
    });
    assert.equal(selected.disabled, false);
  } finally {
    delete globalThis.document;
    delete globalThis.fetch;
    globalThis.Date = RealDate;
  }
});
