# **Engineering Research Report: Canonical Capability Surface and Global Control Plane Architecture for Claude Code on Windows**

The architectural formulation of a global control plane for autonomous coding agents demands a rigorous, evidence-based delineation between deterministic constraint enforcement, probabilistic model guidance, and execution lifecycle state management. This comprehensive analysis exhausts the configuration mechanisms, extension interfaces, and empirically documented failure modes of Claude Code, strictly bounded by capabilities available as of October 1, 2026\. The objective is to design a centralized, secure, and production-grade Windows control plane rooted in the global %USERPROFILE%\\.claude\\ directory, optimizing for PowerShell portability, strict execution security, and usability for software-engineering novices.  
The analysis synthesizes authoritative documentation, peer-reviewed empirical studies, and deployment observations to separate deterministic run-time enforcement from probabilistic model behavior. It specifically evaluates token cost dynamics, context pollution, and the systemic risks of agent hallucination to define the boundaries of a robust execution harness.

## **Canonical Supported Configuration Surface Matrix**

The following matrix establishes the exact resolution paths, precedence rules, context mechanics, and operational status for all officially supported configuration vectors. In Windows environments, the POSIX \~/.claude/ path resolves natively to %USERPROFILE%\\.claude\\, though enterprise architectures frequently override this globally via the CLAUDE\_CONFIG\_DIR environment variable to ensure multi-tenant isolation1.

| Mechanism | Global / User Path | Project-Local Equivalent | Precedence Rules | Merge vs Override | Context Entry | Token Cost | Discovery | Invocation | Det. vs Prob. | Windows Support | Security Implications | Status |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **CLAUDE.md** | \~/.claude/CLAUDE.md | CLAUDE.md, .claude/CLAUDE.md, CLAUDE.local.md | Managed \> Project \> Global | Loads all concurrently | Session start | High (Always active) | Auto-discovered | Probabilistic | Probabilistic | Full | Low (Guidelines only) | Stable |
| **Rules** | \~/.claude/rules/\*.md | .claude/rules/\*.md | Managed \> Project \> Global | Loads all matched | Dynamic (on file match) | Variable (Scoped) | Auto-discovered | Probabilistic | Probabilistic | Full | Low (Context only) | Stable |
| **Skills** | \~/.claude/skills/\<name\>/SKILL.md | .claude/skills/\<name\>/SKILL.md | Local \> Project \> Global \> Synced | Overrides by name | Invocation only | Low upfront; High on use | Auto-discovered | Both (Model & User) | Probabilistic | Full | Moderate (Arbitrary prompts) | Stable |
| **Agents / Subagents** | \~/.claude/agents/\*.md | .claude/agents/\*.md | Managed \> CLI \> Project \> Global \> Plugin | Overrides by name | Replaces main context | High (Isolated windows) | Auto-discovered | Both (Model & User) | Probabilistic | Full | High (Tool sandboxing) | Stable |
| **Agent Teams** | N/A (Env Var enabled) | N/A | Feature toggle | N/A | Peer contexts | Extreme (Multi-agent) | CLI Triggered | Both | Probabilistic | Partial (No tmux natively) | High (Peer hallucination) | Experimental |
| **Dynamic Workflows** | \~/.claude/workflows/\*.js | .claude/workflows/\*.js | Local \> Global | Overrides by name | Out-of-band | High (Orchestrates agents) | Auto-discovered | Both (Model & User) | Deterministic script, Prob. agents | Full | High (Arbitrary JS) | Preview |
| **Hooks** | settings.json (hooks key) | settings.json (hooks key) | Managed \> Local \> Project \> Global | Merges arrays | Conditionally via output | Negligible | Auto-discovered | Runtime enforced | Deterministic | Full (PowerShell requires config) | Critical (Executes binaries) | Stable |
| **Settings.json** | \~/.claude/settings.json | .claude/settings.json, .claude/settings.local.json | Managed \> CLI \> Local \> Project \> Global | Scalars override, Arrays merge | Never | Zero | Runtime loaded | Runtime enforced | Deterministic | Full | Critical (Overrides behavior) | Stable |
| **Global Config** | \~/.claude.json | None | Overridden only by CLI | Overrides | Never | Zero | Runtime loaded | Runtime enforced | Deterministic | Full | Critical (Auth & State) | Stable |
| **Permissions** | settings.json (permissions key) | settings.json | Managed \> Local \> Project \> Global | Merges arrays | Never | Zero | Runtime loaded | Runtime enforced | Deterministic | Full | Critical (Tool gating) | Stable |
| **Output Styles** | \~/.claude/output-styles/\*.md | .claude/output-styles/\*.md | Closest to working dir | Overrides | Session start | High (Replaces core prompt) | Auto-discovered | Both | Probabilistic | Full | High (Removes safety rails) | Stable |
| **Auto Memory** | \~/.claude/projects/\<proj\>/memory/ | None (Managed in global path) | Global only | Appends | Session start | Escalating | Auto-discovered | Both | Probabilistic | Full | High (Plaintext secret leak) | Stable |
| **Status Line** | settings.json (statusLine) | settings.json | Managed \> Project \> Global | Overrides | Never | Zero | Runtime loaded | Runtime enforced | Deterministic | Full | Moderate (Stdin data exposure) | Stable |
| **MCP Servers** | \~/.claude.json | .mcp.json | Managed \> Project \> Global | Merges servers | Session start (Descriptions) | Low upfront | Auto-discovered | Both | Probabilistic | Full | Critical (External access) | Stable |
| **Plugins** | \~/.claude/plugins/ | settings.json | Managed \> Project \> Global | Loads all enabled | Startup | Variable (per component) | Runtime loaded | Runtime enforced | Both | Full | Critical (Arbitrary execution) | Stable |
| **LSP Plugins** | \~/.claude/plugins/ | settings.json | Same as plugins | Loads all enabled | Connects at start | Low | Runtime loaded | Both | Deterministic server, Prob. usage | Full | High (Code execution) | Stable |
| **Worktrees** | .worktreeinclude | .worktreeinclude | Project only | Overrides | On isolation trigger | Zero | Runtime loaded | Runtime enforced | Deterministic | Full | Moderate (Storage & Secrets) | Stable |
| **Checkpoints** | \~/.claude/file-history/ | None | Global only | Overwrites on limit | On restore request | Zero | Auto-managed | User only | Deterministic | Full | Moderate (State rollback) | Stable |
| **Background Agents** | N/A | N/A | N/A | N/A | Out-of-band | High | User CLI | User only | Probabilistic | Full | Moderate | Stable |
| **/goal** | N/A | N/A | N/A | N/A | Turn end | Low (Fast model) | CLI Triggered | User only | Probabilistic | Full | Moderate (Prevents loop) | Stable |
| **Cross-Session Messaging** | settings.json (crossSessionInbound) | N/A | Global only | Overrides | On receipt | Low | Runtime loaded | Both | Probabilistic | Full | Moderate (Context injection) | Stable |
| **Channels** | .mcp.json | .mcp.json | Project \> Global | Merges servers | On external event | Extreme (Push polling) | Runtime loaded | External trigger | Deterministic trigger, Prob. response | Full | Critical (Prompt Injection) | Preview |
| **Scheduled Tasks** | Local App State | N/A | Desktop App only | Overrides | Scheduled time | High | User configured | Daemon trigger | Deterministic trigger, Prob. response | Full | Moderate | Stable |
| **Routines** | Cloud API | N/A | Cloud only | Overrides | API/GitHub event | High | Cloud configured | External trigger | Deterministic trigger, Prob. response | N/A (Cloud) | Moderate | Stable |

