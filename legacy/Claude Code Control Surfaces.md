# **Engineering a Production-Quality Global Claude Code Control Plane**

The deployment of autonomous software-engineering agents fundamentally shifts the paradigm of development environments from static toolchains to dynamic, context-aware orchestrations. The engineering of a global Claude Code control plane—intended to live primarily under the global user scope at C:\\Users\\USERNAME\\.claude\\—requires a rigorous architectural strategy to balance agent autonomy with deterministic safety. As the ecosystem scales to support complete software-engineering novices taking unformed ideas through requirements, architecture, implementation, testing, debugging, review, and minimum viable product (MVP) delivery, the scaffolding must mitigate inherent large language model (LLM) failure modes. These include context degradation, recursive tool-call loops, and unrestrained token expenditure that rapidly breaches the economic viability of agentic labor.  
This research report exhausts the architectural constraints, mechanisms, and empirical evidence surrounding Claude Code as of the research cutoff of October 1, 2026\. It establishes a principled framework for distributing instructions, guardrails, and knowledge across Claude Code's primary control surfaces. The analysis explicitly delineates currently supported, experimental, deprecated, and unsupported behaviors, while factoring in the unique portability constraints of Windows PowerShell and Python execution environments.

## **1\. The Physics of Agentic Context and Empirical Baselines**

To determine the optimal division of responsibility across the control plane, the underlying mechanics of how language models process information must be reconciled with Claude Code's specific context-loading and caching behaviors. The architecture must treat token cost, latency, context pollution, failure recovery, security, and novice usability as first-class constraints.

### **1.1 The Context Degradation Phenomenon**

Empirical research consistently demonstrates that language models exhibit a U-shaped performance curve when retrieving and reasoning over information in their context window1. Models reliably extract information from the extreme beginning (primacy bias) and the extreme end (recency bias) of a prompt but suffer severe intelligence degradation when critical instructions are buried in the middle4. While raw context windows have expanded, the effective reasoning capacity over that context remains bottlenecked by this attention degradation2. The phenomenon occurs because spatial token dependencies undergo sharp efficiency degradation as sequence length grows, meaning that extending context length alone can degrade performance even with perfect retrieval quality6.  
In Claude Code, the context window is populated sequentially. The loading order prioritizes the system prompt (including tool definitions), followed by project context (CLAUDE.md, unscoped rules, auto-memory), and finally the conversational history8. Placing massive, monolithic rule sets in a global CLAUDE.md forces those rules into the vulnerable "middle" of the expanded context as the conversational history grows. This structural limitation mathematically guarantees that the agent will eventually hallucinate, ignore repository conventions, or fail to adhere to security constraints if instructions are not progressively disclosed.

### **1.2 The Expenditure Horizon and Scaffolding Overhead**

The Model Evaluation and Threat Research (METR) organization defines the "Expenditure Horizon" as the budget threshold at which an AI agent becomes more expensive than human labor for a given task9. Agent scaffolding—the loops, context injections, and multi-agent routing mechanisms—can dramatically improve capability but scales computational cost linearly11. For a novice user, a control plane that indiscriminately loads hundreds of skills or spawns unnecessary subagents will breach the expenditure horizon rapidly, exhausting the user's budget before MVP delivery.  
Claude Code optimizes API costs and latency via shared prompt caching8. The API reuses processed prefixes, billing re-read content at a lower rate. However, caching relies on matching the exact start of a request against recently processed content. Any dynamic injection into the early context—such as changing an output style mid-session, altering permission modes, or connecting a new tool definition via the Model Context Protocol (MCP)—triggers a full cache miss, forcing the API to recompute the entire history8. Consequently, the control plane must avoid volatile context injections.

### **1.3 Windows Portability and Execution Environments**

The global control plane must account for disparate execution environments, particularly the nuances of Windows. On Windows, Claude Code relies on PowerShell (irm ... | iex) or CMD unless Git for Windows is explicitly installed and configured via the CLAUDE\_CODE\_GIT\_BASH\_PATH environment variable13. This introduces portability friction. File paths in permission scopes must be normalized; for example, C:\\Users\\ must be written as //c/Users/ for glob matching to function correctly in settings files15. Furthermore, deterministic hooks utilizing shell scripts must either be written in cross-platform languages or provide dual Bash and PowerShell implementations. Shell command matching in permissions must account for PowerShell aliases, ensuring that both Bash(ls \*) and PowerShell(Get-ChildItem \*) are defined17.

## **2\. Failure Modes in Agent Orchestration**

