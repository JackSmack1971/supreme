---
title: "Finding 2 — Auto mode is useful but probabilistic"
summary: "Imported unverified source material from Containment, Auto Mode, Network, and Change-Surface Addendum; verification remains pending."
as_of: 2026-10-02
last_verified: 2026-10-02
reverify_by: 2026-11-01
status: partial
confidence: low
volatility: volatile
sources:
  - id: S1
    url: "https://www.anthropic.com/engineering/claude-code-auto-mode"
    accessed: 2026-10-02
    locator: "How it works, lines 23-29; Results, lines 78-95; Deny-and-continue, lines 127-130"
  - id: S2
    url: "https://www.anthropic.com/engineering/how-we-contain-claude"
    accessed: 2026-10-02
    locator: "Pattern 2, lines 53-60; user injection exercise, lines 66-68; overview, lines 23-25"
  - id: S3
    url: "https://code.claude.com/docs/en/desktop"
    accessed: 2026-10-02
    locator: "Permission modes and Auto mode availability, lines 207-227"
  - id: S4
    url: "https://code.claude.com/docs/en/permissions"
    accessed: 2026-10-02
    locator: "Permissions documentation, permission modes and rules"
  - id: S5
    url: "https://code.claude.com/docs/en/security"
    accessed: 2026-10-02
    locator: "Security documentation, built-in protections and prompt injection safeguards"
  - id: S6
    url: "https://www.anthropic.com/engineering/claude-code-sandboxing"
    accessed: 2026-10-02
    locator: "Article title and publication date, lines 13-19; sandbox isolation, lines 30-45"
  - id: S7
    url: "https://depot-e.uqtr.ca/8430/1/032072458.pdf"
    accessed: 2026-10-02
    locator: "Boucher and Badri, Introduction, lines 3329-3334; validity limitations, lines 9008-9013"
  - id: S8
    url: "https://code.claude.com/docs/en/hooks"
    accessed: 2026-10-02
    locator: "Hook events, lines 180-194; PreToolUse can block before execution, lines 191-193"
  - id: S9
    url: "https://git-scm.com/docs/git-status"
    accessed: 2026-10-02
    locator: "Description of working tree and index changes, lines 231-240"
  - id: S10
    url: "https://git-scm.com/docs/git-diff"
    accessed: 2026-10-02
    locator: "Description and options for comparing changes"
  - id: S11
    url: "https://code.claude.com/docs/en/sandboxing"
    accessed: 2026-10-02
    locator: "Sandbox platform support, lines 81-85; default boundaries, lines 95-104"
  - id: S0
    url: "legacy/Containment, Auto Mode, Network, and Change-Surface Addendum.md"
    accessed: 2026-10-02
    locator: "Finding 2 — Auto mode is useful but probabilistic"
origin: "legacy/Containment, Auto Mode, Network, and Change-Surface Addendum.md#Finding 2 — Auto mode is useful but probabilistic"
tags: [imported, unverified]
aliases: []
related: []
---
## Answer
Imported material; unverified content is explicitly tagged below. [UNVERIFIED]

## Conditions
Original source text is preserved below without factual review. [UNVERIFIED]

## Detail
7. **Cost/context implications:** Less interruption and approval fatigue; isolation/network configuration adds setup cost. [VERIFIED 2026-10-02 S1,S2,S6]
8. **Security implications:** Approval fatigue can reduce attention to individual approval prompts and weaken oversight. [VERIFIED 2026-10-02 S1,S2]
9. **Open question remaining:** What default containment/permission combination best serves novice Windows users? [UNVERIFIED]

### Finding 2 — Auto mode is useful but probabilistic