### **Non-Native Community Conventions**

The analysis identifies specific conventions heavily utilized by the developer community that are not native Claude Code mechanisms, though the runtime tolerates them:

> 1. **AGENTS.md Files:** Claude Code parses AGENTS.md automatically alongside CLAUDE.md to maintain compatibility with competing coding agents (e.g., Cursor, Aider), but this file does not unlock unique configuration pathways; it acts identically to a global context injection2.  
> 2. **Custom Bash Orchestrator Loops:** Novices frequently attempt to write custom Bash scripts to continuously loop Claude Code execution until a test passes. This is an anti-pattern superseding the native /goal evaluator and dynamic workflows, often resulting in catastrophic token consumption and endless error loops without proper semantic evaluation4.

## **Configuration Precedence and Deterministic Foundations**

The architectural foundation of the control plane depends entirely on the correct evaluation of configuration file precedence and the rigid enforcement of deterministic settings. Probabilistic mechanisms, such as system prompts, cannot provide verifiable security guarantees.

### **Material Finding 1: Array Merging vs. Scalar Overrides in Configuration**

> 1. **Finding:** Within settings files (settings.json), array structures such as permissions.allow and permissions.deny undergo a merging process across all scopes (Managed, Local, Project, Global), whereas scalar values completely override lower-precedence definitions.  
> 2. **Evidence/source:** Official Claude Code settings precedence documentation1.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** settings.json, managed-settings.json, Permissions.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic.  
> 7. **Cost/context implications:** Zero token footprint. Handled entirely by the underlying Node/TypeScript runtime.  
> 8. **Security implications:** This behavior introduces a critical security vulnerability for novice users. A permissive local .claude/settings.local.json file inside a cloned repository can maliciously inject unauthorized tools into the permissions.allow array, combining them with the user's global constraints rather than replacing them. Secure control planes must utilize the enterprise managed-settings.json file or explicitly deploy disableClaudeAiConnectors: true (a scalar override) to enforce restrictive precedence, as managed policies definitively override all lower tiers1.  
> 9. **Open question remaining:** How does the deterministic runtime evaluate overlapping and contradictory regular expressions injected into the merged allow and deny permission arrays from differing topological scopes?

### **Material Finding 2: PowerShell Execution Policy Bypass on Windows Hosts**

