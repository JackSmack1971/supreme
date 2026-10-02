# Evidence-Backed Brownfield Reconnaissance and Change Containment

## Status

**Accepted research synthesis** for the Supreme corpus.

Research cutoff: **October 1, 2026**.

This document incorporates the conclusions of the uploaded research report *Evidence-Backed Repository Reconnaissance for a Global Claude Code Control Plane* and records the resulting corpus-level decisions without rewriting earlier research reports. Where this document conflicts with an older Supreme hypothesis inside the brownfield/reconnaissance/containment scope, this document takes precedence until later evidence supersedes it.

## Executive conclusion

An existing repository should be treated as an environment to be understood and preserved before it is treated as code to be changed.

The best-supported protocol is adaptive rather than ceremonial:

`preserve current state -> discover repository instructions -> identify the project toolchain -> localize the requested behavior -> inspect the nearest existing implementation and interfaces -> identify protected/generated/dependency-sensitive areas -> reproduce the defect or establish a verification oracle -> produce a proportional change map -> only then permit writes`

This protocol explicitly rejects four universal defaults:

- read everything;
- always write a formal plan;
- always use TDD;
- always delegate to multiple agents.

The stopping condition is **evidence sufficiency**, not a fixed number of files, tokens, searches, lines changed, or complexity points.

## Core design correction

The global control plane should implement a **small invariant layer plus project-derived behavior**.

Global policy may require that the agent discover repository facts, preserve user work, maintain scope, produce evidence, and escalate consequential ambiguity. It should not globally dictate architecture, testing doctrine, dependency style, formatting conventions, or repository topology when those should come from the project itself.

## Control-surface corrections

### Permissions before hooks where possible

Static catastrophic prohibitions should prefer declarative permission rules where Claude Code can express them. Permission evaluation is deny-first, making `permissions.deny` the simpler hard mechanism for universal static hazards.

Use `PreToolUse` only when policy requires runtime computation or contextual inspection, such as evaluating whether a target belongs to the pre-task dirty-file set.

Do not treat command hooks as infallible security boundaries. A command hook that times out, cannot start, or otherwise fails in a nonblocking way can leave the normal tool/permission path available. Hook health therefore becomes part of the control-plane safety model.

### `PostToolUse` is validation, not prevention

A `PostToolUse` hook runs after the tool action has happened. It can provide feedback or participate in verification, but it cannot retroactively prevent the original write.

Use:

- `permissions.deny` / `PreToolUse` for prevention;
- post-action validation for diagnostics and corrective feedback;
- Stop/completion gates for evidence required before declaring work finished.

### Undocumented configuration fails closed

A production control plane must not depend on a Claude Code configuration key, environment variable, path, frontmatter field, hook schema, or feature unless a current Tier-1 source establishes it for the target version.

Earlier Supreme research named several settings that were not independently verified in the October 1 review, including:

- `defaultShell: powershell`
- `autoCompactEnabled`
- `askUserQuestionTimeout`
- a settings key named `ultracode`

These are **not production requirements** unless future authoritative documentation/schema confirms them.

This rule is bidirectional: a later verification can also restore a setting previously considered uncertain. Configuration validation must therefore be version-aware and repeatable.

## Brownfield reconnaissance state

For nontrivial work in an existing repository, Supreme should enter a pre-write reconnaissance state.

The state should be read-oriented and fact-producing. It should not become a heavyweight documentation exercise or duplicate the repository into context.

### 1. Preserve repository state

Before mutation, establish at minimum:

- repository root;
- current branch;
- staged changes;
- unstaged changes;
- untracked files.

The control plane should record the pre-task changed/untracked paths as an ownership baseline.

Invariant:

> A file changed or created before the task began is user-owned unless the requested task actually requires touching it.

The agent must not silently use `stash`, `reset`, `checkout`, `clean`, broad deletion, regeneration, formatter sweeps, or similar operations to obtain a convenient baseline.

Editing a pre-dirty file may be legitimate when required by the task, but the user's existing content must be preserved and distinguished from the agent's own patch.

Destructive restoration or cleanup affecting pre-existing user work should require explicit human approval unless operating inside disposable agent-owned isolation where the target is unambiguous.

### 2. Discover effective instructions

Before applying global preferences, identify relevant repository instructions such as:

- `CLAUDE.md`;
- `.claude/CLAUDE.md`;
- `CLAUDE.local.md`;
- applicable `.claude/rules/*.md`;
- `AGENTS.md` where supported/applicable;
- repository governance such as README, CONTRIBUTING, development docs, and CI configuration when relevant.

