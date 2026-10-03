# **Engineering Research Protocol: Global Control Plane Architecture for Claude Code**

The deployment of a production-quality global control plane for Claude Code requires a rigorous synthesis of autonomous agent constraints, state management primitives, and deterministic execution boundaries. Designed to guide software engineering novices from conceptualization through implementation, testing, and continuous maintenance, this control plane must mediate between human intent and the inherent mechanical limitations of large language models (LLMs). The operational environment resides primarily within the global configuration directory, explicitly C:\\Users\\USERNAME\\.claude\\ on Windows systems or \~/.claude/ on Unix-like environments. By establishing foundational configurations through global settings, system-level hooks, and durable memory architectures, the control plane must prevent catastrophic context degradation, mitigate agentic drift, and enforce absolute safety invariants without demanding sophisticated engineering supervision from the human user.  
The ensuing analysis leverages official Anthropic documentation, empirical performance benchmarks on frameworks such as SWE-bench, and long-horizon agent research valid as of October 1, 2026\. The objective is to construct an architecture that differentiates clearly between deterministic enforcement (hardware/software boundaries) and prompt-based orchestration (LLM behavioral guidance), explicitly addressing the friction points encountered in autonomous software engineering.

## **Deconstructing Legacy Paradigms and Hypotheses**

Previous architectural paradigms for autonomous coding agents, notably those found in repository structures such as "JackSmack1971/supreme," prescribed rigid, deterministic methodologies designed for human engineers. Empirical research and the mechanical realities of the Claude Code agentic harness invalidate several of these early assumptions, necessitating a transition toward context-aware, LLM-native constraints.  
The imposition of fixed complexity thresholds, such as strict line-count limits for files, represents a fundamental misunderstanding of LLM context processing. Early frameworks mandated these limits to prevent context exhaustion. However, current evidence demonstrates that context exhaustion is a function of token relevance, attention rot, and prompt complexity, rather than arbitrary line limits1. While adherence to CLAUDE.md instructions demonstrably degrades when the file exceeds roughly 200 lines, this is a prompt engineering heuristic rather than a deterministic physical boundary2. Enforcing rigid line limits globally via a control plane introduces unnecessary friction and frequently breaks legitimate code structures. Instead, dynamic context compaction managed natively by Claude Code, paired with explicit path-scoped rules (.claude/rules/\*.md), is the CURRENTLY SUPPORTED method for managing token budgets and context relevance2.  
Similarly, mandating comprehensive Architecture Decision Records (ADRs) universally pollutes the agent's context window. Long-form documentation requires the model to process significant historical rationale, displacing tokens needed for immediate working memory and active code synthesis4. Evidence from long-horizon agent execution suggests that replacing verbose ADRs with highly compressed, stateful JSON files improves adherence and prevents the agent from forgetting current objectives5. An agent does not need to know why a database was chosen; it only needs to know which database to query.  
The hypothesis that all tasks should be routed through a complex hierarchy of specialized multi-agents is also empirically flawed. While agentic delegation is a powerful pattern, subagents incur substantial operational overhead. Each subagent begins with a fresh context window, losing the prompt caching benefits accumulated in the primary session, which increases both latency and token costs7. Universal multi-agent routing fractures context unnecessarily for trivial tasks. Subagents are CURRENTLY SUPPORTED but should be reserved exclusively for highly parallelizable analysis, isolated tool restrictions, or tasks explicitly requiring a divergent system prompt, such as a heavily constrained code-reviewer agent restricted to Read and Grep tools7.  
Applying conventional Test-Driven Development (TDD) dogma universally to autonomous agents has proven counterproductive. Controlled experiments on SWE-bench Verified demonstrate that baseline TDD prompting actually increases regression rates from 6.08% to 9.94% and exacerbates pass-to-pass failures9. The underlying cause is the "TDD Prompting Paradox": procedural TDD instructions consume vital context tokens, pushing out repository-specific context, while simultaneous ambition leads the agent to attempt unlocalized, sweeping changes9. TDD is only effective for AI agents when paired with static dependency mapping, known experimentally as Test-Driven Agentic Development (TDAD), which localizes the tests before generation begins9.  
Finally, relying on undocumented Claude Code configuration keys is strictly UNSUPPORTED. The Claude Code settings JSON schema statically validates inputs upon load. Unrecognized keys are either silently ignored or trigger a terminal "Settings Warning" that drops the invalid entries10. The control plane must rely strictly on documented primitives within \~/.claude/settings.json, utilizing PreToolUse or UserPromptSubmit command hooks to enforce behaviors that lack native configuration keys11.

