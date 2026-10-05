---
title: "Finding 2 — Auto mode is useful but probabilistic"
summary: "Claude Code Auto mode evidence, limitations, containment context, and explicitly unverified recommendations."
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
  - id: S12
    url: "https://code.claude.com/docs/en/permission-modes"
    accessed: 2026-10-02
    locator: "Which mode a session starts in; Eliminate prompts with auto mode; When auto mode falls back; Repeated-block thresholds"
  - id: S13
    url: "https://claude.com/blog/auto-mode"
    accessed: 2026-10-02
    locator: "Date March 24, 2026; update banner dated July 10, 2026; Getting started"
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
Auto mode reduces approval prompts but remains a probabilistic supervision layer that can miss unsafe actions. [VERIFIED 2026-10-02 S1,S2]

## Conditions
These claims describe Claude Code and the cited Anthropic reports and documentation as fetched on 2026-10-02. Product availability varies by surface and settings scope. [VERIFIED 2026-10-02 S1,S3]

## Detail
### Verified claims
- C01: Auto mode reduces approval prompts. (locator: lines 17, 23) [VERIFIED 2026-10-02 S1]
- C02: Auto mode can miss unsafe actions. (locator: S1 lines 78-95; S2 lines 23-25) [VERIFIED 2026-10-02 S1,S2]
- C03: Auto mode delegates approvals to model-based classifiers. (locator: lines 23-29) [VERIFIED 2026-10-02 S1]
- C04: Auto mode probes tool outputs for prompt injection. (locator: lines 26-30) [VERIFIED 2026-10-02 S1]
- C07: The full Auto mode pipeline had a 17% false-negative rate on 52 real overeager-action examples. (locator: lines 78-95) [VERIFIED 2026-10-02 S1]
- C08: The full Auto mode pipeline had a 0.4% false-positive rate on benign real-traffic actions. (locator: lines 78-90) [VERIFIED 2026-10-02 S1]
- C10: Anthropic cautions that Auto mode is not a replacement for careful high-stakes human review. (locator: lines 94-95) [VERIFIED 2026-10-02 S1]
- C11: Anthropic reported successful credential exfiltration in 24 of 25 controlled retries. (locator: lines 66-70) [VERIFIED 2026-10-02 S2]
- C12: Environmental egress controls and filesystem boundaries can block exfiltration independently of model intent. (locator: lines 36-44, 67-68) [VERIFIED 2026-10-02 S2]
- C14: The described macOS/Linux sandbox permits workspace writes and denies network access by default. (locator: lines 57-59) [VERIFIED 2026-10-02 S2]
- C18: Anthropic reported users approved roughly 93% of permission prompts. (locator: S1 lines 17-20; S2 lines 23-24) [VERIFIED 2026-10-02 S1,S2]
- C19: Anthropic reported sandboxing reduced permission prompts by 84%. (locator: lines 57-60) [VERIFIED 2026-10-02 S2]
- C21: The cited study warns that fault-proneness metric thresholds do not generalize uniformly. (locator: lines 3329-3334) [VERIFIED 2026-10-02 S7]
- C23: Claude Code PreToolUse hooks can block actions before execution. (locator: lines 180-194) [VERIFIED 2026-10-02 S8]
- C29: Auto mode returns a blocked action as a tool result that can enable a safer retry. (locator: lines 125-130) [VERIFIED 2026-10-02 S1]
- C30: Corrected: auto mode pauses after three consecutive or twenty total denials and Claude Code resumes prompting; a non-interactive `-p` run without a `--permission-prompt-tool` does not stop the run. (locator: "When auto mode falls back") [VERIFIED 2026-10-02 S12]
- C34: Auto mode uses classifier review, permission results, and denial escalation. (locator: lines 23-29, 127-130) [VERIFIED 2026-10-02 S1]
- C39: Anthropic describes permission bypass as high risk and suitable only for isolated environments. (locator: S1 lines 19-20; S3 lines 214-216) [VERIFIED 2026-10-02 S1,S3]
- C41: The cited Configure permissions page is official Claude Code documentation. (locator: page title and content) [VERIFIED 2026-10-02 S4]
- C42: The cited Security page covers built-in protections and prompt-injection safeguards. (locator: lines 54-85) [VERIFIED 2026-10-02 S5]
- C43: Anthropic’s “Beyond permission prompts: making Claude Code more secure and autonomous” article was published October 20, 2025. (locator: lines 13-17) [VERIFIED 2026-10-02 S6]
- C44: Anthropic reports repeated permission prompts can cause approval fatigue. (locator: S1 lines 17-20; S2 lines 23-24) [VERIFIED 2026-10-02 S1,S2]
- C45: Sandboxing and network controls require configuration that adds setup or maintenance work. (locator: S1 lines 19-20; S6 lines 17-19) [VERIFIED 2026-10-02 S1,S6]
- C46: Rubber-stamp approvals can create oversight without sustained attention to each prompt. (locator: S1 lines 17-20; S2 lines 23-24) [VERIFIED 2026-10-02 S1,S2]
- C47: Auto mode uses server-side classifier and probe checks for actions and tool outputs. (locator: lines 26-29) [VERIFIED 2026-10-02 S1]
- C48: Auto mode optimizes common safe in-project writes for fast passage. (locator: lines 48-55) [VERIFIED 2026-10-02 S1]
- C49: Claude Code’s Bash sandbox supports macOS, Linux, and WSL2; native Windows commands run unsandboxed. (locator: lines 81-85) [VERIFIED 2026-10-02 S11]

### Atomic splits of partly verified claims