> 1. **Finding:** By default, Claude Code proactively bypasses the native Windows execution policy at the process scope when spawning PowerShell instances (-ExecutionPolicy Bypass), permitting arbitrary script execution regardless of the host's administrative restrictions.  
> 2. **Evidence/source:** Claude Code environment variable definitions and configuration overrides7.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Bash / PowerShell Tool Execution.  
> 5. **Global \~/.claude candidate?:** Yes, via environment variable configurations.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic.  
> 7. **Cost/context implications:** Zero token footprint.  
> 8. **Security implications:** This default behavior allows agents to download and execute arbitrary PowerShell payloads seamlessly. A production Windows control plane must deploy the environment variable CLAUDE\_CODE\_POWERSHELL\_NO\_BYPASS=1 (or its equivalent toggle in settings.json) to enforce local system administration policies and prevent unauthorized process spawning7.  
> 9. **Open question remaining:** Does setting the no-bypass execution flag subsequently cripple the execution of legitimate, user-defined PreToolUse hook scripts written in PowerShell?

## **Probabilistic Context and Knowledge Management**

The system relies extensively on Markdown files (CLAUDE.md, rules, skills) to provide the agent with project conventions and architectural constraints. These mechanisms are probabilistic; the model interprets the text but is not deterministically bound by it. Reliance on these files for security or absolute execution paths constitutes a systemic failure mode.

### **Material Finding 3: Context Pollution and Path-Gated Rule Optimization**

> 1. **Finding:** Global and project-root CLAUDE.md files are loaded entirely into the active context window at the start of every session, creating persistent and escalating token bloat. In contrast, files placed in .claude/rules/\*.md utilize YAML paths: frontmatter glob patterns to inject context dynamically only when matching files are accessed or modified.  
> 2. **Evidence/source:** Claude Code context window and memory management documentation9.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** CLAUDE.md and .claude/rules/\*.md.  
> 5. **Global \~/.claude candidate?:** Yes, for user-level global rules.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Prompt-based guidance.  
> 7. **Cost/context implications:** This represents a massive cost optimization mechanism. Path-gated rules prevent hundreds of thousands of tokens from polluting the active context during unrelated tasks, lowering per-turn latency and preserving the model's attention span for pertinent code blocks10.  
> 8. **Security implications:** Low. These files provide instructions for formatting, code structure, and logic. They do not constitute an access control mechanism.  
> 9. **Open question remaining:** What is the maximum recursive directory traversal depth the path-matching algorithm permits before timing out in massive enterprise monorepos?

### **Material Finding 4: Safety Guardrail Stripping via Output Styles**

> 1. **Finding:** Custom output styles defined in \~/.claude/output-styles/\*.md completely replace Claude Code's built-in software engineering instructions (which govern scoping changes, writing comments, and verifying destructive work) unless the keep-coding-instructions: true frontmatter key is explicitly provided.  
> 2. **Evidence/source:** Output styles configuration and frontmatter documentation12.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Output Styles.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Prompt-based.  
> 7. **Cost/context implications:** Custom styles can drastically alter token usage economics. A terse style reduces output token consumption, while an explanatory style exponentially increases it.  
> 8. **Security implications:** Stripping the core engineering instructions removes the foundation model's baseline safety prompts regarding destructive file operations and verification loops, severely degrading the overall reliability and safety of the autonomous agent12.  
> 9. **Open question remaining:** Does dynamically applying a new custom output style via the /output-style command immediately invalidate the existing prompt cache for the entire session?

### **Material Finding 5: Auto-Memory Plaintext Cryptographic Leakage**

> 1. **Finding:** The agent's autonomous observations and cross-session learnings are continuously appended to persistent plaintext files located in \~/.claude/projects/\<project\>/memory/, which are subsequently re-injected into the context window at the start of every new session.  
> 2. **Evidence/source:** Claude directory schema and auto-memory documentation2.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Auto Memory.  
> 5. **Global \~/.claude candidate?:** Yes (data storage).  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Probabilistic generation, Deterministic storage.  
> 7. **Cost/context implications:** Auto-memory compounding leads to significant token consumption over the lifecycle of a project as the agent recursively reads its own historical notes at startup.  
> 8. **Security implications:** High risk of secret leakage. The agent routinely memorizes sensitive credentials, database connection strings, or environment variables it observes in terminal outputs, persisting them indefinitely in unencrypted plaintext on the local disk2.  
> 9. **Open question remaining:** Can a deterministic PreToolUse hook intercept the internal memory-writing tool to programmatically scrub cryptographic secrets before they are committed to the filesystem?

## **Capability Extension: Tools, MCP, and Lazy Loading**

To expand the baseline capabilities of the model beyond terminal command execution, the architecture utilizes Skills for reusable prompts, MCP (Model Context Protocol) servers for external API integration, and Plugins for ecosystem distribution.

### **Material Finding 6: Lazy Loading of Skill Tokens**

> 1. **Finding:** Skills defined in \~/.claude/skills/\<name\>/SKILL.md do not load their body text into the model's active context window until they are explicitly invoked by the user (/name) or autonomously invoked by the model via the Skill tool.  
> 2. **Evidence/source:** Skills syntax and features overview9.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Skills.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Prompt-based (invocation is probabilistic unless explicitly restricted).  
> 7. **Cost/context implications:** This architecture guarantees zero upfront token cost aside from injecting the skill's name and description into the system prompt. It is the most token-efficient method for distributing large operational playbooks9.  
> 8. **Security implications:** By setting the disable-model-invocation: true key in the YAML frontmatter, administrators can cryptographically ensure the model cannot hallucinate the usage of a destructive operational skill autonomously; it mandates explicit human invocation9.  
> 9. **Open question remaining:** When dynamic shell injection is used within a skill's body (\!command), does the evaluation occur within the bounds of the host's PowerShell execution policy restrictions, or is it executed via a secondary subprocess wrapper?