## **Durable Memory Architecture and Long-Horizon Execution**

Autonomous agents suffer from horizon degradation. As context windows fill during extended execution, Claude Code triggers automatic compaction. This mechanism silently clears older tool outputs first, then summarizes the conversation, frequently resulting in the permanent loss of early instructions and transient state3. This mechanical reality necessitates a robust, out-of-context memory architecture that survives compaction boundaries.  
The architecture must separate state (what is true now) from rules (how to behave) and rationale (why we behave this way). Recent empirical studies, including Anthropic's StructAgent and Traverse models, emphasize a "unified causal structure" where planning, acting, and verification interact with a shared, externalized representation of task progress12.

### **Comparative Analysis of Memory Mechanisms**

To construct a durable state machine for the novice-oriented control plane, various memory mechanisms must be evaluated against context costs, retention fidelity, and programmatic immutability.

| Memory Mechanism | Evaluation for Long-Horizon Autonomy | Classification |
| :---- | :---- | :---- |
| **CLAUDE.md** | High utility for static, universal project rules (e.g., coding standards). Ineffective for dynamic state tracking because the file loads entirely at session start and survives compaction natively. Overloading it causes severe context pollution. | CURRENTLY SUPPORTED2 |
| **Auto memory (MEMORY.md)** | Moderate utility. Automatically captures behavioral corrections but is capped at 25KB or 200 lines. The contents are highly variable, LLM-generated, and entirely unsuitable for maintaining strict engineering invariants. | CURRENTLY SUPPORTED2 |
| **Explicit structured memory** | Exceptional utility. JSON-based state files (e.g., feature\_list.json) read dynamically. Models are mathematically resistant to corrupting strict JSON schemas when properly prompted, making this the ideal format for tracking long-horizon tasks. | EVIDENCE-BACKED5 |
| **Project documentation** | Poor utility for active working memory. Consumes excessive tokens unless the agent is specifically constrained to query it via Grep or Glob tools. | CURRENTLY SUPPORTED1 |
| **ADRs / Decision Logs** | Low utility for the active agentic loop. Historical rationale crowds out operational instructions and should be archived out of immediate context. | UNSUPPORTED FOR AGENTS6 |
| **Task ledgers** | High utility if maintained in a flat, boolean format (e.g., {"authentication": {"passes": false}}). Provides the agent with an unambiguous target. | EVIDENCE-BACKED5 |
| **Implementation status** | Vital utility. An explicit, human-readable claude-progress.txt updated via terminal hooks or session-end commands bridges the amnesia between context resets. | EVIDENCE-BACKED5 |
| **Generated repository maps** | Strong utility for fault localization when delivered via a standalone tool or script, significantly reducing the token cost of blind environment exploration. | EXPERIMENTAL9 |
| **Session summaries** | Moderate utility. These are generated automatically during compaction but often lose granular, critical details (like specific port numbers or temporary file paths) during the LLM summarization phase. | CURRENTLY SUPPORTED3 |
| **Git history** | Critical utility. Acts as an immutable ledger. Agents programmed to parse git log \--oneline \-20 recover state reliably and can perform rollbacks upon failure. | CURRENTLY SUPPORTED5 |
| **Subagent handoff artifacts** | High utility for task compartmentalization. Only the final output returns to the primary context, preserving tokens while retaining the synthesized knowledge of a long exploration. | CURRENTLY SUPPORTED7 |
| **Compaction** | Necessary but destructive. Silently erases constraints. Must never be relied upon for critical state retention. | CURRENTLY SUPPORTED3 |
| **Just-in-time retrieval** | Essential for scaling. Loading context via lightweight identifiers dynamically out-performs upfront loading and prevents attention rot. | EVIDENCE-BACKED1 |

### **The Minimum Durable Records Specification**

