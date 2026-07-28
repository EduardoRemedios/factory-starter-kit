import assert from "node:assert/strict";
import test from "node:test";

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${path}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request(`http://localhost${path}`, {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the English product contract", async () => {
  const response = await render("/");
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /AI builds the software\./);
  assert.match(html, /Humans stay in control\./);
  assert.match(html, /AI Delivery Director/);
  assert.match(html, /Factory was designed by Eduardo A dos Remedios\./);
  assert.doesNotMatch(html, /github\.com|View on GitHub|Explore Factory on GitHub/i);
  assert.doesNotMatch(html, /Your site is taking shape|react-loading-skeleton/i);
});

test("server-renders complete Spanish first-view meaning", async () => {
  const response = await render("/?lang=es");
  assert.equal(response.status, 200);

  const html = await response.text();
  assert.match(html, /La IA construye el software\./);
  assert.match(
    html,
    /Las personas mantienen el control\./,
  );
  assert.match(html, /Director de Entrega con IA/);
  assert.match(html, /Factory fue diseñado por Eduardo A dos Remedios\./);
  assert.doesNotMatch(html, /github\.com|Ver en GitHub|Explorar Factory en GitHub/i);
});
