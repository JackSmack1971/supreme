---
title: "**3\\. Deferred Decisions**"
summary: "Imported unverified source material from Global Claude Code Control Plane Architecture for Novice-Driven Software Development; verification remains pending."
as_of: 2026-10-02
last_verified: none
reverify_by: 2026-11-01
status: partial
confidence: low
volatility: volatile
sources:
  - id: S0
    url: "legacy/Global Claude Code Control Plane Architecture for Novice-Driven Software Development.md"
    accessed: 2026-10-02
    locator: "**3\\. Deferred Decisions**"
tag_default: UNVERIFIED
origin: "legacy/Global Claude Code Control Plane Architecture for Novice-Driven Software Development.md#**3\\. Deferred Decisions**"
tags: [imported, unverified]
aliases: []
related: []
---
## Answer
Imported material; claims have not been verified.

## Conditions
Original source text is preserved below without factual review.

## Detail
* Execution of destructive host environment operations (intercepted via PreToolUse hooks)3.  
* Final MVP sign-off and deployment authorization.

### **3\. Deferred Decisions**

To prevent analysis paralysis, complex architectural decisions are deferred until empirical evidence justifies them:

* Cloud provider selection and deployment topology are deferred until the local MVP is fully functional.  
* Database scaling and sharding strategies are deferred until initial data models are validated against realistic loads.

### **4\. Minimum Durable Artifacts**

The control plane relies on a minimum set of durable configuration and context files to maintain systemic state across sessions:

* \~/.claude/settings.json: Global control plane enforcement (hooks, sandboxing, models)4.  
* .claude/rules/requirements.md: Path-scoped functional goals derived from KAOS elicitation34.  
* .claude/rules/contracts.md: JSON Schema API contracts defining system boundaries37.  
* .claude/agents/\*.md: Task-specific subagent definitions with restricted toolsets17.  
* MEMORY.md: The auto-memory index recording persistent architectural decisions34.

### **5\. Pre-Implementation Gates**

Before a single line of implementation code is written, the following gates must be cleared:

* **Gate A:** The API Contract (JSON Schema) and Data Model must be rigidly defined and approved by the user. Implementation agents are blocked from proceeding without these boundaries.  
* **Gate B:** The test harness must be locked via filesystem permissions or disallowedTools, preventing the implementation agent from tampering with the evaluation metrics17.

### **6\. Post-MVP Gates**

Before declaring the MVP complete, the system enforces the following verifications:

* **Gate C:** An independent Evaluation Subagent must parse the test results. The implementation agent is forbidden from grading its own work to prevent metric decoupling22.  
* **Gate D:** All STRIDE security mitigations identified in the design phase must be mapped to implemented code paths.

### **7\. Balancing Bureaucracy and Flexibility**

The control plane avoids waterfall bureaucracy by allowing rapid, unconstrained iteration *within* a given state, while using deterministic hooks to rigidly enforce the transitions *between* states. A novice may freely brainstorm and pivot during the ideation phase, but a UserPromptSubmit hook intercepts any attempt to invoke the Write or Bash tools until the requirements state is formally completed.

## **Minimal Complete Lifecycle State Machine**

The control plane operates as a strict finite state machine, preventing the novice from bypassing critical architectural steps. Transitions between states are monitored and enforced by SessionStart, UserPromptSubmit, and PreToolUse hooks1.

* **State 0: IDEATION\_AND\_FRAMING**  
  * *Action:* The agent acts solely as a KAOS requirements elicitor. It queries the user regarding domain constraints and physical realities.  
  * *Constraint:* Execution of Bash, Write, and Edit tools is universally blocked by PreToolUse hooks.  
  * *Transition:* The user approves the translated problem frame and functional goals, triggering a transition script.  
* **State 1: ARCHITECTURE\_AND\_CONTRACTS**  
  * *Action:* The agent drafts JSON Schema contracts and generates STRIDE threat models based on the approved requirements.  
  * *Constraint:* Only Read and WebSearch tools are permitted.  
  * *Transition:* The user explicitly approves the API interfaces and security risk mitigations.  