### **Material Finding 7: Language Server Protocol (LSP) Telemetry Optimization**

> 1. **Finding:** Claude Code implements deep code intelligence by integrating native LSP plugins via the Model Context Protocol, permitting the agent to perform precise operations such as finding symbol references, jumping to definitions, and intercepting compiler type errors directly.  
> 2. **Evidence/source:** Plugin code intelligence and tools schema reference14.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** LSP plugins and MCP.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic execution, probabilistic invocation.  
> 7. **Cost/context implications:** Substantially reduces context window bloat and execution latency. Instead of the agent running broad, token-heavy Grep or Read commands over entire repositories and consuming raw output, it receives precise programmatic JSON responses from the LSP server15.  
> 8. **Security implications:** LSP servers inherently execute arbitrary workspace code (e.g., executing Python setup scripts or Java build processes to resolve dependency trees). Enabling LSP plugins in untrusted repositories introduces arbitrary code execution vectors outside the direct purview of the primary agent process.  
> 9. **Open question remaining:** Which specific Windows-native LSP binaries (e.g., pylsp, omnisharp) are officially supported and distributed out-of-the-box by Anthropic's verified plugin marketplace?

## **Autonomous Orchestration, Subagents, and Empirical Failures**

The control plane must manage the parallelization of tasks and strict context isolation. Claude Code provides subagents for focused tasks, agent teams for peer coordination, and dynamic workflows for JavaScript-based programmatic orchestration. Peer-reviewed empirical research isolates severe failure modes in these paradigms.

### **Material Finding 8: Epistemic Errors and SubRetrv Token Waste**

> 1. **Finding:** Controlled empirical research demonstrates that 57.9% of all coding agent failures stem from epistemic errors (operating on false assumptions without prior verification). Concurrently, a significant portion of execution cost is wasted on SubRetrv—a behavioral loop where the main agent continuously re-reads code that was already processed and retrieved by a subagent.  
> 2. **Evidence/source:** Peer-reviewed arXiv studies on coding agent failure trajectories and cost inefficiencies (e.g., SWE-bench metrics)16.  
> 3. **Evidence strength:** Strong (Empirical primary research).  
> 4. **Claude Code mechanism implicated:** Subagents and overall Tool Execution.  
> 5. **Global \~/.claude candidate?:** No (This is an observed behavioral failure mode).  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic mitigation via Hooks.  
> 7. **Cost/context implications:** Rampant token waste and latency degradation. Subagents frequently regenerate identical files and endlessly re-read data they have already processed, burning API credits rapidly without advancing the project state17.  
> 8. **Security implications:** Epistemic errors frequently result in agents attempting escalating, destructive recovery actions (e.g., aggressively deleting and recreating environments or wiping package caches) when they misdiagnose the underlying codebase issue16.  
> 9. **Open question remaining:** Can a deterministic PostToolUse hook intercept the SubRetrv behavior by parsing tool output, caching it locally, and serving an abbreviated summary to the model to break the infinite retrieval loop?

### **Material Finding 9: Agent Teams Context Scaling Collapse**

> 1. **Finding:** The Agent Teams feature (CLAUDE\_CODE\_EXPERIMENTAL\_AGENT\_TEAMS) spawns multiple concurrent instances of Claude Code that communicate peer-to-peer via a shared task list. While this provides parallel exploratory power, it generates severe token overhead compared to sequential subagent delegation.  
> 2. **Evidence/source:** Agent teams documentation and operational guidelines18.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Agent Teams.  
> 5. **Global \~/.claude candidate?:** Conditional (Must be strictly enabled via global environment variables).  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Human approval (Mandatory due to cost explosion).  
> 7. **Cost/context implications:** Extreme and unpredictable token burn rates. Every deployed teammate maintains an entirely isolated context window, redundantly loading the global CLAUDE.md, and continually processes verbose inter-agent messaging strings18.  
> 8. **Security implications:** Teammates frequently hallucinate agreements or validations with one another (peer hallucination), compounding the aforementioned epistemic errors across multiple execution threads. Furthermore, Agent Teams rely on split-pane terminal rendering (like tmux), which poses severe compatibility and rendering issues on native Windows consoles19.  
> 9. **Open question remaining:** How does the Claude Code Windows host natively handle the rendering of split-pane agent team outputs without resorting to WSL or third-party multiplexers?

### **Material Finding 10: Headless Goal Evaluation via Fast Models**