1. **Finding:** Auto mode reduces prompt burden and can catch overeager behavior, but a model classifier has a non-zero miss rate. [VERIFIED 2026-10-02 S1,S2]
2. **Evidence/source:** Anthropic, “How we built Claude Code auto mode” (March 25, 2026) and “How we contain Claude across products” (May 25, 2026). [VERIFIED 2026-10-02 S1,S2]
3. **Evidence strength:** Strong, Tier 1. [UNVERIFIED]
4. **Claude Code mechanism implicated:** Permission mode `auto`, documented Auto-mode configuration, classifier-based approval, prompt-injection probe. [VERIFIED 2026-10-02 S1,S3]
5. **Global `~/.claude` candidate?** Conditional; availability varies by plan/model/provider and supported settings scope. [UNVERIFIED]
6. **Enforcement:** Probabilistic classifier inside deterministic outer boundaries; human escalation for high-impact ambiguity. [VERIFIED 2026-10-02 S1,S2]
7. **Cost/context implications:** Fewer user interruptions; classifier checks add service-side work but common safe actions are optimized for fast passage. [VERIFIED 2026-10-02 S1]
8. **Security implications:** Safer than unrestricted bypass, but not a substitute for sandboxing, narrow credentials, or static denies. [VERIFIED 2026-10-02 S1,S2]
9. **Open question remaining:** Should Supreme recommend Auto mode where available, and what fallback should apply where unavailable? [UNVERIFIED]

### Finding 3 — Filesystem, network, and credential boundaries are jointly necessary

1. **Finding:** Strong high-autonomy containment requires jointly restricting filesystem reach, network egress, and credential exposure. [REPORTED S2]
2. **Evidence/source:** Anthropic's sandboxing and containment engineering reports, including the controlled AWS-credential exfiltration result. [VERIFIED 2026-10-02 S2]
3. **Evidence strength:** Strong, Tier 1. [UNVERIFIED]
4. **Claude Code mechanism implicated:** Sandbox filesystem/network controls, environment design, permission rules, connector/tool scopes. [UNVERIFIED]
5. **Global `~/.claude` candidate?** Conditional; the principle is global, enforcement is environment-dependent. [UNVERIFIED]
6. **Enforcement:** Deterministic sandbox/proxy/environment policy where available; human approval to expand egress or secret exposure. [UNVERIFIED]
7. **Cost/context implications:** Added setup friction and occasional blocked network flows; large reduction in potential blast radius. [UNVERIFIED]
8. **Security implications:** Critical for prompt injection, credential theft, and compromised subprocesses. [UNVERIFIED]
9. **Open question remaining:** What Windows-native fallback can provide comparable guarantees without WSL2/VM/container isolation? [UNVERIFIED]

### Finding 4 — Change-size policy should be deviation-based, not numerical

1. **Finding:** Unexpected scope expansion is a stronger safety signal than crossing a universal file/line threshold. [UNVERIFIED]
2. **Evidence/source:** Anthropic's Auto mode report discusses authorization boundaries; a 2018 fault-proneness study states that proposed software-metric thresholds cannot be generalized to all projects, while not evaluating agent change-size policies. [VERIFIED 2026-10-02 S1,S7]
3. **Evidence strength:** Moderate-to-strong. [UNVERIFIED]
4. **Claude Code mechanism implicated:** Change map, Git diff/status, task-local allowed/protected paths, `PreToolUse`, review/completion gates. [UNVERIFIED]
5. **Global `~/.claude` candidate?** Yes for the invariant “detect material deviation”; no for global numeric caps. [UNVERIFIED]
6. **Enforcement:** Deterministic path/diff checks where representable; human/model review for semantic scope expansion. [UNVERIFIED]
7. **Cost/context implications:** Low when based on summarized Git state; avoids false positives and metric gaming. [UNVERIFIED]
8. **Security implications:** Helps detect unrelated rewrites, unexpected dependency/migration edits, and unauthorized deletions. [UNVERIFIED]
9. **Open question remaining:** How should the expected change surface be refreshed after legitimate new discoveries? [UNVERIFIED]

### Finding 5 — Deny-and-continue is preferable to unnecessary interruption when a safe alternative exists