Based on long-horizon empirical testing, an agent recovering from a context reset, a subagent handoff, or a failed session requires exactly six parameters to resume autonomy successfully without human intervention5. These records must be decoupled from the primary CLAUDE.md file to prevent token bloat and ensure isolation of concerns.  
The framework requires the initialization of specific files that answer the fundamental operational questions of the agent. First, the agent must know **WHY** it is building the software. This is represented by a read-only product\_intent.txt file. It contains the unalterable core objective, preventing the agent from hallucinating new project scopes or pivoting the architecture during extended autonomous loops. Second, the agent must know **WHAT is currently true**. This is represented by claude-progress.txt, a highly compressed textual summary updated exclusively at the end of a successful feature implementation, serving as the bridge across context windows.  
Third, the agent requires a record of **WHAT decisions were made**. This is best represented by standing\_decisions.json, a compressed key-value store of finalized architectural choices (e.g., "database": "sqlite", "styling": "tailwind"). This replaces the need for verbose ADRs. Fourth, the agent must track **WHAT remains to do**. This is represented by feature\_list.json, a structured ledger of granular implementation steps, initialized to "passes": false. The agent iterates through this ledger sequentially, preventing the common failure mode of one-shotting the entire application5.  
Fifth, the system must define **WHAT evidence says work is complete**. This evidence criteria must be embedded directly within feature\_list.json as verification steps, relying heavily on visual inspection (e.g., Puppeteer MCP for UI changes) or localized unit test outputs. Finally, the agent must determine **WHAT changed since the documentation was written**. The local Git repository serves this function. The harness must force the agent to query the git log upon session initialization to identify divergent states and uncommitted modifications5.

## **Mitigating Target Failure Modes via Anti-Drift Invariants**

Agents left in multi-hour autonomous loops tend to drift from their original directives. The research identifies several critical failure modes: forgetting earlier decisions, contradicting prior architectural choices, losing requirements after compaction, re-discovering the same information repeatedly, claiming files are missing because session context changed, relying on stale plans or TODOs, allowing implementation to diverge from specification, and failing handoffs between sessions or subagents.  
To combat these, the control plane must enforce explicit anti-drift invariants using a combination of deterministic Claude Code hooks and structured workflow patterns11.  
The phenomenon of **claiming files are missing** typically occurs when the agent changes the current working directory mid-session or when context compaction erases the file path from working memory. This is mitigated by establishing a unified causal structure, ensuring the agent always executes commands relative to a fixed repository root defined in the global settings, and utilizing CwdChanged hooks to reset context appropriately11.  
**Stale plans, stale TODOs, and stale documentation** manifest when the agent relies on its internal memory rather than reading the disk. This failure mode requires a deterministic invariant: State File Integrity. The agent may not delete items from feature\_list.json, nor alter the product\_intent.txt. This is enforced via a deterministic PreToolUse hook targeting the Write and Edit tools. The hook script evaluates the target file path; if the agent attempts to modify an immutable file, the hook returns {"hookSpecificOutput": {"permissionDecision": "deny", "permissionDecisionReason": "State file immutable."}}, physically blocking the hallucination11.  
The failure mode of **implementation diverging from specification** and **contradicting architectural choices** stems from the agent declaring victory prematurely. Agents often edit code and rely solely on internal confidence or successful compilation, mistakenly marking features complete even when they fail user-facing requirements5. This requires the Verified Progress Commits invariant. The agent cannot mark a feature as "passes": true in the JSON ledger without a corresponding testing step. This is enforced via a prompt-based UserPromptSubmit or PostToolUse hook that utilizes a lightweight model (e.g., Claude Haiku) to evaluate the execution transcript. If the agent modifies the state file without invoking a valid test command via the Bash or PowerShell tool, the hook interrupts the loop and demands evidence11.  
Finally, **forgetting decisions** and **re-discovering information** are solved by the Clean State Continuation invariant. The agent cannot begin work on a broken repository. Inspired by the "Initializer Paradigm," the first session generates an init.sh health-check script. Subsequent sessions use a SessionStart command hook to execute this script automatically. If the script fails, the agent is deterministically redirected to fix the baseline before attempting new features, preventing the compounding of errors across sessions5.

## **The Optimal Debugging Workflow: Fault Localization**