An analysis of practitioner reports and empirical benchmark data reveals several critical failure modes induced by improper configuration of Claude Code control surfaces. The eventual control plane must systematically prevent these scenarios.  
The presence of giant CLAUDE.md files is a primary catalyst for agent failure. Files exceeding the recommended limit of 200 lines or 25KB consume excessive context tokens and drastically reduce instruction adherence due to the aforementioned context degradation18. Novices typically place all API documentation, stylistic preferences, and architectural guidelines into this single file, leading to severe instruction-following failures as the session progresses.  
Similarly, deploying too many global rules creates context pollution. If un-scoped global rules are loaded unconditionally at launch, they occupy the same priority tier as CLAUDE.md18. When multiple un-scoped rules contain duplicated instructions or contradictory rules, the language model is forced to resolve the conflict probabilistically, often picking one instruction arbitrarily18. This lack of determinism introduces subtle, cascading bugs into the codebase.  
Skill overlap and vague skill descriptions disrupt the agent's autonomous planning capabilities. Claude uses skill and subagent descriptions to autonomously decide when to invoke them8. If a user accumulates dozens of globally scoped skills in \~/.claude/skills/ with vague or overlapping descriptions, the combined token count of these descriptions—which are loaded before every prompt—pollutes the context8. If custom subagent descriptions exceed 15,000 tokens, Claude Code emits a startup warning, indicating severe degradation8. Furthermore, the automatic invocation of expensive skills by an unguided agent can result in irreversible side effects, such as accidental database drops or massive cloud resource provisioning.  
Excessive subagent delegation introduces severe latency. While subagents isolate context and prevent main-session pollution, spawning them requires repopulating a completely new system prompt and warming a separate cache8. Relying on subagents for trivial tasks reduces novice usability due to perceived sluggishness and high token overhead. Similarly, excessive architectural scaffolding, such as forcing all tasks through an experimental multi-agent team architecture, severely inflates the token budget and coordination overhead, pushing the project past the expenditure horizon20.  
At the enforcement level, hooks that inject excessive context trigger runaway token consumption. If a PostToolUse hook injects verbose logging data into the context window turn-by-turn via hookSpecificOutput.additionalContext, the conversational history bloats rapidly21. This forces premature auto-compaction, which subsequently summarizes and destroys nuanced conversational state21. Finally, excessive MCP and tool exposure allows agents unrestricted access to system internals. Without strict permission scopes and organizational connector tool requirements (such as requiresUserInteraction), a novice's environment is vulnerable to arbitrary code execution or data exfiltration15.

## **3\. Analysis of Claude Code Control Surfaces**

To architect a reliable control plane, the distinct capabilities, lifecycles, and precedence rules of each Claude Code control surface must be evaluated. Configuration precedence strictly follows a hierarchy: Managed Settings \> Command Line \> Project Local (.claude/settings.local.json) \> Shared Project (.claude/settings.json) \> Global User (\~/.claude/settings.json)24.  
The global CLAUDE.md (\~/.claude/CLAUDE.md) provides persistent context loaded into every session. It is concatenated with the project CLAUDE.md from the filesystem root downward18. It must strictly contain brief, absolute invariants. Conversely, global rules (\~/.claude/rules/\*.md) allow for topic-specific instructions. Unscoped rules load globally, while path-scoped rules leverage YAML frontmatter (paths) to load conditionally18. Path-scoped rules represent the optimal mechanism for progressive disclosure, injecting context only when the agent manipulates matching files18.  
Skills (\~/.claude/skills/\*/SKILL.md) provide reusable, multi-step procedures. Their descriptions are loaded globally, but the full markdown payload is injected only upon invocation, capped at 5,000 tokens per skill18. Subagents (\~/.claude/agents/\*.md) define specialized workers with isolated context windows, specific toolsets, and distinct permission modes27. They are optimal for complex exploratory tasks that would otherwise pollute the main conversation.  
Agent teams represent an experimental architecture where multiple subagents operate in parallel, coordinated by a team lead session and communicating via a shared mailbox20. While powerful for cross-layer coordination, they consume massive token budgets and lack robust session resumption capabilities20. Dynamic workflows (.claude/workflows/\*.js) offer a highly scalable alternative for large codebase migrations. They utilize background JavaScript orchestration scripts to coordinate hundreds of subagents while leveraging shared prompt caching via staggered launches8.  
Hooks (\~/.claude/settings.json) provide deterministic lifecycle callbacks. Executed in the host shell environment, hooks intercept events such as PreToolUse or SessionStart, allowing the control plane to enforce hard safety boundaries or inject volatile state without relying on probabilistic LLM instruction adherence21. Output styles (\~/.claude/output-styles/\*.md) govern the persistent persona, tone, and formatting of the agent's responses. They modify the system prompt and require specific frontmatter (keep-coding-instructions: true) to preserve underlying software engineering capabilities29.  
Plugins (\~/.claude/plugins/) bundle skills, agents, hooks, and output styles into distributable units. They are governed by strict managed settings such as strictPluginOnlyCustomization and disableCommandPluginSources, allowing administrators to lock down ad-hoc customizations28. External project artifacts, such as Git worktrees, can be manipulated by hooks (WorktreeCreate) to provide isolated testing environments for background tasks27.

## **4\. The Progressive Disclosure Decision Matrix**

To maximize reliability and minimize global context, the control plane must adhere to a strict principle of Progressive Disclosure. Information should only exist in the context window at the exact moment the agent requires it. The following decision matrix dictates the optimal division of responsibility.