1. **Finding:** A blocked action need not always become a human prompt; letting the agent find a safer path can preserve autonomy while respecting the boundary. [VERIFIED 2026-10-02 S1]
2. **Evidence/source:** Anthropic Auto-mode deny-and-continue design; three consecutive denials or 20 total denials stop the model and escalate, while headless mode terminates. [VERIFIED 2026-10-02 S1]
3. **Evidence strength:** Strong for the product design; moderate for generalization to Supreme's future custom controls. [UNVERIFIED]
4. **Claude Code mechanism implicated:** Auto mode, permission denial results, `PreToolUse`, human escalation. [UNVERIFIED]
5. **Global `~/.claude` candidate?** Conditional. [UNVERIFIED]
6. **Enforcement:** Deterministic/probabilistic denial depending layer; human approval only after repeated or consequential failure. [UNVERIFIED]
7. **Cost/context implications:** Reduces false-positive interruptions; may add one or more retry turns. [UNVERIFIED]
8. **Security implications:** Safer than asking the user to override every denied action; requires anti-circumvention rules so the agent does not route around a boundary. [UNVERIFIED]
9. **Open question remaining:** Which denial patterns should immediately stop versus permit a safer retry? [UNVERIFIED]

## A. Design requirements derived from the evidence

1. Prefer hard environmental containment over high-frequency permission prompting where supported. [UNVERIFIED]
2. Treat Auto mode as an experimental probabilistic supervision layer, never as deterministic containment. [UNVERIFIED]
3. Detect Auto-mode availability and supported configuration instead of assuming it. [UNVERIFIED]
4. Minimize credential exposure to the agent; prefer scoped/proxied/short-lived authority. [UNVERIFIED]
5. Couple filesystem isolation with network egress restrictions for high-autonomy or untrusted work where possible. [UNVERIFIED]
6. Treat expansion of network access or secret exposure as a consequential action requiring policy or human authorization. [UNVERIFIED]
7. Derive task-local expected/protected change surfaces from reconnaissance. [UNVERIFIED]
8. Detect scope deviation relative to that surface rather than imposing universal maximum diff size. [UNVERIFIED]
9. Re-run reconnaissance when legitimate discoveries materially expand the change surface. [UNVERIFIED]
10. Prefer deny-and-continue when a safe alternative exists; escalate repeated or consequential denial patterns. [UNVERIFIED]
11. Keep bypass-permissions modes out of novice defaults unless the execution environment is genuinely isolated. [UNVERIFIED]
12. On native Windows, Claude Code runs commands unsandboxed; its built-in Bash sandbox is documented for macOS, Linux, and WSL2. [VERIFIED 2026-10-02 S11]

## B. Anti-requirements

Supreme should **not**: [UNVERIFIED]

- treat Auto mode or any classifier as a hard security boundary; [UNVERIFIED]
- rely on repeated approval prompts as the primary containment mechanism; [UNVERIFIED]
- expose broad long-lived credentials when narrower authority is practical; [UNVERIFIED]
- allow unrestricted egress for high-autonomy/untrusted work merely for convenience; [UNVERIFIED]
- assume a user will notice model drift quickly enough to serve as the only safety layer; [UNVERIFIED]
- use `--dangerously-skip-permissions` as a novice default on an unrestricted host; [UNVERIFIED]
- hard-code a universal maximum file count, changed-line count, diff size, or complexity threshold; [UNVERIFIED]
- treat a project-wide static file allowlist as equivalent to a task-specific authorized change surface; [UNVERIFIED]
- let a blocked agent route around a safety boundary simply to achieve the same prohibited side effect by another tool. [UNVERIFIED]

## C. Unresolved questions