The strongest debugging workflow for autonomous coding agents relies on Test-Driven Agentic Development (TDAD) augmented with unified state tracking, directly refuting the assumption that generic TDD prompting is effective. Unstructured debugging prompts—telling the model to simply "find the bug and fix it"—cause the agent to thrash. The agent frequently hallucinates connections across the codebase, attempts overly ambitious refactoring, and introduces severe regressions9.  
Effective fault localization requires pre-change impact analysis. The control plane must implement a static dependency graph mapping source files to test files (test\_map.txt). When an error is encountered, the agent is constrained by a SKILL.md directive to query this dependency graph rather than performing a blind grep of the entire repository. This localized approach ensures the agent knows exactly which tests to run before and after code modification9.  
Empirical evaluations on the SWE-bench dataset demonstrate that providing the agent with this static structural knowledge reduces Pass-to-Pass failures by over 70% and drastically lowers the regression rate9. Furthermore, visual and interactive verification via the Model Context Protocol (MCP), such as connecting a Puppeteer automated browser instance, drastically reduces the hallucination of successful implementations5. The integration of TDAD principles within a dedicated /debug skill represents the most robust, evidence-backed workflow for resolving implementation failures autonomously.

## **Material Findings and Component Analysis**

The following exhaustive assessments detail the specific architectural components required for the global control plane, evaluated against Anthropic documentation and empirical literature. Each finding separates deterministic enforcement from prompt-based orchestration and explicitly considers environmental portability.

### **1\. The Initializer State Machine and Context Resets**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Context resets are mechanically inevitable in long-horizon tasks; bridging them requires an "Initializer Agent" sequence to scaffold claude-progress.txt and feature\_list.json before any feature generation begins. |
| **Evidence/Source** | Anthropic Engineering: Effective Harnesses for Long-Running Agents5 |
| **Evidence Strength** | Strong |
| **Claude Code Mechanism Implicated** | Session lifecycle, Context Window, Skills |
| **Global \~/.claude Candidate?** | Yes. The initializer sequence can be enforced via a global skill (\~/.claude/skills/init.md). |
| **Enforcement Type** | Deterministic (SessionStart hook) or Prompt-based (Skill invocation) |
| **Cost/Context Implications** | Reduces total token cost significantly by preventing regressions and limiting redundant environment discovery upon every session restart. |
| **Security Implications** | Low risk. Standardizes the project structure safely. |
| **Open Question Remaining** | How to reliably determine programmatically when the initializer phase is perfectly complete before transitioning to the coding phase without requiring human approval. |

The Initializer Paradigm is essential because agents cannot effectively plan and execute simultaneously over long horizons without drifting. By splitting responsibilities, the control plane ensures the agent does not attempt to one-shot the architecture5. The control plane should detect a new project—perhaps by the absence of a .claude/settings.json file—and force an initializer prompt. This sequence builds the JSON feature state and the init.sh testing script, establishing the structural invariants required for the remainder of the project lifecycle.

### **2\. Context Window Compaction Degradation**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Context compaction silently erases early conversation constraints and standing decisions. It clears older tool outputs first, preserving the foundational CLAUDE.md but destroying any conversational invariants established mid-session. |
| **Evidence/Source** | Claude Code Context Documentation3 |
| **Evidence Strength** | Strong |
| **Claude Code Mechanism Implicated** | Compaction Engine |
| **Global \~/.claude Candidate?** | No. State preservation must be managed per-project on the local disk. |
| **Enforcement Type** | Prompt-based (Offloading constraints to permanent files) |
| **Cost/Context Implications** | Retaining information in context indefinitely causes massive prompt caching costs; moving it to files allows selective, just-in-time loading. |
| **Security Implications** | Security invariants must never rely on conversational context, as compaction will eventually and silently erase them. |
| **Open Question Remaining** | What is the exact internal token threshold at which the Claude Code heuristic triggers compaction, and can it be bypassed for specific memory blocks? |

The control plane must operate under the architectural assumption that the agent suffers from amnesia regarding anything not explicitly written to disk. Any directive given by the human in the terminal interface is ephemeral. Novice users must be routed to save instructions via the /memory command to ensure survival across compaction cycles, while the control plane itself must continuously force the agent to re-read the standing\_decisions.json file14.

### **3\. Fault Localization via Static Mapping (TDAD)**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Unlocalized TDD prompting increases regression rates to 9.94%. Agents require a static test\_map.txt (dependency map) to know which tests to verify prior to committing changes, preventing ambitious collateral damage. |
| **Evidence/Source** | Test-Driven Agentic Development Empirical Study9 |
| **Evidence Strength** | Strong (SWE-bench verified) |
| **Claude Code Mechanism Implicated** | Skills, Prompting |
| **Global \~/.claude Candidate?** | Conditional. The execution skill is global (\~/.claude/skills/), but the test\_map.txt itself is strictly project-local. |
| **Enforcement Type** | Prompt-based (via SKILL.md) |
| **Cost/Context Implications** | Highly efficient. Parsing the test\_map.txt consumes minimal tokens compared to full repository grepping or blind exploration. |
| **Security Implications** | None. |
| **Open Question Remaining** | Can the agent generate the static graph map autonomously with high fidelity, or does it require an external deterministic script (e.g., Python NetworkX) packaged with the control plane? |