| Contextual Requirement | Optimal Control Surface | Rationale and Enforcement Mechanism |
| :---- | :---- | :---- |
| **IF information must always be known across the entire codebase** | Global CLAUDE.md | Limited strictly to \< 200 lines. Enforced probabilistically via the system prompt. Ideal for absolute core invariants (e.g., "Use TypeScript strictly"). |
| **IF instruction is domain or path-specific** | Path-scoped rules (.claude/rules/\*.md) | Leverages paths YAML frontmatter to load instructions only when matching files are accessed, eliminating context pollution18. |
| **IF procedure is reusable, multi-step, but occasional** | Global Skills (\~/.claude/skills/) | Descriptions are loaded globally for discovery; payload is injected upon invocation19. |
| **IF behavior absolutely must happen (safety constraints)** | Deterministic Hooks (PreToolUse) | LLMs cannot reliably enforce negative constraints. Scripts returning exit code 2 or JSON denials guarantee blocking21. |
| **IF task requires context isolation to prevent bloat** | Subagents (\~/.claude/agents/) | Operates in a distinct context window, returning only parsed summaries to the main session8. |
| **IF independent verification or competing hypotheses are needed** | Agent Teams (Experimental) | Coordinates multiple parallel agents via a shared mailbox. High token cost, reserved for security audits20. |
| **IF workflow requires massive scale (hundreds of files)** | Dynamic Workflows | Orchestrates background subagents via JS scripts, utilizing prompt cache staggering to maintain the expenditure horizon8. |
| **IF behavior has irreversible side effects (e.g., production deploy)** | Skills with disable-model-invocation: true | Removes the skill from the autonomous planning loop, forcing the human user to manually invoke the workflow31. |

## **5\. Material Findings Database**

The following material findings represent the exhaustive technical parameters, mechanisms, and empirical data required to construct the global control plane.

### **Finding 1: Context Degradation Mitigation via Path-Scoped Rules**

The analysis indicates that global instruction files suffer from severe context degradation, necessitating decentralized loading mechanisms.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Global monolithic instruction files suffer from "Lost in the Middle" degradation. Information must be decentralized using path-scoped rules. |
| **Evidence/Source** | 1 |
| **Evidence Strength** | Strong (Backed by official documentation and peer-reviewed arXiv studies). |
| **Mechanism Implicated** | rules/\*.md utilizing paths YAML frontmatter globs. |
| **Global Candidate?** | Yes. Global path-scoped rules can reside in \~/.claude/rules/. |
| **Enforcement Strategy** | Prompt-based (Files load deterministically into context, but adherence is probabilistic). |
| **Cost/Context Implications** | Highly efficient. Tokens are consumed exclusively when the agent interacts with matching file paths. |
| **Security Implications** | Prevents context-hijacking and hallucination caused by overflowing instruction sets. |
| **Open Question** | How efficiently do complex YAML glob patterns resolve across native Windows NTFS paths versus WSL2 translation layers within the same session context? |

Path-scoped rules represent the primary defense against context pollution. By defining rules with frontmatter (e.g., paths: src/components/\*\*/\*.tsx), the control plane can house thousands of lines of highly specific architectural guidelines without incurring token costs until the agent actively edits the frontend. For a novice user, a global control plane can supply an expansive library of best practices that remain dormant, loading gracefully via progressive disclosure.

### **Finding 2: Deterministic Enforcement for Safety-Critical Constraints**

The evidence demonstrates that language models cannot guarantee adherence to negative constraints, requiring system-level interception.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Prompt-based instructions (e.g., "Do not delete production data") are mathematically incapable of guaranteeing safety. Absolute constraints must be offloaded to deterministic hooks. |
| **Evidence/Source** | 19 |
| **Evidence Strength** | Strong (Explicit official guidance dictates that absolute rules must utilize hooks). |
| **Mechanism Implicated** | PreToolUse Hooks returning exit 2 or structured JSON {"hookSpecificOutput": {"permissionDecision": "deny"}}. |
| **Global Candidate?** | Yes. Defined in \~/.claude/settings.json. |
| **Enforcement Strategy** | Deterministic (Runtime blocking prior to tool execution). |
| **Cost/Context Implications** | Zero token cost if the hook allows the action silently; minimal context addition if a denial reason is appended to the prompt. |
| **Security Implications** | Critical. This represents the sole reliable methodology to sandbox destructive novice mistakes. |
| **Open Question** | Can autonomous agents construct obfuscated shell payloads (e.g., eval(base64)) that evade regular expression matchers within the hook script? |

Novices cannot be trusted to verify every agent action manually, making auto permission mode essential for usability. However, auto mode relies on a secondary classifier that is probabilistic23. A global control plane must implement robust PreToolUse hooks targeting Bash and PowerShell tools. These scripts evaluate the tool\_input.command on stdin and force an exit 2 if destructive patterns are detected, stripping the model of the ability to execute the action entirely.

### **Finding 3: Shielding Side-Effect Workflows from Autonomous Invocation**

Workflows that mutate state must be explicitly hidden from the agent's autonomous planning loop to prevent catastrophic misinterpretation.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Skills that trigger external mutations, deployments, or large-scale deletions must be explicitly shielded from Claude's autonomous tool selection. |
| **Evidence/Source** | 31 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | Skill frontmatter attribute disable-model-invocation: true. |
| **Global Candidate?** | Yes. Global skills residing in \~/.claude/skills/. |
| **Enforcement Strategy** | Deterministic (The routing engine drops the skill from the generated tool schema). |
| **Cost/Context Implications** | Preserves context space and prevents massive API costs resulting from hallucinated deployment loops. |
| **Security Implications** | High. Prevents the autonomous execution of high-risk workflows. |
| **Open Question** | If a subagent is explicitly instructed to execute a disabled skill, does it inherit the human user's manual override privilege? |

