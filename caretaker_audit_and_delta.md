# Caretaker Prompt: Audit and Delta Log (2026-10-02)

Basis: your project principles (Output Contract Primacy, Phase Gate Pattern, Extrinsic Self-Correction, Declarative over Procedural, Confidence Tagging, Dangling References, no aspirational language) and the Reference Anchors. Benchmarks are not claimed for the Caretaker itself; the metrics below are structural and measured on the files, not performance claims.

## strategic_overview

v1 has a strong truth doctrine (interrogation, source hierarchy, untrusted-content rule, discovery/dead-ends). Its weaknesses are structural: the output contract is buried, six referenced artifacts have no schema, verification is self-attested, and several rules cannot be measured. v2 keeps the doctrine and adds a contract, precedence, four evidence gates, and an executable validator. [ESTIMATED: structural assessment against project principles; no runtime A/B performed]

Taxonomic position: Self-Improvement & Calibration → Reflection & Correction → CoVe, composed with Tool Use (ReAct+CoVe composite); gates implement extrinsic verification (code as oracle). Calibration branch: tag grammar and abstention.

## technical_breakdown (severity-tiered)

### CRITICAL
| ID | Defect | Principle violated | Fix in v2 |
|---|---|---|---|
| C1 | Output schema (frontmatter, tags, report) is spread across `agent_optimized_format` and `reporting`, positions 5 and 7 | Output Contract Primacy | `<output_contract>` is block 1 |
| C2 | Dangling references: changelog, backlog, index, tool-registry, "dead-ends section" have no path, no schema, no bootstrap rule | Dangling references = critical | Register schemas, fixed filenames, create-if-absent rule; Dead Ends is a required heading slot |
| C3 | No extrinsic verification: "verify content stays true", "demonstrably works" are self-attested | Phase Gate / Extrinsic Self-Correction | Gates G1-G4 with concrete exit evidence; `validate_repo.py` exit 0 |
| C4 | Stale files remain `status: verified` after `reverify_by` passes; consumers read stale facts as verified | Truth doctrine itself | `stale` status; validator error STALE_UNMARKED; consumer-visible |
| C5 | Existing repository files are not covered by the untrusted-data rule; a repo written by agents is a poisoning surface | Adversarial robustness | Repo files declared claims-to-verify; injection-suspect backlog type |

### HIGH
| ID | Defect | Fix |
|---|---|---|
| H1 | No precedence when rules conflict (truth vs completeness vs size) | `<precedence>` ladder, conflicts logged |
| H2 | "impact", "volatility", "load-bearing", "independent", "reasonable load" undefined | Defined; priority score formula; token caps |
| H3 | `confidence` field has no scale; tags lack source linkage (sources are file-level only) | high/medium/low definitions; `[VERIFIED date S#]` ties claim to source id and locator |
| H4 | Procedural numbered lists for reasoning-capable model | Declarative obligations; sequence kept only for true dependencies (preconditions) |
| H5 | Research loop has no stop rule; unattended runs block on "confirm" | 3-attempt cap; G4 defers to pending-confirm backlog when unattended |
| H6 | Report is last output; lost if context exhausts | Report written to `reports/` before chat; changelog written in same batch as edit |
| H7 | Discovery test has no pre-registered pass criterion | G2: criterion and falsifier written before the run; two reproductions |

### MEDIUM
| ID | Defect | Fix |
|---|---|---|
| M1 | "You love this repository", "worst possible outcome": aspirational/affective | Removed; replaced by precedence ladder |
| M2 | No size metric for "fast ingestion" | ≤1,500 token target, split above 4,000 [ESTIMATED defaults] |
| M3 | Unlimited relative-time ban is unchecked | Validator warning RELATIVE_TIME |
| M4 | No secret detection mechanism | Validator SECRET error (regex heuristic) |

## engineered_implementation

Files delivered: `knowledge_caretaker_system_prompt_v2.md`, `validate_repo.py`, this log.

Validator test results (run 2026-10-02, PyYAML 6.0.3):
| Case | Expected | Observed |
|---|---|---|
| Valid sample repo | exit 0 | exit 0, 0 errors [VERIFIED 2026-10-02: ran locally] |
| Deliberately broken file (stale, bad enum, bad URL, dead link, missing headings, undated/unsourced tag, secret, unindexed) | exit 1 | exit 1, 10 errors, 2 warnings [VERIFIED 2026-10-02: ran locally] |
| Untagged factual line | warning | 1 warning (heuristic) [VERIFIED 2026-10-02: ran locally] |

