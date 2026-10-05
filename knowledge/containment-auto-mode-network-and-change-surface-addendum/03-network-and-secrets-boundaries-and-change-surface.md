---
title: "Claude Code network and secrets boundaries, change surface, and change-size policy"
summary: "Verified sandbox network and credential boundaries, documented change-surface mechanisms, and unsupported change-size policy remainders."
as_of: 2026-10-02
last_verified: 2026-10-02
reverify_by: 2026-11-01
status: partial
confidence: low
volatility: volatile
sources:
  - id: S0
    url: "legacy/Containment, Auto Mode, Network, and Change-Surface Addendum.md"
    accessed: 2026-10-02
    locator: "Network and secrets boundaries; Allowed and denied file sets; Maximum change-size policy"
  - id: S1
    url: "https://www.anthropic.com/engineering/how-we-contain-claude"
    accessed: 2026-10-02
    locator: "Published May 25, 2026; Three types of risk, three components of defense; Pattern 2; Pattern 3; Exfiltration through an approved domain; Agent identity"
  - id: S2
    url: "https://www.anthropic.com/engineering/claude-code-auto-mode"
    accessed: 2026-10-02
    locator: "Published Mar 25, 2026; Threat model; The classifier decision criteria; What the classifier blocks by default"
  - id: S3
    url: "https://code.claude.com/docs/en/sandboxing"
    accessed: 2026-10-02
    locator: "What the sandbox restricts; What runs outside the sandbox; Get started; Protected paths; Filesystem isolation; Network isolation; Protect credentials"
  - id: S4
    url: "https://code.claude.com/docs/en/hooks"
    accessed: 2026-10-02
    locator: "Hook lifecycle table; How a hook resolves; Common fields"
  - id: S5
    url: "https://code.claude.com/docs/en/auto-mode-config"
    accessed: 2026-10-02
    locator: "Where the classifier reads configuration; Define trusted infrastructure; Override the block and allow rules"
  - id: S6
    url: "https://code.claude.com/docs/en/permission-modes"
    accessed: 2026-10-02
    locator: "Available modes; What the classifier blocks by default; Actions no mode auto-approves"
  - id: S7
    url: "https://github.com/anthropics/sandbox-runtime"
    accessed: 2026-10-02
    locator: "README: Dual Isolation Model; Filesystem Configuration; Network Configuration; Windows (alpha)"
  - id: S8
    url: "https://depot-e.uqtr.ca/8430/1/032072458.pdf"
    accessed: 2026-10-02
    locator: "Boucher and Badri, Introduction, lines 3329-3334; verification reused from the Stage V pass on 2026-10-02 rather than re-fetched"
origin: "legacy/Containment, Auto Mode, Network, and Change-Surface Addendum.md#Network and secrets boundaries"
tags: [claude-code, sandboxing, network-egress, credentials, change-surface, verified, partial]
aliases: []
related:
  - "knowledge/containment-auto-mode-network-and-change-surface-addendum/01-containment-auto-mode-network-and-change-surface.md"
  - "knowledge/containment-auto-mode-network-and-change-surface-addendum/02-finding-2-auto-mode-is-useful-but-probabilistic.md"
---
## Answer
Anthropic's sandbox runtime requires filesystem and network isolation together, denies network access by default, and covers macOS, Linux, and WSL2 but not native Windows; the corpus's change-size and change-surface prescriptions remain recommendations rather than documented product behaviour. [VERIFIED 2026-10-02 S3,S7,S1]

## Conditions
These claims describe Claude Code and the cited Anthropic sources as fetched on 2026-10-02. [VERIFIED 2026-10-02 S3]

The code.claude.com documentation pages expose no publication or last-updated date, so each is anchored only by its recorded retrieval date. [VERIFIED 2026-10-02 S3,S4,S5,S6]

The threshold study cited as S8 concerns software fault-proneness metrics and was verified during the Stage V pass on 2026-10-02 rather than re-fetched for this file. [UNKNOWN]

## Detail
## Network and secrets boundaries

Strong containment requires **filesystem and network controls together**. [VERIFIED 2026-10-02 S7,S1,S3]

Filesystem isolation without egress control can still allow accessible credentials to be exfiltrated. [VERIFIED 2026-10-02 S7,S3]

Network restriction without filesystem isolation can still expose secrets and host state to the agent or to a compromised subprocess. [VERIFIED 2026-10-02 S3,S1]

Anthropic's sandboxing architecture explicitly couples both. [VERIFIED 2026-10-02 S1,S3,S7]

Supreme requirements:

- keep credentials that are not required for the task outside the agent's reachable environment where feasible; [VERIFIED 2026-10-02 S1]
- use narrowly scoped credentials, short-lived tokens, or proxy-mediated access instead of broad long-lived credentials when practical; [VERIFIED 2026-10-02 S1]
- treat `.env` files, cloud profiles, SSH keys, signing material, package-publishing credentials, and user-home credential stores as sensitive boundaries; [VERIFIED 2026-10-02 S3,S5,S2]
- block or escalate broad credential discovery such as grepping environment variables or home-directory config after an authentication failure; [VERIFIED 2026-10-02 S2,S5]
- prefer deny-by-default or allowlisted outbound network access for high-autonomy/untrusted work where the execution environment can enforce it; [VERIFIED 2026-10-02 S3,S7]
- require human escalation before materially expanding egress or exposing new secrets to the agent; [UNVERIFIED]
- preserve the existing always-escalate rule for publish/provision/delete/bill/revoke and other consequential remote mutations. [UNVERIFIED]

The scoped-credential example is Anthropic's Claude Cowork design, where credentials stay in the host keychain and the guest receives a per-session scoped-down token that can be revoked independently. [VERIFIED 2026-10-02 S1]