* **State 2: SCAFFOLDING\_AND\_SETUP**  
  * *Action:* Base project structure is generated. External dependencies are vetted and installed.  
  * *Constraint:* A transition script executes, applying file-system locks to test framework configurations, securing them against future agent edits22.  
  * *Transition:* Directory structure and initial commits are verified by a background subagent.  
* **State 3: AGENTIC\_IMPLEMENTATION**  
  * *Action:* The Lead Agent utilizes Agent Teams to delegate localized tasks to specialized subagents. Subagents operate concurrently within isolation: worktree environments17.  
  * *Constraint:* Task length is strictly limited by maxTurns to prevent context collapse17.  
  * *Transition:* All pending tasks in the shared task list are marked complete, triggering the TaskCompleted event3.  
* **State 4: INDEPENDENT\_VERIFICATION**  
  * *Action:* An isolated Evaluation Subagent executes the test suite. The implementation LLM is denied write access to the source code during this phase.  
  * *Constraint:* Test failures route the state machine back to State 3 for targeted remediation.  
  * *Transition:* Achieving 100% contract fulfillment and passing all unit tests without evidence of specification gaming.  
* **State 5: RELEASE\_AND\_OBSERVABILITY**  
  * *Action:* Final documentation is compiled into ADRs. Deployment scripts are audited to ensure cryptographic credentials are mathematically masked via the sandbox26.  
  * *Transition:* The codebase is tagged as MVP, and the control plane shifts to a maintenance monitoring state.

## **Derived Requirements and Unresolved Questions**

### **A. Design Requirements Derived from the Evidence**

> 1. **Deterministic Global Hooks:** The control plane must install a suite of shell-based PreToolUse, TaskCreated, and TaskCompleted hooks in the global \~/.claude/settings.json file. These hooks are the sole mechanism capable of enforcing lifecycle gates and preventing catastrophic agent actions1.  
> 2. **Strict Context Isolation:** All localized implementation work must be delegated to subagents defined in \~/.claude/agents/. This architecture prevents large file reads and exploratory data from polluting the main session's context window, preserving prompt cache hit ratios and reducing API costs12.  
> 3. **Read-Only Verification Boundaries:** To prevent specification gaming and reward hacking, the system must utilize file-system permissions or the disallowedTools array to guarantee that agents writing implementation code cannot modify the tests evaluating that code17.  
> 4. **Progressive Pedagogical Disclosure:** The system must utilize UserPromptSubmit hooks to periodically interject and ask clarifying conceptual questions. This forces the novice to engage with system design and prevents the severe skill atrophy associated with complete cognitive offloading to AI6.  
> 5. **Windows Portability and Shell Management:** The system must explicitly manage Windows environments by generating .ps1 wrappers for all hooks, configuring defaultShell: powershell, and explicitly managing timeout limits (BASH\_DEFAULT\_TIMEOUT\_MS) and terminal repainting variables (CLAUDE\_CODE\_ALT\_SCREEN\_FULL\_REPAINT)4.

### **B. Anti-Requirements (What the Control Plane MUST NOT Do)**

> 1. **Do not rely on CLAUDE.md for security or lifecycle enforcement.** Model instructions are advisory, non-deterministic, and easily bypassed by hallucination or context window overflow. Safety enforcement must be deterministic and reside in the settings layers2.  
> 2. **Do not allow implementation agents to self-evaluate.** The system must never allow the entity generating the code to report on its own success. Doing so guarantees metric decoupling and inevitable reward hacking22.  
> 3. **Do not force architectural terminology on the novice.** The system must not prompt the user to provide "UML diagrams," "microservice boundaries," or "database schemas." It must elicit these constraints organically through plain-language domain questioning via the KAOS methodology33.  
> 4. **Do not allow unattended global execution.** Operations must run within isolation: worktree or via strictly sandboxed environments. The \--dangerously-skip-permissions flag must never be enabled without an external, OS-level container boundary protecting the host machine10.

