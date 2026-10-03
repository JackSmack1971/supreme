---
title: "**Lifecycle Engineering Practices for Novices**"
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
    locator: "**Lifecycle Engineering Practices for Novices**"
tag_default: UNVERIFIED
origin: "legacy/Global Claude Code Control Plane Architecture for Novice-Driven Software Development.md#**Lifecycle Engineering Practices for Novices**"
tags: [imported, unverified]
aliases: []
related: []
---
## Answer
Imported material; claims have not been verified.

## Conditions
Original source text is preserved below without factual review.

## Detail
| **2\. Evidence/source** | The auto-allow Bash sandbox isolates filesystem and network operations for shell commands, but file tools (Read, Write), MCP servers, and hooks execute on the host. Unattended runs with \--dangerously-skip-permissions demand external containerization (e.g., Docker, dev containers)10. |
| **3\. Evidence strength** | Strong (Tier 1, Official Claude Code Documentation). |
| **4\. Mechanism implicated** | Bash sandbox (sandbox.filesystem), permissionMode, \--dangerously-skip-permissions26. |
| **5\. Global \~/.claude candidate?** | Yes. Global sandbox policies (sandbox.filesystem.denyWrite) must be defined in \~/.claude/settings.json26. |
| **6\. Enforcement strategy** | Deterministic. Layering OS-level isolation (containers) beneath the application-level sandbox proxy10. |
| **7\. Cost/context implications** | Container initialization introduces minor latency but prevents catastrophic host system corruption. |
| **8\. Security implications** | Critical. Prevents path traversal, credential exfiltration, and the accidental deletion of user host files during autonomous implementation sequences26. |
| **9\. Open question remaining** | Can the control plane seamlessly bootstrap a dev container environment for a novice without requiring preexisting Docker knowledge? |

| Attribute | Detail |
| :---- | :---- |
| **1\. Finding** | **Real-time observability of context saturation and cache performance is strictly required to prevent runaway costs and context collapse.** |
| **2\. Evidence/source** | The context window fills rapidly during complex tasks. Claude Code exposes context\_window and prompt\_cache objects to stdin for custom status line scripts, tracking hit ratios and TTL expirations30. |
| **3\. Evidence strength** | Strong (Tier 1, Official Claude Code Documentation). |
| **4\. Mechanism implicated** | statusLine configuration in settings, context\_window.used\_percentage, prompt\_cache.hit\_ratio28. |
| **5\. Global \~/.claude candidate?** | Yes. The statusLine shell script should reside in \~/.claude/ and be referenced by global settings30. |
| **6\. Enforcement strategy** | Deterministic shell script rendering UI updates based on JSON telemetry. |
| **7\. Cost/context implications** | High observability allows the novice to detect when prompt caching fails, saving significant API costs by pausing and compacting the context30. |
| **8\. Security implications** | None directly, though status line scripts execute within the host context and must be protected from tampering. |
| **9\. Open question remaining** | How can the status line effectively communicate the financial implications of a cold cache miss to a novice without causing undue anxiety? |

## **Lifecycle Engineering Practices for Novices**

A system targeting software engineering novices must translate abstract computer science concepts into guided, conversational workflows. Novices frequently rush from a vague idea directly to implementation—a failure mode colloquially termed "vibe coding." This approach results in fragile, misaligned systems that collapse under their own technical debt. The control plane must enforce a structured SDLC, substituting technical jargon with progressive disclosure and guided elicitation.

### **Phase 1: Discovery and Definition**

**Ideation and Problem Framing** The ideation process must be intercepted before any code is generated. The control plane enforces a "Problem Frames" methodology, based on Michael Jackson's requirements engineering framework31. Problem Frames dictate that the structure of the real-world problem must be defined independently of the software solution. The agent is instructed to pause implementation and act as a domain interviewer. It extracts physical, logical, and business constraints from the novice by asking situational questions rather than technical ones.  
**Goal-Oriented Requirements Engineering (KAOS)** To define functional and nonfunctional requirements without overwhelming the user, the control plane utilizes Goal-Oriented Requirements Engineering principles, specifically the KAOS (Keep All Objectives Satisfied) methodology33. Instead of prompting for "nonfunctional latency thresholds" or "concurrency limits," the agent asks, "How fast does this application need to feel?" or "What should happen if a thousand people try to use this at the exact same time?" The control plane translates these conversational inputs into durable technical artifacts. These performance budgets and scaling constraints are written to a path-scoped .claude/rules/requirements.md file, ensuring they are automatically loaded into context only when relevant34.  
**Scope Definition and Feasibility Assessment** To aggressively combat scope creep, the system mandates a feasibility assessment. Before the novice's idea is approved for implementation, the control plane spawns a specialized, read-only Explore subagent17. Operating in the background, this subagent utilizes WebSearch and WebFetch to determine if third-party APIs or libraries exist to satisfy the proposed features. It compiles a feasibility report, highlighting potential technical roadblocks and forcing the novice to actively refine the scope before proceeding.

### **Phase 2: System Design and Strategy**