Implementing TDAD requires the control plane to ship with an external mechanism capable of analyzing imports and generating the dependency map. The agent is provided a global skill that instructs it to read this map during any debugging loop, entirely replacing generic "fix the bug" prompting. This structured workflow controls how planning and acting intersect with state, matching empirical findings from StructAgent13.

### **4\. Subagent Context Isolation Utility**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Delegating specialized tasks (e.g., code review, broad documentation parsing) to custom subagents prevents the primary conversation's context window from being polluted with raw, verbose tool outputs. |
| **Evidence/Source** | Claude Code Subagents Documentation7 |
| **Evidence Strength** | Strong |
| **Claude Code Mechanism Implicated** | .claude/agents/\*.md, Agent Tool |
| **Global \~/.claude Candidate?** | Yes. General-purpose subagents (e.g., security-scanner) should live in \~/.claude/agents/. |
| **Enforcement Type** | Prompt-based |
| **Cost/Context Implications** | Increases raw API calls and incurs prompt caching misses initially, but dramatically preserves the primary session's token budget and coherence over long horizons. |
| **Security Implications** | Subagents can be strictly constrained via the tools frontmatter field (e.g., \["Read", "Grep"\]), acting as an effective security sandbox for untrusted code. |
| **Open Question Remaining** | How to optimally structure the parent-to-subagent payload to maximize caching efficiency while minimizing redundant token transmission. |

Subagents are defined in markdown files utilizing frontmatter. To protect novice users from runaway execution (noting that subagent chains are capped at five levels deep16), subagents should be explicitly defined globally with restricted toolsets8. A code-reviewer agent possessing only Read and Grep tools ensures that the agent cannot accidentally overwrite files or execute malicious scripts while investigating an issue7.

### **5\. Settings Precedence and Immutability**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Claude Code configuration follows strict precedence: Managed \> Local (.claude/settings.local.json) \> Project (.claude/settings.json) \> User (\~/.claude/settings.json). |
| **Evidence/Source** | Settings Precedence Documentation10 |
| **Evidence Strength** | Strong (Definitive architecture) |
| **Claude Code Mechanism Implicated** | settings.json Configuration |
| **Global \~/.claude Candidate?** | Yes. The control plane natively relies on the User tier to effect change across all projects. |
| **Enforcement Type** | Deterministic |
| **Cost/Context Implications** | Zero cost. |
| **Security Implications** | Project-level configurations downloaded from untrusted repositories can override User-level safety settings unless strictly managed by MDM payloads. |
| **Open Question Remaining** | If a novice user clones a repository containing malicious project-level hooks, how can the global control plane intercept them prior to folder trust approval? |

The control plane must reside in \~/.claude/settings.json to affect all repositories globally. However, because project-level settings override user settings, critical safety invariants for novices cannot be exclusively guaranteed by the global configuration10. The control plane must either utilize managed settings (which supersede everything) or heavily educate the user on the Folder Trust mechanics, ensuring they do not blindy approve untrusted .claude directories18.

### **6\. Hook-Based Deterministic Enforcement**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | The PreToolUse hook can deterministically evaluate shell commands and file paths, successfully blocking agent execution without relying on the LLM's adherence to text prompts. |
| **Evidence/Source** | Claude Code Hooks Documentation2 |
| **Evidence Strength** | Strong |
| **Claude Code Mechanism Implicated** | Hooks (PreToolUse, PostToolUse) |
| **Global \~/.claude Candidate?** | Yes. Global hooks defined in \~/.claude/settings.json apply to all projects. |
| **Enforcement Type** | Deterministic |
| **Cost/Context Implications** | Executing a local shell script incurs zero API cost and bypasses the context window entirely. |
| **Security Implications** | Essential for preventing destructive operations (e.g., rm \-rf /\*, rewriting git history) by novice users who cannot foresee the consequences of an autonomous agent's actions. |
| **Open Question Remaining** | The performance overhead of invoking external Python or Node scripts synchronously for every single tool use during an intense agentic loop. |

