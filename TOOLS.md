# Tool and MCP Capability Index

Snapshot observed from the active tool catalog on 2026-10-02. Availability and permissions can vary by session; refresh this inventory when the catalog changes.

## Direct tools

| tool | best use | verified-on date |
|---|---|---|
| `functions.exec` / `exec_command` | Run repository commands and orchestrate bounded tool calls | 2026-10-02 |
| `functions.apply_patch` | Make focused repository edits | 2026-10-02 |
| `functions.view_image` | Inspect a local image | 2026-10-02 |
| `functions.web__run` | Web search, source retrieval, and current information | 2026-10-02 |
| `functions.image_gen__imagegen` | Generate or edit images | 2026-10-02 |
| `clock` | Read or wait on UTC time | 2026-10-02 |
| `mcp__cua_repl` | Automate browser UI when an API/connector is unavailable | 2026-10-02 |

## MCP servers

| server / namespace | exposed tools | best use | verified-on date |
|---|---:|---|---|
| `codex_apps` — Canva | 40 | Canva designs, assets, templates, and editing | 2026-10-02 |
| `codex_apps` — Context7 | 2 | Current library and framework documentation | 2026-10-02 |
| `codex_apps` — Exa | 2 | Web search and page fetching | 2026-10-02 |
| `codex_apps` — Finance Data | 83 | CBOE, crypto, FX, macroeconomic, SEC, flights, and prediction-market data | 2026-10-02 |
| `codex_apps` — GitHub | 89 | Repository, issue, pull request, review, and workflow operations | 2026-10-02 |
| `codex_apps` — Higgsfield | 99 | Image, video, audio, website, and marketing workflows | 2026-10-02 |
| `codex_apps` — Linear | 74 | Issues, projects, documents, teams, and review workflows | 2026-10-02 |
| `codex_apps` — Render | 22 | Render services, deploys, logs, databases, and configuration | 2026-10-02 |
| `codex_apps` — Sites | 25 | Site hosting, deployment, domains, versions, and site data | 2026-10-02 |
| `codex_apps` — other connectors | 51 | Document control, Massive market data, Hotline, OpenAI Platform, pets, plugin management, family settings, and tldraw | 2026-10-02 |
| `codex_tui` | 9 | Inspect and manage Codex threads | 2026-10-02 |
| `coingecko` | 2 | CoinGecko market data and documentation | 2026-10-02 |
| `context7` | 2 | Current library/framework documentation lookup | 2026-10-02 |
| `massive` | 4 | Market data endpoint discovery, retrieval, and workspace queries | 2026-10-02 |
| `node_repl` | 3 | Persistent JavaScript execution and module-directory setup | 2026-10-02 |
| `openai_api_key_local_confirmation` | 1 | Confirm a local destination before creating/writing an OpenAI key | 2026-10-02 |

Counts are tool definitions grouped from the active catalog; they do not indicate account entitlement or successful access to every operation. The 51 `other connectors` tools are codex document control (3), Massive (4), OpenAI Platform (4), pets (11), plugin creator (7), plugin management (6), Hotline (1), family settings (5), and tldraw (10).

## Repository tools

| tool | best use | verified-on date |
|---|---|---|
| `scripts/validate_repo.py` | Check caretaker frontmatter, headings, claim tags, links, index sync, dates, size, and likely secrets | 2026-10-02 |
| `scripts/claim_spot_check.py` | Select a deterministic session sample of source-linked `[VERIFIED]` claims for agent re-fetch and review | 2026-10-02 |