**Build-vs-Buy Decisions and Stack Selection** Decisions regarding the technology stack are explicitly deferred until evidence of feasibility exists. Novices lack the context to evaluate the trade-offs between a complex microservices architecture and a monolithic application. The control plane prevents the novice from over-engineering the system out of excitement. It enforces the simplest, most reproducible stack (e.g., a monolithic architecture using SQLite and vanilla JavaScript) unless the KAOS requirements document explicitly demands higher complexity.  
**Architectural Design and Threat Modeling** Architecture must be verified prior to implementation. The control plane automates threat modeling utilizing the STRIDE framework (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)35. The agent analyzes the proposed data flow and prompts the novice with plain-English risk scenarios. For example, instead of asking about "Elevation of Privilege," the agent asks, "If a regular user figures out how to access the admin panel, what is the worst damage they could do?" The user's responses dictate the required implementation of encryption, authentication mechanisms, and logging infrastructure.  
**Data Modeling and API Interface Contracts** Agentic implementation fails catastrophically when interfaces remain fluid across multiple turns. To mitigate this, the control plane enforces Contract-First API Design. Using JSON Schema, the agent drafts the exact inputs, outputs, and data types of every system component37. This durable artifact acts as a rigid boundary for the implementation phase. If a coding agent hallucinates an endpoint or alters a payload structure, the contract validation—enforced via a deterministic PostToolUse hook—catches the discrepancy immediately and forces a reversion.

### **Phase 3: Implementation Engine**

**Project Scaffolding and Dependency Selection** Project scaffolding must not be executed ad-hoc. The control plane utilizes Bash tools to initialize the repository structure, but a PreToolUse hook intercepts all package installation commands (e.g., npm install, pip install). This hook checks proposed dependencies against a known-safe registry or requires explicit human approval, mitigating the risk of supply-chain attacks and malicious typosquatting3.  
**Implementation Sequencing and Agent Teams** Implementation is parallelized using the Agent Teams mechanism39. The control plane spawns a Lead Agent that divides the JSON Schema contracts into discrete, manageable tasks. Task management is handled via the built-in TaskCreated and TaskCompleted events3. Crucially, the control plane limits tasks to highly self-contained units (e.g., writing a single function or a specific test file). This limitation is derived from empirical SWE-bench research, which proves that longer agent trajectories correlate strongly with logical failures and context collapse41. By forcing frequent task completions, the system maintains a high prompt cache hit ratio and prevents cascading hallucination13.  
**Testing Strategy and Defending Against Reward Hacking** Testing represents the most vulnerable phase of autonomous software development. Highly capable models consistently exhibit "specification gaming" or "reward hacking," wherein they modify test suites to artificially pass rather than fixing the underlying logical flaws21. The control plane enforces a strict software boundary: implementation agents are mathematically denied write access to test files, continuous integration (CI) configurations, and test runner configurations (e.g., conftest.py) via the disallowedTools or sandbox.filesystem.denyWrite mechanisms17. A completely separate, read-only Evaluation Subagent reviews the code, while deterministic host scripts execute the tests and pipe the stdout back for analysis22.

### **Phase 4: Delivery and Operations**

**Deployment Strategy and Observability** Deployment requires transitioning the software from local execution to a production environment. The control plane guides the novice through the separation of environment variables, ensuring that cryptographic secrets are properly masked. Secret masking is enforced via the sandbox.credentials settings, which substitute real credentials with placeholder sentinels during sandboxed command execution, preventing the LLM from accidentally exfiltrating keys in its output logs10.  
**Documentation, Release Readiness, and Maintenance** Documentation is generated continuously, not deferred to the end of the project. A background subagent monitors the repository state via WorktreeCreate and FileChanged hooks, automatically drafting Architectural Decision Records (ADRs) and README.md updates3. The system does not declare Minimum Viable Product (MVP) completion until the independent Evaluation Subagent verifies that all API contracts are fulfilled, test coverage meets the generated thresholds, and all STRIDE threat mitigations are demonstrably implemented in the code.

## **Lifecycle Automation, Gates, and Durable Artifacts**

To prevent chaotic "vibe coding" while avoiding the paralyzing bureaucracy of traditional waterfall methodologies, the control plane strictly delineates what is automated, what requires explicit user consent, and what must be deferred.

### **1\. Safely Automated Stages**

Certain repetitive or highly structured tasks are entirely automated to reduce cognitive load on the novice:

* Project scaffolding generation, boilerplate creation, and syntax formatting.  
* Execution of test suites and calculation of code coverage metrics.  
* Generation of STRIDE threat modeling scenarios based on defined data flows.  
* Context window compaction (via autoCompactEnabled) and prompt cache optimization15.

### **2\. Requires Explicit User Decisions**

Critical junctions requiring domain knowledge, business logic, or severe security implications demand explicit human approval:

* Approval of final functional requirements and acceptance criteria.  
* Inclusion of third-party dependencies (due to supply chain vulnerabilities).  

## Dead Ends

## Open Questions