Model-based prompt enforcement is inherently fallible. If an instruction in CLAUDE.md states "Never delete a file," the model may still delete a file if its internal probabilistic reasoning convinces it that the action is a necessary "refactor"2. True safety enforcement requires configuring the hooks array in settings.json to intercept PreToolUse events. The hook receives a JSON payload and can return a denial string, halting the model deterministically before any damage occurs11.

### **7\. Windows Execution Environment Constraints**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Claude Code dynamically relies on PowerShell natively if Git for Windows (Bash) is absent. The \$env:PATH logic and TLS 1.2 initialization requirements are common failure points for novice users. |
| **Evidence/Source** | Windows Terminal Guide & Installation Docs19 |
| **Evidence Strength** | Strong |
| **Claude Code Mechanism Implicated** | Shell Tools (Bash, PowerShell) |
| **Global \~/.claude Candidate?** | Yes. Environment variables dictate shell routing globally in the user configuration. |
| **Enforcement Type** | Deterministic |
| **Cost/Context Implications** | PowerShell outputs can be excessively verbose and stream differently than Bash, requiring aggressive BASH\_MAX\_OUTPUT\_LENGTH tuning to prevent context flooding. |
| **Security Implications** | Windows PowerShell execution policies may silently block deterministic hooks or tools if not globally bypassed by the control plane. |
| **Open Question Remaining** | How accurately does the LLM adjust its syntax generation when dynamically switched from Bash to PowerShell mid-session? |

The control plane must account for operating system variance to protect the novice user. Hardcoding bash syntax in global hooks or initializers will fail catastrophically on naive Windows installations. Environment variables like CLAUDE\_CODE\_GIT\_BASH\_PATH must be explicitly managed, or the control plane must use universally supported, cross-platform runtimes (such as native Python) for all hook execution21.

### **8\. Bounded Shell Output Limitations**

| Parameter | Evaluation |
| :---- | :---- |
| **Finding** | Unbounded logging (e.g., running verbose test suites or infinite loops) rapidly degrades the context window. The bashOutputMaxChars setting or BASH\_MAX\_OUTPUT\_LENGTH environment variable must be strictly tuned. |
| **Evidence/Source** | Environment Variables Reference23 |
| **Evidence Strength** | Strong |
| **Claude Code Mechanism Implicated** | Shell Tools |
| **Global \~/.claude Candidate?** | Yes. |
| **Enforcement Type** | Deterministic |
| **Cost/Context Implications** | Aggressively caps context bloat from failed commands, ensuring the agent retains its prompt instructions. |
| **Security Implications** | Mitigates buffer-based denial of service within the local terminal execution environment. |
| **Open Question Remaining** | Does the arbitrary truncation of stack traces remove the specific error lines required for the agent to achieve accurate fault localization? |

Novices frequently ask the agent to "run the server," which can emit endless logs, filling the context window with useless network telemetry. The control plane must globally set reasonable bounds (e.g., via BASH\_DEFAULT\_TIMEOUT\_MS and max output limits) to prevent the agent from hanging indefinitely or consuming massive context quotas on repetitive output23.

## **Synthesis and Control Plane Architecture**

The culmination of this research dictates a specific structural deployment for the C:\\Users\\USERNAME\\.claude\\ control plane, designed to navigate the friction between human intent and LLM mechanics.

### **A. Design Requirements Derived from Evidence**

> 1. **Deployment Architecture:** The control plane must install its configuration payload globally into \~/.claude/settings.json, with global subagents deployed to \~/.claude/agents/ and skills to \~/.claude/skills/. This ensures the novice user benefits from the guardrails regardless of which project directory they initialize.  
> 2. **The Initializer State Machine:** The system must supply a global skill (e.g., /init-project) that bootstraps the Two-Agent Paradigm. This command must explicitly generate product\_intent.txt, feature\_list.json (initialized with boolean flags), and a foundational testing script (init.sh).  
> 3. **Deterministic Safety Boundaries:** The global settings.json must configure a PreToolUse hook utilizing a cross-platform script to evaluate Write and Edit commands. This script deterministically blocks modifications to feature\_list.json (preventing requirement deletion) and product\_intent.txt.  
> 4. **Mandatory Baseline Verification:** The control plane must utilize a SessionStart hook to invoke init.sh automatically. The agent is thereby forced to evaluate the baseline repository health before commencing new feature work, preventing the compounding of errors.  
> 5. **Context Defense via TDAD:** Universal TDD prompting must be rejected. Instead, the control plane must include a script to generate a static dependency map (test\_map.txt) and a debugging skill (/debug) that directs the agent to query this map for fault localization prior to generating patches.  
> 6. **Cross-Platform Execution Wrapping:** All global hooks must explicitly query the execution environment (detecting \$env:PATH vs \$PATH) and ensure compatibility with PowerShell on Windows systems lacking Git Bash, overriding BASH\_DEFAULT\_TIMEOUT\_MS to prevent zombie processes.  
> 7. **Subagent Specialization, Not Routing:** The control plane must provide pre-configured, context-isolated subagents strictly for high-pollution tasks (e.g., a doc-reader equipped only with Read and Grep), completely abandoning mandatory hierarchical task-routing for basic code edits.