Size: v1 1,074 words / 6,994 chars; v2 1,270 words / 8,718 chars (about +24.7% by chars÷4) [ESTIMATED: chars÷4 token proxy]. The increase buys the contract, gates, and precedence; the prose was compressed (affective and procedural text removed). CoD-style compression headroom of 35-58% on redundant procedural content is reported in your project principles [REPORTED: project principles]; v2 has little redundant procedure left, so I do not expect that range to apply.

Delta log:
| Section | Before | After | Technique |
|---|---|---|---|
| Position 1 | role | output_contract | Output Contract Primacy |
| role | affective, 5 sentences | 2 sentences | Density |
| session_start | 3 numbered steps | preconditions + selection formula | Declarative; dependency-only sequence |
| truth_doctrine | 7 bullets | same doctrine + 3-attempt cap, repo-files-untrusted, relative-time rule | Calibration; adversarial defense |
| discovery | 4 steps | G2 gate with falsifier | Extrinsic verification |
| maintenance_loop, change_discipline | separate | merged into session_obligations + invariants | De-duplication |
| reporting | 1 sentence | metric-bearing schema in contract | Measurable outputs |

### Refinement execution

| Item | Result | Target errors before → after | Valid sample errors before → after | Broken sample errors before → after |
|---|---|---:|---:|---:|
| 1 | Bootstrapped the four missing registers and made a first validator sweep. The target had 27 errors before and 33 after: four missing-register errors disappeared, while ten index-path errors appeared because the existing validator could not parse paths with spaces. The target corpus still lacks v2 frontmatter and has hard-size violations; a full factual migration was not safe without source review. Sample repositories were created at this checkpoint, so there was no pre-item sample run. | 27 → 33 | n/a → 0 | n/a → 4 |
| 3 | Added `--write-index` generation from frontmatter and fixed index parsing for paths containing spaces. | 33 → 23 | 0 → 0 | 4 → 4 |
| 2 | Added a deterministic N=5 source-linked claim sampler and the re-fetch/review agent protocol. The real target had zero eligible `[VERIFIED]` claims; a five-claim valid sample was selected reproducibly and its claims were checked against the official Python 3.14.8 documentation, lines 90–127. | 23 → 23 | 0 → 0 | 4 → 4 |

Item 4 policy confirmed by the user: documentation changes should auto-open PRs; require human merge for correct, deprecate, remove, and schema changes; allow auto-merge only for `last_verified`/`reverify_by` bumps with unchanged claims. This repository has no PR automation to apply that policy. Item 5 is deferred because the target currently has 13 Markdown files, below the 50-file threshold.

Item 2 sample source: [Python 3.14.8 `random` documentation](https://docs.python.org/3/library/random.html), accessed 2026-10-02, sections `random.choice` and `random.sample` (lines 90–127). The source supports all five temporary fixture claims used to exercise the sampler.

Limits:
- The validator checks form, not truth. It cannot tell whether a source supports a claim; G1 still depends on the agent re-reading the fetched text. [UNKNOWN: no rate of G1 failures measured]
- Untagged-line detection is a heuristic. Secret regex is a heuristic.
- Interval days (30/90/365), size caps, and priority weights are defaults I chose; no empirical anchor. [ESTIMATED]

## refinement_path (task queue)

1. Run v2 against a real repository copy and record validator error counts before/after the first sweep (supplies a baseline; none exists now).
2. Add a claim-level spot-check agent: sample N [VERIFIED] claims per session, re-fetch the source, compare. Default N = 5 (confirm or change). Strengthens G1 beyond self-check.
3. Generate INDEX.md from frontmatter in the validator (`--write-index`) to remove the hand-sync failure mode.
4. Open decision, from your documentation-PR automation item: should VERIFIED findings auto-open PRs? Stated default: auto-open the PR for all changes, require a human merge gate only for correct, deprecate, remove, and schema changes; allow auto-merge for pure `last_verified`/`reverify_by` bumps with unchanged claims. Confirm or override.
5. Add a contradiction detector (shared-tag files with differing numeric claims) once ≥50 files exist.
