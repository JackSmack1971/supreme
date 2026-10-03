# **Engineering a Global Claude Code Control Plane: Preventing Architectural Decay in Agent-Generated Greenfield Projects**

## **1\. Introduction**

The proliferation of autonomous coding agents has fundamentally transformed the velocity of software development, driving the marginal cost of code generation toward zero. However, this acceleration introduces a critical vulnerability: the rapid accumulation of structural entropy. When novice developers utilize systems like Claude Code to bootstrap greenfield projects, the absence of human architectural intuition, combined with the agent’s propensity for probabilistic token prediction, frequently results in catastrophic architectural decay. Codebases rapidly degrade into spaghetti architecture, encumbered by premature abstractions, needless frameworks, and hidden coupling.  
To mitigate these failure modes, relying purely on behavioral prompting (such as CLAUDE.md instructions) is insufficient. Prompts are inherently probabilistic, susceptible to context dilution, and easily overridden by subsequent conversational turns. True architectural governance requires a deterministic control plane. This report investigates the empirical evidence surrounding AI-generated technical and cognitive debt, evaluating the relative efficacy of various architectural paradigms. It derives an exhaustive set of material findings and specifications for a global control plane—intended to reside primarily under C:\\Users\\USERNAME\\.claude\\ on Windows systems—that programmatically enforces simple, evolvable, and testable design for novice-led greenfield projects.

## **2\. The Pathology of AI-Generated Architecture**

Understanding why coding agents produce locally plausible but globally poor architecture requires analyzing the intersection of large language model (LLM) mechanics, empirical software engineering research, and the strict constraints of agentic memory and computation horizons.

### **2.1 The Crisis of Cognitive and Intent Debt**

Traditional software engineering literature focuses heavily on technical debt, defined as the long-term cost of messy code implemented for short-term speed. However, recent empirical studies on AI-assisted development identify two far more dangerous variants introduced by autonomous coding agents: cognitive debt and intent debt1.  
Cognitive debt occurs when an AI system generates functional code faster than a human developer can build an accurate mental model of its execution flow. For a software engineering novice, this debt is incurred instantly upon project initialization, leaving them incapable of verifying or maintaining the system1. Intent debt occurs when the rationale behind a design decision is never externalized1. When an agent generates a complex service layer, it does so based on transient context window weights. Once that context window is compacted or the session is terminated, the specific intent behind the abstraction is permanently lost. Subsequent agent sessions attempting to modify the code cannot reverse-engineer the original intent, leading directly to duplicated concepts, circular dependencies, and the dreaded "god module" anti-pattern1.

### **2.2 Context Horizons and the METR Degradation**

The METR (Model Evaluation and Threat Research) task-completion time horizons demonstrate that frontier models struggle significantly with sustained, open-ended autonomous work5. While models achieve high success rates on short, well-scoped tasks, their reliability decays exponentially as the time horizon extends. The 50% success horizon for state-of-the-art models currently sits between 4 and 17 hours of equivalent human effort, depending on the specific benchmark methodology5. Furthermore, high success rates in synthetic benchmarks often mask severe data contamination; for example, the MirrorCode benchmark revealed that up to 68% of the complex, week-long target programs were already present in the models' training data9.  
In the context of greenfield architecture, this horizon limitation manifests as architectural drift. An agent may begin with a coherent design paradigm, but as the session lengthens and the context window fills with tool execution results, stack traces, and environment noise, the agent’s architectural coherence degrades10. The agent defaults to statistical conveniences, aggressively copying patterns seen in training data regardless of their necessity in the current project. This directly causes speculative extensibility, where the agent builds out framework-default architectures complete with unnecessary microservices and abstract factories, entirely devoid of underlying reasoning9.

### **2.3 The Cyclomatic Complexity Barrier**

Empirical research on AI code generation reveals a steep drop in agent reliability as the cognitive and cyclomatic complexity of a codebase increases13. Models struggle with the compositional jumps required to reason over nested and branching semantic units13.  
When agents are allowed to build horizontally layered architectures (such as standard N-Tier or traditional Clean Architecture), feature logic becomes scattered across controllers, services, repositories, and data transfer objects. To implement or fix a single feature, the agent must load multiple interdependent files into its context, artificially inflating the cyclomatic complexity of the prompt12. This directly triggers reasoning failures, hallucinated variable assignments, and hidden coupling, as the agent fails to maintain the strict invariants required across disparate files13.

## **3\. Relative Value of Architectural Interventions**

To protect a novice developer, the global control plane must force the agent into architectural patterns that inherently limit context pollution, enforce locality, and require minimal cognitive load to test and maintain. An evaluation of contemporary architectural interventions reveals a stark divide between mechanisms that are mandatory for AI-assisted greenfield builds and those that introduce needless ceremony.

### **3.1 Highly Effective Mandatory Safeguards**