### **C. Unresolved Questions**

> 1. **Hook Distribution and Execution Policies:** How can global hook binaries (e.g., Python scripts or compiled executables) be safely distributed, updated, and executed in \~/.claude/hooks/ across diverse operating systems without triggering heuristic antivirus software or requiring complex manual PowerShell execution policy overrides?  
> 2. **Dynamic Cache Tuning:** How can the control plane dynamically parse the prompt\_cache status line object telemetry to optimize the autoCompactWindow setting in real-time, effectively balancing API token costs against the degradation of conversational context?  
> 3. **Evaluating the Evaluator:** If an independent Evaluation Subagent is utilized to prevent reward hacking by the implementation agent, what mechanisms prevent the Evaluation Subagent itself from hallucinating false-positive test results without requiring the novice to manually audit the raw command line stdout?

#### **Works cited**

> 1. claude-howto/06-hooks/README.md at main \- GitHub, [https\://github.com/luongnv89/claude-howto/blob/main/06-hooks/README.md](https://github.com/luongnv89/claude-howto/blob/main/06-hooks/README.md)  
> 2. Claude Code settings.json, hooks, and permissions: a practical guide, [https\://claudefolio.com/guides/claude-code-settings-hooks-permissions](https://claudefolio.com/guides/claude-code-settings-hooks-permissions)  
> 3. Hooks reference \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
> 4. Environment variables \- Claude Code Docs, [https\://code.claude.com/docs/en/env-vars](https://code.claude.com/docs/en/env-vars)  
> 5. Extend Claude Code \- Claude Code Docs, [https\://code.claude.com/docs/en/features-overview](https://code.claude.com/docs/en/features-overview)  
> 6. Automate actions with hooks \- Claude Code Docs, [https\://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
> 7. Quickstart \- Claude Code Docs, [https\://code.claude.com/docs/en/agent-sdk/quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)  
> 8. Fullscreen rendering \- Claude Code Docs, [https\://code.claude.com/docs/en/fullscreen](https://code.claude.com/docs/en/fullscreen)  
> 9. Tools reference \- Claude Code Docs, [https\://code.claude.com/docs/en/tools-reference](https://code.claude.com/docs/en/tools-reference)  
> 10. Choose a sandbox environment \- Claude Code Docs, [https\://code.claude.com/docs/en/sandbox-environments](https://code.claude.com/docs/en/sandbox-environments)  
> 11. SWE-Bench Pro \- Scale AI, [https\://static.scale.com/uploads/654197dc94d34f66c0f5184e/SWEAP\_Eval\_Scale%20(9).pdf](https://static.scale.com/uploads/654197dc94d34f66c0f5184e/SWEAP_Eval_Scale%20\(9\).pdf)  
> 12. How Claude Code uses prompt caching, [https\://code.claude.com/docs/en/prompt-caching](https://code.claude.com/docs/en/prompt-caching)  
> 13. How Claude Code uses prompt caching, [https\://code.claude.com/docs/en/prompt-caching?stixel\_click=eyJzIjoiNjc4MGI5YjctYjczMy00YzEyLWJlMmItNWVlZTg0ZTM5ZGYyIn0%3D\&fcdaa149\_sort\_date=desc](https://code.claude.com/docs/en/prompt-caching?stixel_click=eyJzIjoiNjc4MGI5YjctYjczMy00YzEyLWJlMmItNWVlZTg0ZTM5ZGYyIn0%3D&fcdaa149_sort_date=desc)  
> 14. Claude code docs map, [https\://code.claude.com/docs/en/claude\_code\_docs\_map](https://code.claude.com/docs/en/claude_code_docs_map)  
> 15. Manage costs effectively \- Claude Code Docs, [https\://code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs)  

## Dead Ends

## Open Questions