- C05 supported: Auto mode availability varies by product surface and supported settings scope. (locator: lines 207-227) [VERIFIED 2026-10-02 S3]
- C05 remainder resolved: auto mode availability is documented as depending on plan, model, provider, and organization setting, with all plans qualifying and Team and Enterprise administrators able to disable it. (locator: "Eliminate prompts with auto mode") [VERIFIED 2026-10-02 S12]
- C13 supported: Anthropic describes layered containment controls for filesystem, network, and credentials. (locator: lines 36-44, 67-68) [VERIFIED 2026-10-02 S2]
- C13 remainder: The source does not state that every deployment universally requires all three restrictions. [UNVERIFIED]
- C16 supported: Documented Auto mode availability differs across supported product surfaces and settings scopes. (locator: lines 207-227) [VERIFIED 2026-10-02 S3]
- C16 remainder: The source does not establish a general rule covering configuration enforcement in every environment. [UNVERIFIED]
- C17 supported: Anthropic’s examples ground permission decisions in user authorization and environment boundaries. (locator: S1 lines 63-65; S2 lines 36-44) [VERIFIED 2026-10-02 S1,S2]
- C17 remainder: The sources do not state that every egress or secret-exposure expansion universally requires human approval. [UNVERIFIED]
- C20 supported: The cited study cautions that software-metric thresholds do not generalize uniformly across projects. (locator: lines 3329-3334) [VERIFIED 2026-10-02 S7]
- C20 remainder: The study does not compare deviation signals with universal file or line thresholds for agent safety. [UNVERIFIED]
- C22 supported: Anthropic’s Auto mode examples discuss authorization boundaries and scope escalation. (locator: lines 40-45, 63-65) [VERIFIED 2026-10-02 S1]
- C22 remainder: The examples do not directly prescribe Supreme’s expected-change-scope workflow. [UNVERIFIED]
- C24 supported: Git documents commands for viewing working-tree status and differences. (locator: S9 lines 231-240; S10 description) [VERIFIED 2026-10-02 S9,S10]
- C24 remainder: The cited Git manuals do not document task-local path sets as a product mechanism. [UNVERIFIED]
- C25 supported: Anthropic evaluates classifier decisions on examples involving authorization boundaries. (locator: lines 40-45, 63-65) [VERIFIED 2026-10-02 S1]
- C25 remainder: The source does not establish that human or model review generally detects semantic scope expansion. [UNVERIFIED]
- C28 supported: Anthropic’s examples include unauthorized deletion and scope escalation. (locator: lines 40-45) [VERIFIED 2026-10-02 S1]
- C28 remainder: The source does not cover every listed unrelated rewrite, dependency change, or migration case. [UNVERIFIED]
- C31 supported: Auto mode returns a denied action as a tool result and permits a safer retry. (locator: lines 125-130) [VERIFIED 2026-10-02 S1]
- C31 remainder: The source does not measure a reduction in total user interruptions from deny-and-continue. [UNVERIFIED]
- C32 supported: Auto mode documents denial results that let Claude try a safer alternative. (locator: lines 127-130) [VERIFIED 2026-10-02 S1]
- C32 remainder: The source does not directly compare this design with asking users to override every denial. [UNVERIFIED]
- C33 supported: Anthropic instructs Auto mode not to route around a denied action. (locator: lines 127-129) [VERIFIED 2026-10-02 S1]
- C33 remainder: A universal requirement for anti-circumvention rules remains a recommendation, not a measured result. [UNVERIFIED]
- C35 supported: Anthropic’s credential-exfiltration example used a VM-provisioned session token. (locator: lines 66-68) [VERIFIED 2026-10-02 S2]
- C35 remainder: The example does not establish scoped, proxied, or short-lived credentials as a universal product requirement. [UNVERIFIED]
- C36 supported: Anthropic describes filesystem isolation combined with network controls as a containment pattern. (locator: lines 36-44, 67-68) [VERIFIED 2026-10-02 S2]
- C36 remainder: The sources do not guarantee that this pattern always reduces blast radius in every deployment. [UNVERIFIED]
- C37 supported: Auto mode distinguishes user authorization from trusted environment configuration. (locator: lines 63-75) [VERIFIED 2026-10-02 S1]
- C37 remainder: The source does not directly compare a project-wide static allowlist with a task-specific change surface. [UNVERIFIED]
- C38 supported: The cited study warns against generalizing software-metric thresholds across projects. (locator: lines 3329-3334) [VERIFIED 2026-10-02 S7]
- C38 remainder: The study does not evaluate fixed file, line, diff, or complexity caps for agent changes. [UNVERIFIED]
- C40 supported: The imported addendum contains sections on Auto mode availability, incidents, containment, change surface, and denial behavior. (locator: legacy source, “Finding 2” and adjacent sections) [VERIFIED 2026-10-02 S0]
- C40 remainder: The presence of those sections does not independently verify the external Claude Code product claims they discuss. [UNVERIFIED]

### Corrected and unverified claims
- C06 corrected: auto mode was a research preview at its March 24, 2026 launch and has been generally available for all users since July 10, 2026. (locator: update banner; "Getting started") [VERIFIED 2026-10-02 S13,S12]
- C26: Summarized Git state makes deviation checks low-cost. [UNVERIFIED]
- C27: Deviation-based policies avoid false positives and metric gaming. [UNVERIFIED]

## Dead Ends
The March 25, 2026 engineering report states that a headless run terminates the process, but current permission-modes documentation states that Claude Code does not stop the run. [VERIFIED 2026-10-02 S1,S12]

## Open Questions
- What default containment and permission combination best serves novice Windows users? [UNVERIFIED]
