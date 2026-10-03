# **Architectural Protocol: Developing a Global Claude Code Control Plane for the Software Development Lifecycle**

The integration of autonomous, large language model (LLM) powered coding agents into the software development lifecycle (SDLC) represents a fundamental paradigm shift in software engineering. However, deploying these agents without deterministic boundaries exposes projects to catastrophic context collapse, cognitive deadlocks, and severe validation tautologies. Designing a production-quality, global control plane for Claude Code—anchored primarily in C:\\Users\\USERNAME\\.claude\\ for Windows environments and \~/.claude/ for UNIX-like systems—requires a rigorous reconciliation of official system capabilities with empirical software engineering research.  
This research report establishes the architectural requirements for a control plane designed to guide software engineering novices through the entire SDLC. From unformed ideas through architecture, implementation, testing, debugging, and continued maintenance, the system must abstract complexity while preventing the distinct failure modes unique to non-deterministic coding agents. The following analysis strictly delineates currently supported Claude Code behaviors from experimental features, relying on authoritative documentation and peer-reviewed studies as of October 2026\.

## **Part I: Configuration Topology and Environmental Portability**

The foundational layer of the Claude Code control plane is its hierarchical configuration resolution engine. A robust control plane must explicitly separate global developer preferences from strict, project-local security and operational constraints.

### **The Precedence Stack and Scope Boundaries**

Claude Code evaluates configuration keys in a strict, deterministic precedence stack. When the same key appears across multiple files, the system uses the value from the highest precedence level. The architecture prevents global preferences from inadvertently violating project-specific mandates. The configuration engine processes files in the following order of precedence: managed organizational settings (e.g., managed-settings.json), project local overrides (.claude/settings.local.json), shared project settings (.claude/settings.json), and finally global user settings (\~/.claude/settings.json)1.  
A critical design requirement for the global control plane located at C:\\Users\\USERNAME\\.claude\\ is the minimization of permissive state. Global settings apply to every project accessed by the developer. If a permissive rule, such as auto-approving all shell commands, is placed in the global scope, it compromises the security of every repository on the host machine1. Therefore, the global configuration must be restricted to non-destructive ergonomic defaults, environmental normalization, and telemetry preferences, while lifecycle hooks and permission logic must be strictly localized to the project root.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Claude Code enforces a deterministic precedence stack where managed settings and project-local files override global user configurations, necessitating strict isolation of permissive rules. |
| **2\. Evidence/Source** | Official Claude Code documentation on settings architecture and precedence1. |
| **3\. Evidence Strength** | Strong (Tier 1 authoritative documentation). |
| **4\. Claude Code Mechanism Implicated** | Configuration resolution engine and JSON settings parsing. |
| **5\. Global \~/.claude Candidate?** | Conditional. Appropriate for non-destructive preferences, but dangerous for permissive execution rules. |
| **6\. Enforcement Type** | Deterministic. Handled by the application binary prior to LLM invocation. |
| **7\. Cost/Context Implications** | Zero token cost. Deterministic parsing occurs outside the model's context window. |
| **8\. Security Implications** | High. Incorrectly scoping permissive rules globally exposes the entire host machine to autonomous destructive actions. |
| **9\. Open Question Remaining** | How does the resolution engine handle deeply nested arrays across different scopes, specifically regarding the merging versus overwriting of MCP servers? |

### **Windows Native Portability via PowerShell**