No cited source establishes scoped, proxied, or short-lived credentials as a universal product requirement. [UNVERIFIED]

On native Windows, Claude Code does not provide sandbox containment equivalent to WSL2 at the cutoff. [VERIFIED 2026-10-02 S3]

Supreme must therefore distinguish ordinary interactive native-Windows work from high-autonomy work that needs enforceable filesystem/network boundaries. [UNVERIFIED]

WSL2, dev containers, VMs, or cloud isolation may be appropriate depending on repository compatibility; this remains a dedicated Windows-security design question. [UNVERIFIED]

## Allowed and denied file sets

A global fixed file allowlist is usually the wrong abstraction because the legitimate change surface is task- and repository-specific. [UNVERIFIED]

The classifier trusts the working directory and the remotes configured when the session started, and everything else is treated as external until trusted infrastructure is configured. [VERIFIED 2026-10-02 S6,S5]

The stronger pattern is:

1. derive an **expected change surface** during reconnaissance; [UNVERIFIED]
2. record protected/out-of-scope paths where relevant; [VERIFIED 2026-10-02 S3,S6]
3. compare proposed writes against that task-local surface; [UNVERIFIED]
4. challenge or block unexpected writes with `PreToolUse` or an equivalent enforcement layer; [VERIFIED 2026-10-02 S4]
5. refresh the change surface when new repository evidence legitimately expands scope. [UNVERIFIED]

Claude Code protects a fixed set of configuration, hook, credential, and shell-startup paths from writes, and no allow rule lifts that protection. [VERIFIED 2026-10-02 S3]

The hooks documentation states that a hook's `if` filter is best-effort and that the permission system should be used to enforce a hard allow or deny. [VERIFIED 2026-10-02 S4]

Static universal hazards may still belong in global deny policy. [VERIFIED 2026-10-02 S5,S6]

`permissions.deny` in managed settings blocks an action before the classifier is consulted and cannot be overridden. [VERIFIED 2026-10-02 S5,S6]

Project-specific generated/vendor/protected paths belong at project scope once verified. [UNVERIFIED]

Project settings in `.claude/settings.json` and `.claude/settings.local.json` are excluded from `autoMode` classifier configuration and are ignored for sandbox filesystem entries when an admin-required sandbox is in force. [VERIFIED 2026-10-02 S5,S3]

## Maximum change-size policy

Supreme should **not** use a universal maximum number of files, lines, or diff bytes as a hard quality/safety gate. [UNVERIFIED]

Reasons:

- thresholds do not generalize across repositories and task types; [VERIFIED 2026-10-02 S8]
- generated changes can be legitimately large; [UNVERIFIED]
- dangerous changes can be very small; [UNVERIFIED]
- fixed metrics invite gaming through artificial splitting or indirection; [UNVERIFIED]
- a broad refactor may be appropriate when explicitly requested, while a ten-line unrelated deletion is not. [VERIFIED 2026-10-02 S2,S5]

The study behind the first reason concerns software fault-proneness prediction and does not evaluate agent change-size limits. [VERIFIED 2026-10-02 S8]

Anthropic's classifier distinguishes general requests from explicit intent, so asking to clean up a repository does not authorize force-pushing while naming the force push explicitly does. [VERIFIED 2026-10-02 S2,S5]

The supported policy is **deviation-based scope control**: [UNVERIFIED]

- compare the live diff with the expected change surface; [UNVERIFIED]
- flag unplanned edits to dependency manifests, lockfiles, migrations, deployment/configuration, generated outputs, public contracts, security-sensitive areas, or user-owned dirty files; [UNVERIFIED]
- require re-reconnaissance when new evidence changes the plan; [UNVERIFIED]
- escalate when scope expands materially beyond what the user authorized; [VERIFIED 2026-10-02 S2,S5]
- keep diff size/complexity metrics as advisory telemetry, not universal deterministic caps. [UNVERIFIED]

Anthropic's classifier blocks production deploys and migrations, changes to shared infrastructure, force pushes, and package installs routed around an internal registry. [VERIFIED 2026-10-02 S6]

That blocking behaviour is not documented as change-surface deviation review, and no cited source compares deviation signals against universal file or line thresholds. [UNVERIFIED]

### Evidence added by this verification pass

The imported text does not contain these points; each is verified against the cited source. [UNKNOWN]

- The Anthropic Sandbox Runtime denies all network access by default and treats writes as allow-only, while reads use a deny-then-allow pattern. [VERIFIED 2026-10-02 S7]
- The Claude Code Bash sandbox proxy checks each connection hostname against allowed and denied domains, and the allowed list starts empty. [VERIFIED 2026-10-02 S3]
- Sandbox filesystem write access is confined to the working directory, a per-user temp directory, and added directories. [VERIFIED 2026-10-02 S3]
- The standalone Anthropic Sandbox Runtime has alpha Windows support that runs a sandboxed process under a dedicated local account with a Windows Filtering Platform egress fence. [VERIFIED 2026-10-02 S7]
- Whether Claude Code's built-in Bash sandbox can use that Windows backend is not stated on either the Claude Code sandboxing page or the sandbox runtime repository. [UNKNOWN]

## Dead Ends

The Anthropic Sandbox Runtime README shows a basic-usage example where `srt "curl anthropic.com"` succeeds while the same document states that all network access is denied by default. [UNKNOWN]

## Open Questions
- What Windows-native mechanism can provide egress and credential isolation without WSL2, VM, or container isolation? [UNVERIFIED]
- How should the expected and protected change surface be refreshed after legitimate discoveries expand scope? [UNVERIFIED]
- How should external MCP and connector capabilities be reduced to least privilege without breaking common workflows? [UNVERIFIED]