**Vertical Slices:** Vertical Slice Architecture (VSA) is empirically superior for agentic workflows12. By grouping code by specific business feature rather than technical concern, VSA ensures high cohesion and low coupling. When an agent modifies a feature, it only reads files within a single directory, perfectly aligning with context window constraints and preventing cross-domain hallucinations10.  
**Architecture Fitness Functions and Static Dependency Checks:** Prompting an agent to "respect boundaries" reliably fails over long horizons. Architectural drift must be caught by static dependency checks, known as fitness functions17. Tools such as dependency-cruiser (JavaScript/TypeScript) or ArchUnitTS validate import graphs to detect circular dependencies or boundary violations (e.g., a domain model illegally importing a UI component)18. These functions are mandatory deterministic safeguards.  
**Architecture Decision Records (ADRs):** To combat intent debt, architectural decisions must be explicitly documented via ADRs22. For coding agents, ADRs provide essential heuristic guidance that survives session termination and context compaction. A deterministic control plane must intercept structural changes, forcing the agent to author an ADR justifying the complexity against the project's budget, ensuring future agent sessions load this ADR via InstructionsLoaded hooks24.  
**Architectural Budgets and YAGNI:** Every team has a complexity budget, and exceeding it early guarantees systemic failure24. Enforcing YAGNI (You Aren't Gonna Need It) and strict architectural budgets prevents the agent from deploying speculative extensibility. Imposing limits on cyclomatic complexity per module serves as an effective proxy for this budget, forcing the agent to maintain simple-design principles13.  
**Evolutionary Architecture:** Software ecosystems managed by AI must be designed for continuous, incremental change rather than rigid upfront design. Evolutionary architecture relies heavily on fitness functions to protect the system as it mutates, making it an essential philosophical underpinning for the control plane17.

### **3.2 High-Value Interventions with Implementation Challenges**

**Explicit Quality Attributes:** While explicitly defining quality attributes (e.g., latency limits, memory ceilings) helps agents avoid premature optimization, these attributes are difficult for a complete novice to articulate accurately12. They are highly valuable but must be scaffolded by the control plane rather than demanded from the user.  
**Dependency Direction Rules:** Establishing explicit rules (e.g., high-level policies must not depend on low-level details) is a core tenet of stable design. However, relying on the agent to intuitively understand and consistently apply these rules fails12. Dependency direction rules are highly valuable only when codified directly into deterministic fitness functions.

### **3.3 Needless Ceremony for Novices**

**Interface-First Design:** While vital for massive enterprise systems, requiring a novice's greenfield project to define abstract interfaces before concrete implementations exhausts the agent's context window with boilerplate, directly reducing the token budget available for functional logic12.  
**Independent Architecture Review:** Incremental design reviews—where humans evaluate proposed complexity against a budget—are the gold standard in enterprise environments30. However, for a complete novice working with an AI agent, independent human review is unavailable. The control plane must substitute this with automated fitness functions and mandatory ADR generation.

## **4\. Criteria for a Future Architecture Agent or Skill**

A dedicated Architecture Agent or Architecture Skill must be capable of evaluating greenfield codebase proposals against a strict set of heuristics designed to prevent AI-induced architectural decay. The evaluation criteria must include the following metrics:

| Evaluation Criterion | Metric/Threshold | Primary Purpose |
| :---- | :---- | :---- |
| **Context Locality (Cohesion)** | \> 85% of feature-specific dependencies must reside within the same vertical slice directory. | Prevents scattered logic and context window exhaustion during future agent modifications. |
| **Dependency Acyclicity** | 0 detected circular dependencies across the global module graph. | Eliminates infinite initialization loops and hidden coupling that agents fail to debug. |
| **Cognitive Complexity Budget** | Cyclomatic complexity must not exceed a predetermined threshold (e.g., 10-15 paths) per function/module. | Ensures the agent's semantic reasoning capabilities are not overwhelmed during subsequent maintenance. |
| **Intent Verification** | Presence of a valid Architecture Decision Record (ADR) for any newly introduced framework, external service, or global state mechanism. | Prevents intent debt and ensures future sessions understand the rationale behind complex boundaries. |
| **Speculative Extensibility Score** | Detection of unused abstractions, empty interfaces, or uninstantiated abstract factories. | Enforces YAGNI by flagging code that exists purely for theoretical future requirements. |
| **Testability and Side-Effects** | Domain logic modules must not import I/O boundaries (e.g., database drivers, network fetchers) directly. | Ensures the architecture can be verified deterministically via fast, isolated unit tests. |

## **5\. Material Findings and Control Plane Implementation**

The following material findings define the precise interventions the global C:\\Users\\USERNAME\\.claude\\ control plane must implement to govern greenfield projects securely and reliably, utilizing the specific capabilities of Claude Code as of October 2026\.

### **Finding 1: Vertical Slice Enforcement via Static Dependency Checks**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Relying on prompt instructions to maintain architectural boundaries consistently fails. Architectural drift must be caught by static dependency checks running automatically after file writes to enforce vertical slice architecture. |
| **2\. Evidence/source** | 20 (Xebia, *Taking frontend architecture serious with dependency-cruiser*);18 (*Architecture Fitness Functions*);12 (*Agentic Codebase Principles*). |
| **3\. Evidence strength** | Strong. Broad industry consensus aligns with empirical modularity research. |
| **4\. Claude Code mechanism implicated** | PostToolUse hook combined with \`matcher: "Write |
| **5\. Global \~/.claude candidate?** | **Conditional**. The \~/.claude/settings.json file can globally mandate the execution of a fitness function runner, but the specific dependency rules must reside in the project-local directory. |
| **6\. Enforcement type** | Deterministic. A PostToolUse hook returning {"hookSpecificOutput": {"block": true}} or exit code 2 strictly prevents the agent from proceeding until the dependency violation is resolved31. |
| **7\. Cost/context implications** | Moderate local computational cost, but yields massive context savings by instantly truncating erroneous architectural paths before they compound. |
| **8\. Security implications** | Executing global hooks that invoke project-local binaries (like a node module linter) poses local execution vulnerabilities if the project dependencies are compromised. |
| **9\. Open question remaining** | Can a lightweight, language-agnostic dependency graph parser be safely embedded directly into the control plane to avoid reliance on external, potentially insecure toolchains? |

### **Finding 2: Mandatory ADR Generation for Intent Debt**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Autonomous agents must be forced to write Architecture Decision Records to prevent catastrophic intent debt; without them, context compaction permanently destroys design rationale, leading to future hallucinated rewrites. |
| **2\. Evidence/source** | 1 (Storey, 2026, *From Technical Debt to Cognitive and Intent Debt*);22 (*One Size Fits All? An Empirical Comparison of ADR Templates*);25 (Claude Code Docs, *Hooks*). |
| **3\. Evidence strength** | Strong. Supported by recent peer-reviewed empirical software engineering studies. |
| **4\. Claude Code mechanism implicated** | UserPromptSubmit hooks, PreToolUse hooks, and InstructionsLoaded events for .claude/rules/\*.md. |
| **5\. Global \~/.claude candidate?** | **Yes**. A global UserPromptSubmit hook can analyze the user's request for architectural triggers and deterministically append additionalContext forcing the agent to draft an ADR prior to coding. |
| **6\. Enforcement type** | Prompt-based (via injected context) combined with Deterministic checking. A PreToolUse hook targeting file creation can block massive structural changes if an associated ADR does not exist. |
| **7\. Cost/context implications** | Low cost. Reading ADRs consumes minor context but massively reduces hallucinated code rewriting over the project lifecycle, ultimately saving API tokens. |
| **8\. Security implications** | None directly, though ADRs serve as excellent locations to explicitly document security boundaries for the agent. |
| **9\. Open question remaining** | How can the control plane reliably differentiate between a user prompt warranting a formal ADR and a trivial feature iteration to avoid inducing needless bureaucratic ceremony? |

### **Finding 3: Cyclomatic Complexity Budgets**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Agent reliability degrades exponentially as code complexity increases. Cognitive complexity must be strictly budgeted and enforced to prevent the creation of unmaintainable god objects. |
| **2\. Evidence/source** | 13 (JAAFR, *Empirical Analysis of AI-Assisted Code Generation*);14 (*AI and Software Quality: The Wall of Cognitive Debt*);24 (*Economics of Software Architecture*). |
| **3\. Evidence strength** | Moderate. Represents emerging academic research on LLM processing limitations. |
| **4\. Claude Code mechanism implicated** | PreToolUse or PostToolUse command hooks utilizing BASH\_MAX\_OUTPUT\_LENGTH and local AST parsers. |
| **5\. Global \~/.claude candidate?** | **Yes**. A global \~/.claude/settings.json hook can automatically evaluate modified files against a complexity threshold script31. |
| **6\. Enforcement type** | Deterministic. The hook blocks the Edit tool by printing {"hookSpecificOutput": {"permissionDecision": "deny", "permissionDecisionReason": "Complexity budget exceeded. Refactor into smaller modules."}}32. |
| **7\. Cost/context implications** | Forces the agent to refactor immediately, consuming more tokens upfront but saving significant technical debt remediation tokens in subsequent sessions. |
| **8\. Security implications** | None. |
| **9\. Open question remaining** | Will strict complexity limits inadvertently induce the agent to create premature abstractions and unnecessary helper classes simply to bypass the function-level complexity check? |

### **Finding 4: Dynamic Workflows for Long-Horizon Tasks**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Monolithic agent sessions degrade severely over multi-hour time horizons. Complex greenfield features should be orchestrated via dynamic workflows that delegate subtasks to isolated subagents, preserving the primary context window. |
| **2\. Evidence/source** | 10 (Anthropic, *Effective context engineering for AI agents*);5 (*METR time horizon benchmarks*);34 (Claude Code Docs, *Dynamic Workflows*). |
| **3\. Evidence strength** | Strong. Anthropic official guidance aligns perfectly with independent benchmark failure data. |
| **4\. Claude Code mechanism implicated** | workflows/\*.js, ultracode setting, and agents/\*.md definitions. |
| **5\. Global \~/.claude candidate?** | **Yes**. The global \~/.claude/settings.json can define "ultracode": true to force the agent into automatic workflow orchestration for all substantive tasks34. |
| **6\. Enforcement type** | Architectural/Design configuration. |
| **7\. Cost/context implications** | Highly efficient context management. Subagents run in entirely isolated context windows, returning only summaries to the parent orchestrator, bypassing the METR degradation limit35. |
| **8\. Security implications** | Subagents can be strictly limited via disallowedTools in their YAML frontmatter, preventing a documentation-review subagent from accidentally executing destructive shell commands36. |
| **9\. Open question remaining** | Can a novice accurately review and approve the complex JavaScript orchestration scripts generated by the agent before they execute, or does this introduce cognitive overload? |

### **Finding 5: Native PowerShell Interoperability**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | For software engineering novices on Windows, reliance on Git Bash frequently causes environment and pathing execution failures. The control plane must seamlessly leverage native PowerShell while respecting OS execution policies. |
| **2\. Evidence/source** | 38 (Claude Code Docs, *Troubleshoot install*, *PowerShell tool*);40 (Claude Code Docs, *Environment Variables*). |
| **3\. Evidence strength** | Strong. Tier 1 authoritative documentation. |
| **4\. Claude Code mechanism implicated** | env configurations targeting CLAUDE\_CODE\_USE\_POWERSHELL\_TOOL, and BASH\_DEFAULT\_TIMEOUT\_MS. |
| **5\. Global \~/.claude candidate?** | **Yes**. Global \~/.claude/settings.json must configure "env": {"CLAUDE\_CODE\_USE\_POWERSHELL\_TOOL": "1"} to ensure native Windows cmdlet execution40. |
| **6\. Enforcement type** | Deterministic configuration. |
| **7\. Cost/context implications** | Eliminates significant context waste caused by the agent fruitlessly attempting to translate POSIX shell syntax into Windows environments. |
| **8\. Security implications** | Windows execution policies must be securely managed; utilizing Set-ExecutionPolicy RemoteSigned \-Scope CurrentUser enables hooks while mitigating the risk of executing untrusted external scripts38. |
| **9\. Open question remaining** | Documentation indicates that hooks spawn PowerShell directly on Windows regardless of the CLAUDE\_CODE\_USE\_POWERSHELL\_TOOL flag. Are there edge cases where global hooks written as POSIX shell scripts cause silent failures?25. |

### **Finding 6: Anti-Framework Guardrails via Permissions Deny**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Coding agents inherently default to speculative extensibility and complex frameworks seen in their training data. Greenfield projects require strict dependency limitation to enforce YAGNI principles. |
| **2\. Evidence/source** | 12 (*Agentic Codebase Principles*);43 (AntonDevTips, *Why most AI-generated code fails in production*). |
| **3\. Evidence strength** | Moderate. Represents strong practitioner consensus regarding LLM behavior. |
| **4\. Claude Code mechanism implicated** | permissions.deny arrays within settings.json. |
| **5\. Global \~/.claude candidate?** | **Conditional**. A global template should seed the project's .claude/settings.json with deny rules blocking heavily abstracted framework CLIs (e.g., Bash(npx create-react-app \*) or Bash(django-admin \*)) if a minimalist stack is designated. |
| **6\. Enforcement type** | Deterministic. Deny rules are evaluated strictly before ask or allow rules, instantly blocking the tool prior to execution44. |
| **7\. Cost/context implications** | Prevents massive context bloat by forcing the agent to rely on standard libraries or specifically designated minimalist modules. |
| **8\. Security implications** | Enhances supply chain security by drastically reducing the total dependency surface area. |
| **9\. Open question remaining** | How can the control plane balance strict YAGNI enforcement with the reality that certain established frameworks ultimately save context tokens by providing highly predictable, well-documented architectural patterns? |

### **Finding 7: Proactive Output Styles for Architectural Guidance**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | The default system prompt prioritizes generic software engineering completion. Novices require the agent to assume an expert architect persona capable of challenging poor assumptions rather than blindly implementing them. |
| **2\. Evidence/source** | 43 (*The human is the architect. Claude proposes, you decide.*);46 (Claude Code Docs, *Output Styles*). |
| **3\. Evidence strength** | Strong. Combines Tier 1 feature documentation with Tier 3 expert practice. |
| **4\. Claude Code mechanism implicated** | output-styles/\*.md definitions and the outputStyle global setting. |
| **5\. Global \~/.claude candidate?** | **Yes**. A custom style \~/.claude/output-styles/architecture-mentor.md can be globally enforced via "outputStyle": "architecture-mentor" in the user's \~/.claude/settings.json47. |
| **6\. Enforcement type** | Prompt-based. Output styles overwrite or append to system instructions. Utilizing keep-coding-instructions: true in the YAML frontmatter retains core coding capabilities while dramatically altering the agent's architectural behavior47. |
| **7\. Cost/context implications** | Results in a minor increase in system prompt tokens per turn, but effectively mitigates severe, costly architectural mistakes. |
| **8\. Security implications** | None. |
| **9\. Open question remaining** | Does a highly restrictive, pedantic architectural output style cause the underlying model to enter frustrating refusal loops on otherwise trivial coding requests? |

### **Finding 8: Lifecycle Environment Verification**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Agents routinely waste tokens attempting to execute code in uninitialized environments or missing dependency contexts, causing cascading errors that rapidly pollute the context window. |
| **2\. Evidence/source** | 11 (Anthropic, *Effective harnesses for long-running agents*);25 (Claude Code Docs, *Hooks Guide*). |
| **3\. Evidence strength** | Strong. Backed by Anthropic primary engineering research. |
| **4\. Claude Code mechanism implicated** | SessionStart and Setup lifecycle hooks. |
| **5\. Global \~/.claude candidate?** | **Yes**. Global hooks can systematically ensure necessary environment variables and project state are loaded before the agent assumes control. |
| **6\. Enforcement type** | Deterministic. SessionStart hooks executing shell commands feed environment context directly to Claude via stdout (e.g., verifying package manager status or current sprint objectives)31. |
| **7\. Cost/context implications** | Minimal context cost; powerfully prevents multi-turn hallucination regarding the state of the build environment. |
| **8\. Security implications** | Can be leveraged to securely verify or inject necessary API keys into the session environment without exposing them directly within the raw LLM prompt. |
| **9\. Open question remaining** | How can the system prevent SessionStart hooks from accumulating unbounded stdout context pollution over multiple session resumes? |

### **Finding 9: Preventing Tool Definition Bloat via MCP Code Execution**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Loading hundreds of tool definitions directly into the context window causes massive context exhaustion and severe latency. Agents scale far more efficiently by writing code to interact with Model Context Protocol (MCP) servers on-demand. |
| **2\. Evidence/source** | 49 (Anthropic, *Code execution with MCP: Building more efficient agents*). |
| **3\. Evidence strength** | Strong. Anthropic official engineering blog. |
| **4\. Claude Code mechanism implicated** | .mcp.json definitions and progressive disclosure implementation patterns. |
| **5\. Global \~/.claude candidate?** | **No**. MCP configurations are strictly project-local via .mcp.json unless explicitly deployed at the enterprise level50. |
| **6\. Enforcement type** | Architectural/Design configuration. |
| **7\. Cost/context implications** | Generates a major reduction in token costs and context processing latency by loading tool capabilities dynamically49. |
| **8\. Security implications** | While code execution mode isolates tool definitions, executing dynamically generated code requires strict OS-level or container sandboxing to prevent system compromise52. |
| **9\. Open question remaining** | Can progressive disclosure of complex MCP tools be fully automated such that a novice never has to manually configure search paths or detail levels? |

### **Finding 10: Centralized Governance via Managed Settings**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | To absolutely prevent novice overrides of critical safety mechanisms, project templates or organizations must utilize Managed Settings to lock down permissions, restrict hooks, and block unverified plugins. |
| **2\. Evidence/source** | 25 (Claude Code Docs, *Managed Settings*). |
| **3\. Evidence strength** | Strong. Tier 1 definitive documentation. |
| **4\. Claude Code mechanism implicated** | managed-settings.json, utilizing allowManagedHooksOnly and allowManagedPermissionRulesOnly keys. |
| **5\. Global \~/.claude candidate?** | **Yes**. Operates above standard user configuration files. |
| **6\. Enforcement type** | Deterministic. A managed-settings.json file on the filesystem outranks all user, project, local, and CLI flag settings, making its constraints immutable by the novice51. |
| **7\. Cost/context implications** | Zero direct context cost. |
| **8\. Security implications** | Extremely high security benefit. Prevents malicious plugins or prompt-injected agents from silently altering permissions.allow or disabling protective fitness function hooks51. |
| **9\. Open question remaining** | Is deploying a managed-settings.json file too frictionless for a novice operating individually, creating a high risk of accidental, difficult-to-debug local lock-out? |

### **Finding 11: Auto Memory and Strategic Context Management**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Allowing agents to endlessly accumulate context pollutes their reasoning capabilities. Strategic memory management, utilizing deterministic path scoping and auto-compaction, is essential to maintain agent focus. |
| **2\. Evidence/source** | 10 (Anthropic, *Effective context engineering for AI agents*);42 (Claude Code Docs, *Memory*). |
| **3\. Evidence strength** | Strong. |
| **4\. Claude Code mechanism implicated** | autoMemoryEnabled, autoMemoryDirectory, and path-scoped .claude/rules/\*.md. |
| **5\. Global \~/.claude candidate?** | **Yes**. Global settings can configure the autoMemoryDirectory to centralize organizational learnings, while autoCompactEnabled manages immediate session bloat42. |
| **6\. Enforcement type** | Deterministic configuration. Utilizing YAML frontmatter paths in .claude/rules/\*.md ensures instructions only load when the agent touches relevant files, preserving the token budget56. |
| **7\. Cost/context implications** | Directly mitigates the exponential cost of expanding context windows by ensuring only locally relevant rules and compacted memory are loaded. |
| **8\. Security implications** | None directly. |
| **9\. Open question remaining** | How does auto memory distinguish between temporary debugging workarounds and permanent architectural learnings that should be persisted across all future sessions? |

### **Finding 12: Experimental Agent Hooks for Complex Condition Verification**

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | Traditional shell command hooks lack the semantic understanding to evaluate complex codebase states. Experimental Agent Hooks allow the control plane to spawn subagents specifically to verify architectural conditions before approving actions. |
| **2\. Evidence/source** | 31 (Claude Code Docs, *Hooks Guide*). |
| **3\. Evidence strength** | Moderate. The feature is documented as strictly experimental and subject to change58. |
| **4\. Claude Code mechanism implicated** | Hook configuration utilizing type: "agent" instead of type: "command". |
| **5\. Global \~/.claude candidate?** | **Yes**. Global agent hooks can enforce deep semantic policies across all projects. |
| **6\. Enforcement type** | Deterministic (via LLM reasoning). The hook spawns an isolated subagent with tools like Read, Grep, and Glob to verify conditions, returning a concrete decision (allow/deny) to the primary orchestrator32. |
| **7\. Cost/context implications** | High token cost and execution latency, as a separate agent session must be spun up and execute tool calls before the primary hook resolves. |
| **8\. Security implications** | The verifying agent runs in isolation, providing a secure secondary check against prompt injections attempting to bypass architectural rules. |
| **9\. Open question remaining** | Is the latency introduced by spawning a secondary LLM agent on every PreToolUse event acceptable for a fluid development experience? |

## **6\. Conclusions and Strategic Directives**

### **A. Design Requirements Derived from the Evidence**

Based on the empirical evidence and verified Claude Code mechanisms, the eventual control plane must adhere to the following architecture and lifecycle requirements for greenfield projects:

> 1. **Global vs. Local Separation of Concerns:**  
   * **Global Level (C:\\Users\\USERNAME\\.claude\\):** Must contain generalized enforcement logic, including settings.json configured for CLAUDE\_CODE\_USE\_POWERSHELL\_TOOL: 1, global proactive output-styles, and generic PreToolUse hooks utilizing BASH\_MAX\_OUTPUT\_LENGTH to intercept and evaluate cyclomatic complexity thresholds.  
   * **Local Level (.claude/):** Must contain domain-specific constraints, including permissions.deny lists blocking non-approved frameworks, dynamic workflows (workflows/\*.js), and project-specific dependency-cruiser configurations enforcing Vertical Slice boundaries.  
> 2. **Mandatory Intent Tracking (ADRs):**  
   * The control plane must deploy a UserPromptSubmit or PreToolUse hook that identifies structural additions. It must deterministically block execution via exit 2 or permissionDecision: "deny", feeding a permissionDecisionReason that forces the agent to write a .claude/rules/adr-00X.md file detailing its intent before generating code.  
> 3. **Automated Fitness Function Integration:**  
   * A PostToolUse hook must trigger static architecture validation on every file Write|Edit. If the agent's code violates dependency boundaries (e.g., importing an external API driver directly into a core domain model), the hook must return an error to Claude's context, forcing an immediate refactor before the task is marked complete.  
> 4. **Long-Horizon Delegation via Dynamic Workflows:**  
   * For tasks exceeding simple feature iterations, the control plane must configure "ultracode": true or instruct the agent to utilize Dynamic Workflows. This forces the agent into an orchestrator role, delegating specific implementation tasks to isolated subagents restricted by disallowedTools, preserving the primary context window and mitigating METR-documented degradation.

### **B. Anti-Requirements — What the Control Plane Should NOT Do**

To ensure the control plane remains effective and does not create needless ceremony or dangerous security vectors, it must rigorously avoid the following:

> 1. **Do Not Rely on Prompt-Based Governance:**  
   * CLAUDE.md is behavioral and probabilistic. It must never be used to enforce hard architectural constraints (e.g., "Do not use React"). All mandatory constraints must be encoded as deterministic hooks or permissions.deny rules.  
> 2. **Do Not Enforce Heavy Horizontal Layering:**  
   * The control plane must not enforce Clean Architecture, N-Tier, or heavily abstracted interfaces (such as generic repository patterns) on greenfield projects. This artificially inflates cyclomatic complexity and context bloat, leading directly to agent reasoning failure. Vertical Slice Architecture must be the default.  
> 3. **Do Not Expose Novices to Unbounded Auto Mode on Destructive Tools:**  
   * While defaultMode: "auto" is helpful for velocity, the control plane must not bypass fitness functions. The dontAsk or bypassPermissions modes must be strictly avoided for core architectural changes to maintain human-in-the-loop oversight.  
> 4. **Do Not Accumulate Global Context Pollution:**  
   * Hooks like PostToolUse must not return massive AST dumps or verbose linter outputs via additionalContext. additionalContext is strictly capped at 10,000 characters and becomes stale upon session resume. Summarized, actionable violations must be returned instead.

### **C. Unresolved Questions**

> 1. **Subagent Discovery vs. Configuration Overhead:** While Vertical Slices mapped to isolated subagents provide the strongest protection against context pollution, it remains unclear how a complete novice can dynamically generate these agents/\*.md definitions without spending more time configuring the agent's environment than actually generating software.  
> 2. **The "Vibe Coding" Paradox:** Novices naturally gravitate toward vague, natural language prompts. If the control plane strictly enforces ADRs, fitness functions, and complexity budgets, it may create intense friction, leading novices to abandon the safety plane entirely. Balancing strict architectural governance with novice UX is a major Human-Computer Interaction challenge.  
> 3. **Evolution of the METR Horizon:** As frontier models scale rapidly, the 50% success time horizon is increasing exponentially. If models soon achieve 40-hour reliable horizons, strict subagent isolation may become computationally unnecessary, though Intent Debt—the need for explicit ADRs—will persist indefinitely due to the requirements of human maintainability.

### **D. Sources**

> 1. \[cite: 25, 31, 58\] Claude Code Docs: Hooks Guide & Reference (code.claude.com/docs). Updated: \~2026.  
> 2. \[cite: 50\] Claude Code Docs: Claude Directory (code.claude.com/docs). Updated: \~2026.  
> 3. \[cite: 10, 11, 49\] Anthropic Engineering Blog: Effective Context Engineering, Long-running Agents, MCP Code Execution (anthropic.com/engineering). Updated: 2024-2026.  
> 4. \[cite: 1, 2\] Storey, M.A., et al. (2026). "From Technical Debt to Cognitive and Intent Debt: Rethinking Software Health in the Age of AI". arXiv/ResearchGate.  
> 5. \[cite: 13, 14\] JAAFR & Sogeti Labs (2026). "Empirical Analysis of AI-Assisted Code Generation" / "The Wall of Cognitive Debt".  
> 6. \[cite: 44, 59, 60\] Claude Code Docs: Agent SDK (Hooks, Permissions, Typescript). Updated: \~2026.  
> 7. \[cite: 52\] Claude Code Docs: Sandboxing (code.claude.com/docs). Updated: \~2026.  
> 8. \[cite: 18, 19, 20, 21\] Xebia, ArchUnitTS, PlatformToolSmith: Architecture Fitness Functions, Dependency-Cruiser. Updated: \~2026.  
> 9. \[cite: 12, 29\] Martin Fowler / Maintainable Software: Sensors for Coding Agents, Agentic Codebase Principles. Updated: \~2026.  
> 10. \[cite: 36, 37\] Claude Code Docs: Sub-agents (code.claude.com/docs). Updated: \~2026.  
> 11. \[cite: 12, 15, 61, 62\] ResearchGate / CSA / Maintainable Software: Vertical Slice Architecture vs. Clean Architecture. Updated: \~2026.  
> 12. \[cite: 4, 22, 23, 24\] arXiv / Simplicity First: Empirical Comparison of ADRs, Economics of Software Architecture. Updated: \~2026.  
> 13. \[cite: 16\] EAPJ: De-Siloing Enterprise Architecture (Conway's Law & Technical Debt). Updated: \~2026.  
> 14. 38 Claude Code Docs: Troubleshoot Install & PowerShell Tool. Updated: \~2026.  
> 15. \[cite: 40, 41, 42\] Claude Code Docs: Environment Variables & Changelog. Updated: \~2026.  
> 16. \[cite: 24, 26, 30\] Simplicity First / Abstractopedia: Complexity Budgets & Incremental Design Review. Updated: \~2026.  
> 17. \[cite: 5, 6, 7, 8, 9\] METR (Model Evaluation and Threat Research): Task-Completion Time Horizons of Frontier AI Models. Updated: 2025-2026.  
> 18. \[cite: 25, 51, 53, 54, 55\] Claude Code Docs: Managed Settings & Admin Setup. Updated: \~2026.  
> 19. \[cite: 3\] Levi9: Cognitive Debt Is the New Technical Debt. Updated: \~2026.  
> 20. \[cite: 25, 42, 56, 57\] Claude Code Docs: Memory & Rules. Updated: \~2026.  
> 21. \[cite: 45, 63\] Claude Code Docs: Permission Modes. Updated: \~2026.  
> 22. 43 AntonDevTips: Why most AI-generated code fails in production. Updated: \~2026.  
> 23. \[cite: 32, 33\] Pushary / Thomas Wiegold: Claude Code Hooks Explained. Updated: \~2026.  
> 24. \[cite: 46, 47, 48\] Claude Code Docs: Output Styles. Updated: \~2026.  
> 25. \[cite: 34, 35\] Claude Code Docs: Dynamic Workflows. Updated: \~2026.

#### **Works cited**

> 1. (PDF) From Technical Debt to Cognitive and Intent Debt: Rethinking, [https\://www\.researchgate.net/publication/403071950\_From\_Technical\_Debt\_to\_Cognitive\_and\_Intent\_Debt\_Rethinking\_Software\_Health\_in\_the\_Age\_of\_AI](https://www.researchgate.net/publication/403071950_From_Technical_Debt_to_Cognitive_and_Intent_Debt_Rethinking_Software_Health_in_the_Age_of_AI)  
> 2. Towards Automated Domain Model Extraction from Source Code, [https\://arxiv.org/html/2608.12228v1](https://arxiv.org/html/2608.12228v1)  
> 3. When AI Agents Join the Team: AI-Assisted Development in Practice, [https\://www\.levi9.rs/article/when-ai-agents-join-the-team-ai-assisted-development-in-practice/](https://www.levi9.rs/article/when-ai-agents-join-the-team-ai-assisted-development-in-practice/)  
> 4. risk-driven model \- ️ l-lin, [https\://l-lin.github.io/architecture/just-enough-architecture/risk-driven-model](https://l-lin.github.io/architecture/just-enough-architecture/risk-driven-model)  
> 5. Agents struggle with long-horizon tasks \- AI 2027 Tracker, [https\://ai2027-tracker.com/predictions/long-horizon-struggle/](https://ai2027-tracker.com/predictions/long-horizon-struggle/)  
> 6. Measuring AI Ability to Complete Long Software Tasks \- arXiv, [https\://arxiv.org/html/2503.14499v3](https://arxiv.org/html/2503.14499v3)  
> 7. Task-Completion Time Horizons of Frontier AI Models \- METR, [https\://metr.org/time-horizons/](https://metr.org/time-horizons/)  
> 8. Measuring AI Ability to Complete Long Software Tasks \- METR, [https\://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)  
> 9. MirrorCode: METR and EpochAI's week-long coding benchmark., [https\://medium.com/@AIchats/mirrorcode-metr-and-epochais-week-long-coding-benchmark-e6fe3f09f4fe](https://medium.com/@AIchats/mirrorcode-metr-and-epochais-week-long-coding-benchmark-e6fe3f09f4fe)  
> 10. Effective context engineering for AI agents \- Anthropic, [https\://www\.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
> 11. Effective harnesses for long-running agents \- Anthropic, [https\://www\.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)  
> 12. How to Design a Maintainable Codebase for AI Coding Agents, [https\://maintainable.software/agentic-engineering-part-2-agentic-codebase-principles/](https://maintainable.software/agentic-engineering-part-2-agentic-codebase-principles/)  
> 13. Empirical Analysis of LLM Performance in Automated Code, [https\://rjwave.org/jaafr/papers/JAAFR2605811.pdf](https://rjwave.org/jaafr/papers/JAAFR2605811.pdf)  
> 14. AI and Software Quality \- Sogeti Labs, [https\://labs.sogeti.com/ai-and-software-quality-the-speed-illusion-against-the-wall-of-cognitive-debt/](https://labs.sogeti.com/ai-and-software-quality-the-speed-illusion-against-the-wall-of-cognitive-debt/)  
> 15. Architectures in Comparison: Onion or Vertical Slice?, [https\://www\.csa.ch/en/blog/architectures-in-comparison-onion-or-vertical-slice](https://www.csa.ch/en/blog/architectures-in-comparison-onion-or-vertical-slice)  
> 16. De-Siloing Enterprise HR Technology, [https\://eapj.org/de-siloing-enterprise-hr-technology/](https://eapj.org/de-siloing-enterprise-hr-technology/)  
> 17. Operationalizing ADRs with Automated Fitness Functions, [https\://platformtoolsmith.com/blog/operationalizing-adrs-fitness-functions/](https://platformtoolsmith.com/blog/operationalizing-adrs-fitness-functions/)  
> 18. The Modular Monolith 2026 Complete Guide — Spring Modulith, [https\://dev.to/x4nent/the-modular-monolith-2026-complete-guide-spring-modulith-archunit-fitness-functions-and-lessons-878](https://dev.to/x4nent/the-modular-monolith-2026-complete-guide-spring-modulith-archunit-fitness-functions-and-lessons-878)  
> 19. Architecture Fitness Functions Guide | CodeIntelligently, [https\://codeintelligently.com/blog/architecture-fitness-functions-testing](https://codeintelligently.com/blog/architecture-fitness-functions-testing)  
> 20. Taking Frontend Architecture Serious With Dependency-cruiser, [https\://xebia.com/blog/taking-frontend-architecture-serious-with-dependency-cruiser/](https://xebia.com/blog/taking-frontend-architecture-serious-with-dependency-cruiser/)  
> 21. ArchUnitTS \- v2.5.3, [https\://lukasniessen.github.io/ArchUnitTS/](https://lukasniessen.github.io/ArchUnitTS/)  
> 22. One Size Fits All? An Empirical Comparison of ADR Templates, [https\://arxiv.org/pdf/2604.27333](https://arxiv.org/pdf/2604.27333)  
> 23. Integrating TOGAF ADM, ArchiMate, and Scrum to Align Enterprise, [https\://www\.preprints.org/manuscript/202607.1837](https://www.preprints.org/manuscript/202607.1837)  
> 24. Economics of Software Architecture \- Simplicity-First, [https\://simplicity-first.dev/docs/Economics\_of\_Software\_Architecture\_Digital.pdf](https://simplicity-first.dev/docs/Economics_of_Software_Architecture_Digital.pdf)  
> 25. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 26. BEFORE LAUNCH: A Design-Stage Systems Engineering Doctrine, [https\://www\.tdcommons.org/cgi/viewcontent.cgi?article=13251\&context=dpubs\_series](https://www.tdcommons.org/cgi/viewcontent.cgi?article=13251&context=dpubs_series)  
> 27. Earned Complexity: A Disciplined, Evidence-Based Framework, [https\://dev.to/grantwatsondev/earned-complexity-a-disciplined-evidence-based-framework-54pn](https://dev.to/grantwatsondev/earned-complexity-a-disciplined-evidence-based-framework-54pn)  
> 28. Architectural Fitness Functions: An intro to building evolutionary, [https\://medium.com/yonder-techblog/architectural-fitness-functions-an-intro-to-building-evolutionary-architectures-dc529ac76351](https://medium.com/yonder-techblog/architectural-fitness-functions-an-intro-to-building-evolutionary-architectures-dc529ac76351)  
> 29. Maintainability sensors for coding agents \- Martin Fowler, [https\://martinfowler.com/articles/sensors-for-coding-agents.html](https://martinfowler.com/articles/sensors-for-coding-agents.html)  
> 30. Incremental Design Review \- The Encyclopedia of Abstractions, [https\://abstractopedia.org/mechanisms/incremental\_design\_review/](https://abstractopedia.org/mechanisms/incremental_design_review/)  
> 31. Automate actions with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
> 32. Claude Code hooks explained: PreToolUse, PostToolUse, and Stop, [https\://pushary.com/blog/claude-code-hooks-explained](https://pushary.com/blog/claude-code-hooks-explained)  
> 33. Claude Code Hooks: From Linting to Hardened AI Workflows, [https\://thomas-wiegold.com/blog/claude-code-hooks/](https://thomas-wiegold.com/blog/claude-code-hooks/)  
> 34. Orchestrate subagents at scale with dynamic workflows, [https\://code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows)  
> 35. 使用动态工作流大规模编排子代理- Claude Code Docs, [https\://code.claude.com/docs/zh-CN/workflows](https://code.claude.com/docs/zh-CN/workflows)  
> 36. Subagents in the SDK \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)  
> 37. Create custom subagents \- Claude Code Docs, [https\://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
> 38. Troubleshoot installation and login \- Claude Code Docs, [https\://code.claude.com/docs/en/troubleshoot-install](https://code.claude.com/docs/en/troubleshoot-install)  
> 39. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 40. Environment variables \- Claude Code Docs, [https\://code.claude.com/docs/en/env-vars](https://code.claude.com/docs/en/env-vars)  
> 41. Week 21 · May 18–22, 2026 \- Claude Code Docs, [https\://code.claude.com/docs/en/whats-new/2026-w21](https://code.claude.com/docs/en/whats-new/2026-w21)  
> 42. All settings \- Claude Code Docs, [https\://code.claude.com/docs/en/settings-reference](https://code.claude.com/docs/en/settings-reference)  
> 43. How to Build Production-Ready Projects With Claude Code, [https\://antondevtips.com/blog/how-to-build-production-ready-projects-with-claude-code](https://antondevtips.com/blog/how-to-build-production-ready-projects-with-claude-code)  
> 44. Configure permissions \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/permissions](https://code.claude.com/docs/en/agent-sdk/permissions)  
> 45. Choose a permission mode \- Claude Code Docs, [https\://code.claude.com/docs/en/permission-modes](https://code.claude.com/docs/en/permission-modes)  
> 46. Modifying system prompts \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/modifying-system-prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts)  
> 47. Output styles \- Claude Code Docs, [https\://code.claude.com/docs/en/output-styles](https://code.claude.com/docs/en/output-styles)  
> 48. Output styles \- Claude Code Docs, [https\://code.claude.com/docs/it/output-styles](https://code.claude.com/docs/it/output-styles)  
> 49. Code execution with MCP: building more efficient AI agents \- Anthropic, [https\://www\.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)  
> 50. Explore the .claude directory \- Claude Code Docs, [https\://code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory)  
> 51. Deploy managed settings \- Claude Code Docs, [https\://code.claude.com/docs/en/managed-settings](https://code.claude.com/docs/en/managed-settings)  
> 52. Configure the sandboxed Bash tool \- Claude Code Docs, [https\://code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing)  
> 53. Set up Claude Code for your organization, [https\://code.claude.com/docs/en/admin-setup](https://code.claude.com/docs/en/admin-setup)  
> 54. Settings files and precedence \- Claude Code Docs, [https\://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
> 55. Claude apps gateway for Amazon Bedrock, Claude Platform on, [https\://code.claude.com/docs/en/claude-apps-gateway](https://code.claude.com/docs/en/claude-apps-gateway)  
> 56. How Claude remembers your project \- Claude Code Docs, [https\://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)  
> 57. Claude code docs map, [https\://code.claude.com/docs/en/claude\_code\_docs\_map](https://code.claude.com/docs/en/claude_code_docs_map)  
> 58. Hooks 参考- Claude Code Docs, [https\://code.claude.com/docs/zh-CN/hooks](https://code.claude.com/docs/zh-CN/hooks)