### **B. Anti-Requirements**

The eventual control plane should explicitly **NOT** do the following, as these actions directly contradict empirical evidence and Claude Code mechanics:

> 1. **Do not use CLAUDE.md for dynamic state tracking.** Passing evolving TODO lists or status ledgers through CLAUDE.md guarantees prompt cache misses on every turn and eventual loss during context compaction. CLAUDE.md must remain static.  
> 2. **Do not define logic via undocumented settings keys.** The Claude Code validation schema will silently drop unsupported parameters. All programmatic logic must map strictly to documented settings.json features or hook events.  
> 3. **Do not rely on LLM prompts for destructive action prevention.** System prompts instructing the model not to delete files will eventually fail due to probabilistic generation and context rot. Absolute invariants must use PreToolUse hooks.  
> 4. **Do not mandate comprehensive Architecture Decision Records (ADRs).** Deep historical context severely degrades the agent's ability to focus on immediate tasks. Decisions must be compacted into flat key-value pairs (standing\_decisions.json).  
> 5. **Do not mandate multi-agent routing for standard operations.** Initializing a subagent costs time, API calls, and context caching efficiency. Most standard engineering operations should occur in the primary session.  
> 6. **Do not rely on Context Compaction for memory.** Compaction is a lossy survival mechanism, not a memory storage system. Critical data must be flushed to disk prior to the compaction trigger.

### **C. Unresolved Questions**

> 1. **Cross-Boundary MDM Overrides:** If a novice user operates on a corporate machine managed by an MDM payload, the server-managed settings will silently supersede the global \~/.claude/settings.json control plane. It remains unresolved how a local, open-source control plane can definitively audit server-managed state without complex network interception.  
> 2. **Subagent Prompt Caching Optimization:** While subagents provide crucial context isolation, the exact mechanics for passing the necessary preamble from the primary session to the subagent without triggering a complete cache miss on the Anthropic API backend remain under-documented.  
> 3. **Automated TDAD Graph Generation:** Relying on the agent to construct test\_map.txt introduces the risk of hallucinated dependencies. Integrating a universal, language-agnostic Abstract Syntax Tree (AST) parser into a lightweight control plane without bloating the dependency footprint remains a significant software engineering challenge.  
> 4. **Evolution of Context Resets:** As foundation models expand their context windows into the millions of tokens with near-perfect recall, the necessity of the "Initializer Paradigm" and hard context resets may diminish. Research from Anthropic indicates that on advanced models, rigid resets occasionally become "dead weight"24, suggesting the control plane must remain modular enough to deprecate these features as underlying models improve.

### **D. Sources**

