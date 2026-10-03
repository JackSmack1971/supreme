# Evidence-Backed Brownfield Reconnaissance and Change Containment

> **Corpus status:** Accepted research report for Supreme  
> **Research cutoff:** October 1, 2026  
> **Claude Code cutoff boundary used by source research:** v2.1.287  
> **Scope:** Existing-repository reconnaissance, scope containment, destructive-action control, and pre-write evidence requirements  
> **Precedence:** Supersedes conflicting earlier Supreme hypotheses within this scope while preserving older reports as provenance

## Research question

What procedure should a production-quality Claude Code control plane require **before an AI coding agent modifies an existing repository**, and which controls can actually prevent destructive, unrelated, or scope-expanding changes without forcing the user to approve every harmless command?

The target system lives primarily under:

`C:\Users\USERNAME\.claude\`

The target user may be a complete software-engineering novice.

## Executive conclusion

An existing repository should be treated as an environment to be **understood and preserved before it is treated as code to be changed**.

The strongest evidence supports an adaptive evidence-sufficiency protocol:

`PRESERVE STATE -> DISCOVER INSTRUCTIONS -> DISCOVER TOOLCHAIN -> LOCALIZE BEHAVIOR -> INSPECT NEARBY PATTERNS/INTERFACES -> IDENTIFY SENSITIVE/GENERATED AREAS -> ESTABLISH REPRODUCER/ORACLE -> BUILD PROPORTIONAL CHANGE MAP -> WRITE`

The protocol rejects four universal defaults:

- read the entire repository;
- always write a formal plan;
- always use TDD;
- always delegate to multiple agents.

The stopping condition is **semantic evidence sufficiency**, not a fixed number of files, tokens, searches, lines changed, or complexity points.

The resulting control-plane direction is a **small global invariant layer plus project-derived behavior**. Supreme may require preservation, evidence, scope control, verification, and escalation. It should not globally impose one architecture, testing doctrine, dependency style, or repository topology.

## Evidence hierarchy and interpretation

This report follows the Supreme corpus evidence policy:

1. current official Claude Code documentation/changelog and documented schemas;
2. official Anthropic engineering/research;
3. peer-reviewed or strong primary empirical research;
4. reproducible benchmark evidence;
5. GitHub issues/practitioner reports only as observational evidence of failure classes;
6. engineering judgment, explicitly labeled.

An undocumented Claude Code key, path, hook schema, CLI switch, or feature is not accepted as a production dependency merely because an earlier Supreme report named it.

## Claude Code mechanisms relevant to this research

| Mechanism | Status at cutoff | What it can support | Important limitation |
|---|---|---|---|
| `~/.claude/settings.json` | Currently supported | User-scope permissions, hooks, environment and other supported settings | Cannot override higher managed policy |
| Project `.claude/settings.json` | Currently supported | Project-specific hooks/permissions/settings | Project-specific behavior should not be guessed globally |
| `CLAUDE.md` / `.claude/CLAUDE.md` | Currently supported | Behavioral context and repository conventions | Guidance, not hard enforcement |
| `.claude/rules/*.md` with documented `paths` | Currently supported | Conditional/path-scoped guidance | Still prompt/context, not access control |
| `AGENTS.md` | Currently supported in cutoff version | Repository instructions under documented loading rules | Must follow actual current loading semantics |
| Plan mode | Currently supported | Read-oriented reconnaissance/planning | Adds overhead; not mandatory for trivial obvious changes |
| Permission `deny`, `ask`, `allow` | Currently supported | Static client-enforced tool/action policy | Must use documented rule syntax; list scopes can merge |
| `PreToolUse` | Currently supported | Context-sensitive blocking before execution | Command/HTTP/MCP hook timeout/start failures can be nonblocking |
| `PostToolUse` | Currently supported | Post-action validation/feedback | Cannot retroactively prevent the action |
| Stop hook | Currently supported | Prevent completion until a deterministic check passes | Completion gate, not a pre-action containment mechanism |
| Custom subagents | Currently supported | Context-isolated reconnaissance/review | Additional inference cost and latency |
| Agent teams | Experimental | Coordinated parallel sessions | Higher token cost, known limitations, inappropriate as universal default |
| Checkpoints/rewind | Currently supported | Recover some Claude file-tool changes | Not a replacement for Git; shell/external changes are not comprehensively captured |
| Native Windows sandbox | Unsupported at cutoff | — | WSL2 has sandbox support; native Windows must not be described as equivalently sandboxed |
| `CLAUDE_CODE_GIT_BASH_PATH` | Documented | Windows Git Bash selection where applicable | Do not invent alternative shell-setting keys |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | Documented | Windows PowerShell tool behavior | Exact use must follow version/provider documentation |

The source research did **not** verify `defaultShell: powershell`, `autoCompactEnabled`, `askUserQuestionTimeout`, or a settings key named `"ultracode": true` as supported production settings at the cutoff. They remain excluded unless a Tier-1 source for the target version establishes them.

## Reconnaissance protocol before modification

### 1. Preserve repository state

Before mutation, establish from Git:

- repository root;
- current branch;
- staged changes;
- unstaged changes;
- untracked files.

Capture the equivalent information of:

- `git branch --show-current`;
- `git status --short --branch --untracked-files=all`;
- `git diff`;
- `git diff --cached`.

The control plane should create an ownership baseline:

> A file changed or created before the task began is user-owned unless the requested task actually requires touching it.

The agent must not silently `stash`, `reset`, `checkout`, `clean`, broadly delete, regenerate, normalize, or formatter-sweep unrelated pre-existing work merely to create a convenient baseline.

Editing a pre-dirty file may be legitimate when required by the task, but the user's prior content must be preserved and distinguishable from the agent's own patch.

### 2. Discover effective repository instructions

Before applying global preferences, identify the instructions governing the target area, including as applicable:

- `CLAUDE.md`;
- `.claude/CLAUDE.md`;
- `CLAUDE.local.md`;
- applicable `.claude/rules/*.md`;
- `AGENTS.md` under documented loading rules;
- README, CONTRIBUTING, developer documentation, CI configuration, and repository-specific governance artifacts when relevant.

Principle:

> **Discover, do not invent.**

If the repository does not prescribe an architecture, test doctrine, dependency policy, or formatting convention, the control plane must not pretend one exists.

### 3. Discover the actual toolchain

Infer from repository evidence rather than language stereotypes:

- package/dependency manager;
- build system;
- test runner;
- formatter;
- linter;
- type checker;
- code generators;
- CI entry points;
- relevant local development/run commands.

Dependency manifests and lockfiles are first-class evidence.

Running a build, test, package-manager command, generator, or script executes repository-controlled code. A novice-oriented control plane must not equate “test command” with “safe command” in an untrusted repository.

### 4. Localize the requested behavior

Build a task-local map instead of reading the entire repository.

Find:

- the implementation currently responsible for the behavior;
- direct callers/callees/imports as needed;
- the nearest analogous implementation;
- existing utilities or abstractions that may already solve part of the problem;
- relevant tests;
- public or persisted boundaries crossed by the change.

The agent should be able to answer:

- What currently implements this behavior?
- What existing repository pattern should be followed?
- What utility already exists that should be reused?
- What calls this code, and what does this code call?
- What API, CLI, schema, event, file format, or persisted state could be affected?
- Where is similar behavior verified?

Repository-local evidence outranks the model's generic preferred pattern unless the user explicitly requested architectural replacement.

### 5. Identify protected, generated, vendor, migration, and dependency-sensitive areas

Determine whether the change touches:

- generated artifacts;
- vendored/third-party code;
- generated API clients;
- migrations;
- lockfiles;
- snapshots/fixtures;
- build output;
- dependency manifests;
- infrastructure/security/configuration;
- project-declared protected paths.

Do not classify a file as generated solely from its filename. Establish provenance from comments, scripts, build configuration, repository instructions, or other concrete evidence.

Policy:

> Do not directly modify derived or policy-controlled artifacts unless the repository workflow and task require it; when regeneration is required, modify the canonical source and use the repository's established generator.

This is not a universal ban on migrations, lockfiles, or generated outputs. Some projects intentionally commit them.

### 6. Reproduce defects or establish a credible verification oracle

For bugs, reproduce the failing behavior before editing when reasonably feasible and meaningful.

Record the failing command/input/environment or another observable signal and retain it for final verification.

An agent-generated failing test is **not automatically the complete specification**. Research on automated reproduction shows that generated reproducers are fallible and can represent only one manifestation of a defect.

The invariant is:

> Establish an appropriate verification oracle before claiming completion.

The oracle may be:

- a trustworthy existing or human-written test;
- a generated reproducer corroborated by issue text/contracts/other tests;
- an integration or end-to-end check;
- build/type/static contract;
- runtime smoke test;
- browser/UI behavior;
- API parity;
- domain-specific validation.

### 7. Use history/blame conditionally

Git history/blame is useful when:

- the current implementation looks anomalous;
- compatibility rationale is unclear;
- a regression origin matters;
- an API shape seems inexplicable;
- competing conventions exist.

It should not be loaded reflexively for every change because context and latency are scarce.

### 8. Build a proportional change map

For non-obvious work, record:

- files/areas expected to change;
- files/areas explicitly out of scope when useful;
- existing repository pattern being followed;
- expected verification evidence;
- meaningful risks;
- rollback/recovery approach where consequences are nontrivial.

Do not require heavyweight paperwork for obvious one-line changes where the relevant facts and verification path are already clear.

## Evidence Sufficiency Gate

Nontrivial writes may begin when the agent can state, from repository evidence:

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

These are semantic conditions, not quotas.

If they are obvious after a few targeted reads, stop reconnaissance. If they remain uncertain, expand only along unresolved dependency or behavior paths.

## Containment model

### Static hazards: prefer declarative permission policy

Where a catastrophic prohibition can be expressed in documented permission rules, prefer `permissions.deny`.

This is simpler and less fragile than routing every safety decision through a script.

### Contextual hazards: use `PreToolUse`

Use `PreToolUse` for policies requiring runtime facts, such as:

- whether a path belonged to the pre-task dirty set;
- whether a command targets a protected location;
- whether a proposed operation violates a task-local allowed change surface.

Hook health is part of the safety model because ordinary command/HTTP/MCP hooks can fail open on timeout/start failure/nonblocking error.

### Post-action validation: use `PostToolUse`

`PostToolUse` can inspect what happened and feed corrective information back, but it must never be described as preventing the original action.

### Completion gates: use deterministic verification and Stop semantics where appropriate

A Stop hook or equivalent completion gate may require checks to pass before Claude can legitimately finish.

This is distinct from pre-write safety.

### Checkpoints are recovery aids, not containment

Claude checkpoints do not replace Git and do not comprehensively capture shell/external-process changes.

The control plane must not rely on rewind/checkpoints as the primary protection against destructive shell commands.

### Worktrees provide isolation when the work itself can be isolated

Agent-owned disposable Git worktrees are useful for:

- independent exploratory implementation;
- high-risk experiments;
- parallel sessions that should not collide.

They do not eliminate the need to understand repository state, nor do they make production/external side effects safe.

## Always-escalate boundary

For the novice-oriented Supreme profile, **model confidence does not waive escalation** for actions with irreversible, user-owned, security-sensitive, or externally consequential effects.

Always require explicit human escalation by default for:

- discarding, overwriting, obscuring, cleaning, resetting, or otherwise destroying pre-existing user work;
- destructive Git cleanup/restoration that can affect files outside an agent-owned disposable worktree;
- irreversible or data-destructive migrations;
- production-data mutation;
- production deployment or production configuration changes;
- infrastructure operations with material external side effects;
- credential, secret, authentication, authorization, encryption, or security-boundary changes whose consequences cannot be safely established from repository-local evidence;
- external network actions that create, delete, publish, bill, provision, revoke, or otherwise mutate remote state outside ordinary local development;
- breaking public API/schema/CLI/persistence contracts unless the user has explicitly requested and authorized the compatibility break.

Require escalation **unless clear standing authority already exists in user/project policy** for:

- adding or materially upgrading production/runtime dependencies;
- deliberately departing from established repository architecture/conventions.

This boundary is consequence-based, not command-based. Read-only inspection, ordinary edits inside the evidenced change surface, local deterministic checks, and reversible project-authorized actions should not be forced through repetitive approval prompts.

## Material findings

### Finding 1 — Preserve the pre-task working tree as a first-class invariant

1. **Finding:** Pre-existing dirty, staged, and untracked work must be identified before mutation and preserved as user-owned state.
2. **Evidence/source:** Claude Code checkpoints do not cover all shell/external-process changes and are not a replacement for Git. Claude Code issue reports document destructive cleanup of untracked/unrelated files as a real failure class.
3. **Evidence strength:** Strong for relying on Git/state capture rather than checkpoints; weak-to-moderate for incidence because issue reports are observational.
4. **Claude Code mechanism implicated:** Git via shell, plan/read-only exploration, permissions, `PreToolUse`.
5. **Global `~/.claude` candidate?** Yes for the invariant; exact path ownership is task/project state.
6. **Enforcement:** Deterministic where possible plus human approval for destructive restoration/cleanup.
7. **Cost/context implications:** Tiny up-front cost compared with potentially catastrophic recovery cost.
8. **Security implications:** High integrity risk; broad cleanup can also delete credentials/configuration/evidence.
9. **Open question remaining:** How should ownership track files modified concurrently by editors, other agents, or build tools?

### Finding 2 — Repository instructions must be discovered before global preferences are applied

1. **Finding:** Effective project instructions and governance must be identified before editing.
2. **Evidence/source:** Claude Code supports user/project/local/managed instruction and settings scopes; project context is not equivalent to a deterministic precedence policy.
3. **Evidence strength:** Strong, Tier 1.
4. **Claude Code mechanism implicated:** `CLAUDE.md`, `CLAUDE.local.md`, `.claude/rules/`, `AGENTS.md`.
5. **Global `~/.claude` candidate?** Yes only for the universal behavior “discover instructions first.”
6. **Enforcement:** Prompt/workflow policy; optionally a pre-write state gate.
7. **Cost/context implications:** Small and high leverage; avoids broad rewrites and convention drift.
8. **Security implications:** Repository instructions are part of the trust boundary and may themselves contain hostile content.
9. **Open question remaining:** Should effective instructions be summarized visibly for novices or only machine-audited?

### Finding 3 — Toolchain discovery should precede execution and implementation

1. **Finding:** Build, test, format, lint, typecheck, generator, CI, and package commands should be derived from repository evidence.
2. **Evidence/source:** Anthropic guidance emphasizes executable verification and documenting non-obvious commands.
3. **Evidence strength:** Strong official guidance; moderate as a universal empirical claim.
4. **Claude Code mechanism implicated:** File search/read, shell tools, skills, project instructions.
5. **Global `~/.claude` candidate?** Yes for discovery behavior; no for prescribing specific ecosystem commands.
6. **Enforcement:** Prompt/workflow-based; hard gating only when discovery completion can be represented reliably.
7. **Cost/context implications:** Modest; reduces repeated failed commands and unnecessary broad test runs.
8. **Security implications:** Project test/build/generator commands execute repository-controlled code.
9. **Open question remaining:** Which commands are safe to execute before an untrusted workspace is sufficiently trusted/isolated?

### Finding 4 — Relevant-context retrieval is superior to whole-repository ingestion

1. **Finding:** Reconnaissance should retrieve the task-relevant implementation, dependencies, interfaces, patterns, and tests rather than indiscriminately reading the repository.
2. **Evidence/source:** SWE-Explore, CoRet, and Anthropic context guidance.
3. **Evidence strength:** Strong-to-moderate.
4. **Claude Code mechanism implicated:** Search/read, code intelligence, optional read-only subagents.
5. **Global `~/.claude` candidate?** Yes as an adaptive strategy, not a read quota.
6. **Enforcement:** Prompt/model routing.
7. **Cost/context implications:** Critical; preserves reasoning context and lowers token/latency cost.
8. **Security implications:** Reduces unnecessary ingestion of unrelated secrets/sensitive code.
9. **Open question remaining:** Can evidence sufficiency be estimated reliably without benchmark ground truth?

### Finding 5 — Nearby implementations and public interfaces should outrank generic preferred patterns

1. **Finding:** Existing repository patterns and boundaries should be inspected before introducing new abstractions or architectural styles.
2. **Evidence/source:** Anthropic best-practice guidance plus repository-retrieval research.
3. **Evidence strength:** Strong official guidance; moderate empirical support.
4. **Claude Code mechanism implicated:** Search/read, code intelligence, plan mode.
5. **Global `~/.claude` candidate?** Yes for “prefer demonstrated repository patterns absent a reason to diverge.”
6. **Enforcement:** Primarily prompt/model reasoning; architectural equivalence is too semantic for a universal regex gate.
7. **Cost/context implications:** Usually lowers cost and duplicate-code creation.
8. **Security implications:** Reusing established auth/validation/data paths may reduce accidental bypasses, but insecure legacy patterns still require judgment.
9. **Open question remaining:** How should deliberate modernization be distinguished from unsolicited architectural preference?

### Finding 6 — Generated/vendor/migration/dependency-sensitive artifacts require discovery, not blanket bans

1. **Finding:** Provenance and project workflow should determine whether/how sensitive artifacts are changed.
2. **Evidence/source:** Claude Code hook examples and official workflow guidance; general software-engineering reproducibility/supply-chain considerations.
3. **Evidence strength:** Strong for mechanism semantics; moderate for generalized policy.
4. **Claude Code mechanism implicated:** `PreToolUse`, permissions, project rules, generators/build tools.
5. **Global `~/.claude` candidate?** Conditional; global behavior can require discovery, while actual protected paths belong to the project.
6. **Enforcement:** Deterministic only after protected/canonical relationships are established; human approval for consequential dependency/migration changes.
7. **Cost/context implications:** Small up-front cost; prevents noisy generated diffs and dependency churn.
8. **Security implications:** Dependencies/generators can execute third-party code; migrations can mutate persistent state.
9. **Open question remaining:** How can provenance be discovered consistently across ecosystems?

### Finding 7 — Reproduce defects before editing when practical, but generated reproducers are not infallible specifications

1. **Finding:** Observable failing behavior should normally precede bug repair, while reproduction tests remain hypotheses until corroborated.
2. **Evidence/source:** Anthropic guidance, ReProAgent, TDFlow, SWE-Doctor.
3. **Evidence strength:** Strong for executable feedback; strong evidence against treating autonomous reproductions as complete specifications.
4. **Claude Code mechanism implicated:** Test runner, shell, plan mode, completion verification.
5. **Global `~/.claude` candidate?** Yes as a default behavior; conditional when reproduction is unsafe, impossible, flaky, or prohibitively expensive.
6. **Enforcement:** Prompt-based to select/create the oracle; deterministic once a trustworthy executable oracle exists.
7. **Cost/context implications:** Up-front cost generally reduces speculative patch loops.
8. **Security implications:** Test execution is code execution.
9. **Open question remaining:** What evidence permits safe progress when a production-only defect cannot be reproduced locally?

### Finding 8 — Universal TDD is not supported

1. **Finding:** Strong feedback and credible verification are supported; one universal test-ordering doctrine is not.
2. **Evidence/source:** TDD meta-analysis plus TDFlow's dependence on trustworthy human-written tests.
3. **Evidence strength:** Strong, context-dependent.
4. **Claude Code mechanism implicated:** Workflow guidance, tests, completion gates.
5. **Global `~/.claude` candidate?** No for “always use TDD”; yes for “establish a credible verification oracle.”
6. **Enforcement:** Test execution can be deterministic; test-first versus test-after versus E2E should be task-dependent.
7. **Cost/context implications:** TDD can narrow search when a trustworthy spec exists, but forced tests can create ceremony with low signal.
8. **Security implications:** Test gaming/weakening is a larger risk than test ordering; higher assurance may require independent/protected evaluation.
9. **Open question remaining:** Which task characteristics predict the best verification strategy?

### Finding 9 — Reconnaissance should stop at evidence sufficiency, not arbitrary thresholds

1. **Finding:** Stop exploring when semantic conditions are satisfied rather than after fixed files/tokens/minutes/complexity.
2. **Evidence/source:** Anthropic context/planning guidance, SWE-Explore, software metric threshold generalizability research.
3. **Evidence strength:** Strong for bounded context; moderate for the exact semantic gate design.
4. **Claude Code mechanism implicated:** Plan mode, context management, subagents.
5. **Global `~/.claude` candidate?** Yes as semantic exit criteria.
6. **Enforcement:** Prompt/workflow-based.
7. **Cost/context implications:** Primary token-efficiency mechanism of the reconnaissance design.
8. **Security implications:** Over-reading exposes unrelated sensitive content; under-reading increases misunderstanding.
9. **Open question remaining:** How should epistemic uncertainty be measured robustly?

### Finding 10 — Static safety policy should prefer declarative denies over hook-only enforcement when possible

1. **Finding:** Hard static prohibitions should use permission rules where expressible; hooks should be reserved for contextual computation.
2. **Evidence/source:** Official permissions and hooks documentation.
3. **Evidence strength:** Strong, Tier 1.
4. **Claude Code mechanism implicated:** `permissions.deny`, `permissions.ask`, `PreToolUse`.
5. **Global `~/.claude` candidate?** Yes for truly universal static hazards.
6. **Enforcement:** Deterministic, with human approval for ambiguous high-impact actions.
7. **Cost/context implications:** Permission rules have negligible conversational cost; hooks add latency/maintenance.
8. **Security implications:** Critical; fail-open hook behavior can create false confidence.
9. **Open question remaining:** Which contextual policies are severe enough to require an enforcement layer beyond ordinary command hooks?

### Finding 11 — Multi-agent reconnaissance is an optimization, not the default architecture

1. **Finding:** Use extra agents only when context isolation/parallelism produces expected value.
2. **Evidence/source:** Anthropic agent-team guidance and Agentless benchmark evidence.
3. **Evidence strength:** Strong for “not universal”; no evidence establishes one universally optimal orchestration shape.
4. **Claude Code mechanism implicated:** Main session, subagents, experimental agent teams.
5. **Global `~/.claude` candidate?** No for mandatory routing; yes for optional reusable read-only specialists.
6. **Enforcement:** Model/harness routing.
7. **Cost/context implications:** Subagents protect parent context but consume separate inference; teams multiply token use.
8. **Security implications:** More agents/tool surfaces create more actions and data flows to govern.
9. **Open question remaining:** What measurable task characteristics predict when parallel exploration pays for itself?

### Finding 12 — Windows is a first-class execution environment with materially different containment

1. **Finding:** Native Windows and WSL2 cannot be treated as equivalent from a Claude Code containment standpoint.
2. **Evidence/source:** Official Claude Code Windows/setup/security documentation.
3. **Evidence strength:** Strong, Tier 1.
4. **Claude Code mechanism implicated:** PowerShell tool, Bash tool, environment variables, permissions, sandbox support.
5. **Global `~/.claude` candidate?** Yes for environment detection and portability policy.
6. **Enforcement:** Deterministic environment detection plus human approval/isolation for high-risk native-Windows operations.
7. **Cost/context implications:** Small bootstrap cost avoids repeated shell/path failures.
8. **Security implications:** Critical; the control plane must not falsely claim sandbox guarantees on native Windows.
9. **Open question remaining:** Should high-autonomy work default to WSL2/dev-container isolation while native Windows remains the ordinary interactive mode?

### Finding 13 — Novice oversight should focus on consequences, not approval count

1. **Finding:** Useful autonomy requires concentrating human attention on consequential decisions rather than low-level command prompts.
2. **Evidence/source:** Anthropic research on coding-skill formation and expertise plus permission/harness guidance.
3. **Evidence strength:** Moderate-to-strong.
4. **Claude Code mechanism implicated:** Permission policy, plan/explanation workflows, human approval.
5. **Global `~/.claude` candidate?** Conditional; novice-safe explanation is useful but universal interrogation would create fatigue.
6. **Enforcement:** Interaction design and human approval.
7. **Cost/context implications:** Some additional interaction cost, offset by better oversight quality.
8. **Security implications:** A novice who cannot understand consequences is a weak final security boundary.
9. **Open question remaining:** What explanation level preserves comprehension without turning every task into a tutorial?

## A. Design requirements derived from the evidence

1. Implement a **pre-write reconnaissance state** for nontrivial brownfield work.
2. Snapshot **facts, not repository contents**: branch, user-owned paths, effective instructions, toolchain, target implementation, nearby pattern, boundary impact, verification oracle, change surface.
3. Treat pre-existing user changes as **immutable by default**; touching a dirty file is allowed only when the task requires it and prior content is preserved.
4. Keep the global layer limited to **cross-project invariants**. Architecture/build/test conventions should be project-derived.
5. Prefer repository-local patterns/utilities over global stylistic preferences.
6. Explicitly identify public API/schema/CLI/persistence/dependency boundaries before nontrivial edits.
7. Discover generated/canonical relationships before editing derived artifacts.
8. Make dependency churn visible and justified; production/runtime dependency changes need standing authority or escalation.
9. Prefer observable reproduction before bug repair when feasible.
10. Require verification broader than “one test passed” when the task risk demands it.
11. Use Stop/completion checks for “cannot claim done until verification passes,” not as a substitute for pre-action policy.
12. Prefer declarative permission policy over custom hook code for static hazards.
13. Add **hook/control-plane health diagnostics** so missing interpreters/scripts/timeouts do not silently masquerade as protection.
14. Treat Windows/PowerShell pathing, quoting, encoding, process execution, and sandbox differences as first-class design constraints.
15. Do not globally weaken PowerShell or OS execution policy merely to simplify hooks.
16. Scale change maps/planning with uncertainty and blast radius.
17. Keep subagents optional and task-conditioned; keep experimental agent teams opt-in.
18. Preserve active-task evidence across compaction/handoff: intended files, user-owned paths, verification oracle, current status, risks, unresolved decisions.
19. Make the control plane **version-aware** and validate supported Claude Code schemas/keys before use.
20. Present novice approvals in consequence language: “deletes uncommitted work,” “adds a production dependency,” “changes schema,” “deploys externally,” etc.

## B. Anti-requirements

Supreme should **not**:

- mandate Vertical Slice, Clean, hexagonal, layered, microservice, modular-monolith, CQRS, event-sourcing, repository/service, or any other universal architecture;
- hard-code universal cyclomatic-complexity, locality, file-count, changed-line, token, or “complex task” thresholds;
- require ADRs for every architectural-looking change;
- require universal TDD;
- route every substantive task through multiple agents or experimental agent teams;
- treat subagents as free;
- read the entire repository before editing;
- require heavyweight plans/change maps for trivial obvious changes;
- silently stash/reset/clean/checkout/revert or otherwise “clean” pre-existing user work;
- directly edit generated/vendor outputs merely because finding the canonical source is harder;
- globally forbid migrations, lockfiles, or generated files when the repository intentionally commits them;
- treat one generated failing test as necessarily equal to the full specification;
- allow test/evaluation infrastructure to be weakened merely to satisfy a completion gate unless changing that evaluation is the explicit task;
- treat hooks as infallible hard security boundaries;
- use `PostToolUse` as though it prevented an already executed write;
- invent hook output schemas or undocumented settings;
- assume native Windows has Bash or Claude Code sandbox containment equivalent to WSL2;
- silently weaken Windows execution/security policy for convenience;
- place a giant software-engineering handbook in global `CLAUDE.md`;
- freeze 2025–2026 model limitations into permanent workflow mandates.

## C. Unresolved questions

1. How should `RECONNAISSANCE_COMPLETE` be represented without creating stale state?
2. How should file ownership be tracked when an editor, build process, or another agent modifies files after the initial baseline?
3. Should dirty-file protection be path-based, content-aware, or three-way/diff-aware?
4. Which destructive Git operations should be unconditionally denied versus escalated?
5. Which project-controlled commands may safely run during reconnaissance in an untrusted repository?
6. Should high-autonomy work prefer WSL2/dev-container isolation while ordinary work remains native Windows?
7. What runtime should implement portable deterministic policy across Windows and Unix-like environments?
8. What should happen when a contextual command hook fails open?
9. Can static permission rules express enough file-level protection to minimize custom hooks?
10. How should generated-source provenance be discovered across heterogeneous ecosystems?
11. How should dependency approvals distinguish harmless tooling from significant production supply-chain changes without causing fatigue?
12. When is an automated reproducer trustworthy enough to gate implementation?
13. What should happen when reproduction is impossible or production-only?
14. How should change maps and ownership baselines refresh after compaction/resume/worktree changes?
15. What is the right trigger for an ADR?
16. How should convention preservation interact with an explicit user request to replace/refactor the architecture?
17. Can complexity metrics remain advisory telemetry without becoming gaming targets?
18. When do subagents save tokens/time end-to-end?
19. How quickly should model-compensation heuristics expire or be re-evaluated?

## D. Sources

### Tier 1 — Anthropic / Claude Code

- [Claude Code changelog](https://code.claude.com/docs/en/changelog) — live release history; cutoff baseline v2.1.287 on October 1, 2026; AGENTS.md support noted by the source research at v2.1.277 on September 18, 2026.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) — live official documentation; used for explore/plan/implement guidance, planning overhead, nearby-pattern reuse, verification, subagents, concise CLAUDE.md, and checkpoint limitations.
- [Settings files and precedence](https://code.claude.com/docs/en/settings) — live official documentation; user/project/local/managed settings and precedence/merging.
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — live official documentation; CLAUDE.md/rules/scope and AGENTS.md behavior.
- [Hooks reference](https://code.claude.com/docs/en/hooks) — live official documentation; blocking semantics, exit codes, timeout/start behavior, `PreToolUse`, `PostToolUse`, Stop, and hook output fields.
- [Configure permissions](https://code.claude.com/docs/en/permissions) — live official documentation; deny/ask/allow behavior and ordering.
- [Security](https://code.claude.com/docs/en/security) — live official documentation; workspace trust, permission boundaries, prompt injection, Windows-specific security.
- [Advanced setup](https://code.claude.com/docs/en/setup) — live official documentation; native Windows/WSL support and shell behavior.
- [Agent teams](https://code.claude.com/docs/en/agent-teams) — live official documentation; experimental coordinated-agent behavior and limitations.
- [Anthropic, “Effective harnesses for long-running agents”](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — November 26, 2025.
- [Anthropic, “How AI assistance impacts the formation of coding skills”](https://www.anthropic.com/research/AI-assistance-coding-skills) — January 29, 2026.
- [Anthropic, “Agentic coding and persistent returns to expertise”](https://www.anthropic.com/research/claude-code-expertise) — June 16, 2026.

### Tier 2 — Empirical software-engineering / agent research

- [Zhang et al., “SWE-Explore: Benchmarking How Coding Agents Explore Repositories”](https://arxiv.org/abs/2606.07297) — June 5, 2026 preprint.
- [Liu et al., “Context as a Tool: Context Management for Long-Horizon SWE-Agents”](https://aclanthology.org/2026.findings-acl.1032/) — Findings of ACL 2026.
- [Fehr et al., “CoRet: Improved Retriever for Code Editing”](https://aclanthology.org/2025.acl-short.62/) — ACL 2025.
- [Han et al., “TDFlow: Agentic Workflows for Test Driven Development”](https://aclanthology.org/2026.eacl-long.70/) — EACL 2026.
- [Zhang et al., “ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports”](https://arxiv.org/abs/2607.09123) — July 10, 2026 preprint.
- [Guo et al., “SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Multi-Faceted Bug Reproduction Tests”](https://arxiv.org/abs/2607.00990) — July 1, 2026 preprint.
- [Xia et al., “Demystifying LLM-based Software Engineering Agents”](https://doi.org/10.1145/3715754) — FSE 2025.
- [Rafique and Misic, “The Effects of Test-Driven Development on External Quality and Productivity: A Meta-Analysis”](https://doi.org/10.1109/TSE.2012.28) — IEEE Transactions on Software Engineering, online May 8, 2012.
- [Garcia de Santana Junior et al., “Architecture Decision Records: Adoption, Impact, and Developer Engagement in Open-Source Software”](https://conf.researchr.org/details/icsa-2026/icsa-2026-papers/34/Architecture-Decision-Records-Adoption-Impact-and-Developer-Engagement-in-Open-Sou) — ICSA 2026.
- [“Software metrics thresholds calculation techniques to predict fault-proneness: An empirical comparison”](https://doi.org/10.1016/j.infsof.2017.11.005) — Information and Software Technology, April 2018.
- [METR, “Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity”](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — July 10, 2025.
- [METR, “We are Changing our Developer Productivity Experiment Design”](https://metr.org/blog/2026-02-24-uplift-update/) — February 24, 2026.

### Tier 3 — Observational evidence only

- [Claude Code issue #45974, destructive `git clean -fd` report](https://github.com/anthropics/claude-code/issues/45974) — opened April 9, 2026; used only as evidence that the failure class exists, not for prevalence.
- [Claude Code issue #64559, unrequested wildcard deletion report](https://github.com/anthropics/claude-code/issues/64559) — opened June 1, 2026; used only as observational evidence.

## Corpus impact

This research status now records:

- **Brownfield reconnaissance:** strongly answered.
- **Scope/destructive change containment:** mostly answered; implementation/runtime details remain.
- **Testing strategy:** materially advanced, especially against universal TDD and single generated-test oracles.
- **Efficiency/context:** materially advanced via targeted retrieval and semantic evidence sufficiency.
- **Windows enforcement:** materially advanced; dedicated security/runtime research remains.
- **Novice interaction:** materially advanced toward consequence-based approval.
- **Completion evidence:** materially advanced; full debugging/testing/proof-of-completion remains a separate research pass.

The next highest-value research pass is **Debugging, Testing & Proof of Completion**.
