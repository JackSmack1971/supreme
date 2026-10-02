# **Engineering Research Report: Production-Quality Global Claude Code Control Plane Architecture**

The rapid maturation of agentic artificial intelligence and the deployment of general-purpose coding assistants necessitate the design of structured control planes. As software engineering paradigms shift from manual authoring to AI-driven orchestration, unconstrained large language model (LLM) agents exhibit catastrophic failure modes over long-running tasks. These include context pollution, sycophantic validation, and exponential token cost scaling1.  
This research delineates the architectural requirements for a robust, production-quality global control plane localized at the C:\\Users\\USERNAME\\.claude\\ directory. The system is designed to shepherd projects from inception to sustained maintenance on behalf of novice users. It achieves this by abstracting the complexities of deterministic enforcement, multi-agent coordination, git worktree isolation, and token-budget management, translating raw frontier model capabilities into reliable software engineering outcomes.

## **Material Findings and Empirical Analysis**

The formulation of a global control plane requires separating foundational agent behaviors from deterministic environmental constraints. The following material findings synthesize authoritative documentation, empirical research on SWE-bench trajectories, and advanced harness designs to establish the operational mechanics of the control plane.  
The analysis explicitly challenges universal application assumptions—such as those hypothesized in legacy frameworks like JackSmack1971/supreme—by rigorously evaluating the conditions under which multi-agent routing, Test-Driven Development (TDD), and architectural decision records (ADRs) become token-wasting liabilities rather than assets.

### **Mitigating Evaluator Sycophancy Through Context Isolation**

The evaluation of multi-agent interactions reveals critical vulnerabilities in LLM consensus mechanisms. When an evaluator agent is exposed to a builder agent's chain of thought or prior conversational trajectory, the evaluator inherently suffers from confirmation bias and sycophancy2. Empirical studies testing LLM-based code review demonstrate that models frequently echo the builder's logic, with up to 52.8% of incomplete reviews explicitly claiming complete task coverage4. This effect is present in a majority of production deployments and can only be mitigated by utilizing an independent evaluator operating in a fresh context window that has never seen the builder's reasoning5.  
Furthermore, providing an evaluator with file modification permissions introduces a secondary failure mode where the evaluator introduces novel hallucinations while attempting to patch the builder's code. Therefore, the evaluator must be strictly read-only, structurally incapable of modifying the codebase.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | LLM evaluators exhibit severe sycophancy; they must operate in isolated, fresh context windows with read-only permissions to provide objective code review. |
| **Evidence/Source** | "Challenging the evaluator: LLM sycophancy under user rebuttal" (arXiv:2603.18740); Anthropic: "Harness design for long-running application development"2. |
| **Evidence Strength** | Strong (Corroborated by empirical SWE-bench testing and Anthropic harness engineering). |
| **Implicated Mechanism** | Subagent architecture (.claude/agents/), Agent tool restrictions (disallowedTools). |
| **Global Candidate?** | Yes. The global control plane must provide a built-in evaluator subagent definition. |
| **Enforcement Strategy** | Deterministic (Subagent tool restriction) and Prompt-based (System prompt directing strict verification). |
| **Cost & Context** | Moderately increases token costs by requiring a separate LLM call, but drastically reduces overall costs by preventing spiraling failure loops and context bloat. |
| **Security Impact** | Prevents supply-chain attacks or malicious code injections that a sycophantic reviewer would otherwise approve2. |
| **Open Question** | What is the optimal temperature and top-p configuration to maximize skepticism in the evaluator without inducing false-positive rejections? |

### **The Default-FAIL Contract for Task Verification**