1. Should Supreme recommend Auto mode whenever available, or prefer sandbox + narrower deterministic permissions for novice defaults? [UNVERIFIED]
2. What policy should apply on plans/providers where Auto mode is unavailable? [UNVERIFIED]
3. What Windows-native mechanism, if any, can provide robust egress and credential isolation without WSL2/VM/container use? [UNVERIFIED]
4. How should expected/protected file sets refresh when legitimate implementation discoveries expand scope? [UNVERIFIED]
5. When should repeated denials terminate work versus escalate to a human? [UNVERIFIED]
6. How should Supreme distinguish a harmless new development dependency from a meaningful supply-chain expansion? [UNVERIFIED]
7. Can network/credential policy be enforced portably enough from a primarily `~/.claude`-based control plane, or must high-assurance containment live outside `.claude`? [UNVERIFIED]
8. How should external MCP/connector capabilities be reduced to least privilege without making common workflows unusable? [UNVERIFIED]

## D. Sources

### Tier 1 — Anthropic / Claude Code

- [Claude Code Desktop](https://code.claude.com/docs/en/desktop) — official documentation describing permission modes and Auto mode availability. [VERIFIED 2026-10-02 S3]
- [Configure permissions](https://code.claude.com/docs/en/permissions) — official Claude Code permissions documentation. [VERIFIED 2026-10-02 S4]
- [Security](https://code.claude.com/docs/en/security) — official Claude Code security documentation covering built-in protections and prompt-injection safeguards. [VERIFIED 2026-10-02 S5]
- [Anthropic, “Beyond permission prompts: making Claude Code more secure and autonomous”](https://www.anthropic.com/engineering/claude-code-sandboxing) — published October 20, 2025. [VERIFIED 2026-10-02 S6]
- [Anthropic, “How we built Claude Code auto mode: a safer way to skip permissions”](https://www.anthropic.com/engineering/claude-code-auto-mode) — published March 25, 2026. [VERIFIED 2026-10-02 S1]
- [Anthropic, “How we contain Claude across products”](https://www.anthropic.com/engineering/how-we-contain-claude) — published May 25, 2026. [VERIFIED 2026-10-02 S2]
- [Hooks reference](https://code.claude.com/docs/en/hooks) — official documentation says `PreToolUse` runs before a tool call and can block it. [VERIFIED 2026-10-02 S8]
- [Git status](https://git-scm.com/docs/git-status) and [Git diff](https://git-scm.com/docs/git-diff) — primary command references for viewing working-tree state and changes. [VERIFIED 2026-10-02 S9,S10]
- [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing) — official docs identify macOS, Linux, and WSL2 support and state that native Windows commands run unsandboxed. [VERIFIED 2026-10-02 S11]

### Existing Supreme evidence reused

- `Evidence-Backed Brownfield Reconnaissance and Change Containment.md` — repository-state, change-map, evidence-sufficiency, worktree/checkpoint/hook/permissions foundation. [UNVERIFIED]
- [Boucher and Badri, “Software metrics thresholds calculation techniques to predict fault-proneness: An empirical comparison”](https://depot-e.uqtr.ca/8430/1/032072458.pdf) — the study warns that thresholds cannot be generalized to all projects, but studies fault-proneness metrics rather than agent change-size policies. [VERIFIED 2026-10-02 S7]

## Corpus impact

This addendum closes the named gaps from the research brief around: [UNVERIFIED]

- Auto mode status and limitations; [UNVERIFIED]
- Anthropic's overeager-action incident evidence; [UNVERIFIED]
- containment versus repeated permission prompting; [UNVERIFIED]
- network egress and secrets boundaries; [UNVERIFIED]
- allowed/protected task-local file surfaces; [UNVERIFIED]
- maximum-change-size policy; [UNVERIFIED]
- deny-and-continue behavior; [UNVERIFIED]
- the relationship between probabilistic supervision and deterministic containment. [UNVERIFIED]

The remaining brownfield questions are now predominantly **implementation/runtime questions**, especially native-Windows containment, portable hook health, state freshness across concurrent actors, and the representation of task-local authorized change surfaces. [UNVERIFIED]

## Dead Ends

## Open Questions