> 1. **Finding:** The /goal command delegates the continuous evaluation of task completion criteria to a secondary, smaller "fast model" that autonomously checks the terminal execution state after every turn, operating entirely out-of-band from the primary reasoning model.  
> 2. **Evidence/source:** Goal command documentation5.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** /goal Evaluator.  
> 5. **Global \~/.claude candidate?:** No.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Probabilistic generation, deterministic evaluation triggers.  
> 7. **Cost/context implications:** Introduces recurring micro-costs due to continuous fast-model queries, but mathematically prevents the massive token burn associated with an agent endlessly spinning in a failed state5.  
> 8. **Security implications:** Serves as a vital circuit breaker. It prevents runaway execution loops where the primary agent exhibits "inaccurate self-reporting"—believing it has succeeded in deploying code when the terminal environment remains critically broken20.  
> 9. **Open question remaining:** Which exact model alias (e.g., Haiku vs. Sonnet) is hardcoded for the background /goal evaluator, and can it be globally overridden in settings.json?

## **Event-Driven Lifecycle and Deterministic Hook Execution**

Hooks constitute the definitive security and automation boundary for the entire control plane. They allow arbitrary shell scripts, HTTP requests, or JavaScript modules to execute deterministically at highly specific lifecycle events.

### **Material Finding 11: PreToolUse Security Mediation and STDIO Execution**

> 1. **Finding:** PreToolUse hooks receive comprehensive JSON event data via standard input (stdin) and possess the authority to definitively block model actions by exiting with a serialized JSON object dictating a permissionDecision of allow, deny, ask, or defer.  
> 2. **Evidence/source:** Hooks guide and schema reference documentation6.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Hooks and Hook Scripts.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic.  
> 7. **Cost/context implications:** Absolute zero token footprint unless the hook explicitly returns a hookSpecificOutput.additionalContext object, which subsequently injects string data into the model's prompt stream21.  
> 8. **Security implications:** This mechanism is the primary and most robust defense against catastrophic autonomous failures. A global PowerShell script registered as a PreToolUse hook can syntactically analyze every Bash tool invocation for destructive Windows commands (e.g., Remove-Item \-Recurse \-Force) and forcefully deny the tool call before the OS execution layer is ever reached, bypassing model hallucination entirely6.  
> 9. **Open question remaining:** Do multiple PreToolUse hooks matching the same tool invocation execute sequentially in a blocking chain, or concurrently, and how are conflicting decisions (e.g., one hook returns allow, another returns deny) reconciled by the runtime engine?

### **Material Finding 12: Auto-Mode Classifier Manipulation via PostToolUse**

> 1. **Finding:** A PostToolUse callback script can return a classifierContext string to feed a concise note directly into the auto-mode permission classifier, programmatically manipulating how the system calculates the risk heuristic of subsequent agent actions.  
> 2. **Evidence/source:** Agent SDK hooks documentation and event references23.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** PostToolUse Hooks.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic execution manipulating probabilistic evaluation.  
> 7. **Cost/context implications:** Negligible execution cost.  
> 8. **Security implications:** Extreme vulnerability. A compromised or poorly written local hook script could continuously feed benign-looking classifierContext notes to the auto-mode evaluator. This effectively tricks the risk classifier into bypassing human approval prompts for escalating, destructive actions, blinding the user to the agent's actual intent23.  
> 9. **Open question remaining:** What is the precise integer character limit for the classifierContext field before the runtime engine silently truncates the payload?

### **Material Finding 13: Push-Event Prompt Injection via Channels**

> 1. **Finding:** The experimental Channels feature enables an external MCP server to push events (such as CI pipeline failures or Discord chat messages) directly into an active, headless Claude Code session, prompting the agent to react autonomously to state changes without human terminal interaction.  
> 2. **Evidence/source:** Channels reference and configuration guides24.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Channels and MCP Servers.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic access control.  
> 7. **Cost/context implications:** Massive risk of token exhaustion. An unchecked channel bridging a high-velocity Slack room to the agent will consume tens of thousands of tokens per minute as the agent continuously evaluates and responds to every incoming message24.  
> 8. **Security implications:** Ungated channels serve as direct, unauthenticated prompt injection vectors. Any external actor capable of reaching the channel endpoint can inject malicious instructions directly into the session's active context window, commanding the agent to execute shell scripts on the host machine24.  
> 9. **Open question remaining:** How does the Node runtime serialize concurrent asynchronous channel events arriving precisely while the model is blocking on the execution of a synchronous, long-running shell tool call?

## **Isolation, State Rollback, and Continuous Artifact Archiving**

For an autonomous agent to function across disparate repositories without cross-contamination or irreversible workspace destruction, the control plane must enforce rigorous state isolation and rollback mechanics.

### **Material Finding 14: Worktree Sandboxing for Subagents**

> 1. **Finding:** Subagents can be strictly isolated into temporary Git worktrees by configuring the isolation: worktree key in their YAML frontmatter. This branches the environment off the repository's default branch rather than the session's active HEAD, segregating experimental code generation from the developer's working state.  
> 2. **Evidence/source:** Subagent frontmatter reference and architecture documentation26.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Subagents and Git Worktrees.  
> 5. **Global \~/.claude candidate?:** Conditional (Applied per agent definition in global path).  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic.  
> 7. **Cost/context implications:** Requires significant physical disk I/O and storage capacity for the duplicated repository worktree, but entirely prevents context and file pollution in the primary interactive session.  
> 8. **Security implications:** This deterministically isolates destructive file writes to a disposable branch. If a subagent hallucinates and recursively deletes source files, the primary HEAD and local uncommitted changes remain untouched and secure26.  
> 9. **Open question remaining:** Does the .worktreeinclude file parser support regex negations to explicitly prevent sensitive local configurations (e.g., .env files containing production database credentials) from being automatically copied into the isolated subagent worktree?

