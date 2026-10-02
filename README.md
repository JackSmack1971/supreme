# Supreme Research Corpus

Research corpus for designing a production-quality global Claude Code control plane centered on `C:\Users\USERNAME\.claude\` for novice-driven software development.

## Research cutoff

Current corpus baseline: **October 1, 2026**. Claude Code product claims must be verified against Tier-1 Anthropic/Claude Code documentation current to that cutoff before they become production requirements.

## Evidence policy

This repository preserves research reports as provenance. Later reports may correct, narrow, or supersede earlier hypotheses. Do not silently rewrite older reports to make them appear consistent.

When reports conflict, use this order:

1. Current official Claude Code documentation/changelog and current documented schemas.
2. Official Anthropic engineering/research evidence.
3. Peer-reviewed or strong primary empirical research.
4. Reproducible benchmark evidence.
5. Practitioner/issue-tracker evidence for failure classes, not incidence estimates.
6. Engineering judgment, explicitly labeled as such.

An undocumented Claude Code setting, hook schema, environment variable, path, frontmatter field, CLI switch, or feature must not become a production dependency merely because an earlier report named it.

## Current corpus

| Document | Role | Current status |
|---|---|---|
| `Claude Code Capability Inventory Research.md` | Initial capability/configuration inventory | Useful baseline; some product claims require re-verification against later research |
| `Claude Code Control Surfaces.md` | Allocation across CLAUDE.md, rules, skills, agents, hooks, workflows, etc. | Strong directional input; later evidence governs disputed product details |
| `Global Claude Code Control Plane Architecture for Novice-Driven Software Development.md` | Initial novice lifecycle/control-plane architecture | Hypothesis-generating; methodology mandates are not automatically accepted requirements |
| `Preventing Architectural Decay in Agent-Generated Greenfield Projects.md` | Greenfield architecture safeguards | Valuable failure analysis; universal architecture/threshold claims are downgraded to conditional hypotheses |
| `Evidence-Backed Brownfield Reconnaissance and Change Containment.md` | Full research report for repository reconnaissance, scope containment, and destructive-action control | **Accepted research input**; supersedes conflicting earlier prescriptions in this scope |
| `Containment, Auto Mode, Network, and Change-Surface Addendum.md` | Focused addendum on Auto mode, approval fatigue, environmental containment, network/secrets boundaries, and deviation-based scope control | **Accepted research addendum**; governs where more specific in this scope |

## Accepted cross-project invariants

The current evidence supports a **small universal kernel plus project-derived behavior**, not a giant global methodology.

The global control plane should preserve these invariants:

- Preserve pre-existing user work and distinguish it from agent-created changes.
- Discover repository instructions before applying global preferences.
- Discover the repository's actual build/test/lint/typecheck/generation workflow rather than assuming generic commands.
- Prefer existing nearby implementations and repository conventions over the agent's preferred architecture.
- Search for existing utilities before creating new abstractions.
- Identify public/API/schema/persistence/dependency boundaries before nontrivial edits.
- Establish observable behavior or another credible verification oracle before claiming completion.
- Keep implementation scope proportional and explicitly surface unresolved high-impact decisions.
- Use the simplest reliable enforcement mechanism: declarative permission denials for static hazards; contextual hooks only where computation is needed; human approval for ambiguous consequential actions.
- Treat Windows as a first-class environment and never claim sandbox containment where the platform does not provide it.
- Validate control-plane health; a missing or failing hook/interpreter must not silently masquerade as protection.
- Prefer hard filesystem/network/credential boundaries over repeated permission prompts when the execution environment supports them.
- Treat Claude Code Auto mode as an **experimental probabilistic supervision layer**, not deterministic containment.
- Use task-local expected/protected change surfaces to detect scope deviation; do not impose universal file-count or line-count caps.
- Keep model-compensation heuristics replaceable as Claude Code/model capabilities evolve.

## Brownfield pre-write policy

For nontrivial existing-repository work, the accepted research direction is:

`PRESERVE STATE -> DISCOVER INSTRUCTIONS -> DISCOVER TOOLCHAIN -> LOCALIZE BEHAVIOR -> INSPECT NEARBY PATTERNS/INTERFACES -> IDENTIFY SENSITIVE/GENERATED AREAS -> ESTABLISH REPRODUCER/ORACLE -> BUILD PROPORTIONAL CHANGE MAP -> WRITE`

This is an **adaptive evidence-sufficiency protocol**, not a fixed file-count/token-count ceremony. Small obvious changes may take a shorter path when the relevant facts are already evident.

The Evidence Sufficiency Gate is semantic. Before nontrivial writes, the agent should be able to state from repository evidence:

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

## Consequence-based escalation boundary

For the novice-oriented profile, **model confidence does not waive escalation** for operations with hard-to-reverse or externally consequential effects.

Always escalate by default:

- discarding, overwriting, obscuring, cleaning, resetting, or otherwise destroying pre-existing user work;
- destructive Git cleanup/restoration that can affect files outside an agent-owned disposable worktree;
- irreversible or data-destructive migrations and production-data mutations;
- production deployments, production configuration changes, or infrastructure actions with material external side effects;
- credential, secret, authentication, authorization, encryption, or other security-boundary changes whose consequences cannot be safely established from repository-local evidence alone;
- external network actions that create, delete, publish, bill, provision, revoke, or otherwise mutate remote state outside ordinary local development;
- breaking public API/schema/CLI/persistence contracts unless the compatibility break was explicitly requested and authorized.

Escalate unless standing project/user authorization already exists:

- adding or materially upgrading production/runtime dependencies;
- deliberately departing from established repository architecture or conventions.

Do **not** translate this into approval spam. Harmless read-only inspection, ordinary edits inside the evidenced change surface, local deterministic checks, and reversible project-authorized actions should remain autonomous.

## Enforcement hierarchy

Use the simplest mechanism that actually provides the required guarantee:

1. `permissions.deny` for static expressible catastrophic prohibitions.
2. `PreToolUse` for contextual/computed decisions.
3. project-local instructions/rules/skills for behavioral guidance.
4. `PostToolUse` for validation and corrective feedback, never as retroactive prevention.
5. Stop/completion checks for evidence required before claiming work finished.
6. explicit human approval for consequential ambiguity or irreversible/external effects.

Hooks are not assumed infallible. Command hooks can fail open on timeout/start failure/nonblocking errors, so hook health and runtime availability are themselves control-plane requirements.

## Containment and autonomy policy

Anthropic's 2025–2026 engineering evidence favors **containment plus selective supervision** over repeated approval prompts. Anthropic reports that users approve roughly 93% of permission dialogs and that sandboxing reduced prompts by 84% in internal use. Its documented overeager-action incidents include remote-branch deletion, credential misuse, and attempted production migrations.

Supreme therefore treats the layers differently:

1. **Environment containment where available:** filesystem reach, network egress, and credential exposure.
2. **Declarative permissions:** static deny/ask/allow policy.
3. **Auto mode where supported:** experimental model-classifier supervision that reduces prompts but is not deterministic.
4. **Contextual `PreToolUse`:** computed task-local ownership/scope decisions.
5. **Human escalation:** irreversible, security-sensitive, ambiguous, or externally consequential operations.

When an action can be safely denied and the agent can pursue a harmless alternative, prefer **deny-and-continue** over immediately interrupting the user. Repeated denials or consequential ambiguity should escalate.

For high-autonomy or untrusted work, strong containment requires both filesystem and network boundaries and minimizing reachable credentials. Native Windows must not be described as having the same Claude Code sandbox guarantees as supported WSL2/Linux/macOS environments.

## Superseded or downgraded hypotheses

The following earlier ideas are **not accepted as universal global requirements** unless later evidence re-establishes them:

- Mandatory Vertical Slice Architecture, Clean Architecture, hexagonal architecture, layered architecture, microservices, modular monoliths, CQRS, event sourcing, or any other single topology.
- Fixed global complexity thresholds such as cyclomatic complexity `<=10`/`<=15`, `>85%` feature-local dependencies, maximum file counts, or changed-line limits.
- Mandatory ADR creation for every architectural-looking change.
- Universal TDD. The invariant is credible verification, not one test-ordering doctrine.
- Mandatory multi-agent or agent-team routing for substantive tasks.
- Reading the entire repository before editing.
- Heavyweight planning/change-map documents for trivial obvious edits.
- Treating `PostToolUse` as a mechanism that prevents a tool action that already executed.
- Treating command hooks as infallible security boundaries.
- Assuming native Windows Claude Code provides the same sandbox guarantees as WSL2.
- Shipping undocumented configuration keys. Earlier references to `defaultShell`, `autoCompactEnabled`, `askUserQuestionTimeout`, or a settings key named `ultracode` remain excluded until independently verified in Tier-1 documentation/schema for the target Claude Code version.

## Research coverage

Completed or substantially covered:

- Claude Code capability/configuration surface
- Control-surface responsibility allocation
- Novice-to-MVP lifecycle foundations
- Greenfield architectural failure analysis
- **Brownfield reconnaissance — strongly answered**
- **Scope/destructive change containment — strongly answered at the policy level; implementation/runtime mechanics remain**
- Testing strategy foundations against universal TDD and single generated-test oracles
- Efficiency/context foundations through targeted retrieval and evidence sufficiency
- Windows-enforcement constraints relevant to native Windows vs WSL2
- Novice approval design toward consequence-based escalation
- Auto mode / approval-fatigue / deny-and-continue policy
- Network egress, secret-boundary, and credential-minimization principles
- Deviation-based change-surface control instead of fixed maximum diff thresholds

Still requiring dedicated or consolidated research before final design:

- Root-cause debugging, testing strategy, and proof-of-completion semantics
- Durable project state, grounding, memory, and documentation-drift detection
- Windows-native security, credentials, hook runtime, and containment architecture
- Adaptive orchestration, cost/latency policy, and independent-task routing
- Maintainability quality ratchets, novice interaction policy, and evaluation/ablation methodology

## Design principle

Supreme should not be a static pile of prompts that forces every repository into one engineering ideology. The target is an evidence-driven control plane with:

- a thin universal invariant layer,
- deterministic safety where the platform can actually enforce it,
- project-derived conventions and verification,
- progressive disclosure through skills/rules,
- isolated agents/workflows only when their cost is justified,
- durable evidence across sessions/compaction,
- explicit human escalation for consequential ambiguity,
- version-aware validation of Claude Code configuration and control surfaces, and
- an evaluation/ablation loop that requires every added rule, hook, skill, agent, or workflow to earn its complexity.

## Next research priority

The next highest-value pass is **Debugging, Testing & Proof of Completion**:

`OBSERVE -> REPRODUCE -> LOCALIZE -> HYPOTHESIZE -> DISCRIMINATE -> FIX -> VERIFY -> REGRESSION CHECK -> COMPLETE`

The research should determine which transitions require executable evidence, when independent verification is warranted, how to resist test gaming, and exactly what evidence permits Claude to claim that work is fixed, passing, working, or complete.