By default, Claude evaluates loaded skill descriptions to invoke them autonomously. If a novice user casually asks Claude to "clean up the codebase," the agent might autonomously invoke a global /purge-database skill. By enforcing disable-model-invocation: true, the skill is removed from the tool schema presented to Claude, requiring the novice to explicitly type the slash command to initiate the sequence.

### **Finding 4: Subagent Context Limits and Description Bloat**

While subagents isolate operational context, their global definitions introduce substantial overhead to the main session.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Over-populating the global agents directory triggers context pollution, as all subagent descriptions are injected into the main session's system prompt prior to execution. |
| **Evidence/Source** | 8 |
| **Evidence Strength** | Moderate (Documented via the 15,000 token limit startup warning). |
| **Mechanism Implicated** | Subagent Markdown files (name and description YAML). |
| **Global Candidate?** | Conditional. Only highly generalized, universally applicable agents should reside globally. |
| **Enforcement Strategy** | Prompt-based (Descriptions guide Claude's delegation decisions). |
| **Cost/Context Implications** | High continuous token cost if descriptions are excessively long or numerous. |
| **Security Implications** | Low. |
| **Open Question** | Are descriptions from plugin-provided agents counted against the 15,000 token limit concurrently with user-defined global agents? |

Subagents effectively isolate tasks, preventing temporary search results from polluting the main conversation17. However, the control plane must restrict the description fields in \~/.claude/agents/\*.md to extreme brevity. Complex behavioral instructions must reside exclusively below the \--- frontmatter separator, as that text is only loaded when the subagent is actively spawned and its isolated context window is initialized27.

### **Finding 5: Context Re-hydration Post-Compaction**

The auto-compaction mechanism destroys volatile state variables, requiring deterministic re-injection to maintain continuity.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | When a session reaches the context limit, auto-compaction summarizes the history, permanently discarding dynamically acquired environmental variables and temporal state. |
| **Evidence/Source** | 21 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | SessionStart hook configured with matcher: "compact". |
| **Global Candidate?** | Yes. Global hooks apply to all compaction events uniformly. |
| **Enforcement Strategy** | Deterministic injection of stdout text into the active prompt. |
| **Cost/Context Implications** | Re-consumes a minor portion of the newly freed context window to preserve continuity. |
| **Security Implications** | Low. |
| **Open Question** | Does the output of the SessionStart hook bypass the prompt cache if it contains highly volatile temporal data such as timestamps? |

Long-lived MVP development sessions will inevitably experience multiple /compact events. While CLAUDE.md and unscoped rules are natively re-read from disk, dynamically acquired state—such as active debugging variables, sprint focus, or current git branch status—is lost. The global control plane must define a SessionStart hook matching the compact event to dynamically echo critical system state back to stdout. Claude Code will subsequently prepend this output to the new compacted context, ensuring the agent remains oriented21.

### **Finding 6: Securing Cross-Session Agent Interactivity**

The ability for independent agent sessions to communicate introduces vectors for privilege escalation that must be strictly governed.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Cross-session messaging enables agents to hand over findings, but introduces a critical risk of privilege escalation if a locked-down session accepts commands from a bypass-permissions session. |
| **Evidence/Source** | 20 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | The crossSessionInbound configuration setting and the internal SendMessage tool. |
| **Global Candidate?** | Yes. Must be explicitly configured in \~/.claude/settings.json. |
| **Enforcement Strategy** | Deterministic (Runtime network boundary enforcement). |
| **Cost/Context Implications** | Low. Only plain text is transferred, preventing context history cross-contamination. |
| **Security Implications** | High. Cross-session messages cannot approve permission prompts on behalf of the user, preventing indirect authorization attacks. |
| **Open Question** | Can a meticulously crafted prompt be transmitted via SendMessage to trigger an adversarial injection attack on the receiving agent's planning loop? |

Novices managing complex projects may run multiple Claude instances simultaneously (e.g., one auditing the backend, one styling the frontend). While they can message each other to coordinate, the control plane must govern this interaction via the crossSessionInbound setting. A global default should be set to hold or refuse for highly sensitive environments. This configuration prevents a compromised web-research agent from transmitting malicious execution instructions to a local-filesystem agent running with elevated privileges20.

### **Finding 7: Portability Imperatives for Windows PowerShell**

The control plane must accommodate disparate operating system architectures to prevent systemic failures for Windows-based users.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Global permission rules and hooks fail catastrophically on Windows systems if they assume POSIX compliance or UNIX path structures. |
| **Evidence/Source** | 13 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | permissions.allow structures, and the distinction between the Bash and PowerShell internal tools. |
| **Global Candidate?** | Yes. |
| **Enforcement Strategy** | Deterministic path resolution and command matching. |
| **Cost/Context Implications** | N/A |
| **Security Implications** | Moderate. Misconfigured path rules failing to parse correctly may accidentally expose unintended system directories. |
| **Open Question** | Are PowerShell command aliases (e.g., ls resolving to Get-ChildItem) reliably parsed and restricted by the permissions.allow abstract syntax tree? |

A control plane architected exclusively for macOS or Linux environments will fail for Windows novices. The target system must meticulously account for C:\\ drives. Specifically, setting global permission scopes in settings.json requires Windows paths to be formatted as //c/Users/15. Furthermore, the control plane must not exclusively hardcode rules such as Bash(ls \*); it must explicitly define PowerShell(Get-ChildItem \*) to ensure functional parity and secure command gating across all supported environments17.

### **Finding 8: Optimizing the Expenditure Horizon via Dynamic Workflows**

Large-scale repository operations must leverage architectural features designed to maximize cache utilization and minimize redundant prompt processing.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Launching dozens of agents manually shatters API rate limits and token budgets due to the redundant processing of the system prompt and global context. |
| **Evidence/Source** | 8 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | Dynamic Workflows (.claude/workflows/\*.js) and the CLAUDE\_CODE\_WORKFLOW\_PREFIX\_STAGGER\_MS environment variable. |
| **Global Candidate?** | Yes. Generalized workflow templates can reside globally. |
| **Enforcement Strategy** | Deterministic (Execution within an isolated V8 runtime sandbox). |
| **Cost/Context Implications** | Drastically reduces aggregate token costs via staggered cache warming. |
| **Security Implications** | High. The JavaScript script cannot access the filesystem directly; it strictly coordinates subagent execution parameters. |
| **Open Question** | Can a dynamic workflow resume execution cleanly if a subset of the orchestrated subagents encounters a hard API failure mid-run? |

For massive repository refactors, the control plane should provide pre-built Dynamic Workflows rather than relying on experimental Agent Teams. Agent Teams populate the main terminal UI and consume immense token budgets via inter-agent communication20. Conversely, Dynamic Workflows run isolated JavaScript scripts in the background, staggering their subagent launches (defaulting to 5000ms) to ensure all child agents hit the exact same prompt cache prefix. They return only the final synthesized result to the user8. This mechanism is the only mathematically viable approach to keeping large-scale automation beneath the expenditure horizon.

### **Finding 9: Classifier Overhead in Auto Mode**

While automated permissions improve usability, over-reliance on secondary classifiers introduces unacceptable latency penalties.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | The auto permission mode relies on a secondary classifier model. Routing benign, read-only commands through this classifier induces massive interactive latency for the user. |
| **Evidence/Source** | 23 |
| **Evidence Strength** | Moderate |
| **Mechanism Implicated** | The autoMode.classifyAllShell boolean and permissions.allow AST logic. |
| **Global Candidate?** | Yes. |
| **Enforcement Strategy** | Deterministic routing logic. |
| **Cost/Context Implications** | Introduces secondary API calls and latency per shell execution. |
| **Security Implications** | High. Modifies the rigor of the secondary safety gate. |
| **Open Question** | Does the classifier cache its results for identical, repeated shell commands during a single active session? |

For a novice, the auto permission mode is essential to prevent prompt fatigue resulting from constant manual approvals. However, setting autoMode.classifyAllShell \= true forces every single benign command—such as ls, pwd, or cat—through the secondary LLM safety classifier, causing the CLI to become unresponsive and sluggish25. The control plane should define robust permissions.allow rules for read-only commands, which bypass the classifier natively, and leave classifyAllShell as false. This relies on the default classifier logic, which efficiently scrutinizes only unrecognized external mutations.

### **Finding 10: State Management via Output Styles**

Behavioral tuning must be isolated from procedural instructions to preserve the agent's core capabilities and optimize the context window.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Appending behavioral modifiers (e.g., "be concise", "explain your reasoning step-by-step") to the global CLAUDE.md is an inefficient use of the highly constrained context window. |
| **Evidence/Source** | 29 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | The .claude/output-styles/\*.md architecture and associated configurations. |
| **Global Candidate?** | Yes. Global personas should reside in \~/.claude/output-styles/. |
| **Enforcement Strategy** | Prompt-based (Modifies the foundational system prompt). |
| **Cost/Context Implications** | Alters generation length and density (output tokens), thereby controlling aggregate API costs. |
| **Security Implications** | Low. |
| **Open Question** | Does switching an output style mid-session invalidate the prompt cache for the entire preceding conversational history across all supported cloud providers? |

Novice users frequently struggle with the agent over-explaining code modifications. Rather than cluttering instructional memory with stylistic preferences, the control plane should ship custom Output Styles (e.g., a custom Concise persona). These styles inject specific tone instructions globally across the session. Crucially, the frontmatter attribute keep-coding-instructions: true must be utilized in all custom styles; omitting it strips the model of its foundational software engineering system prompt, degrading code quality29.

### **Finding 11: Protecting the Agentic Loop from Hook Validation Failures**

The runtime behavior of hook execution requires stringent output formatting to prevent fail-open security bypasses.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Hooks that return invalid JSON payloads or fail schema validation do not halt the agentic loop; they fail open, allowing the intercepted action to proceed as a non-blocking error. |
| **Evidence/Source** | 21 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | Hook stdout JSON parsing and validation logic. |
| **Global Candidate?** | Yes (Applies universally to all hook implementations). |
| **Enforcement Strategy** | Deterministic (Runtime exception handling protocols). |
| **Cost/Context Implications** | N/A |
| **Security Implications** | Critical vulnerability if security-focused hooks are improperly formatted or emit debugging text. |
| **Open Question** | Is there a strict configuration mode available to force a fail-closed behavior upon encountering JSON parse errors? |

If a control plane relies on a global PreToolUse hook to block unauthorized database deletions, but the underlying bash script accidentally prints an initialization string or debug statement alongside its JSON decision payload, Claude Code will fail to parse the JSON. Alarmingly, the runtime treats this as a non-blocking error and allows the potentially destructive tool call to proceed21. Control plane developers must enforce extreme strictness on hook stdout, systematically redirecting all debug, logging, and initialization outputs to stderr to prevent catastrophic fail-open security bypasses.

### **Finding 12: Bypassing Extraneous Data via claudeMdExcludes**

Large-scale environments require explicit firewalls against context pollution originating from unrelated directory structures.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | In large monorepos, the recursive loading of CLAUDE.md files from unrelated sibling directories poisons the context window with irrelevant architectural guidelines. |
| **Evidence/Source** | 18 |
| **Evidence Strength** | Moderate |
| **Mechanism Implicated** | The claudeMdExcludes array defined in settings.json. |
| **Global Candidate?** | Conditional. Highly effective in \~/.claude/settings.json for managing massive enterprise setups. |
| **Enforcement Strategy** | Deterministic file exclusion during the recursive discovery phase. |
| **Cost/Context Implications** | Yields exceptionally high context savings by eliminating redundant instructions. |
| **Security Implications** | Low. |
| **Open Question** | Are files explicitly imported into a valid CLAUDE.md (via the @import syntax) subjected to the claudeMdExcludes evaluation, or do they bypass the filter? |

When a user navigates a large enterprise repository, Claude Code recursively discovers and concatenates all CLAUDE.md files from the filesystem root downward to the current working directory18. The global control plane must define a robust claudeMdExcludes array in the global settings to explicitly ignore legacy or deprecated directories (e.g., "\*\*/legacy-\*/\*\*")18. This configuration acts as a critical firewall against context degradation initiated by legacy or irrelevant team documentation.

### **Finding 13: Deprecation of Legacy MCP Replacements**

Modern control planes must rely exclusively on current schemas to prevent silent failures during runtime updates.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Legacy fields designed for updating tool outputs are officially deprecated and must not be used in modern scaffolding architectures. |
| **Evidence/Source** | 22 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | The updatedMCPToolOutput field versus the modern updatedToolOutput field. |
| **Global Candidate?** | Yes. |
| **Enforcement Strategy** | Schema enforcement and validation. |
| **Cost/Context Implications** | N/A |
| **Security Implications** | Low. |
| **Open Question** | Will the updatedMCPToolOutput field be entirely removed, resulting in hard crashes, in the next major runtime update? |

When designing PostToolUse hooks to sanitize, filter, or format tool outputs before Claude reads them—such as stripping sensitive credentials from an API response before it enters the context window—the control plane must exclusively utilize the updatedToolOutput JSON field. The older updatedMCPToolOutput is explicitly marked as deprecated in official documentation22. Relying on deprecated schemas introduces the risk of silent failures in future Claude Code versions, potentially exposing sensitive data to the language model.

### **Finding 14: Centralized Lockdown via strictPluginOnlyCustomization**

In environments requiring strict compliance, user-level customizations present an unacceptable security risk and must be programmatically disabled.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Locally defined skills, hooks, and agents can introduce unchecked vulnerabilities, allow data exfiltration, or bypass organizational safety guardrails. |
| **Evidence/Source** | 25 |
| **Evidence Strength** | Strong |
| **Mechanism Implicated** | The strictPluginOnlyCustomization boolean defined in managed settings. |
| **Global Candidate?** | Yes. Must be enforced via managed-settings.json. |
| **Enforcement Strategy** | Deterministic disabling of custom component discovery. |
| **Cost/Context Implications** | N/A |
| **Security Implications** | High. Ensures that only verified, centrally distributed capabilities are executed. |
| **Open Question** | Can an adversarial user bypass this lockdown by injecting complex prompt instructions that emulate the capabilities of a disabled skill? |

If the control plane is intended for a structured enterprise environment (even if the end-users are novices), security cannot rely on user discipline. Administrators must deploy a managed-settings.json file setting strictPluginOnlyCustomization to true30. This completely disables ad-hoc .claude/skills/ or .claude/hooks/ written by the user, ensuring that only cryptographically verified or centrally managed plugins are executed by the engine.

### **Finding 15: Agent SDK Hook Context Mutability**

If the control plane architecture integrates the Agent SDK, language selection dictates the availability of critical cancellation primitives.

| Attribute | Detail |
| :---- | :---- |
| **Finding** | Hooks operating via the Agent SDK interact differently with execution context depending on the language bindings, with Python lacking the cancellation primitives present in TypeScript. |
| **Evidence/Source** | 22 |
| **Evidence Strength** | Moderate |
| **Mechanism Implicated** | The AbortSignal implementation in TypeScript versus the reserved Context argument in Python. |
| **Global Candidate?** | No (SDK specific implementation detail). |
| **Enforcement Strategy** | Language runtime boundaries. |
| **Cost/Context Implications** | N/A |
| **Security Implications** | Low. |
| **Open Question** | When will the Python SDK receive functional parity for AbortSignal cancellation primitives? |

If the control plane eventually wraps Claude Code via the Agent SDK rather than relying solely on the CLI, architectural language choices matter significantly. The TypeScript SDK passes an AbortSignal via the hook context argument, allowing hooks to gracefully intercept and cancel runaway agentic loops. Conversely, the Python SDK currently reserves this argument and cannot gracefully abort the execution flow from within a hook callback22.

## **6\. Synthesis and Deliverables**

Based on the empirical evidence and architectural analysis of the Claude Code runtime, the following requirements strictly dictate the construction of the global control plane.

### **A. Design Requirements Derived from the Evidence**

> 1. **Context Decentralization:** The control plane must completely abandon the monolithic CLAUDE.md pattern. Core project metadata must be restricted to a global CLAUDE.md strictly under 200 lines. All domain-specific instructions must be placed in \~/.claude/rules/ utilizing the paths frontmatter. This ensures lazy loading based on active file targets, preserving the integrity of the context window.  
> 2. **Hook-Driven Safety Net:** A globally deployed \~/.claude/settings.json must establish PreToolUse hooks targeting Bash and PowerShell. These hooks must strictly write only valid JSON to stdout, outputting {"hookSpecificOutput": {"permissionDecision": "deny"}} when destructive commands (e.g., rm \-rf) are detected. All debug and initialization outputs must route to stderr to prevent fail-open parsing errors that compromise security.  
> 3. **Skill Frontmatter Governance:** Any global skill in \~/.claude/skills/ that mutates state, provisions resources, or interacts with external services must include disable-model-invocation: true. This constraint prevents Claude from autonomously breaching the expenditure horizon by hallucinating the necessity of expensive routines without explicit user confirmation.  
> 4. **Cross-Platform Path Normalization:** Permission rules and deterministic scripts within the control plane must explicitly support Windows execution environments. Permissions must specify //c/ style paths, and shell rules must account for PowerShell syntax (e.g., Get-ChildItem) parallel to Bash equivalents.  
> 5. **Dynamic Workflow Orchestration for Scale:** Tasks involving more than a dozen files or distinct operations must not be routed to experimental Agent Teams. The control plane must provide .claude/workflows/\*.js scripts. This leverages the 5000ms stagger window (CLAUDE\_CODE\_WORKFLOW\_PREFIX\_STAGGER\_MS) to ensure all background agents share a cached prompt prefix, minimizing redundant token spend.  
> 6. **Context Re-hydration:** A global SessionStart hook matching the compact event must be deployed to immediately re-inject critical, volatile state variables back into the context window after the Claude Code engine summarizes the conversational history.

### **B. Anti-Requirements (What the Control Plane Should NOT Do)**

> 1. **Do Not Inflate Subagent Descriptions:** The control plane must not provide global subagents (\~/.claude/agents/) with verbose descriptions. Exceeding the 15,000-token aggregate limit poisons the main session's prompt cache. Granular instructions belong exclusively below the \--- markdown separator, never in the YAML description field.  
> 2. **Do Not Overuse autoMode.classifyAllShell:** The control plane must not set classifyAllShell: true in the global settings. This configuration forces every safe, read-only shell command (e.g., ls, cat) through the secondary LLM safety classifier, introducing unacceptable interactive latency and extraneous API costs for the novice user.  
> 3. **Do Not Use Deprecated MCP Hooks:** The architecture must not use updatedMCPToolOutput in PostToolUse hooks. It must be completely replaced by updatedToolOutput to ensure forward compatibility and prevent silent failures during runtime updates.  
> 4. **Do Not Mix Rules and Personas:** The control plane must not put behavioral tone modifiers ("be concise," "explain step-by-step") in CLAUDE.md or .claude/rules/. These directives must be isolated into .claude/output-styles/ with the mandatory keep-coding-instructions: true flag to prevent the model from losing its foundational software engineering reasoning capabilities.

### **C. Unresolved Questions**

> 1. **Cross-OS Glob Resolution:** It remains empirically unverified how seamlessly YAML paths globs resolve across native Windows NTFS paths versus WSL2 translation layers when evaluated within the same active session context.  
> 2. **Hook Evasion via Obfuscation:** While deterministic PreToolUse hooks effectively block known destructive strings, it is unclear if an autonomously acting agent—hallucinating a complex fix—could construct a base64-encoded shell payload that bypasses regex matchers while successfully executing in Bash.  
> 3. **Cache Invalidation on Output Style Shifts:** Switching an output style mid-session alters the foundational system prompt instructions. It is not strictly documented whether this triggers a complete, irrecoverable cache invalidation for the entire preceding conversational history across all supported cloud providers.  
> 4. **Subagent Hook Inheritance:** If a main session runs in bypassPermissions mode but delegates to a subagent that triggers a globally defined PreToolUse hook, the exact precedence of the bypass flag versus the deterministic hook's exit code requires further runtime validation to ensure security boundaries are maintained.

#### **Works cited**

> 1. Context-Engineering Challenges & Best-Practices \- Ali Arsanjani, [https\://dr-arsanjani.medium.com/context-engineering-challenges-best-practices-8e4b5252f94f](https://dr-arsanjani.medium.com/context-engineering-challenges-best-practices-8e4b5252f94f)  
> 2. Lost in the Middle: Why LLMs Struggle With Long Contexts \- Pristren, [https\://pristren.com/blog/lost-in-middle-attention-paper/](https://pristren.com/blog/lost-in-middle-attention-paper/)  
> 3. Lost in the Middle: How Language Models Use Long Contexts, [https\://cs.stanford.edu/\~nfliu/papers/lost-in-the-middle.arxiv2023.pdf](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf)  
> 4. What Works for 'Lost-in-the-Middle' in LLMs? A Study on GM-Extract, [https\://arxiv.org/html/2511.13900v1](https://arxiv.org/html/2511.13900v1)  
> 5. On Problems of Implicit Context Compression for Software ... \- arXiv, [https\://arxiv.org/pdf/2605.11051](https://arxiv.org/pdf/2605.11051)  
> 6. DRIVEN FRAMEWORK FOR AI-NATIVE CODE GENERATION \- arXiv, [https\://arxiv.org/pdf/2606.05720](https://arxiv.org/pdf/2606.05720)  
> 7. Coding Agents are Effective Long-Context Processors \- arXiv, [https\://arxiv.org/html/2603.20432v1](https://arxiv.org/html/2603.20432v1)  
> 8. [https\://code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows)  
> 9. Expenditure Horizon: Measuring Optimization Ability, with ... \- METR, [https\://metr.org/blog/2026-07-21-expenditure-horizon/](https://metr.org/blog/2026-07-21-expenditure-horizon/)  
> 10. NanoGPT Speedrun Frontier \- Hacker News, [https\://news.ycombinator.com/item?id=49404380](https://news.ycombinator.com/item?id=49404380)  
> 11. Evaluating frontier AI R\&D capabilities of language model agents, [https\://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/](https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/)  
> 12. Your Harness Is the Cost Line, Not Your Model \- Dik Rana, [https\://dikrana.dev/blog/agent-harness-token-overhead/](https://dikrana.dev/blog/agent-harness-token-overhead/)  
> 13. Terminal guide for new users \- Claude Code Docs, [https\://code.claude.com/docs/en/terminal-guide](https://code.claude.com/docs/en/terminal-guide)  
> 14. Advanced setup \- Claude Code Docs, [https\://code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup)  
> 15. Configure permissions \- Claude Code Docs, [https\://code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)  
> 16. Berechtigungen konfigurieren \- Claude Code Docs, [https\://code.claude.com/docs/de/permissions](https://code.claude.com/docs/de/permissions)  
> 17. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 18. How Claude remembers your project \- Claude Code Docs, [https\://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)  
> 19. Extend Claude Code \- Claude Code Docs, [https\://code.claude.com/docs/en/features-overview](https://code.claude.com/docs/en/features-overview)  
> 20. [https\://code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)  
> 21. Automate actions with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
> 22. Intercept and control agent behavior with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/hooks](https://code.claude.com/docs/en/agent-sdk/hooks)  
> 23. Choose a permission mode \- Claude Code Docs, [https\://code.claude.com/docs/en/permission-modes?1e959936\_page=2&46f68bc1\_page=1](https://code.claude.com/docs/en/permission-modes?1e959936_page=2&46f68bc1_page=1)  
> 24. Settings files and precedence \- Claude Code Docs, [https\://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
> 25. All settings \- Claude Code Docs, [https\://code.claude.com/docs/en/settings-reference](https://code.claude.com/docs/en/settings-reference)  
> 26. Explore the context window \- Claude Code Docs, [https\://code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window)  
> 27. Create custom subagents \- Claude Code Docs, [https\://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
> 28. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 29. Output styles \- Claude Code Docs, [https\://code.claude.com/docs/en/output-styles](https://code.claude.com/docs/en/output-styles)  
> 30. Deploy managed settings \- Claude Code Docs, [https\://code.claude.com/docs/en/managed-settings](https://code.claude.com/docs/en/managed-settings)  
> 31. Commands \- Claude Code Docs, [https\://code.claude.com/docs/en/commands](https://code.claude.com/docs/en/commands)  
> 32. Extend Claude with skills \- Claude Code Docs, [https\://code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)  
> 33. Best practices for Claude Code, [https\://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)  
> 34. Common workflows \- Claude Code Docs, [https\://code.claude.com/docs/en/common-workflows](https://code.claude.com/docs/en/common-workflows)  
> 35. Configure auto mode \- Claude Code Docs, [https\://code.claude.com/docs/en/auto-mode-config](https://code.claude.com/docs/en/auto-mode-config)  
> 36. Set up Claude Code in a monorepo or large codebase, [https\://code.claude.com/docs/en/large-codebases](https://code.claude.com/docs/en/large-codebases)  
> 37. Manage Claude Code plugins for your organization, [https\://code.claude.com/docs/en/plugins/org](https://code.claude.com/docs/en/plugins/org)