Coding agents frequently declare victory prematurely, especially when visual UI components or complex backend logic appear superficially correct to the model's spatial reasoning. Anthropic's long-running agent experiments demonstrate that asking an agent nicely in the prompt to verify its work does not reliably prevent premature termination5.  
Enforcing a "Default-FAIL contract" makes task completion structural rather than behavioral. By initializing all required features in a structured file (e.g., test-results.json) to false, the control plane forces the agent to generate verifiable evidence before marking a task complete. This replaces the brittle hypothesis of universal TDD (where LLMs often write flawed tests to pass their own flawed code) with a deterministic verification gate that the agent cannot bypass via hallucination.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Agents require a structural Default-FAIL contract to prevent premature task completion, overriding prompt-based requests for diligence. |
| **Evidence/Source** | Anthropic GitHub cwc-long-running-agents repository; "Learn Harness Engineering" curriculum5. |
| **Evidence Strength** | Strong (Demonstrated in Anthropic's million-line codebase experiments). |
| **Implicated Mechanism** | PostToolUse hooks matching testing/execution tools, or Agent SDK Stop callbacks. |
| **Global Candidate?** | Yes. The harness logic can be deployed globally to enforce strict state transitions across all projects. |
| **Enforcement Strategy** | Deterministic (Shell scripts or Python validators verifying the contract file before allowing the Stop event). |
| **Cost & Context** | High token efficiency. It prevents the model from hallucinating success, averting the need for human intervention and manual rollbacks. |
| **Security Impact** | Ensures that all deployed code has passed a rigid validation barrier, preventing the deployment of untested execution paths. |
| **Open Question** | How can a complete software-engineering novice define the criteria for the verification contract without understanding unit testing frameworks? |

### **Diff-Based Editing Radically Outperforms Full-File Generation**

Token consumption and the probability of introducing regression errors scale proportionally with the number of generated tokens. The AgentForge empirical analysis proves that for a file of length ![][image1] and an edit size ![][image2], diff-based editing incurs ![][image3] tokens, whereas full-file generation incurs ![][image4] tokens10.  
When general-purpose agents rewrite entire files, they frequently drop critical security configurations, imports, or unrelated logic due to context-window attention degradation. Utilizing targeted tools (like Claude Code's Edit tool or sed-based patching) over complete file rewrites (Write) is critical for performance and cost. The control plane must override any default behavior that prefers full-file replacement.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Diff-based editing (![][image3]) radically outperforms full-file generation (![][image4]) in both token cost and regression avoidance. |
| **Evidence/Source** | "AgentForge" empirical paper (arXiv:2604.13120v1)10. |
| **Evidence Strength** | Strong (Mathematical proof and SWE-bench Lite validation). |
| **Implicated Mechanism** | Tool configuration (Edit vs Write tools in permissions schema). |
| **Global Candidate?** | Yes. The control plane should globally preference the Edit tool while aggressively limiting the Write tool for existing files. |
| **Enforcement Strategy** | Deterministic (via PreToolUse hooks that reject Write operations on files exceeding a specific line count). |
| **Cost & Context** | Massive reduction in output token generation, minimizing latency and API expenditure. |
| **Security Impact** | Reduces the surface area for accidental deletion of security configurations during large file rewrites. |
| **Open Question** | At what file size threshold does the LLM's spatial reasoning break down when using unified diffs, necessitating a full file read? |

### **Git Worktree Isolation Enables Safe Parallel Execution**

Parallel agentic work on a single repository leads to catastrophic file collisions. Claude Code currently supports git worktree isolation (.claude/worktrees/), providing each subagent or background session a separate checkout branch branched from HEAD11.  
This mechanism enables the concurrent execution of features, testing, and reviews without corrupting the novice user's primary working directory. However, worktree creation defaults to isolating everything, meaning .env files and ignored secrets are not carried over automatically unless a .worktreeinclude file is configured11. The control plane must manage this configuration silently to ensure agents have the necessary environment variables to run local tests.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Git worktree isolation is required to prevent file collisions during parallel agent execution, but requires explicit dotfile management. |
| **Evidence/Source** | Claude Code official documentation: Worktrees, Agent Teams11. |
| **Evidence Strength** | Strong (CURRENTLY SUPPORTED, Tier 1 documentation). |
| **Implicated Mechanism** | EnterWorktree tool, \--worktree CLI flag, subagent YAML frontmatter (isolation: worktree). |
| **Global Candidate?** | Conditional. Worktree handling (e.g., .worktreeinclude files carrying .env secrets) must be project-local to avoid global credential leakage. |
| **Enforcement Strategy** | Deterministic (Configuration file deployment). |
| **Cost & Context** | Increases local disk I/O, but enables parallel model inference, drastically reducing wall-clock time for complex builds. |
| **Security Impact** | Isolates untrusted agent-generated code from the main working directory, providing a sandbox that can be forcefully discarded. |
| **Open Question** | How seamlessly can a novice user resolve merge conflicts if parallel worktrees modify adjacent code blocks simultaneously? |

### **Context Duplication Wastes Substantial Token Budgets**

In long-running software engineering trajectories, up to 14.5% of observation spans are exact duplicates, unnecessarily bloating the context window and degrading the LLM's retrieval accuracy3. Naive truncation, where the oldest messages are dropped, discards critical instructions and architectural decisions, meaning context must be actively managed via structured note-taking and state-file handoffs14.  
Claude Code implements a compact event during context exhaustion. The control plane must utilize SessionStart hooks matching this event to re-inject critical context, ensuring that the agent does not lose its operational mandate while discarding redundant shell execution logs.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Agent trajectories suffer from severe context duplication (up to 14.5%); aggressive compaction and state re-injection are mandatory. |
| **Evidence/Source** | Empirical research on SWE-bench trajectories3; Anthropic "Effective context engineering for AI agents"14. |
| **Evidence Strength** | Strong (Measured via tiktoken proxies on public corpora). |
| **Implicated Mechanism** | SessionStart hooks with a compact matcher; markdown memory files. |
| **Global Candidate?** | Yes. Global hooks can dictate a standard memory summarization and re-injection protocol across all projects. |
| **Enforcement Strategy** | Prompt-based (LLM summarization) combined with Deterministic (file read/writes). |
| **Cost & Context** | Highly favorable. Keeps context informative yet tight, preserving the token budget for reasoning rather than redundant memory recall. |
| **Security Impact** | Tighter contexts reduce the risk of prompt injection payloads lingering in long conversational histories. |
| **Open Question** | What is the optimal token threshold to trigger an aggressive compaction cycle without losing the thread of the current debugging task? |

### **Agent Teams are Computationally Inefficient for Sequential Software Engineering**

The "Agent Teams" feature in Claude Code allows multiple sessions to act as a coordinated group, sharing a task list, claiming work, and messaging each other directly. However, official guidance explicitly states that Agent Teams add severe coordination overhead and utilize significantly more tokens than single sessions or standard subagents16.  
This directly refutes the hypothesis that universal multi-agent routing is optimal. For sequential tasks, same-file edits, or routine programming work, Agent Teams are highly inefficient. The control plane must treat this feature as an anti-pattern for standard novice workflows.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | The Agent Teams feature introduces massive token bloat and coordination overhead, rendering it ineffective for sequential software engineering tasks. |
| **Evidence/Source** | Claude Code official documentation: Agent Teams16. |
| **Evidence Strength** | Strong (Tier 1 documentation, explicitly labeled EXPERIMENTAL and disabled by default). |
| **Implicated Mechanism** | CLAUDE\_CODE\_EXPERIMENTAL\_AGENT\_TEAMS=1 environment variable, Agent tool name passing. |
| **Global Candidate?** | No. The control plane should actively suppress this environment variable for standard novice workflows. |
| **Enforcement Strategy** | Deterministic (Environment variable override). |
| **Cost & Context** | Disabling Agent Teams prevents novices from accidentally burning massive token budgets on redundant inter-agent chatter. |
| **Security Impact** | Limits emergent, unpredictable agent behaviors that are difficult to trace and audit1. |
| **Open Question** | Are there specific multi-repository architectural refactors where Agent Teams overcome their inherent token inefficiencies? |

### **Subagent Specialization Requires Explicit Tool Restriction**

Delegating to subagents is only effective when the subagent possesses a tailored system prompt and restricted tools. Providing a generic subagent with full Bash and Write access defeats the purpose of modularity, violates the principle of least privilege, and risks context pollution13.  
A documentation-reviewer subagent, for example, must be deterministically limited to Read and Grep tools. If it discovers a syntax error during review, it must not possess the ability to fix it; rather, it must report the error back to the primary agent. The control plane must supply a library of strictly gated subagents for the novice user.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Subagents require deterministic tool stripping to prevent blast-radius expansion and enforce modularity. |
| **Evidence/Source** | Claude Code official documentation: Subagents, Tools Reference13. |
| **Evidence Strength** | Strong (CURRENTLY SUPPORTED). |
| **Implicated Mechanism** | .claude/agents/\*.md YAML frontmatter (tools and disallowedTools). |
| **Global Candidate?** | Yes. A suite of pre-configured, heavily restricted global subagents should reside in \~/.claude/agents/18. |
| **Enforcement Strategy** | Deterministic (Tool gating via YAML frontmatter). |
| **Cost & Context** | Prevents agents from executing expensive, irrelevant tools during narrow tasks. |
| **Security Impact** | Enforces strict blast-radius constraints, ensuring a research subagent cannot accidentally execute a destructive shell command. |
| **Open Question** | How should the global control plane handle dynamic tool discovery (MCP servers) when generating tool restrictions for legacy subagents? |

### **Managed Settings Guarantee Immutable Policy Enforcement**

To prevent agent logic or novice user error from overriding safety boundaries, critical configurations must be placed in managed-settings.json. This tier sits at the absolute top of the precedence stack, overriding user (\~/.claude/settings.json), project, and local settings19.  
While a local control plane is typically deployed in the user's home directory, true immutability on Windows requires deploying the policy to C:\\Program Files\\ClaudeCode\\managed-settings.json, and via HKLM registry keys rather than HKCU. This guarantees that parameters like allowManagedPermissionRulesOnly cannot be bypassed by an agent modifying the project-local configuration20.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Immutable security policies and model restrictions must be deployed via OS-level managed settings to prevent agent or user bypass. |
| **Evidence/Source** | Claude Code official documentation: Managed Settings, Precedence19. |
| **Evidence Strength** | Strong (CURRENTLY SUPPORTED). |
| **Implicated Mechanism** | OS-level managed-settings.json and HKLM registry keys. |
| **Global Candidate?** | Conditional. While \~/.claude/ is the user global directory, strict immutability requires the OS-level system paths. |
| **Enforcement Strategy** | Deterministic (Configuration precedence hierarchy). |
| **Cost & Context** | Negligible inference cost, but critical for organizational cost-control (e.g., pinning availableModels to prevent usage of expensive tiers). |
| **Security Impact** | Paramount. It is the only mechanism that securely enforces allowManagedPermissionRulesOnly and blocks unverified MCP plugins20. |
| **Open Question** | Does deploying managed-settings.json on a personal novice machine introduce unacceptable friction when the user attempts legitimate privilege escalation? |

### **Dynamic Workflows Outperform Autonomous Routing for Known Domains**

Relying on an LLM's turn-by-turn judgment to route tasks often leads to inefficient tool loops and hallucinated workflows. Dynamic workflows—where a deterministic script holds the execution plan and invokes subagents sequentially or in parallel—provide superior reliability for standardized pipelines1.  
The hypothesis that agents must autonomously decide their own architecture for every task is fundamentally flawed. Standardized processes like CI/CD validation, test suite execution, and dependency updates should be relegated to deterministic shell scripts that invoke claude \-p headless sessions, explicitly removing the model's ability to deviate from the known optimal path.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Deterministic dynamic workflows outperform autonomous LLM routing for standardized, repeatable software engineering tasks. |
| **Evidence/Source** | Claude Code official documentation: Agents and parallel work; "Building Effective AI Agents"1. |
| **Evidence Strength** | Strong. |
| **Implicated Mechanism** | External shell scripts interacting with claude \-p or the Agent SDK. |
| **Global Candidate?** | Yes. Standardized workflows (e.g., build-and-test.sh) can be stored in the global directory and invoked via standard Bash tools. |
| **Enforcement Strategy** | Deterministic (Shell scripting). |
| **Cost & Context** | Highly predictable token usage compared to open-ended autonomous routing. |
| **Security Impact** | Scripted workflows minimize the LLM's opportunity to execute out-of-bounds shell commands. |
| **Open Question** | How can a novice user visually track the execution state of a dynamic workflow running entirely via headless bash scripts? |

### **Hook Architectures Enable Granular Lifecycle Intervention**

Claude Code's hook architecture allows automated scripts to execute in response to specific lifecycle events. For instance, a PreToolUse hook can validate bash syntax before execution, and a PostToolUse hook can run security scanners immediately after a file edit24.  
These hooks communicate with Claude Code via exit codes, where an exit code of 0 allows the action to proceed, and a code of 2 denies it, feeding the structured JSON error back into the agent's context window26. This deterministic feedback loop is vastly superior to prompt-based instructions, as it physically blocks the agent from making destructive changes while providing immediate corrective context.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Hook architectures provide deterministic, zero-token intervention during the agentic loop, physically blocking invalid tool usage. |
| **Evidence/Source** | Claude Code official documentation: Hooks, Hooks Guide24. |
| **Evidence Strength** | Strong (CURRENTLY SUPPORTED). |
| **Implicated Mechanism** | hooks array in settings.json, utilizing matcher regex strings and standard exit codes. |
| **Global Candidate?** | Yes. Global hooks can enforce ubiquitous guardrails (e.g., blocking rm \-rf globally). |
| **Enforcement Strategy** | Deterministic (via exit codes fed back to the LLM). |
| **Cost & Context** | Deterministic bash hooks cost zero tokens and provide immediate feedback, saving the context window from failed execution logs. |
| **Security Impact** | Foundational for local security. Can intercept and block operations on sensitive data proactively8. |
| **Open Question** | Will intensive synchronous hooks (e.g., running a full linter on every PostToolUse) cause unacceptable latency and trigger Claude Code's timeouts? |

### **Agent-Maintained Handoffs are Required for Long-Running Stability**

Context windows eventually exhaust themselves, and transferring state across sessions purely via internal LLM summarization loses critical technical nuances. Agents must externalize their artifacts into markdown files (e.g., BUILD\_PLAN.md or MEMORY.md), committing to version control so the next session picks up a clean, verifiable state1.  
Claude Code explicitly supports this via the memory field in subagent definitions, which automatically loads the first 200 lines of a target MEMORY.md directory into the subagent's system prompt upon initialization27. This mechanism replaces the need for the control plane to hold infinite conversation history.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Long-running tasks require agents to externalize state into markdown files to prevent context decay and enable cross-session continuity. |
| **Evidence/Source** | Anthropic Engineering Blog; "Harness design for long-running application development"15. |
| **Evidence Strength** | Strong (Core tenet of Anthropic's million-line code experiment). |
| **Implicated Mechanism** | Persistent Memory for Subagents (loading the first 200 lines of MEMORY.md into the system prompt). |
| **Global Candidate?** | No. Memory files are inherently project-specific and must reside in the project repository. |
| **Enforcement Strategy** | Prompt-based (System instructions directing the agent to write handoff files). |
| **Cost & Context** | Reduces the token load of continuous conversation history. Relevant memory is loaded cleanly at initialization. |
| **Security Impact** | State files must be protected from prompt injection if the project processes untrusted external data. |
| **Open Question** | How should the system automatically prune MEMORY.md when it exceeds the 200-line automatic load limit? |

### **Windows Portability Requires Explicit PowerShell Configuration**

A critical failure mode for globally distributed control planes is the assumption of a POSIX-compliant environment. Standard Bash commands generated by the LLM routinely fail on Windows environments. The system must explicitly route shell commands to PowerShell by ensuring powershell.exe is in the PATH and that tool permissions are accurately defined for PowerShell cmdlets13.  
Furthermore, memory restrictions (caps) enforced by Claude Code rely on cgroups, which are native to Linux13. Translating these constraints to a Windows environment requires utilizing WSL2 or specific Windows registry management to maintain parity in resource control.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Windows environments require explicit tool mapping to PowerShell and registry-level configuration to maintain feature parity with Linux/macOS. |
| **Evidence/Source** | Claude Code official documentation: Terminal guide and tool reference13. |
| **Evidence Strength** | Strong (CURRENTLY SUPPORTED). |
| **Implicated Mechanism** | PowerShell tool; permissions.allow for PowerShell(Get-ChildItem \*) instead of Bash. |
| **Global Candidate?** | Yes. The global control plane must implement an OS-detection shim to configure default tools. |
| **Enforcement Strategy** | Deterministic (Settings configuration). |
| **Cost & Context** | Prevents token-burning loops where the agent repeatedly attempts Bash commands on a native Windows host. |
| **Security Impact** | PowerShell requires specific execution policy management to allow local script execution by the agent. |
| **Open Question** | Can the agent seamlessly transition between WSL2 (Bash) and native Windows (PowerShell) within the same session? |

### **Scaling Effort to Query Complexity**

Agents inherently struggle to judge appropriate effort, often overinvesting token budgets in simple queries while underinvesting in complex architectural changes. Anthropic's multi-agent research architectures demonstrate that routing heuristics must be established explicitly in the prompt or harness: simple tasks use a single agent limited to 3-10 tool calls, while complex tasks use specialized subagents with distinct task boundaries29.  
Fixed complexity thresholds (a hypothesis present in legacy designs) fail because they cannot account for the semantic weight of the code being modified. Instead, the control plane must evaluate the AST (Abstract Syntax Tree) and user intent to dynamically allocate the token budget.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Effort and token expenditure must be dynamically scaled to query complexity; fixed thresholds and universal architectures fail efficiently. |
| **Evidence/Source** | Anthropic: "How we built our multi-agent research system"29. |
| **Evidence Strength** | Strong. |
| **Implicated Mechanism** | System prompts guiding the Lead agent's delegation logic; \--effort flags. |
| **Global Candidate?** | Yes. The global planner agent should contain explicit scaling heuristics in its prompt. |
| **Enforcement Strategy** | Prompt-based (Delegation instructions) and Deterministic (API limits). |
| **Cost & Context** | Directly optimizes quality per token by preventing exhaustive searches for trivial bugs. |
| **Security Impact** | Minimal direct impact, though it bounds the financial risk of runaway execution. |
| **Open Question** | How can computational complexity be accurately pre-calculated before the agent begins its exploration phase? |

### **Background Agents Maximize Novice Developer Throughput**

A novice user cannot manually supervise multiple complex agent workflows simultaneously. Claude Code supports background sessions managed by a separate supervisor process. These agents run asynchronously, persist through machine sleep, and are managed via an "Agent View" (claude agents), allowing the user to peek, attach, or dispatch parallel work30.  
This feature operates independently of the experimental Agent Teams, providing isolated, non-communicating parallel execution that maximizes throughput without incurring the massive token coordination penalty associated with inter-agent messaging.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Background agents supervised by claude agents provide highly efficient parallel execution without the token bloat of Agent Teams. |
| **Evidence/Source** | Claude Code official documentation: Agent view30. |
| **Evidence Strength** | Strong (CURRENTLY SUPPORTED, Research Preview). |
| **Implicated Mechanism** | claude agents CLI, /bg slash command, supervisor process. |
| **Global Candidate?** | Yes. The user workflow should default to dispatching complex tasks to the background. |
| **Enforcement Strategy** | Deterministic (User interface abstraction). |
| **Cost & Context** | High parallelization reduces total time-to-completion, provided worktree isolation is active to prevent file collisions. |
| **Security Impact** | Background agents executing without supervision require rigid managed-settings.json permissions to prevent unattended damage. |
| **Open Question** | How does the system resolve interactive permission prompts (e.g., bash approvals) for a background agent while the user is away? |

### **Agent-Computer Interfaces (ACI) Must Be "Poka-Yoke"**

Designing tools for AI agents requires fundamentally different ergonomics than designing for human operators. Tool parameters must be mistake-proofed ("Poka-Yoke"), strongly typed, and include rigid pagination/truncation defaults. For example, capping database query responses at 25,000 tokens is critical to prevent context exhaustion1.  
When an agent is presented with an unconstrained tool, it frequently requests massive data dumps, obliterating its own context window and losing its system instructions in the process. The control plane must wrap all external tools in strict truncation handlers.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Agent-Computer Interfaces must be mistake-proofed with strict truncation limits to prevent data-dump context exhaustion. |
| **Evidence/Source** | "Building Effective AI Agents: Architecture Patterns and Implementation Frameworks" (Anthropic)1. |
| **Evidence Strength** | Strong. |
| **Implicated Mechanism** | MCP Server tool schema definitions and Hook output modification. |
| **Global Candidate?** | Yes. All globally provided MCP tools must be hardened against LLM hallucinations. |
| **Enforcement Strategy** | Deterministic (API response truncation and strict typing). |
| **Cost & Context** | Prevents runaway token consumption caused by agents dumping massive database tables into context. |
| **Security Impact** | Truncation and sanitization prevent buffer overflows in the context window that could be exploited by data-driven prompt injection. |
| **Open Question** | How does an agent autonomously realize that a truncated response requires it to utilize pagination parameters rather than assuming the data is complete? |

### **Refuting Rigid Framework Hypotheses**

Frameworks that mandate universal multi-agent routing, universal Test-Driven Development (TDD), mandatory Architectural Decision Records (ADRs), or fixed complexity thresholds are mathematically and empirically flawed.  
Universal multi-agent routing wastes tokens on simple tasks due to context duplication3. Universal TDD fails because LLMs frequently write tests designed specifically to pass their own hallucinated code implementations; external validation via the Default-FAIL contract is required5. Mandatory ADRs pollute the context window for minor bug fixes14. Finally, undocumented Claude Code configuration keys must never be utilized, as they break deterministic enforcement and create irreproducible environments across Windows and Linux deployments. The control plane must adapt dynamically rather than imposing rigid software engineering dogmas on the model.

| Dimension | Finding Specification |
| :---- | :---- |
| **Finding** | Rigid mandates (universal TDD, mandatory ADRs, fixed thresholds, undocumented keys) severely degrade agent performance and bloat token costs. |
| **Evidence/Source** | Anthropic multi-agent research; SWE-bench evaluation metrics1. |
| **Evidence Strength** | Strong (Supported by direct comparative performance data). |
| **Implicated Mechanism** | System prompt engineering and routing logic. |
| **Global Candidate?** | Yes. The control plane logic must actively suppress rigid generation mandates. |
| **Enforcement Strategy** | Deterministic (Routing logic) and Prompt-based (Heuristic instructions). |
| **Cost & Context** | Eliminating rigid generation mandates significantly improves quality per token. |
| **Security Impact** | Utilizing strictly documented configuration keys ensures deterministic security posture across diverse operating systems. |
| **Open Question** | How can the system differentiate between a minor structural refactor requiring an ADR and a standard bug fix without executing a full LLM analysis pass? |

## **The Strongest Debugging Workflow for Coding Agents**

The strongest debugging workflow for coding agents relies on the **Generator/Evaluator iteration loop** operating within a constrained sandbox, augmented by deterministic execution feedback.  
When a bug is encountered, unconstrained single agents often fall into "thrashing"—making rapid, unverified edits that compound the issue, eventually exhausting their context window with repeated stack traces1. The optimal protocol explicitly divorces the act of *reasoning about a problem* from the act of *writing the code*. Mathematical ablation studies on frameworks like AgentForge prove this separation is the primary driver of resolution performance10.  
The workflow proceeds as follows:

> 1. **State Snapshot:** The current failing state is committed to a temporary git worktree to provide a pristine rollback point11.  
> 2. **Independent Diagnosis:** A specialized, read-only "Debugger" subagent is spawned. Its sole objective is to read crash logs, execute grep searches, and formulate a hypothesis. Because its toolset is stripped of Write or Edit capabilities via disallowedTools, it cannot impulsively modify code13.  
> 3. **Constraint Formulation:** The Debugger generates a rigid test case (the Default-FAIL contract) that will mathematically prove the bug is resolved, writing this to a shared file5.  
> 4. **Targeted Generation:** The primary Coder agent receives the hypothesis and test case. It utilizes diff-based ![][image3] edits to apply the fix, drastically minimizing token output and regression risk compared to full-file generation10.  
> 5. **Verification:** An independent Evaluator runs the test. If it fails, the loop repeats, but the agent's context is compacted to include only the delta of the failure, preventing context duplication bloat3.

This workflow guarantees that code is only modified after a testable hypothesis is formed, completely eliminating hallucination thrashing.

## **Architectural Comparison: When Specialized Agents Materially Improve Outcomes**

Specialized agents materially improve software-engineering outcomes when task complexity demands distinct cognitive postures (e.g., creative generation vs. skeptical validation) or when tasks have completely disjoint context boundaries (e.g., frontend styling vs. database schema migration). Conversely, they merely waste tokens when tasks are highly sequential, require identical context windows, or involve single-file edits16.  
The following evaluates nine distinct architectural topologies against empirical SWE-bench data and Anthropic harness research:

| Architectural Paradigm | Utility & Efficacy | Drawbacks & Token Waste | Best Applied For |
| :---- | :---- | :---- | :---- |
| **1\. Single Strong Agent** | Highly token-efficient; low coordination overhead. Achieves baseline SWE-bench resolution rates rapidly. | Vulnerable to context bloat, sycophancy, and premature task completion due to lack of external oversight1. | Routine bug fixes, single-file refactoring, sequential tasks. |
| **2\. Planner \-\> Builder** | Front-loads compute to define scope; prevents the "wandering" architecture phenomenon seen in unconstrained agents7. | Highly rigid. If the planner hallucinates a flawed design, the builder executes the flaw perfectly, wasting the entire trajectory. | Green-field feature creation, initial repository scaffolding. |
| **3\. Planner \-\> Builder \-\> Reviewer** | Adds a verification layer to the workflow, attempting to mimic human peer review. | If context is shared, the reviewer exhibits severe confirmation bias (sycophancy) and rubber-stamps errors34. | Internal team tasks where the blast radius is minimal and token budgets allow redundancy. |
| **4\. Planner \-\> Builder \-\> Independent Evaluator** | **The Gold Standard.** A fresh-context evaluator enforces rigorous quality control without sycophancy, dramatically increasing resolution rates2. | High token cost; requires strict file-based state handoffs (e.g., test-results.json) to communicate across isolated contexts. | Complex long-running tasks, full-stack application development, high-risk code modifications. |
| **5\. Parallel Specialist Reviewers** | Maximizes domain expertise by running Security, Style, and Performance agents concurrently via background tasks17. | O(N) token scaling. Requires complex deterministic merge logic to resolve conflicting instructions from different reviewers. | Pre-deployment audits, critical blast-radius tasks involving authentication or infrastructure. |
| **6\. Agent Teams** | Excellent for broad research and parallel exploration where tasks do not overlap16. | Experimental feature; massive token bloat; erratic behavior and file collisions on sequential coding tasks16. | Data gathering, exploring unfamiliar architectures, or reading vast documentation sets. |
| **7\. Dynamic Workflows** | Deterministic, highly reliable; prevents LLM routing hallucinations by utilizing hardcoded shell scripts to coordinate agents23. | Rigid; fails catastrophically if the task falls outside the bash script's predefined boundaries. | CI/CD pipelines, automated dependency updates, test-driven development validation loops. |
| **8\. Generator/Evaluator Iteration** | GAN-inspired loop ensures near-perfect output over multi-hour runs, iterating until the Default-FAIL contract passes7. | Exorbitant cost (can reach hundreds of dollars per session) and lengthy latency. Overkill for standard development. | Producing production-ready MVPs entirely autonomously from single-prompt specifications. |
| **9\. Human Approval Between Stages** | Guarantees blast-radius security; ideal for novice oversight of critical operations. | Creates asynchronous bottlenecks, breaking agent autonomy and increasing time-to-completion1. | Touching production databases, deploying infrastructure, or spending significant financial resources. |

## **Investigative Inquiries & Agent Behavior Directives**

Based on the empirical research and Anthropic system cards, the following directives answer critical questions regarding agent communication, context management, and scaling.  
**Which roles actually benefit from isolated context?** Evaluators, Security Auditors, and Researchers demand isolated context. Evaluators must maintain strict skepticism; if they share context with the builder, they fall prey to confirmation bias2. Security Auditors must independently verify code without trusting the builder's hallucinated compliance claims. Researchers require isolation so their broad web-search data dumps do not pollute the primary coding context, which would degrade the model's spatial reasoning over the AST17.  
**When must reviewer/evaluator independence be protected?** Independence must be mathematically protected—via isolated subagent contexts and strict stripping of Write/Edit capabilities—whenever the code dictates security boundaries, application architecture, or functional correctness2. An evaluator that can edit the code it is reviewing will frequently introduce novel regressions rather than reporting the error back to the primary builder.  
**Should an evaluator see the builder's reasoning?** Absolutely not. Extensive research on LLM sycophancy demonstrates that if an evaluator sees the builder's chain of thought, it is highly likely to echo the builder's logic and approve flawed code, assuming the builder's reasoning is sound4. Evaluators must only see the final bytecode, the source file, and the original system requirements.  
**When should agents share context?** Context should only be natively shared (via forking or continuous sessions) when the workflow is strictly sequential and the secondary task fundamentally relies on the exact intermediate execution steps of the primary task. For example, a "Fixer" agent must share context with a "Tester" agent to understand exactly how the stack trace was generated during the test execution14.  
**When should they communicate directly?** Direct agent-to-agent communication (as seen in the experimental Agent Teams feature) introduces emergent unpredictability and high token overhead16. Agents should communicate asynchronously via structured file handoffs (e.g., test-results.json, BUILD\_PLAN.md). This externalizes the artifact, allowing deterministic scripts to verify state transitions before the next agent is invoked1.  
**How many agents are justified for ordinary work?** For ordinary, routine bug fixes, only **one** agent is justified. Adding agents to simple tasks scales costs linearly or exponentially with zero measurable gain in SWE-bench resolution quality16.  
**What complexity/risk threshold should trigger extra review?** Extra review via subagent invocation must be triggered by specific heuristics, not fixed arbitrary numbers:

> 1. **Blast Radius:** Any modifications to authentication logic, database schemas, or cloud infrastructure configurations.  
> 2. **Size:** Edits exceeding 50 lines of code, or tasks touching more than three disparate architectural files.  
> 3. **Verification Difficulty:** Code that cannot be covered by a deterministic unit test, such as visual frontend design or complex race-condition mitigation7.

**When should cheap models versus strongest models be used?** To optimize quality per token, cheap, high-speed models (e.g., Claude 3.5 Haiku) must be utilized for context compaction, log summarization, state-file generation, and basic regex linting. Frontier models (e.g., Claude 3.5 Sonnet or Opus 4.6) must be reserved strictly for overarching planning, complex code generation, and final architectural evaluation36.  
**When should the system deliberately remain single-agent?** The system must remain single-agent when making syntax corrections, appending documentation, updating dependencies, or executing strictly sequential same-file edits16. In these scenarios, the overhead of instantiating a subagent and passing context exceeds the computational effort required to simply execute the fix.

## **Dynamic Routing Policy for the Control Plane**

To optimize **quality PER TOKEN** rather than pursuing raw quality regardless of cost, the global control plane must implement a deterministic routing policy that assesses task parameters *before* executing inference.

> 1. **Phase 1: Task Intake & Complexity Assessment**  
   * The user submits a prompt. A fast, cheap model (Haiku) evaluates the prompt against the codebase AST to determine three metrics:  
     * *Uncertainty* (Are the required files known, or is discovery required?)  
     * *Complexity* (How many files/modules require structural edits?)  
     * *Blast Radius* (Does this touch secure data, authentication, or infrastructure?)  
> 2. **Phase 2: The Routing Matrix**  
   * **Low Complexity, Low Radius:** Route to a **Single Strong Agent** utilizing diff-based ![][image3] editing.  
   * **High Uncertainty, Low Radius:** Route to an **Explore Subagent** (read-only) to build a knowledge map and output a RESEARCH.md file, followed by a Single Builder agent.  
   * **High Complexity, High Radius:** Route to the **Planner \-\> Builder \-\> Independent Evaluator** dynamic workflow. Establish the Default-FAIL contract in test-results.json before any code generation begins.  
> 3. **Phase 3: Execution & Verification**  
   * Execute all generated code in isolated Git Worktrees11. Enforce verification via headless test scripts interacting with the Default-FAIL contract. If tests pass, present a single, clean unified diff to the novice user for final approval.

## **Final System Design Directives**

The culmination of this research dictates the specific requirements and anti-requirements for constructing the global control plane at C:\\Users\\USERNAME\\.claude\\.

### **A. Design Requirements Derived from Evidence**

> 1. **Immutable Security Tier:** The system must utilize managed-settings.json deployed at the OS level (e.g., C:\\Program Files\\ClaudeCode\\ for Windows, /etc/claude-code/ for Linux) to enforce tool blocklists, maximum API caps, and restricted model usage, preventing the novice user or a rogue agent from accidentally escalating privileges20.  
> 2. **Mandatory Git Worktree Isolation:** The control plane must default all multi-agent or background tasks to execute inside .claude/worktrees/. This guarantees that concurrent background operations do not destroy or conflict with the user's local working directory11.  
> 3. **Diff-Based Editing Standard:** Global configuration must preference the Edit tool over the Write tool to ensure ![][image3] token consumption and minimize hallucinated regressions on large file rewrites10.  
> 4. **Fresh-Context Evaluator Subagents:** The global \~/.claude/agents/ directory must be seeded with an independent Evaluator agent that possesses zero Write capabilities. It must be invoked exclusively to verify the builder's output against a predefined test contract4.  
> 5. **OS-Aware Tooling Routing:** The global configuration must implement OS-detection logic to explicitly map shell execution to PowerShell on Windows environments, overriding default POSIX Bash loops, and ensuring powershell.exe is appended to the environment PATH13.  
> 6. **Aggressive Context Compaction:** Use deterministic SessionStart hooks to invoke a fast model that compacts the MEMORY.md file, mitigating the 14.5% redundancy bloat found in long-running SWE-bench trajectories3.  
> 7. **Poka-Yoke ACI:** All globally provided MCP tools must enforce strict pagination, filtering, and 25,000-token truncation limits to prevent massive database or log dumps from exhausting the agent's context window1.

### **B. Anti-Requirements (What the Control Plane Should NOT Do)**

* **Do NOT mandate universal Multi-Agent routing:** Treating every task as a multi-agent problem is an anti-pattern that burns tokens, duplicates context, and increases latency. Routine tasks must remain single-agent3.  
* **Do NOT enable Agent Teams by default:** The environment variable CLAUDE\_CODE\_EXPERIMENTAL\_AGENT\_TEAMS must remain 0\. Direct agent-to-agent chatter is highly inefficient and erratic for standard software engineering compared to deterministic workflows16.  
* **Do NOT allow Evaluators to see Builder logs:** Feeding the builder's chain-of-thought into the evaluator's context window mathematically induces sycophancy and invalidates the evaluation process4.  
* **Do NOT rely on LLMs for rigid verification:** Do not use prompt-based hooks to check if code compiled successfully. Use deterministic PostToolUse bash hooks to verify exit codes directly24.  
* **Do NOT assume \~/.claude/settings.json is secure:** User-level settings can be overridden by the agent itself modifying the project-local configuration. Security constraints must live in managed-settings.json19.  
* **Do NOT utilize undocumented configuration keys:** Utilizing undocumented keys (as seen in legacy user frameworks) breaks deterministic enforcement and creates irreproducible environments across Windows and Linux deployments.

### **C. Unresolved Questions**

> 1. **Dynamic Pruning of Subagent Memory:** How can the control plane intelligently self-prune the MEMORY.md file when a complex project outgrows the 200-line automatic load limit, without losing critical architectural tenets?  
> 2. **Windows Cgroup Equivalence:** The documentation states Claude Code applies memory and execution caps via cgroups (a Linux kernel feature)13. How does the control plane seamlessly enforce these specific memory caps on native Windows PowerShell environments without forcing the novice user to install WSL2 virtualization?  
> 3. **Novice Threshold for Default-FAIL:** How can the system assist a complete software-engineering novice in defining mathematically verifiable criteria for visual or subjective frontend features within the test-results.json contract?

### **D. Sources**

* 24  
  : Current official Claude Code documentation: Hooks / Hooks Guide (code.claude.com/docs/en/hooks). Accessed October 2026\.  
* 17  
  : Current official Claude Code documentation: Subagents / Agent SDK (code.claude.com/docs/en/agent-sdk/subagents). Accessed October 2026\.  
* 11  
  : Current official Claude Code documentation: Git Worktrees / Tools Reference (code.claude.com/docs/en/worktrees). Accessed October 2026\.  
* 16  
  : Current official Claude Code documentation: Agent Teams (code.claude.com/docs/en/agent-teams). Accessed October 2026\.  
* 19  
  : Current official Claude Code documentation: Managed Settings / Settings Precedence (code.claude.com/docs/en/managed-settings). Accessed October 2026\.  
* 23  
  : Current official Claude Code documentation: Agent View / Dynamic Workflows (code.claude.com/docs/en/agent-view). Accessed October 2026\.  
* 13  
  : Current official Claude Code documentation: Terminal Guide / PowerShell (code.claude.com/docs/en/terminal-guide). Accessed October 2026\.  
* 1  
  : "Building Effective AI Agents: Architecture Patterns and Implementation Frameworks", Anthropic eBook/Report. Published 2025\.  
* 14  
  : "Effective context engineering for AI agents", Anthropic Engineering Blog. Published September 29, 2025\.  
* 7  
  : "Harness design for long-running application development", Anthropic Engineering Blog. Published March 24, 2026\.  
* 5  
  : Anthropic GitHub (cwc-long-running-agents) / "Learn Harness Engineering" curriculum. Updated 2026\.  
* 2  
  : Peer-reviewed empirical research on LLM Sycophancy (arXiv:2603.18740v1, arXiv:2609.20812v2). Published 2026\.  
* 29  
  : "How we built our multi-agent research system", Anthropic Engineering Blog. Published June 13, 2025\.  
* 3  
  : Empirical software engineering research on AgentForge, token cost, and context duplication on SWE-bench (arXiv:2604.13120v1, CASTER). Published 2026\.

#### **Works cited**

> 1. Building Effective AI Agents: Architecture Patterns and ... \- Anthropic, [https\://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf](https://resources.anthropic.com/hubfs/Building%20Effective%20AI%20Agents-%20Architecture%20Patterns%20and%20Implementation%20Frameworks.pdf)  
> 2. Measuring and Exploiting Confirmation Bias in LLM-Assisted ... \- arXiv, [https\://arxiv.org/html/2603.18740v1](https://arxiv.org/html/2603.18740v1)  
> 3. Tessera: Lossless-First, Vendor-Free Session Compression for Long, [https\://assets-eu.researchsquare.com/files/rs-11000146/v1\_covered\_f61abea9-7c0e-4857-ad85-3eef6f9d2d7d.pdf](https://assets-eu.researchsquare.com/files/rs-11000146/v1_covered_f61abea9-7c0e-4857-ad85-3eef6f9d2d7d.pdf)  
> 4. Quantifying Overclaiming Propensity in Frontier LLM Agents \- arXiv, [https\://arxiv.org/html/2609.20812v2](https://arxiv.org/html/2609.20812v2)  
> 5. anthropics/cwc-long-running-agents \- GitHub, [https\://github.com/anthropics/cwc-long-running-agents](https://github.com/anthropics/cwc-long-running-agents)  
> 6. The Sycophancy Tax: How Agreeable LLMs Silently Break, [https\://tianpan.co/blog/2026/04/10/sycophancy-tax-agreeable-llms-production](https://tianpan.co/blog/2026/04/10/sycophancy-tax-agreeable-llms-production)  
> 7. Harness design for long-running application development \- Anthropic, [https\://www\.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)  
> 8. AudAgent: Automated Auditing of Privacy Policy Compliance in AI, [https\://petsymposium.org/popets/2026/popets-2026-0077.pdf](https://petsymposium.org/popets/2026/popets-2026-0077.pdf)  
> 9. Welcome to Learn Harness Engineering \- GitHub Pages, [https\://walkinglabs.github.io/learn-harness-engineering/](https://walkinglabs.github.io/learn-harness-engineering/)  
> 10. AgentForge: Execution-Grounded Multi-Agent LLM Framework for, [https\://arxiv.org/html/2604.13120v1](https://arxiv.org/html/2604.13120v1)  
> 11. Run parallel sessions with worktrees \- Claude Code Docs, [https\://code.claude.com/docs/en/worktrees](https://code.claude.com/docs/en/worktrees)  
> 12. Common workflows \- Claude Code Docs, [https\://code.claude.com/docs/en/common-workflows](https://code.claude.com/docs/en/common-workflows)  
> 13. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 14. Effective context engineering for AI agents \- Anthropic, [https\://www\.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
> 15. Harness Design for Long-Running AI Engineering \- Bloss0m, [https\://www\.bloss0m.com/en/blog/09-harness-design-long-running-apps/](https://www.bloss0m.com/en/blog/09-harness-design-long-running-apps/)  
> 16. Orchestrate teams of Claude Code sessions \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)  
> 17. Subagents in the SDK \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)  
> 18. Create custom subagents \- Claude Code Docs, [https\://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
> 19. Settings files and precedence \- Claude Code Docs, [https\://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
> 20. Deploy managed settings \- Claude Code Docs, [https\://code.claude.com/docs/en/managed-settings](https://code.claude.com/docs/en/managed-settings)  
> 21. Set up Claude Code for your organization, [https\://code.claude.com/docs/en/admin-setup](https://code.claude.com/docs/en/admin-setup)  
> 22. Manage Claude Code plugins for your organization, [https\://code.claude.com/docs/en/plugins/org](https://code.claude.com/docs/en/plugins/org)  
> 23. Run agents in parallel \- Claude Code Docs, [https\://code.claude.com/docs/en/agents](https://code.claude.com/docs/en/agents)  
> 24. claude-howto/06-hooks/README.md at main \- GitHub, [https\://github.com/luongnv89/claude-howto/blob/main/06-hooks/README.md](https://github.com/luongnv89/claude-howto/blob/main/06-hooks/README.md)  
> 25. Automate actions with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
> 26. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 27. claude-howto/04-subagents/README.md at main \- GitHub, [https\://github.com/luongnv89/claude-howto/blob/main/04-subagents/README.md](https://github.com/luongnv89/claude-howto/blob/main/04-subagents/README.md)  
> 28. Terminal guide for new users \- Claude Code Docs, [https\://code.claude.com/docs/en/terminal-guide](https://code.claude.com/docs/en/terminal-guide)  
> 29. How we built our multi-agent research system \- Anthropic, [https\://www\.anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)  
> 30. Manage multiple agents with agent view \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-view?8adb0641\_page=2](https://code.claude.com/docs/en/agent-view?8adb0641_page=2)  
> 31. Manage multiple agents with agent view \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-view](https://code.claude.com/docs/en/agent-view)  
> 32. Building Effective AI Agents \- Anthropic, [https\://www\.anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)  
> 33. OpenCollab: A Multi-Agent Coding Framework with Programmable, [https\://arxiv.org/html/2609.38345](https://arxiv.org/html/2609.38345)  
> 34. Cross-Context Review: Improving LLM Output Qualityby Separating, [https\://ar5iv.labs.arxiv.org/html/2603.12123](https://ar5iv.labs.arxiv.org/html/2603.12123)  
> 35. AMEL: Accumulated Message Effects on LLM Judgments \- arXiv, [https\://arxiv.org/pdf/2605.22714](https://arxiv.org/pdf/2605.22714)  
> 36. Model configuration \- Claude Code Docs, [https\://code.claude.com/docs/en/model-config](https://code.claude.com/docs/en/model-config)  
> 37. Configure server-managed settings \- Claude Code Docs, [https\://code.claude.com/docs/en/server-managed-settings](https://code.claude.com/docs/en/server-managed-settings)  
> 38. Glossary \- Claude Code Docs, [https\://code.claude.com/docs/en/glossary](https://code.claude.com/docs/en/glossary)  
> 39. Trajectory-Aware Benchmark Subset Selection for Cost-Efficient, [https\://arxiv.org/html/2609.24928v2](https://arxiv.org/html/2609.24928v2)  
> 40. CASTER: Breaking the Cost-Performance Barrier in Multi-Agent, [https\://arxiv.org/html/2601.19793v1](https://arxiv.org/html/2601.19793v1)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAdCAYAAACaCl3kAAAARElEQVR4XmNgGJngPxZMEiBZAwiQZRMIUKSRLEBfjRT5D5dGXOJggE8SnxxeSXxyeCWxysH8hk0SlziKJnx4FIyCgQIAeM4m2vkRtdcAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAcCAYAAABVo158AAAATklEQVR4Xu2OWwoAIAgEvf+liz4Em8we0I80EMWug4nkouBsczTceCd4/w9lCvZ2xWtB3zYLBbckHF5KFDSzXQcDbmM/BjIZVLwiFD7ZqXj3NMzAcewPAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAbCAYAAADoOQYqAAAA20lEQVR4Xu2S2wqEQAxD/f+f3qWylVqTXrT7IMwBwUnTZAS3bfFuPr+nQ9dP0fLOJZCvmpHNS7zq0qwgK2e6EO0p2RySXUqI5kwXopml6tupXFhgHqRZsrlS9e1Uzezj/Nnj5yhDYPqFsnG7d2nrt/soR0DaBbbsuVuE9vzZwvQTUYAFlStIU9gOo+Sthkaeymyi52AirDKb6DmohGUeNvN73ufPAtIgkdEXI9jc7+q71y1Mv6Ah6KnAfF7Pspn+F6bKJjJaTBROZLR4Wvh0/zbR/xrR9S8Wi0WTL1nkmGgLCcuMAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAYCAYAAAB5j+RNAAAAwklEQVR4Xu2SSw6DMAxEuf+lWwXVlbE94yENVSX6JDbzcxZs25/f4hGFk0j9EfKfAsrFrW6TeTvqkAfl4la3WXqsiHSDeUa3YaQMe5gx6xlKJtE9ykAZpHvUGwm1hA5UWgR1KWdKKFtpEdSlqCWWQ7pHySTYUQ/LId3ousjjpoPlkG50XeRx08EyzBuwG8zj5osuw7wB6ldagoXQsGfWR/oBe0D1KVS5uIO+y/naoVlu87iVWzsrB1duvVnx733avzlPIiiFe2vYqhcAAAAASUVORK5CYII=>