* \[cite: 2\] Current official Claude Code documentation at code.claude.com/docs/en/memory. (Accessed October 1, 2026).  
* \[cite: 3\] Official Claude Code documentation: How Claude Code Works. code.claude.com/docs/en/how-claude-code-works.  
* \[cite: 15\] Official Claude Code documentation: Directory Structure. code.claude.com/docs/en/claude-directory.  
* \[cite: 14\] Official Claude Code documentation: Glossary. code.claude.com/docs/en/glossary.  
* \[cite: 11\] Official Claude Code documentation: Hooks Reference. code.claude.com/docs/en/hooks.  
* \[cite: 12\] Traverse: Autonomous Context Management in Long-Horizon Search. arXiv:2609.37082v1. (September 2026).  
* \[cite: 5\] Anthropic Engineering Blog: Effective Harnesses for Long-Running Agents. www\.anthropic.com/engineering/effective-harnesses-for-long-running-agents.  
* \[cite: 6\] Hierarchical Architectures for Long-Horizon LLM Agents. arXiv:2609.19519v1. (September 2026).  
* \[cite: 24\] Anthropic Engineering Blog: Scaling Managed Agents. www\.anthropic.com/engineering/managed-agents. (April 2026).  
* \[cite: 1\] Anthropic Engineering Blog: Effective Context Engineering for AI Agents. www\.anthropic.com/engineering/effective-context-engineering-for-ai-agents. (September 2025).  
* \[cite: 4\] Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research. arXiv:2609.15983v1. (September 2026).  
* \[cite: 13\] StructAgent: Harness Long-horizon Digital Agents with Unified Causal Structure. arXiv:2607.11388v1. (July 2026).  
* \[cite: 10, 17\] Official Claude Code documentation: Settings and Precedence. code.claude.com/docs/en/settings.  
* \[cite: 18\] Official Claude Code documentation: Permissions. code.claude.com/docs/en/permissions.  
* \[cite: 7, 8\] Official Claude Code documentation: Subagents. code.claude.com/docs/en/agent-sdk/subagents.  
* \[cite: 16\] Official Claude Code Changelog (2026-W24). code.claude.com/docs/en/whats-new/2026-w24.  
* \[cite: 19, 20, 21\] Official Claude Code documentation: Setup and Windows Terminal Guide. code.claude.com/docs/en/setup.  
* \[cite: 23\] Official Claude Code documentation: Environment Variables. code.claude.com/docs/en/env-vars.  
* \[cite: 9\] Test-Driven Agentic Development (TDAD). arXiv:2603.17973. (March 2026).

#### **Works cited**

> 1. Effective context engineering for AI agents \- Anthropic, [https\://www\.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
> 2. How Claude remembers your project \- Claude Code Docs, [https\://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)  
> 3. How Claude Code works \- Claude Code Docs, [https\://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)  
> 4. Stellar Colosseum: A Many-Agent Harness for Long-Horizon ... \- arXiv, [https\://arxiv.org/html/2609.15983v1](https://arxiv.org/html/2609.15983v1)  
> 5. Effective harnesses for long-running agents \- Anthropic, [https\://www\.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  
> 6. An Architecture for Long-Horizon Agents:Levels, Ticks and ... \- arXiv, [https\://arxiv.org/html/2609.19519v1](https://arxiv.org/html/2609.19519v1)  
> 7. Subagents in the SDK \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)  
> 8. Create custom subagents \- Claude Code Docs, [https\://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
> 9. TDAD: Test-Driven Agentic Development \- arXiv, [https\://arxiv.org/pdf/2603.17973](https://arxiv.org/pdf/2603.17973)  
> 10. Settings files and precedence \- Claude Code Docs, [https\://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
> 11. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 12. Learning When to Remember, Reset, and Redirect for Long-Horizon, [https\://arxiv.org/html/2609.37082v1](https://arxiv.org/html/2609.37082v1)  
> 13. Harness Long-horizon Digital Agents with Unified Causal Structure, [https\://arxiv.org/html/2607.11388v1](https://arxiv.org/html/2607.11388v1)  
> 14. Glossary \- Claude Code Docs, [https\://code.claude.com/docs/en/glossary](https://code.claude.com/docs/en/glossary)  
> 15. Explore the .claude directory \- Claude Code Docs, [https\://code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory)  
> 16. Week 24 · June 8–12, 2026 \- Claude Code Docs, [https\://code.claude.com/docs/en/whats-new/2026-w24](https://code.claude.com/docs/en/whats-new/2026-w24)  
> 17. Debug your configuration \- Claude Code Docs, [https\://code.claude.com/docs/en/debug-your-config](https://code.claude.com/docs/en/debug-your-config)  
> 18. Configure permissions \- Claude Code Docs, [https\://code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)  
> 19. Terminal guide for new users \- Claude Code Docs, [https\://code.claude.com/docs/en/terminal-guide](https://code.claude.com/docs/en/terminal-guide)  
> 20. Overview \- Claude Code Docs, [https\://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)  
> 21. Advanced setup \- Claude Code Docs, [https\://code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup)  
> 22. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 23. Environment variables \- Claude Code Docs, [https\://code.claude.com/docs/en/env-vars](https://code.claude.com/docs/en/env-vars)  
> 24. Scaling Managed Agents: Decoupling the brain from the hands, [https\://www\.anthropic.com/engineering/managed-agents](https://www.anthropic.com/engineering/managed-agents)