A persistent challenge in cross-platform agentic engineering has been the reliance on POSIX-compliant translation layers (e.g., Git Bash) in Windows environments. This translation often introduces latency, path-resolution errors, and token inflation as the agent attempts to navigate mixed backslash and forward-slash syntaxes.  
Current system capabilities natively support Windows execution through the PowerShell tool2. This allows the coding agent to execute cmdlets, pipe objects, and manipulate Windows-native file paths directly without intermediary translation2.  
For the global control plane on Windows, setting the environment variable "CLAUDE\_CODE\_USE\_POWERSHELL\_TOOL": "1" within C:\\Users\\USERNAME\\.claude\\settings.json is a mandatory baseline2. This ensures that any project initialized by the novice developer defaults to the native shell, significantly reducing context pollution associated with pathing errors.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Native PowerShell support eliminates the requirement for Git Bash translation layers on Windows, improving execution reliability and reducing token waste. |
| **2\. Evidence/Source** | Official Claude Code changelog and environment variable documentation2. |
| **3\. Evidence Strength** | Strong (Tier 1 authoritative documentation). |
| **4\. Claude Code Mechanism Implicated** | Internal execution shell and environment variable configuration (env block). |
| **5\. Global \~/.claude Candidate?** | Yes. Environment normalization should be enforced globally per machine environment. |
| **6\. Enforcement Type** | Deterministic via settings.json environment injection. |
| **7\. Cost/Context Implications** | Reduces context pollution and latency by eliminating POSIX-to-Windows path translation debugging cycles. |
| **8\. Security Implications** | PowerShell execution exposes the Windows registry and deep system configurations. Proper PreToolUse restrictions must accompany this setting. |
| **9\. Open Question Remaining** | To what extent does the agent's pre-trained knowledge of POSIX bash scripting dominate its behavior, potentially leading to syntax hallucination within the PowerShell host? |

## **Part II: Context Survivability and Deterministic Guardrails**

The target user for this control plane is a software engineering novice. Consequently, the system must autonomously manage the lifecycle of the project, abstracting the complexity of memory management and failure recovery. A fundamental limitation of all current LLMs is context degradation. As a session lengthens, prompt-based instructions are deprioritized by attention mechanisms, leading to protocol violations5.

### **Mitigating Context Compaction**

When the Claude Code context window reaches a predefined token threshold (autoCompactWindow), the system automatically compacts the transcript to free space6. This summarization process is destructive; it frequently results in the irreversible loss of nuanced project constraints, architectural guidelines, and security rules8.  
To guarantee workflow compliance, the control plane must offload critical state management to deterministic lifecycle hooks. By configuring a SessionStart hook with a compact matcher, the control plane can execute a shell script that automatically dumps critical contextual plain-text via standard output (stdout) back into the context window immediately following compaction8.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Automatic context compaction destroys nuanced project instructions, necessitating deterministic re-injection to maintain agent compliance over long SDLC lifecycles. |
| **2\. Evidence/Source** | Official documentation on hooks, compaction, and automation8. |
| **3\. Evidence Strength** | Strong (Tier 1 authoritative documentation). |
| **4\. Claude Code Mechanism Implicated** | SessionStart hook event, compact matcher, and stdout consumption. |
| **5\. Global \~/.claude Candidate?** | Conditional. The hook mechanism can be defined globally, but the injected text must be project-specific. |
| **6\. Enforcement Type** | Deterministic. Operates independently of the LLM's stochastic routing. |
| **7\. Cost/Context Implications** | Increases immediate token consumption post-compaction but mathematically guarantees constraint survival, preventing costly downstream hallucinations. |
| **8\. Security Implications** | Prevents the agent from "forgetting" security constraints defined in standard text. |
| **9\. Open Question Remaining** | What is the optimal mathematical balance between the autoCompactWindow threshold and the volume of re-injected text to maximize utility without triggering infinite compaction loops? |

### **Deterministic Security Interception**