### **Material Finding 15: Deterministic Checkpoint State Restoration**

> 1. **Finding:** The fileCheckpointingEnabled setting (defaulting to true) mandates that Claude Code snapshots all target files into \~/.claude/file-history/\<session\>/ immediately prior to editing them, enabling precise, deterministic rollbacks via the /rewind command.  
> 2. **Evidence/source:** Settings reference and Claude internal directory schema2.  
> 3. **Evidence strength:** Strong.  
> 4. **Claude Code mechanism implicated:** Checkpoints and File History.  
> 5. **Global \~/.claude candidate?:** Yes.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** Deterministic.  
> 7. **Cost/context implications:** Negligible token cost, moderate disk storage cost. The global system retains up to 100 recent file checkpoints per active session before triggering the cleanup sweep2.  
> 8. **Security implications:** Provides a critical, non-probabilistic recovery mechanism against "faulty implementation" failures (a leading cause of agent degradation). If an agent autonomously corrupts a build script or introduces a syntax error, the novice user can instantly restore the pre-edit snapshot without parsing Git logs2.  
> 9. **Open question remaining:** Do file checkpoints natively capture underlying filesystem metadata (such as executable bits, ACLs, and modification timestamps), or do they strictly archive plaintext file contents?

### **Material Finding 16: Scaffold Conflation and Benchmark Noise**

> 1. **Finding:** Variations in agent harness configurations (the control plane) account for massive statistical variations in task success rates. Empirical benchmarking on SWE-bench reveals swings of up to 20 percentage points for the exact same foundation model depending on the harness implementation.  
> 2. **Evidence/source:** Peer-reviewed arXiv research on evaluating agent fixes and scaffolding conflation28.  
> 3. **Evidence strength:** Strong (Empirical primary research).  
> 4. **Claude Code mechanism implicated:** The holistic Control Plane Environment.  
> 5. **Global \~/.claude candidate?:** N/A.  
> 6. **Should enforcement be prompt-based, deterministic, or human approval?:** N/A.  
> 7. **Cost/context implications:** Poor scaffolding burns massive amounts of tokens with zero corresponding improvement in task resolution.  
> 8. **Security implications:** An improperly designed control plane cannot be compensated for by a "smarter" or larger foundation model. The harness must rigidly dictate security, execution bounds, and memory flow28.  
> 9. **Open question remaining:** Which specific scaffold variables within Claude Code (e.g., container memory allocation, maximum shell read limits, or context window compaction thresholds) possess the highest statistical correlation with successful task resolution?

## **A. Design Requirements Derived from the Evidence**

To construct a production-quality, novice-friendly global control plane under C:\\Users\\USERNAME\\.claude\\ on Windows, the final architecture must adhere to the following strict requirements derived from the collected evidence:

> 1. **Deterministic Execution Layering**: The control plane must implement security constraints entirely via PreToolUse hooks (defined in a global \~/.claude/settings.json) that intercept, parse, and validate Bash and PowerShell commands, preventing destructive operations prior to OS evaluation6. Prompt-based rules (CLAUDE.md) must be reserved exclusively for project styling and semantic formatting11.  
> 2. **Environment Variable Enclosures**: Because the runtime defaults to bypassing PowerShell execution policies (-ExecutionPolicy Bypass), the control plane initialization scripts must export CLAUDE\_CODE\_POWERSHELL\_NO\_BYPASS=1 to ensure local Windows system administrators retain total control over agent scripting capabilities7.  
> 3. **Context Token Optimization Strategy**: The control plane must enforce lazy-loading paradigms. Expansive reference documents must be implemented as Skills (\~/.claude/skills/\*/SKILL.md) utilizing disable-model-invocation: true, ensuring they consume zero tokens until human invocation9. Dynamic rules must heavily rely on the paths: YAML frontmatter to gate injection based strictly on active files26.  
> 4. **Mandatory State Sandboxing**: All exploratory tasks or background agents defined in the global \~/.claude/agents/ registry must contain the isolation: worktree frontmatter key. This deterministically isolates file edits and protects the novice user's main branch from "faulty implementation" failures20.  
> 5. **Persistent Artifact Archiving**: The global settings.json must enforce fileCheckpointingEnabled: true and define a lengthy cleanupPeriodDays to ensure novices can always execute /rewind to recover from agent hallucinations, failed deployments, or cascading epistemic errors2.

## **B. Anti-Requirements (What the Control Plane Should NOT Do)**

