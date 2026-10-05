---
title: "**The Expert-Executor Architecture**"
summary: "Imported unverified source material from Claude Code Testing Research Protocol; verification remains pending."
as_of: 2026-10-02
last_verified: none
reverify_by: 2026-11-01
status: partial
confidence: low
volatility: volatile
sources:
  - id: S0
    url: "legacy/Claude Code Testing Research Protocol.md"
    accessed: 2026-10-02
    locator: "**The Expert-Executor Architecture**"
tag_default: UNVERIFIED
origin: "legacy/Claude Code Testing Research Protocol.md#**The Expert-Executor Architecture**"
tags: [imported, unverified]
aliases: []
related: []
---
## Answer
Imported material; claims have not been verified.

## Conditions
Original source text is preserved below without factual review.

## Detail
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


## Dead Ends

## Open Questions