Security constraints and architectural boundaries must never rely solely on natural language prompts within CLAUDE.md. Empirical evidence demonstrates that agents will violate text-based boundaries when optimizing for task completion5.  
Instead, security must be enforced by PreToolUse hooks defined in the .claude/settings.json file. These hooks evaluate the tool\_name and tool\_input via standard input (stdin). If an unauthorized action is detected (e.g., executing destructive shell commands, attempting to alter protected framework files, or exposing environment secrets), the hook must terminate the process with Exit 2\. This definitively blocks the tool before execution and writes a rejection reason to standard error (stderr), which Claude Code captures and feeds back to the model for self-correction8.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Security and architectural boundaries must be enforced via PreToolUse shell scripts returning Exit 2, definitively blocking unauthorized actions prior to execution. |
| **2\. Evidence/Source** | Official documentation on hook lifecycle, error handling, and automation8. |
| **3\. Evidence Strength** | Strong (Tier 1 authoritative documentation). |
| **4\. Claude Code Mechanism Implicated** | PreToolUse hook execution, JSON input parsing, and exit code interpretation. |
| **5\. Global \~/.claude Candidate?** | Yes. Absolute security guardrails (e.g., blocking rm \-rf /) belong in the global control plane. |
| **6\. Enforcement Type** | Deterministic. Short-circuits the LLM's intended action. |
| **7\. Cost/Context Implications** | Highly efficient. Saves compute time and token cost of executing and rolling back failed operations, providing immediate context for self-correction. |
| **8\. Security Implications** | Critical. This is the sole mechanism to isolate the host machine from autonomous destructive behavior in auto permission mode. |
| **9\. Open Question Remaining** | How severely does constant deterministic rejection degrade the model's confidence, potentially inducing cognitive deadlocks? |

## **Part III: Subagent Topologies and the Accuracy Paradox**

A critical challenge identified in recent empirical evaluations on the SWE-bench dataset is the propensity for autonomous coding agents to become trapped in unproductive, long-tail exploratory loops. When an agent confronts a complex multi-file task, monolithic execution architectures degrade rapidly. The agent exhausts its context window exploring false hypotheses, leading to an "accuracy paradox" where increased token generation actively degrades problem-solving efficacy5.

### **The Expert-Executor Architecture**

The software engineering literature strongly suggests mitigating this failure mode through structural decomposition, specifically the "Expert-Executor" pattern12. In this topology, a primary supervisor agent maintains high-level objectives while delegating specific, isolated tasks to ephemeral subagents.  
Claude Code supports this natively via its subagent topology, allowing the definition of localized .claude/agents/\*.md files13. Subagents in Claude Code operate in fully isolated context windows unless explicitly forked. A subagent can explore dozens of files, execute deep log analysis, and summarize its findings without polluting the parent agent's context window with thousands of tokens of stack traces or discarded source code13. The built-in subagents, such as Explore and Plan, explicitly skip loading CLAUDE.md and repository snapshots to keep research fast and inexpensive14.  
For a novice user, the control plane should autonomously route complex tasks to these subagents, preventing the novice from watching the main session spiral into token exhaustion.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Delegating exploratory tasks to isolated subagents prevents parent context inflation and mitigates the accuracy paradox observed in extended software engineering workloads. |
| **2\. Evidence/Source** | Tier 1 official documentation on subagents13; Tier 2 empirical analysis on agentic loops5. |
| **3\. Evidence Strength** | Strong. |
| **4\. Claude Code Mechanism Implicated** | The Agent tool, .claude/agents/\*.md definitions, and context window sandboxing. |
| **5\. Global \~/.claude Candidate?** | Yes. General-purpose utility subagents (e.g., security-scanner) should be defined globally for reuse. |
| **6\. Enforcement Type** | Prompt-based/Autonomous. The agent invokes the Agent tool dynamically. |
| **7\. Cost/Context Implications** | Drastically reduces context pollution in the primary session, minimizing the aggregate token cost of long-running exploratory tasks. |
| **8\. Security Implications** | Subagents can be sandboxed with limited allowedTools, preventing file modifications during analysis. |
| **9\. Open Question Remaining** | At what precise task complexity threshold does the overhead of prompting and spawning a subagent eclipse the token savings of context isolation? |

## **Part IV: Testing Strategies, Validation, and the Tautology Trap**

A significant portion of the control plane's design must dictate how the agent validates its own work. A prevalent assumption in modern agentic software engineering is that Test-Driven Development (TDD) or conventional unit testing naturally yields robust software when executed by an LLM.  
Empirical evidence exposes a profound vulnerability in this assumption. When an LLM generates tests for its own code, it frequently generates tautological tests9. A tautological test is one whose oracle mirrors the exact implementation logic of the system under test, rather than challenging it with independent domain constraints.  
If the LLM incorrectly implements an algorithm, it will write a test that expects the exact incorrect output produced by its algorithm, or it will compute the expected output dynamically using the exact same flawed implementation9. This creates a dangerous "false sense of security" where test suites achieve 100% pass rates on objectively broken software9. Furthermore, empirical studies reveal that coding agents are highly predisposed to "over-mocking." When creating tests, agents employ the mock type in 95% of cases, actively avoiding more robust fake or spy implementations, thereby masking deep integration failures18.  
To construct a robust validation process that reliably prevents an agent from validating its own mistaken implementations, the control plane must implement a Verification Hierarchy utilizing multiple distinct testing paradigms.