Principle:

> Discover, do not invent.

If the repository does not prescribe an architecture, testing doctrine, or dependency policy, Supreme should not pretend one exists.

### 3. Discover the actual toolchain

Determine from repository evidence:

- dependency/package manager;
- build system;
- test runner;
- formatter;
- linter;
- type checker;
- generators;
- CI entry points;
- relevant local run/development commands.

Do not assume generic commands merely because a language was detected.

Running tests/builds/generators is itself code execution. In untrusted repositories, "test command" must not automatically mean "safe command."

### 4. Localize the requested behavior

Build a task-local map instead of reading the entire repository.

Start from the issue/request and expand only as needed:

- responsible implementation;
- direct callers/callees/imports;
- nearest analogous implementation;
- existing utility or abstraction that may already solve part of the problem;
- relevant tests;
- public or persisted boundary crossed by the change.

The goal is to answer:

- What currently implements this behavior?
- What repository pattern should be followed?
- What already exists that should be reused?
- What calls this code and what does it call?
- What API/CLI/schema/event/file format/persisted state may change?
- Where is similar behavior verified?

Nearby repository evidence outranks the agent's preferred generic architecture.

### 5. Identify sensitive, generated, or policy-controlled regions

Determine whether the task touches:

- generated artifacts;
- vendored/third-party code;
- generated clients;
- migrations;
- lockfiles;
- snapshots/fixtures;
- build output;
- dependency manifests;
- security/infrastructure/configuration areas;
- other project-declared protected paths.

Do not infer "generated" solely from a filename. Establish provenance from repository instructions, comments, scripts, build configuration, or other concrete evidence.

Correct policy:

> Do not directly modify derived or policy-controlled artifacts unless the repository workflow and task require it; when regeneration is required, modify the canonical source and use the repository's established generator.

This is not a blanket ban on migrations, lockfiles, or committed generated outputs.

### 6. Establish observable behavior or a credible verification oracle

For defects, reproduce before repairing when reasonably feasible and meaningful.

Capture the failing command/input/environment or another observable signal before editing. Keep the original failure available for final verification.

However, an agent-generated failing test is not automatically the complete specification. Reproduction generation is fallible and a narrow reproducer can cover only one manifestation of a broader defect.

The invariant is:

> Establish an appropriate verification oracle before claiming completion.

That oracle may be a human-written test, generated reproducer corroborated by other evidence, integration behavior, end-to-end check, type/build contract, runtime smoke test, screenshot/UI behavior, API parity, or another task-specific executable observation.

### 7. Produce a proportional change map

For non-obvious work, record a concise map containing:

- files/areas expected to change;
- files/areas explicitly out of scope where relevant;
- existing repository pattern being followed;
- verification evidence expected;
- nontrivial risks;
- rollback/recovery approach when consequences are meaningful.

Do not require this artifact for obvious one-line changes where the relevant facts and verification path are already clear.

## Evidence Sufficiency Gate

Reconnaissance is sufficient when the agent can state, with repository evidence:

1. current branch and pre-existing dirty/staged/untracked work;
2. effective instructions governing the target area;
3. project commands/toolchain relevant to the task;
4. implementation currently responsible for the behavior;
5. at least one relevant existing pattern, or an explicit finding that none exists;
6. public/interface/dependency boundaries affected;
7. whether generated/vendor/migration/dependency-sensitive artifacts are involved;
8. how requested behavior will be reproduced or verified;
9. expected change surface and deliberate out-of-scope areas;
10. unresolved ambiguity severe enough to require human judgment.

These are semantic exit conditions, not quotas.

If they are obvious after a few targeted reads, stop reconnaissance. If they remain uncertain, expand only along unresolved behavior/dependency paths.

## Human-approval boundaries

For the novice-oriented profile, human approval should concentrate on consequences the user can meaningfully evaluate rather than low-level shell trivia.

Strong candidates for explicit escalation include:

- discarding or obscuring pre-existing user work;
- destructive Git cleanup/restoration outside disposable isolation;
- irreversible or data-destructive migrations;
- new production/runtime dependencies where project policy has not delegated authority;
- changes to public APIs/contracts with compatibility impact;
- production-facing/deployment operations;
- credential/security-sensitive changes;
- network or infrastructure actions with nontrivial side effects;
- architectural divergence from established repository conventions when not explicitly requested.

Approval quality matters more than approval count.

## Windows-specific requirements

Windows must be treated as a first-class execution environment rather than Unix with altered paths.