> 1. **Do Not Rely on Array Overrides**: The control plane must never attempt to override a globally permitted MCP server or tool by declaring an empty array in a local .claude/settings.local.json. Because arrays merge rather than overwrite, local configurations can only be additive; explicit restriction requires managed enterprise settings (managed-settings.json) or deterministic hooks1.  
> 2. **Do Not Enable Agent Teams for Routine Work**: Due to the severe token scaling issues documented with concurrent, multi-context agent communication, CLAUDE\_CODE\_EXPERIMENTAL\_AGENT\_TEAMS must remain disabled by default. Parallel execution should be handled exclusively by isolated subagents returning concise summaries, avoiding peer-to-peer agent chat18.  
> 3. **Do Not Deploy Ungated Channels**: The control plane must never define a global MCP channel server that accepts untrusted external input (e.g., a Slack/Discord listener) without a deterministic, cryptographic sender allowlist. Doing so introduces a direct prompt-injection vector into the novice's terminal session, permitting arbitrary command execution24.  
> 4. **Do Not Strip Core Instructions via Output Styles**: Global custom output styles (\~/.claude/output-styles/) must never omit the keep-coding-instructions: true key. Stripping Anthropic's baseline software engineering guardrails drastically increases the probability of agent failures, infinite execution loops, and faulty implementations12.

## **C. Unresolved Questions**

> 1. **State Conflicts in Checkpoint Restorations**: If an agent utilizes a PostToolUse hook to commit structural changes to an external database schema, and the user subsequently runs /rewind to restore the local file system checkpoint, how does the control plane reconcile the desynchronized external cloud state?  
> 2. **PowerShell PreToolUse Latency**: In a Windows environment, does spawning a new PowerShell subprocess to evaluate a PreToolUse hook for every single sub-command requested by the agent introduce unacceptable latency for interactive workflows?  
> 3. **Auto-Memory Plaintext Leakage**: Given that \~/.claude/projects/\<project\>/memory/ files are continuous and persistent, what mechanisms exist (beyond manual file deletion) to prevent the agent from inadvertently caching API keys it reads from temporary terminal outputs into plaintext disk storage?  
> 4. **Cross-Scope Regex Merging**: When a global user profile defines a permissions.deny rule using a broad glob pattern (e.g., Bash(git \*)), and a project-local profile defines a permissions.allow rule with a specific subset (e.g., Bash(git push)), what is the exact internal resolution sequence during array merging, and how does Windows path escaping affect the regex execution engine?

## **D. Sources**

