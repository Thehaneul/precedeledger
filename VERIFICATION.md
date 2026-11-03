# PrecedeLedger verification

Date: 3 November 2026. Version: `precedeledger-0.1`.

## Completed local checks

- `pytest test_precedeledger.py -q`: **94 passed in 23.14 seconds**.
- SDK linter: three checks passed.
- SDK semantic validation: passed; PrecedeLedger, eight public methods, five
  reads, three writes, and no constructor arguments.
- Dependency consistency: `pip check` reported no broken requirements.
- Python 3.12.14; genlayer-test 0.29.2; genvm-linter 0.11.0;
  pytest 9.2.0; cloudpickle 3.1.2. Full environment in requirements-lock.txt.
- Direct-mode official SDK archive: v0.3.0-rc7, prepared by prepare_test_sdk.py.
- Runner dependency: py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6.
- SDK notice: a newer runner is available. This package retains the explicitly
  tested runner; the newer one was not tested. No claim of latest-version status.

Exact source SHA-256 is recorded in EVIDENCE.json and PACKAGE_MANIFEST.json.
Raw test and SDK output are included. No failed test run occurred in this build.

## What the checks cover

1. Complete local phone workflow: valid interpretation, immutable saved rules,
   exact-hash partner acceptance, early completion rejection, both prerequisite
   receipts, unlocked final task and completed state.
2. All 512 directed graphs on three nodes, including self-loops, compared with
   Python's graphlib.TopologicalSorter cycle result. Every accepted topological
   order was independently checked against all edges.
3. Each of the six full task orderings, branching prerequisites, explicit
   independence, repeated edges and normalized model ordering.
4. Review/cycle states prevent acceptance and completion.
5. Wrong wallet, stale/wrong hash, duplicate acceptance, duplicate completion,
   separate creator namespaces, per-plan isolation and the 100-plan cap.
6. Hashes bind the original plan, acceptance and completion receipts; the final
   receipt references both predecessor receipts.
7. Strict model output validation: extra/missing keys, omitted rules, duplicate
   rule IDs and JSON keys, unsupported task IDs, malformed edges, partial review
   output, wrong types and blank reasons.
8. One bounded structural retry; persistent invalid output saves nothing.
   Provider errors propagate after one call. No fallback authorizes a plan.
9. Validator disagreement about either interpretation or any rule's edges rejects
   the proposal. Original evidence is checked; reasons are separately audited.
10. A negative audit is not retried; malformed audit responses have a fixed limit.
11. Non-deterministic closures serialize with the original evidence. SDK pickling
    checks were enabled.
12. An explicitly simulated rejection gate checks that rejection happens before
    the contract's first storage write.

## Evidence boundaries

Model responses and audit responses were authored fixtures. Tests verify how
the code treats supplied decisions; they do not prove that real models will infer
the intended edges or resist all prompt attacks. Some structural fixtures use
placeholder prose deliberately; they are not linguistic accuracy examples.

Direct-mode execution is not a hosted validator network. Calling run_validator()
tests the validator function separately; it does not roll back leader-side local
state. The rejection harness is explicitly simulated, not evidence of real
consensus or rollback. No live model reliability percentage is claimed.

A user-operated Studio deployment and bounded walkthrough are now evidenced by
screenshots. No independent on-chain source comparison, finality audit, load
test, security audit or real user validation was performed. Other inputs may
still produce hosted disagreement or REVIEW_REQUIRED.

## Completed bounded Studio check

The user supplied screenshots on 3 November 2026 showing plan 0 progress from
AWAITING_PARTNER through ACTIVE to COMPLETE. Early cards completion was rejected
with the expected prerequisite error. The cards receipt contains two prerequisite
receipt hashes. Plan 1 records the intended two-edge cycle as BLOCKED_CYCLE with
all tasks LOCKED_PLAN. Source code remained unchanged.

One additional attempt omitted task_id and was rejected with
`task_id_must_be_wording_tables_cards`; the corrected input then reached the
planned prerequisite rejection. Both are retained in HOSTED_RESULTS.json.

These are observed screenshot results. Successful transaction IDs and finality
receipts were not supplied; the two error details do show FINALIZED / ERROR and
Accepted consensus history. The summary accompanying the prerequisite rejection
predates that error, so it is not described as a post-error state read. Full
get_plan data and the individual prerequisite receipts were not fetched.

The agreed stop point is reached. No optional tests are required. GitHub
publication and submission remain pending.
