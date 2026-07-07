# Robust Agent Web-Reading & Scraping Tools — 2026 Survey + Recommended Stack

**Audience:** OpenGoldSDR / Grok Go agent fleet
**Date:** 2026-06-18
**Goal:** Let a local Mac agent reliably pull *clean, LLM-ready content* out of JS-heavy pages, ideally reusing our already-running logged-in debug Chrome on CDP `:9222` (the `chrome-login` skill / `~/.chrome-debug-x` profile, driven by `~/agent-bridge/cdp_*.js`).

---

## TL;DR Recommendation

For Grok Go's situation (we already own a logged-in Chrome on `:9222`), the winning architecture is **two layers**:

1. **Rendering layer = our existing CDP Chrome.** Don't spin up a second browser. Keep using the persistent debug profile so we inherit logged-in sessions (X, Grok, Discord, etc.). This is the hard part of robust scraping (JS, auth, anti-bot) and we already solved it.
2. **Extraction layer = `trafilatura` (primary) + `readability` (fallback).** Take the rendered HTML out of the CDP tab and run it through a local, free, fast, deterministic main-content extractor. No API keys, no per-page cost, no network round-trip.

**Glue:** `Crawl4AI` is the best single library that already speaks `cdp_url="http://127.0.0.1:9222"` *and* bundles content filtering → markdown, so it can be both the driver and the extractor when you want one dependency instead of wiring Playwright + trafilatura yourself.

Add on demand:
- **`MarkItDown`** for non-HTML artifacts (PDF/DOCX/PPTX/XLSX) that pages link to.
- **Jina Reader (`r.jina.ai`)** as a zero-infra fallback for *public* pages when local rendering fails or isn't worth it.
- **`browser-use` / `Stagehand`** only when the task is *agentic interaction* (click-through flows, multi-step forms), not plain reading.

---

## The tools, scored for our use case

### Rendering / driving engines