* \[cite: 9\] Anthropic. *Match features to your goal*. code.claude.com/docs.  
* \[cite: 29\] Anthropic. *Subagents in the Claude Agent SDK*. code.claude.com/docs.  
* \[cite: 9\] Anthropic. *Compare similar features*. code.claude.com/docs.  
* \[cite: 4\] Anthropic. *Dynamic Workflows*. code.claude.com/docs.  
* \[cite: 2\] Anthropic. *Choose the right file*. code.claude.com/docs.  
* \[cite: 2\] Anthropic. *Application Data and Claude Directory*. code.claude.com/docs.  
* \[cite: 21\] Anthropic. *Hooks Guide*. code.claude.com/docs.  
* \[cite: 9\] Anthropic. *Features Overview: Hooks*. code.claude.com/docs.  
* \[cite: 23\] Anthropic. *Agent SDK Hooks*. code.claude.com/docs.  
* \[cite: 6\] Anthropic. *Hooks Reference*. code.claude.com/docs.  
* \[cite: 22\] Anthropic. *Hooks Configuration (RU)*. code.claude.com/docs.  
* \[cite: 18\] Anthropic. *Agent Teams*. code.claude.com/docs.  
* \[cite: 19\] Anthropic. *Agent Teams (ZH-CN)*. code.claude.com/docs.  
* \[cite: 24\] Anthropic. *Channels Reference*. code.claude.com/docs.  
* \[cite: 25\] Anthropic. *Push Events with Channels*. code.claude.com/docs.  
* \[cite: 30\] Anthropic. *Routines*. code.claude.com/docs.  
* \[cite: 31\] Anthropic. *Desktop Scheduled Tasks*. code.claude.com/docs.  
* \[cite: 14\] Anthropic. *Code Intelligence Plugins*. code.claude.com/docs.  
* \[cite: 15\] Anthropic. *Tools Reference (LSP)*. code.claude.com/docs.  
* \[cite: 16\] arXiv:2607.09510v1. *Empirical Study of CLI Coding-Agent Failure Trajectories*.  
* \[cite: 17\] arXiv:2609.30725v1. *Behavioral Cost Inefficiencies in Coding Agents*.  
* \[cite: 28\] arXiv:2606.17799v1. *Conflating the Model with the Harness in SWE-Bench*.  
* \[cite: 20\] arXiv:2605.29442v1. *Developer Friction and Inaccurate Self-Reporting*.  
* \[cite: 7\] Anthropic. *Environment Variables (Execution Policy)*. code.claude.com/docs.  
* \[cite: 8\] Kunpeng-AI. *Claude Code Windows Proxy Guide*.  
* \[cite: 1\] Anthropic. *Settings Configuration and Precedence*. code.claude.com/docs.  
* \[cite: 26\] Anthropic. *Custom Subagents in \~/.claude/agents/*. code.claude.com/docs.  
* \[cite: 27\] Anthropic. *Settings Reference*. code.claude.com/docs.  
* \[cite: 12\] Anthropic. *Output Styles*. code.claude.com/docs.  
* \[cite: 13\] Anthropic. *Output Styles (IT)*. code.claude.com/docs.  
* \[cite: 1\] Anthropic. *CLAUDE\_CONFIG\_DIR Settings*. code.claude.com/docs.  
* \[cite: 2\] Anthropic. *Claude Directory*. code.claude.com/docs.  
* \[cite: 3\] Anthropic. *Sessions and Storage Off \~/.claude*. code.claude.com/docs.  
* \[cite: 5\] Anthropic. *The /goal Command*. code.claude.com/docs.  
* \[cite: 9\] Anthropic. *Features Overview (Rules)*. code.claude.com/docs.  
* \[cite: 26\] Anthropic. *Subagent Frontmatter*. code.claude.com/docs.  
* \[cite: 10\] Anthropic. *Context Window and Compaction*. code.claude.com/docs.  
* \[cite: 32\] Anthropic. *Choose where skills load*. code.claude.com/docs.  
* \[cite: 9\] Anthropic. *Features Overview (Skills)*. code.claude.com/docs.  
* \[cite: 11\] Anthropic. *Rule Frontmatter Reference*. code.claude.com/docs.  
* \[cite: 6\] Anthropic. *Hook Matchers and Locations*. code.claude.com/docs.  
* \[cite: 6\] Anthropic. *Managed Settings JSON*. code.claude.com/docs.  
* \[cite: 33\] Anthropic. *Plugins Overview*. code.claude.com/docs.

#### **Works cited**

> 1. Settings files and precedence \- Claude Code Docs, [https\://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
> 2. Explore the .claude directory \- Claude Code Docs, [https\://code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory)  
> 3. Manage sessions \- Claude Code Docs, [https\://code.claude.com/docs/en/sessions](https://code.claude.com/docs/en/sessions)  
> 4. Orchestrate subagents at scale with dynamic workflows, [https\://code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows)  
> 5. Keep Claude working toward a goal \- Claude Code Docs, [https\://code.claude.com/docs/en/goal](https://code.claude.com/docs/en/goal)  
> 6. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 7. Environment variables \- Claude Code Docs, [https\://code.claude.com/docs/en/env-vars](https://code.claude.com/docs/en/env-vars)  
> 8. Claude Code On Windows PowerShell: Install, PATH, [https\://kunpeng-ai.com/en/blog/claude-code-windows-proxy-guide/](https://kunpeng-ai.com/en/blog/claude-code-windows-proxy-guide/)  
> 9. Extend Claude Code \- Claude Code Docs, [https\://code.claude.com/docs/en/features-overview](https://code.claude.com/docs/en/features-overview)  
> 10. Explore the context window \- Claude Code Docs, [https\://code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window)  
> 11. How Claude remembers your project \- Claude Code Docs, [https\://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)  
> 12. Output styles \- Claude Code Docs, [https\://code.claude.com/docs/en/output-styles](https://code.claude.com/docs/en/output-styles)  
> 13. Output styles \- Claude Code Docs, [https\://code.claude.com/docs/it/output-styles](https://code.claude.com/docs/it/output-styles)  
> 14. Code intelligence plugins \- Claude Code Docs, [https\://code.claude.com/docs/en/plugins/code-intelligence](https://code.claude.com/docs/en/plugins/code-intelligence)  
> 15. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 16. Failure as a Process: An Anatomy of CLI Coding Agent Trajectories, [https\://arxiv.org/html/2607.09510v1](https://arxiv.org/html/2607.09510v1)  
> 17. Analyzing and Mitigating Cost-Inefficient Behaviors in Coding Agents, [https\://arxiv.org/html/2609.30725v1](https://arxiv.org/html/2609.30725v1)  
> 18. Orchestrate teams of Claude Code sessions, [https\://code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)  
> 19. 协调Claude Code 会话团队, [https\://code.claude.com/docs/zh-CN/agent-teams](https://code.claude.com/docs/zh-CN/agent-teams)  
> 20. How Coding Agents Fail Their Users: A Large-Scale Analysis ... \- arXiv, [https\://arxiv.org/html/2605.29442v1](https://arxiv.org/html/2605.29442v1)  
> 21. Automate actions with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
> 22. Справочник по hooks \- Claude Code Docs, [https\://code.claude.com/docs/ru/hooks](https://code.claude.com/docs/ru/hooks)  
> 23. Intercept and control agent behavior with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/hooks](https://code.claude.com/docs/en/agent-sdk/hooks)  
> 24. Channels reference \- Claude Code Docs, [https\://code.claude.com/docs/en/channels-reference](https://code.claude.com/docs/en/channels-reference)  
> 25. Push events into a running session with channels \- Claude Code Docs, [https\://code.claude.com/docs/en/channels](https://code.claude.com/docs/en/channels)  
> 26. Create custom subagents \- Claude Code Docs, [https\://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
> 27. [https\://code.claude.com/docs/en/settings-reference](https://code.claude.com/docs/en/settings-reference)  
> 28. Position: Coding Benchmarks Are Misaligned with Agentic Software, [https\://arxiv.org/html/2606.17799v1](https://arxiv.org/html/2606.17799v1)