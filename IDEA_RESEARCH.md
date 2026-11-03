# New GenLayer project selection — 3 November 2026

## Decision

Build **PrecedeLedger**, a small prototype for interpreting explicit written task
prerequisites, blocking cycles, and enforcing the agreed completion order.
This is a bounded contribution experiment, not validated demand or a prediction
of commercial success, project acceptance, XP or rewards.

## Three candidates

| Candidate | Practical use | GenLayer decision | Differentiation and effort | Decision |
|---|---|---|---|---|
| Duplicate-report registry | Link differently worded reports of the same issue | Whether two supplied reports describe the same issue | Distinct from our seven projects, but an existing GenLayer Dedup Registry directly covers this; false merges and candidate selection widen testing | Do not build this round |
| Milestone evidence gate | Decide whether submitted work meets a frozen milestone | Evidence satisfies the parties' acceptance criteria | Recognized GenLayer use case, but much of its rubric-and-progression logic repeats ExplainGate and scope-related work; genuine delivery evidence adds complexity | Defer |
| Written prerequisite contract | Agree what must happen before another task can be reported done | Meaning and completeness of explicit before/after rules | Different from our previous purposes; deterministic cycle detection and permission tests are bounded; related GenLayer coordination work exists | Selected |

The assessment above is design judgment. It is not a quantified market ranking.

## Existing projects we must not repeat

| Our earlier project | Core purpose | Difference here |
|---|---|---|
| SourceRoots | Evidence-origin relationships | Interprets task precedence, not sources |
| HoldoutLedger | Experiment train/test group separation | Detects cyclic prerequisites and gates reports |
| ScopeHandshake | Included work versus approved extra work | Assesses order of fixed work, not whether work is in scope |
| NoticeParity | Translation fact preservation and reuse | Builds a directed task graph from supplied rules |
| ExplainGate | Learner explanation assessment and checkpoint progress | No grading; branching prerequisites and cycle detection |
| QueuePact | Route requests to a team and record acknowledgement | No routing; task owners are fixed and prerequisites govern later actions |
| CommonPick | Intersect two participants' acceptable options | No option selection; agreed dependency relations govern progress |

## Public sources checked

1. GenLayer builder-fit guidance:
   https://docs.genlayer.com/developers/intelligent-contracts/when-to-use-genlayer
   Shared interpretation needs a meaningful contract consequence. A normal task
   app would be simpler if all participants already trust one operator.
2. GenLayer non-deterministic execution:
   https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism
   Custom leader/validator evaluation is separated from deterministic writes.
3. GenLayer testing guidance:
   https://docs.genlayer.com/developers/intelligent-contracts/testing
   Local direct-mode fixtures are useful before hosted integration checks.
4. GenLayer setup:
   https://docs.genlayer.com/developers/intelligent-contracts/tooling-setup
   Python tooling, SDK validation and hosted Studio remain documented paths.
5. GenLayer deployment guidance:
   https://docs.genlayer.com/developers/intelligent-contracts/deploying
   Execution outcomes must be checked separately from transaction finalization.
6. Existing duplicate registry, reviewed at README level:
   https://github.com/Ritapossible/GenLayer-Dedup-Registry
   Describes semantic deduplication of bug reports and other submissions. This is
   direct prior art for the first candidate; its README reports verification gaps.
7. Existing coordination project, reviewed at README level:
   https://github.com/tanphung/missionmesh-genlayer
   Describes task decomposition, dependency graphs, agent assignments, work
   assessment and budget accounting. It is relevant prior work, not an independently
   audited performance benchmark.
8. Name collision avoided:
   https://planlatch.com/
   PlanLatch is already used for a Shopify QA product, so we did not use it.

An exact-name public web query and GitHub repository-name query did not return an
exact PrecedeLedger project match in this check. This is a limited discovery check,
not exhaustive novelty research, trademark clearance or assurance of uniqueness.

## Scope pressure test

- AI is needed only for language-to-prerequisite interpretation; graph checking,
  hashes, wallet permissions and state changes belong in deterministic code.
- A participant cannot silently replace the creator's rule text or accepted graph.
- Cycles are recorded and blocked, not silently fixed by the model.
- Unknown conditions must block the entire plan, rather than disappear.
- Completion is wallet testimony. The prototype must never imply verified work.
- Three tasks and six rules bound cost and make the live walkthrough manageable.
- Two different addresses do not establish two distinct humans.
- The live walkthrough has a fixed stop point; do not add optional tests after it.

## Technical choice

Current installed tools resolved to genlayer-test 0.29.2 and genvm-linter 0.11.0.
The official documentation still showed the source dependency header used here.
The known runner v0.3.0-rc7 was explicitly prepared for reproducible local tests.
SDK validation passed but noted a newer runner. Hosted behavior remains untested.