#### Playwright
- **Best at:** The de-facto reliable browser-automation primitive; nearly every other tool here wraps it. Robust waits, network interception, multi-context.
- **JS rendering:** Full (real Chromium/WebKit/Firefox).
- **CDP fit (ours):** Excellent and battle-tested. `chromium.connectOverCDP("http://127.0.0.1:9222")` attaches to our existing Chrome and reuses its logged-in cookies/sessions. Retrieve the WS endpoint from `http://localhost:9222/json/list` → `webSocketDebuggerUrl` if you need the raw socket. This is the lowest-level, most predictable way to drive `:9222`.
- **Caveat:** It's a driver, not an extractor — you still need trafilatura/readability/MarkItDown to turn the DOM into clean content. Use it when Crawl4AI's abstractions get in the way.
- Sources: [playwright.dev BrowserType](https://playwright.dev/docs/api/class-browsertype), [BrowserStack: connect to existing browser](https://www.browserstack.com/guide/playwright-connect-to-existing-browser), [AgentPMT: 10+ agents on one logged-in browser](https://www.agentpmt.com/articles/how-to-run-10-playwright-agents-on-one-logged-in-browser-without-getting-blocked)

#### Crawl4AI (`unclecode/crawl4ai`)
- **Best at:** Python-first, open-source, "Scrapy for the LLM era." A sophisticated Playwright wrapper that goes all the way to clean markdown with configurable content filters, custom hooks, and pluggable extraction strategies (regex/CSS or LLM). Free as a library.
- **JS rendering:** Full (it *is* Playwright underneath).
- **CDP fit (ours):** Strong — directly supports `BrowserConfig(cdp_url="ws://localhost:9222")` / `http://127.0.0.1:9222`, so it can attach to our logged-in debug Chrome instead of launching its own. Also supports `user_data_dir` persistent profiles and "identity-based crawling" for auth.
- **Caveat:** More knobs to turn than a SaaS; total cost is "free lib + your own LLM keys + your own infra." For us that's a feature, not a bug — we want local + free.
- **Why it's our glue:** It's the one OSS tool that natively does *both* (attach to `:9222`) *and* (filter → markdown) in one dependency.
- Sources: [Crawl4AI browser/crawler config docs](https://docs.crawl4ai.com/core/browser-crawler-config/), [Crawl4AI identity-based crawling](https://docs.crawl4ai.com/advanced/identity-based-crawling/), [Brightdata: Crawl4AI vs Firecrawl](https://brightdata.com/blog/ai/crawl4ai-vs-firecrawl)

#### Firecrawl (`firecrawl/firecrawl`)
- **Best at:** "Serverless" scraping — send a URL, get back LLM-ready markdown / structured JSON with zero browser-fleet or retry management. ~85k★, very polished. Handles crawl + extract at scale.
- **JS rendering:** Full, managed for you.
- **CDP fit (ours):** **Poor fit for the logged-in-`:9222` goal.** Firecrawl's value is *not running your own browser*; it renders on *its* infra, so it can't trivially reuse our local logged-in Chrome session. Self-hostable (AGPL-3.0, SDKs MIT) but then you're operating a browser fleet — exactly what we already have for free via `:9222`.
- **Use it when:** You want to crawl lots of *public* pages without babysitting infra, or want a hosted SLA. SaaS from ~$16/mo.
- Sources: [github.com/firecrawl/firecrawl](https://github.com/firecrawl/firecrawl), [Firecrawl SELF_HOST.md](https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md), [WebScraping.AI: is Firecrawl open source / self-host](https://webscraping.ai/faq/firecrawl/is-firecrawl-open-source-and-can-i-self-host-it)

#### chrome-devtools-mcp (`ChromeDevTools/chrome-devtools-mcp`) — *notable, not in the original list*
- **Best at:** Google's official MCP server exposing Chrome DevTools (navigate, inspect, eval, perf, screenshots) to coding agents. Drops straight into an MCP client config.
- **JS rendering:** Full (real Chrome).
- **CDP fit (ours):** **Excellent and directly relevant.** `--browser-url=http://127.0.0.1:9222` attaches to our *exact* running debug Chrome and reuses its logged-in tabs/extensions instead of spawning a new instance. If Grok Go agents speak MCP, this is the cleanest "give the agent our `:9222` browser" path with near-zero glue.
- **Caveat:** It's a control surface, not a content extractor — pair with trafilatura/readability for clean output.
- Sources: [github.com/ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp), [npm chrome-devtools-mcp](https://www.npmjs.com/package/chrome-devtools-mcp)

### Content extractors (HTML → clean text/markdown)

#### trafilatura
- **Best at:** High-accuracy main-content extraction from HTML. Pure Python, free, fast, deterministic, no LLM. Strips boilerplate (nav/footer/sidebar) with near-perfect precision. Best overall mean F1 in 2025 benchmarks and best for English specifically (F1 ~0.883 English; ~0.937 mean in another set).
- **JS rendering:** **None** — it operates on HTML you already have. That's why it pairs with a renderer (our `:9222` Chrome) rather than replacing it.
- **CDP fit (ours):** Perfect as the *extraction half*: grab `document.documentElement.outerHTML` via CDP, feed to trafilatura, get clean markdown. Zero cost, zero network.
- Sources: [Trafilatura evaluation docs](https://trafilatura.readthedocs.io/en/latest/evaluation.html), [SIGIR 2025 multilingual content-extractor benchmark (PDF)](https://maurelf.users.greyc.fr/docs/conferences/SIGIR_2025_paper_1968.pdf), [ACM: empirical comparison of web content extraction (PDF)](https://dl.acm.org/doi/pdf/10.1145/3539618.3591920)

#### readability (Mozilla Readability / `readability-lxml`)
- **Best at:** The reader-mode algorithm. Extremely robust and *predictable*; highest median F1 (~0.970) and best multilingual consistency in 2025 benchmarks (e.g. Greek 0.962). Available in JS (Mozilla) and Python ports.
- **JS rendering:** None (HTML in → article out).
- **CDP fit (ours):** Great fallback extractor. The Mozilla JS version can even run *inside* the CDP page via `Runtime.evaluate`, so extraction happens in-browser with full post-JS DOM — handy for SPAs. (This is exactly what Jina Reader does internally.)
- **Pairing:** Use trafilatura first, fall back to readability when trafilatura returns too little (they win on different sites/languages).
- Sources: [SIGIR 2025 benchmark (PDF)](https://maurelf.users.greyc.fr/docs/conferences/SIGIR_2025_paper_1968.pdf), [Chuniversiteit: comparing extraction algorithms](https://chuniversiteit.nl/papers/comparison-of-web-content-extraction-algorithms)

#### Jina Reader (`r.jina.ai`) / ReaderLM-v2
- **Best at:** Zero-infrastructure "URL → markdown." Prefix any URL with `https://r.jina.ai/`. Internally: headless Chrome → Mozilla Readability → Turndown, now upgraded with **ReaderLM-v2** (1.5B SLM) for HTML→markdown/JSON on complex pages. Handles PDFs and image captioning; can target CSS selectors.
- **JS rendering:** Full (Jina's headless Chrome on their side).
- **CDP fit (ours):** **Doesn't use our session** — it renders on Jina's infra, so it can't read our logged-in/paywalled tabs. Best as a *fallback for public pages* when local rendering is flaky or not worth standing up. Note the dependency/privacy trade-off (URLs go to Jina). The **ReaderLM-v2 model is open-weight on HuggingFace**, so we could run the HTML→markdown model *locally* on our own CDP-rendered HTML if we want a learned cleaner.
- Sources: [Jina Reader API](https://jina.ai/reader/), [ReaderLM-v2 announcement](https://jina.ai/news/readerlm-v2-frontier-small-language-model-for-html-to-markdown-and-json/), [reader-lm-1.5b on HuggingFace](https://huggingface.co/jinaai/reader-lm-1.5b)

#### MarkItDown (`microsoft/markitdown`)
- **Best at:** Converting *non-HTML* documents to clean markdown for LLMs: PDF, DOCX, PPTX, XLSX/XLS, images (with optional vision-LLM captions), audio (transcription), HTML, ZIP. Plugin architecture; optional OCR and Azure Document Intelligence for hard PDFs.
- **JS rendering:** N/A (not a web renderer; it eats files/bytes).
- **CDP fit (ours):** Complementary, not competing. When a page links to a PDF/spreadsheet/deck (very common for SDR/research targets), download via the CDP session's cookies, hand the bytes to MarkItDown. Fills the gap trafilatura/readability can't.
- Sources: [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown), [Real Python: MarkItDown](https://realpython.com/python-markitdown/), [InfoWorld: MarkItDown](https://www.infoworld.com/article/3963991/markitdown-microsofts-open-source-tool-for-markdown-conversion.html)

### Agentic browsers (interaction, not just reading)

#### browser-use (`browser-use/browser-use`)
- **Best at:** Agent-first, goal-driven automation in Python. You give a natural-language goal; it loops observe→decide→act→reassess. SOTA ~89.1% on WebVoyager. Switched to **raw CDP in 2025** for speed.
- **JS rendering:** Full.
- **CDP fit (ours):** Good — `cdp_url="http://localhost:9222"` (or `127.0.0.1:9222`) attaches to an existing Chrome. **Watch out:** Chrome ≥ v136 refuses CDP driving on the *default* `--user-data-dir`; our dedicated `~/.chrome-debug-x` profile sidesteps that (it's a non-default dir), and Chrome only allows remote debugging on `127.0.0.1`.
- **Use it when:** The task is *do something* (log-in walls already passed, click through a wizard, fill a form), not *read this page*. Overkill (and LLM-cost-heavy) for plain content extraction.
- Sources: [browser-use all parameters](https://docs.browser-use.com/open-source/customize/browser/all-parameters), [Issue #1520: Chrome v136 + default profile CDP](https://github.com/browser-use/browser-use/issues/1520), [Skyvern: Browser Use vs Stagehand](https://www.skyvern.com/blog/browser-use-vs-stagehand-which-is-better/)

#### Stagehand (`browserbase/stagehand`)
- **Best at:** Deterministic-first, TypeScript. Write normal Playwright for known steps; call AI helpers (`act`/`extract`/`observe`) only for the dynamic/unknown bits. Great DX. **v3 went CDP-native** (dropped the Playwright dependency, ~44% faster on complex DOM).
- **JS rendering:** Full.
- **CDP fit (ours):** Workable but rougher. `localBrowserLaunchOptions` accepts a `cdpUrl`, and community MCP forks add "connect to existing visible Chrome via CDP." **Known sharp edge:** passing a Playwright page obtained from your own `connectOverCDP` into Stagehand can throw `StagehandInitError` (V3 page-mapping) — use Stagehand's own `cdpUrl` path rather than hand-rolling the page. TS-first, so a fit only if that lane is TS.
- **Use it when:** You want scripted, mostly-deterministic flows with AI only at the seams, in a TS codebase.
- Sources: [Stagehand browser config docs](https://docs.stagehand.dev/v3/configuration/browser), [Issue #1392: V3 page from connectOverCDP](https://github.com/browserbase/stagehand/issues/1392), [Scrapfly: Stagehand vs Browser Use](https://scrapfly.io/blog/posts/stagehand-vs-browser-use)

---

## Quick comparison

| Tool | Role | JS render | Reuses our logged-in `:9222`? | Local & free? |
|---|---|---|---|---|
| **Playwright** | Driver primitive | Full | Yes (`connectOverCDP`) | Yes |
| **Crawl4AI** | Driver + extractor | Full | Yes (`cdp_url`) | Yes (+ your LLM keys if used) |
| **chrome-devtools-mcp** | Driver via MCP | Full | Yes (`--browser-url`) | Yes |
| **Firecrawl** | Hosted scrape→md | Full | No (its own infra) | Self-host = run a fleet; else SaaS |
| **trafilatura** | Extractor | None | N/A (eats our HTML) | Yes |
| **readability** | Extractor | None (JS ver can run in-page) | via in-page eval | Yes |
| **Jina Reader** | Hosted URL→md | Full (Jina side) | No | Model open-weight; API is hosted |
| **MarkItDown** | File→md | N/A | Uses our cookies to fetch files | Yes |
| **browser-use** | Agentic (act) | Full | Yes (`cdp_url`) | Yes (+ LLM cost) |
| **Stagehand** | Agentic (act), TS | Full | Partial (`cdpUrl`; gotchas) | Yes (+ LLM cost) |

---

## Recommended stack for OpenGoldSDR / Grok Go

We already drive a logged-in Chrome on `:9222` — that's the expensive, fragile part of robust scraping, and it's done. Build the reader *on top of it*:

**Default reader path (free, local, no extra browser):**
1. **Render** in our existing CDP Chrome (`chrome-login` skill / `~/agent-bridge/cdp_*.js`). Navigate the target tab, wait for network idle / a content selector.
2. **Get HTML** post-JS: `document.documentElement.outerHTML` via CDP `Runtime.evaluate`.
3. **Extract** with **trafilatura** → markdown. If the output is empty/too short, **fall back to readability** (run Mozilla Readability in-page via CDP eval to capture SPA-rendered DOM, or `readability-lxml` on the HTML).
4. **Linked documents** (PDF/DOCX/XLSX/PPTX): download through the session's cookies, convert with **MarkItDown**.

**One-dependency alternative:** Use **Crawl4AI** with `BrowserConfig(cdp_url="http://127.0.0.1:9222")` to do steps 1–3 in a single Python lib (it attaches to our Chrome *and* runs content-filter→markdown). Pick this if you'd rather maintain one package than wire Playwright + trafilatura yourself.

**If Grok Go agents speak MCP:** add **chrome-devtools-mcp** with `--browser-url=http://127.0.0.1:9222` to expose our `:9222` Chrome to agents as a tool with near-zero glue.

**Public-page fallback (no session needed):** **Jina Reader** (`https://r.jina.ai/<url>`) when local rendering is flaky and the page isn't behind our login. (Be aware the URL is sent to Jina; for a private variant, run **ReaderLM-v2** locally on our own CDP-rendered HTML.)

**Interaction lane (not reading):** when a task needs multi-step clicking/form-filling, use **browser-use** (Python, agent-first, `cdp_url` → our `:9222`; our non-default `~/.chrome-debug-x` profile avoids the Chrome ≥136 default-profile CDP block). Reserve **Stagehand** for TS-side deterministic flows, mindful of the V3 `connectOverCDP` page-mapping gotcha.

**What we are *not* adopting as core:** **Firecrawl** — its whole pitch (render on someone else's infra) conflicts with our reuse-the-logged-in-`:9222`-Chrome goal, and self-hosting it means operating the very browser fleet we already get for free. Keep it as an optional knob for large public-web crawls only.

---

## Sources

- Crawl4AI vs Firecrawl — [Brightdata](https://brightdata.com/blog/ai/crawl4ai-vs-firecrawl), [Capsolver](https://www.capsolver.com/blog/AI/crawl4ai-vs-firecrawl)
- Crawl4AI docs — [browser/crawler config](https://docs.crawl4ai.com/core/browser-crawler-config/), [identity-based crawling](https://docs.crawl4ai.com/advanced/identity-based-crawling/)
- Firecrawl — [GitHub](https://github.com/firecrawl/firecrawl), [SELF_HOST.md](https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md), [open-source/self-host FAQ](https://webscraping.ai/faq/firecrawl/is-firecrawl-open-source-and-can-i-self-host-it)
- Playwright — [BrowserType API](https://playwright.dev/docs/api/class-browsertype), [connect to existing browser (BrowserStack)](https://www.browserstack.com/guide/playwright-connect-to-existing-browser), [10+ agents on one logged-in browser](https://www.agentpmt.com/articles/how-to-run-10-playwright-agents-on-one-logged-in-browser-without-getting-blocked)
- trafilatura / readability benchmarks — [SIGIR 2025 multilingual benchmark (PDF)](https://maurelf.users.greyc.fr/docs/conferences/SIGIR_2025_paper_1968.pdf), [Trafilatura evaluation](https://trafilatura.readthedocs.io/en/latest/evaluation.html), [ACM empirical comparison (PDF)](https://dl.acm.org/doi/pdf/10.1145/3539618.3591920), [Chuniversiteit comparison](https://chuniversiteit.nl/papers/comparison-of-web-content-extraction-algorithms)
- Jina Reader — [Reader API](https://jina.ai/reader/), [ReaderLM-v2](https://jina.ai/news/readerlm-v2-frontier-small-language-model-for-html-to-markdown-and-json/), [reader-lm-1.5b weights](https://huggingface.co/jinaai/reader-lm-1.5b)
- MarkItDown — [GitHub](https://github.com/microsoft/markitdown), [Real Python](https://realpython.com/python-markitdown/), [InfoWorld](https://www.infoworld.com/article/3963991/markitdown-microsofts-open-source-tool-for-markdown-conversion.html)
- browser-use — [all parameters](https://docs.browser-use.com/open-source/customize/browser/all-parameters), [Chrome v136 default-profile CDP issue](https://github.com/browser-use/browser-use/issues/1520), [Browser Use vs Stagehand (Skyvern)](https://www.skyvern.com/blog/browser-use-vs-stagehand-which-is-better/)
- Stagehand — [browser config docs](https://docs.stagehand.dev/v3/configuration/browser), [V3 connectOverCDP page issue #1392](https://github.com/browserbase/stagehand/issues/1392), [Stagehand vs Browser Use (Scrapfly)](https://scrapfly.io/blog/posts/stagehand-vs-browser-use)
- chrome-devtools-mcp — [GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp), [npm](https://www.npmjs.com/package/chrome-devtools-mcp)