### **Exhaustive Analysis of Testing Paradigms for Coding Agents**

**Test-Driven Development (TDD) and Tests Written Before Implementation:** While highly effective for humans, TDD poses unique risks for next-token prediction engines. When forced to write tests before the implementation exists, an LLM must hallucinate the API structure and expected behavior. Without strong external constraints, the LLM will subsequently write the implementation to satisfy its own hallucinated, often flawed, test cases9. Test-first prompting is empirically effective *only* when defining strict mathematical bounds or security constraints. For complex, stateful logic, test-first prompting frequently results in tautological loops.  
**Tests Written After Implementation:** Allowing the agent to write tests post-implementation allows the agent to analyze the working abstract syntax tree (AST). However, if the same agent context writes the test, it remains heavily biased by its own prior reasoning, leading directly to the over-mocking phenomenon where the agent hardcodes expected responses to match the flawed implementation9.  
**Agent-Generated vs. Independently Generated Tests:** To break the correlation between implementation logic and test oracles, test generation must be independent. Utilizing differential testing principles, the implementation should be written by the primary agent, while tests are generated by an entirely isolated subagent (e.g., a .claude/agents/tester.md) that receives only the requirements and the final function signatures, not the implementation logic itself9.  
**Hidden Tests and Characterization Tests:** Hidden tests are critical in benchmarking (e.g., SWE-bench, CRUXEval) to prevent data contamination12. In a development environment, characterization tests—tests generated specifically to map the existing behavior of undocumented legacy code—are highly effective when generated by agents. For a novice user inheriting a project, instructing a subagent to write characterization tests provides an automated safety net before refactoring begins.  
**Acceptance and End-to-End (E2E) Testing:** Acceptance testing relies on high-level business logic. Because coding agents excel at text parsing, integrating frameworks like Cucumber (Behavior-Driven Development) allows the novice user to define plain-text business rules which the agent then translates into E2E integration tests. This fundamentally grounds the agent's work in human-readable reality, preventing algorithmic drift.  
**Fuzzing and Property-Based Testing (PBT):** Property-based testing is a paradigm shift that actively prevents tautologies. Instead of hardcoding example inputs, PBT frameworks (like Python's Hypothesis) require the agent to define mathematical or domain invariants (e.g., "for any integer sequence, the sorted output has the same length as the input and is monotonically increasing"). The runtime dynamically fuzzes thousands of state-space variations. This forces the LLM into a higher order of reasoning, actively discovering buffer overflows, type mismatches, and mathematical boundary violations that an LLM would never intentionally write an example-based test for20.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Instructing an agent to validate logic via Property-Based Testing (PBT) actively prevents the generation of tautological, example-based tests by forcing the definition of generalized invariants. |
| **2\. Evidence/Source** | Literature on Agentic PBT, round-trip correctness, and Hypothesis20. |
| **3\. Evidence Strength** | Strong (Emerging empirical software testing data). |
| **4\. Claude Code Mechanism Implicated** | System prompting via CLAUDE.md and shell execution of PBT frameworks. |
| **5\. Global \~/.claude Candidate?** | Conditional. The instructional strategy can be global, but framework implementation is project-local. |
| **6\. Enforcement Type** | Prompt-based instruction validated by deterministic framework execution. |
| **7\. Cost/Context Implications** | PBT requires significantly less code to achieve massive state-space coverage, directly reducing token consumption in the context window. |
| **8\. Security Implications** | High positive impact. Dynamically explores edge cases and memory safety boundaries missed by static analysis. |
| **9\. Open Question Remaining** | Can LLMs reliably identify non-trivial invariants for complex stateful business logic, or is agentic PBT practically limited to pure functions? |

**Static Analysis, Type Checking, and Mutation Testing:** Before any dynamic testing runs, static analysis and strict type checking (e.g., mypy, tsc) must execute deterministically via PostToolUse hooks8. However, passing static analysis does not ensure logical correctness.  
To systematically evaluate the strength of the agent's tests, the control plane must implement Mutation Testing. Mutation frameworks (e.g., mutmut, Stryker) introduce semantic-preserving or logic-altering bugs into the source code (e.g., swapping \> for \>=). If the agent's tests still pass, the tests are tautological or weak. Recent literature demonstrates that applying dynamic condition augmentation to source code causes drastic performance drops in LLM evaluations, proving that agents struggle with mutated logic15. A robust control plane executes a mutation runner; if the mutation score falls below a threshold, the surviving mutants are fed back to the agent, forcing it to strengthen its assertions9.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Mutation testing provides an objective, deterministic oracle to identify and reject tautological or over-mocked tests generated by coding agents. |
| **2\. Evidence/Source** | Research on structural-adaptive fragmentation, dynamic benchmarking, and LLM test quality9. |
| **3\. Evidence Strength** | Strong (Extensive empirical evaluation). |
| **4\. Claude Code Mechanism Implicated** | PostToolUse hooks targeting testing tools, and stderr feedback mechanisms. |
| **5\. Global \~/.claude Candidate?** | No. Mutation frameworks are language and project specific. |
| **6\. Enforcement Type** | Deterministic execution of the mutation tool triggering an autonomous LLM correction loop. |
| **7\. Cost/Context Implications** | High compute latency locally, but highly token-efficient as the LLM receives precise structural feedback rather than abstract errors. |
| **8\. Security Implications** | Drastically improves detection of edge-case vulnerabilities and unhandled state transitions. |
| **9\. Open Question Remaining** | How effectively can an LLM interpret mutation output without devolving into blindly adding arbitrary assertions simply to satisfy the coverage score? |

## **Part V: The Optimal Debugging Workflow**

Debugging autonomous agent output requires a structured orchestration of tools to prevent the agent from destroying working code while attempting to fix a localized issue. The strongest debugging workflow for coding agents combines the Expert-Executor architecture with strict context isolation12.  
When a test fails, the primary session (the Expert) should not immediately attempt to edit the file. Instead, the control plane should facilitate an automated workflow:

> 1. **Compilation/Execution parsing:** stderr from the failed run is captured.  
> 2. **Read-Only Subagent Analysis:** A debugging subagent, restricted via allowedTools to only Read and Grep, explores the stack trace and the broader repository. This prevents the agent from making panicked, hallucinated edits13.  
> 3. **Hypothesis Generation:** The subagent returns a concise summary of the failure mechanism to the main session.  
> 4. **Targeted Implementation:** The main session uses this summary to execute a precise Edit command.

This workflow structurally prevents the coding agent from writing tests that merely validate its mistaken implementation by ensuring that the entity diagnosing the error is separated from the entity that wrote the original logic.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | The optimal debugging workflow restricts analysis to a read-only subagent, separating diagnosis from execution to prevent hallucinated, destructive edits. |
| **2\. Evidence/Source** | SWE-bench failure analysis and subagent architectural documentation12. |
| **3\. Evidence Strength** | Strong. |
| **4\. Claude Code Mechanism Implicated** | Subagent isolation, allowedTools restrictions, and standard error ingestion. |
| **5\. Global \~/.claude Candidate?** | Yes. A global .claude/agents/debugger.md can be templated for universal use. |
| **6\. Enforcement Type** | Prompt-based workflow orchestration enforced by deterministic tool limitations. |
| **7\. Cost/Context Implications** | Eliminates the massive token cost associated with rapid, trial-and-error editing loops. |
| **8\. Security Implications** | Prevents accidental deletion or corruption of critical infrastructure during panicked debugging attempts. |
| **9\. Open Question Remaining** | Can a read-only debugging subagent effectively diagnose deeply stateful integration errors without the ability to dynamically insert print statements or run isolated execution environments? |

## **Part VI: Deconstructing Legacy Hypotheses (JackSmack1971/supreme)**

The user query explicitly requests a validation of prescriptions present in legacy frameworks, specifically challenging rules surrounding fixed complexity, architectural mandates, and universal routing. Empirical evidence demonstrates that many of these heuristic rules actively degrade LLM performance.  
**Challenge 1: Fixed Complexity Thresholds** Legacy systems frequently mandate arbitrary complexity scoring, enforcing rules that block tasks scored highly. Evidence demonstrates that complexity is non-linear and highly subjective to the model's pre-training data5. Imposing fixed thresholds results in arbitrary workflow interruptions. The optimal alternative relies on Claude Code's native CLAUDE\_CODE\_AUTO\_COMPACT\_WINDOW coupled with token velocity monitoring, dynamically delegating to subagents when token consumption outpaces task progression.  
**Challenge 2: Mandatory Architectural Styles and ADR Policies** Forcing an agent to read and write extensive Architectural Decision Records (ADRs) for minor feature additions causes extreme context inflation. Studies on TDFlow and SWE-bench indicate that models perform best when given concise, localized context5. The control plane should not force universal ADR generation; instead, it should store architectural rules in isolated .claude/rules/\*.md files, loading them lazily via path-gating or semantic triggers only when relevant.  
**Challenge 3: Universal Multi-Agent Routing** Routinely bouncing tasks between a rigid hierarchy of subagents wastes compute and loses subtle context during inter-agent serialization. Built-in subagents actively bypass CLAUDE.md to save context14. Defaulting to a single, monolithic session for linear tasks is mathematically superior. Parallel subagents should be utilized exclusively for asynchronous, context-heavy tasks (e.g., log analysis, codebase security scanning) where context isolation is explicitly required13.  
**Challenge 4: Universal Test-Driven Development (TDD)** As extensively analyzed in Part IV, universal TDD forces next-token predictors to hallucinate APIs, resulting in tautological implementations9. Evidence supports test-first prompting only for defining mathematical bounds (PBT). For complex logic, the agent should implement the code first, followed by an isolated subagent reviewing the implementation to write adversarial tests9.

| Finding Parameter | Assessment & Details |
| :---- | :---- |
| **1\. Finding** | Forcing coding agents into rigid, human-centric procedural workflows (mandatory ADRs, universal TDD, fixed complexity) exacerbates context pollution and degrades resolution rates. |
| **2\. Evidence/Source** | SWE-bench failure analyses, context inflation reports, and literature on TDD prompting5. |
| **3\. Evidence Strength** | Strong (High-quality empirical benchmarking). |
| **4\. Claude Code Mechanism Implicated** | .claude/workflows/\*.js and monolithic prompt instructions in CLAUDE.md. |
| **5\. Global \~/.claude Candidate?** | No. |
| **6\. Enforcement Type** | N/A (Identification of an anti-pattern). |
| **7\. Cost/Context Implications** | Eliminating bloated procedural mandates drastically reduces token consumption per task. |
| **8\. Security Implications** | Neutral, provided deterministic static analysis gates remain in place. |
| **9\. Open Question Remaining** | Is there a programmatic threshold where the transition from a monolithic session to a highly structured multi-agent workflow becomes mathematically beneficial based on AST branch complexity? |

## **Part VII: The Verification Hierarchy for Automatic Workflow Gates**

Synthesizing the evidence regarding validation strategies, tautological failures, and deterministic security, the optimal global control plane must enforce a sequential verification hierarchy. These automatic workflow gates transition from computationally cheap syntax checks to highly rigorous semantic evaluations.

> 1. **Gate 1: Deterministic Static Analysis (Pre-Commit / PostToolUse)** Executed deterministically on every Edit or Write. Linters, formatters, and strict type-checkers evaluate the AST. Obvious tautologies (e.g., assert x \== x) are caught instantly without LLM involvement.  
> 2. **Gate 2: Independent Example-Based Execution** Basic regression checks ensure compilation and successful execution paths. To avoid bias, the test suite is generated by a differentially isolated subagent.  
> 3. **Gate 3: Property-Based Fuzzing** The agent writes invariant-based tests using libraries like Hypothesis. The runtime dynamically explores the state space, providing counter-examples when unhandled states are reached, breaking the LLM's bias toward happy-path scaffolding.  
> 4. **Gate 4: Deterministic Mutation Evaluation** A deterministic runner introduces semantic variations into the source code. If the agent's test suite passes despite the mutations, the tests are flagged as weak, rejecting the commit and forcing an autonomous revision loop.  
> 5. **Gate 5: Semantic Business Review** An isolated "Reviewer" subagent, restricted solely to Read tools, evaluates the final implementation against the novice user's original business requirements, breaking the cognitive deadlock of the primary implementation agent.

## **Part VIII: Strategic Deliverables**

### **A. Design Requirements Derived from Evidence**

* **Hierarchical Configuration Isolation:** Scaffold \~/.claude/settings.json exclusively for non-destructive developer ergonomics (PowerShell flags, themes, telemetry). Utilize .claude/settings.json committed to version control for project-specific lifecycle hooks, permissions, and validation scripts to prevent cross-project vulnerability bleed.  
* **Context Survivability Injection:** Implement SessionStart hooks matching the compact event to deterministically execute scripts that write fundamental project constraints to stdout, ensuring survival past Claude Code's automatic token summarization.  
* **Deterministic Security Perimeters:** Destructive actions and strict architectural violations must be blocked via deterministic PreToolUse shell scripts returning Exit 2\. Never rely on natural language prompts in CLAUDE.md to prevent hazardous actions.  
* **Subagent Exploration Offloading:** Deep file-tree traversals, broad log analysis, and exploratory debugging must be routed to read-only .claude/agents/\*.md subagents to preserve the main session's context window and avoid the SWE-bench accuracy paradox.  
* **Multi-Tiered, Anti-Tautological Validation:** The control plane workflow must enforce a testing hierarchy utilizing independent test generation, property-based testing, and mutation testing to definitively break tautological LLM-generated mock loops.

### **B. Anti-Requirements (What the Control Plane Should NOT Do)**

* **Do not enforce Universal TDD for feature logic:** Instructing the agent to write example-based unit tests prior to implementation heavily biases the model toward writing tautological tests that match its own hallucinated APIs.  
* **Do not use prompt instructions for strict security rules:** Avoid relying on CLAUDE.md to instruct the agent against destructive behavior. Context compaction will eventually erase these rules, leading to autonomous damage. Use deterministic hooks.  
* **Do not deploy highly permissive global rules:** Never establish dangerous auto-approvals (e.g., untethered Bash or PowerShell execution) in the global \~/.claude/settings.json.  
* **Do not force mandatory multi-agent routing for simple tasks:** Structuring the control plane so that every task passes through a rigid sequence of "Planner," "Coder," and "Tester" subagents inflates token costs and degrades performance for tasks easily handled in a monolithic context window.  
* **Do not rely on the LLM to review its own complex logic:** A model reviewing its own output within the same continuous context window suffers from confirmation bias. Validation and diagnosis must utilize isolated subagents.

### **C. Unresolved Questions**

* **Array Merging in Configuration Scopes:** System documentation lacks explicit definitions regarding how deeply nested arrays (such as hook lists or allowed MCP server arrays) behave when identically keyed across user, project, and managed settings files. The precise merge versus overwrite behavior requires empirical validation.  
* **Mutation Testing Scalability:** While mutation testing is the strongest defense against tautological LLM tests, its computational overhead is massive. Can coding agents be prompted to effectively interpret statistically sampled mutants rather than requiring a full test-suite run?  
* **Contextual Degradation of Exit 2 Rejections:** It remains unknown how many consecutive deterministic rejections (Exit 2 via PreToolUse hooks) an agent can experience before it falls into an unrecoverable cognitive deadlock, repeatedly failing to find an alternative execution path.  
* **Property-Based Testing Boundaries:** Can an autonomous agent reliably abstract complex, stateful database transactions and API integrations into pure mathematical invariants suitable for property-based testing, or is agentic PBT practically constrained to algorithmic data transformations?

#### **Works cited**

> 1. Settings files and precedence \- Claude Code Docs, [https\://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
> 2. Week 13 · March 23–27, 2026 \- Claude Code Docs, [https\://code.claude.com/docs/en/whats-new/2026-w13](https://code.claude.com/docs/en/whats-new/2026-w13)  
> 3. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 4. Advanced setup \- Claude Code Docs, [https\://code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup)  
> 5. Measuring the True Cost of Agentic Loops | by Mohit Sewak, Ph.D., [https\://medium.datadriveninvestor.com/measuring-the-true-cost-of-agentic-loops-3549aedc8580](https://medium.datadriveninvestor.com/measuring-the-true-cost-of-agentic-loops-3549aedc8580)  
> 6. All settings \- Claude Code Docs, [https\://code.claude.com/docs/en/settings-reference](https://code.claude.com/docs/en/settings-reference)  
> 7. Environment variables \- Claude Code Docs, [https\://code.claude.com/docs/en/env-vars](https://code.claude.com/docs/en/env-vars)  
> 8. Automate actions with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
> 9. Enforcing TDD in Agentic AI CLIs and IDEs | by Shubham Sharma, [https\://medium.com/@shub-sharma/enforcing-tdd-in-agentic-ai-clis-and-ides-f7a3abc24cd8](https://medium.com/@shub-sharma/enforcing-tdd-in-agentic-ai-clis-and-ides-f7a3abc24cd8)  
> 10. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 11. Intercept and control agent behavior with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/hooks](https://code.claude.com/docs/en/agent-sdk/hooks)  
> 12. An Empirical Study on Failures in Automated Issue Solving \- arXiv, [https\://arxiv.org/html/2509.13941v1](https://arxiv.org/html/2509.13941v1)  
> 13. Subagents in the SDK \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/subagents](https://code.claude.com/docs/en/agent-sdk/subagents)  
> 14. Create custom subagents \- Claude Code Docs, [https\://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
> 15. Is Your Benchmark Still Useful? Dynamic Benchmarking for Code, [https\://arxiv.org/pdf/2503.06643?](https://arxiv.org/pdf/2503.06643)  
> 16. Adaptive and AI-Augmented Security Testing: A Systematic Survey, [https\://arxiv.org/pdf/2604.27000](https://arxiv.org/pdf/2604.27000)  
> 17. Adaptive and AI-Augmented Security Testing: A Systematic Survey, [https\://arxiv.org/html/2604.27000v1](https://arxiv.org/html/2604.27000v1)  
> 18. Are Coding Agents Generating Over-Mocked Tests?An Empirical, [https\://andrehora.github.io/pub/2026-msr-agents-over-mocked-tests.pdf](https://andrehora.github.io/pub/2026-msr-agents-over-mocked-tests.pdf)  
> 19. Transforming AR Software Engineering Through Empirical, [https\://vtechworks.lib.vt.edu/bitstreams/415f021f-c322-4768-8cf5-b51c4870b775/download](https://vtechworks.lib.vt.edu/bitstreams/415f021f-c322-4768-8cf5-b51c4870b775/download)  
> 20. Agentic Property-Based Testing:Finding Bugs Across the Python, [https\://arxiv.org/html/2510.09907v1](https://arxiv.org/html/2510.09907v1)  
> 21. Unsupervised Evaluation of Code LLMs with Round-Trip Correctness, [https\://raw.githubusercontent.com/mlresearch/v235/main/assets/allamanis24a/allamanis24a.pdf](https://raw.githubusercontent.com/mlresearch/v235/main/assets/allamanis24a/allamanis24a.pdf)  
> 22. Is Your Benchmark Still Useful? Dynamic Benchmarking for Code, [https\://openreview.net/pdf?id=MNRLUoaUbw](https://openreview.net/pdf?id=MNRLUoaUbw)  
> 23. TDFlow: Agentic Workflows for Test Driven Software Engineering, [https\://arxiv.org/html/2510.23761v1](https://arxiv.org/html/2510.23761v1)