The October 1 research establishes these design constraints:

- Native Windows must not be described as having Claude Code sandbox containment equivalent to WSL2.
- The control plane must detect available shell/runtime capabilities rather than assuming Bash.
- Documented Windows mechanisms should be preferred over invented shell-selection settings.
- Hook/policy implementation must account for Windows quoting, paths, process launching, encodings, and interpreter availability.
- Supreme must not globally weaken Windows/PowerShell security policy merely for convenience.
- High-autonomy native-Windows execution versus WSL2/dev-container isolation remains an explicit design question for the dedicated Windows/security research pass.

## Architecture and methodology anti-requirements

The brownfield evidence rejects universal enforcement of the following:

- Vertical Slice Architecture;
- Clean Architecture;
- hexagonal/layered architecture;
- microservices;
- modular monoliths;
- CQRS/event sourcing;
- repository/service patterns;
- any other single architecture topology;
- cyclomatic complexity hard gates such as 10 or 15;
- fixed locality thresholds such as >85%;
- arbitrary maximum file/line-count gates;
- mandatory ADRs for every architecture-looking change;
- universal TDD;
- universal multi-agent routing;
- whole-repository ingestion;
- mandatory formal planning for trivial changes.

Evidence supports properties such as locality, cohesion, understandable boundaries, credible verification, preservation, and scope control. It does not establish one universal implementation pattern for achieving them.

Complexity metrics may remain useful as advisory telemetry, but fixed global thresholds create portability and metric-gaming problems.

ADRs remain useful when a decision is consequential, durable, non-obvious, and worth preserving. They are conditional tools, not mandatory paperwork.

TDD remains useful when a trustworthy test specification exists. It is not the invariant; verification is.

## Multi-agent policy correction

Multi-agent reconnaissance is an optimization, not Supreme's default architecture.

A read-only subagent can be valuable when investigation would otherwise pollute the main context, but it consumes separate inference and latency.

Experimental agent teams must remain task-conditioned/opt-in rather than universal. Sequential, same-file, tightly coupled, or dependency-heavy work may be better served by a single session or limited subagent delegation.

Future orchestration research should optimize quality per token/time rather than agent count.

## Durable evidence across compaction

At minimum, the following facts should survive context compaction or handoff for active work:

- intended change surface;
- pre-existing dirty/user-owned paths;
- reproducer or verification command/oracle;
- known risks;
- current implementation/verification status;
- unresolved decisions.

The durable representation must be refreshed when repository state changes; stale task state is itself a hazard.

## Unresolved implementation questions

This research intentionally leaves the following open for later design/research:

1. How should `RECONNAISSANCE_COMPLETE` be represented technically without creating stale machine state?
2. How should user ownership be tracked when editors, other agents, or build tools modify files after the initial baseline?
3. Should dirty-file protection be path-based, content-aware, or three-way/diff-aware?
4. Which destructive Git operations should be globally denied versus escalated for approval?
5. Which project-controlled commands are safe enough to execute during reconnaissance in untrusted repositories?
6. Should high-autonomy Windows workflows prefer WSL2/dev-container isolation by default?
7. What runtime should implement portable policy across native Windows and Unix-like environments?
8. What external/health mechanism should cover catastrophic contextual policy when command hooks can fail open?
9. How should generated-source provenance be discovered across heterogeneous ecosystems?
10. How should dependency approval avoid both supply-chain risk and approval fatigue?
11. What evidence permits progress when a production-only defect cannot be reproduced locally?
12. How should change maps and ownership baselines refresh across compaction/resume/worktrees?
13. What reliable trigger determines when an ADR is warranted?
14. When does parallel reconnaissance save more than it costs?
15. How should model-compensation heuristics expire or be reevaluated as Claude improves?

## Corpus impact

This research materially advances or completes these original research areas:

- **Brownfield reconnaissance:** strongly answered.
- **Scope/destructive change containment:** mostly answered; implementation mechanics remain.
- **Testing strategy:** advanced, especially against universal TDD and single generated-test oracles.
- **Efficiency/context:** advanced through evidence-sufficiency and targeted retrieval.
- **Windows enforcement:** materially advanced, but dedicated security/runtime research remains.
- **Novice interaction:** advanced toward consequence-based approvals.
- **Completion evidence:** advanced, but the full debugging/testing/proof-of-completion protocol remains a separate research task.

The next highest-value research pass is therefore **Debugging, Testing & Proof of Completion**: establish the rigorous path from observed failure to localized cause, implementation, independent verification, regression protection, and legitimate completion claims.
