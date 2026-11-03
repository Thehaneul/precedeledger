# PrecedeLedger

**Status: local checks and bounded Studio walkthrough passed, 3 November 2026. GitHub publication and submission pending.**

PrecedeLedger turns explicit written prerequisites into a shared task order. Two
participants agree to the saved interpretation; code then prevents a task from
being reported complete before its prerequisites. A circular plan is blocked.
Unclear or unsupported instructions require review.

## A concrete example

A community display needs three jobs:

| Task ID | Job | Assigned participant |
|---|---|---|
| `wording` | Finalize display-card wording | Creator |
| `tables` | Arrange display tables | Partner |
| `cards` | Print the cards and place them on the tables | Partner |

The creator writes:

> Finish the card wording before printing and placing the cards.
> Arrange the tables before printing and placing the cards.

GenLayer interprets the two prerequisites. Code combines the accepted edges,
checks for cycles, and stores an immutable plan. The partner accepts the exact
plan hash. Wording and tables are initially available; cards remains blocked
until both have completion reports from their assigned wallets.

Completion means **the assigned wallet reported the task done**. Neither GenLayer
nor this contract observes physical work, confirms identity, or verifies quality.
It gates completion records; it cannot prevent real-world work from starting.

## Why use GenLayer here?

The shared decision is what the supplied natural-language prerequisites mean.
Each validator independently interprets the same rules. Accepted prerequisites
then constrain both participants' contract actions. This is a small exploration
of shared interpretation, not a claim that every task list needs a blockchain.
For one trusted team, an ordinary workflow app can be simpler. If users directly
enter structured dependency IDs, AI is unnecessary.

The design follows the distinction in GenLayer's [builder fit guidance](https://docs.genlayer.com/developers/intelligent-contracts/when-to-use-genlayer):
interpretive decisions belong in the contract only when their shared outcome
matters. [Non-deterministic evaluation](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
is separated from deterministic state updates.

## Bounded behavior

- Three fixed whole tasks, assigned as above; two different wallet addresses.
- One to six nonblank rules, at most 300 characters each and 1,600 total.
- Only unconditional completion prerequisites; no deadlines, OR dependencies,
  partial tasks, conditional rules, external tasks, payments or generated tasks.
- All numbered rules must be represented. Clear repeated edges are deduplicated
  by code; clear circular edges are retained and blocked by code.
- Any ambiguity or unsupported requirement blocks the entire interpretation.
- Maximum 100 plans per deployment. Keys are scoped to the creator wallet.
- Plans, acceptances and completion receipts are immutable. Corrections require
  a new plan with a new key. Do not use a mistaken plan for further reporting.
- Anyone can create a plan; the named partner must accept before either wallet
  can report completion. This prototype has no Sybil/spam protection.

## Outcomes

| Status | Meaning |
|---|---|
| `REVIEW_REQUIRED` | Rules cannot be safely represented in this model |
| `BLOCKED_CYCLE` | Explicit prerequisites form a circular dependency |
| `AWAITING_PARTNER` | Valid interpretation saved; partner has not accepted |
| `ACTIVE` | Partner accepted; completion reports may follow the prerequisites |
| `COMPLETE` | All three tasks have assigned-wallet completion reports |

`VALID_ORDER` is the graph outcome, not an assertion that work is finished.
Task states distinguish `LOCKED_PLAN`, `WAITING_FOR_PREREQUISITES`,
`READY_TO_REPORT` and `REPORTED_DONE`.

## Public interface

Constructor: no arguments.

| Method | Kind | Purpose |
|---|---|---|
| `get_rules()` | Read | Version, task definitions, policy hash and count |
| `get_plan(plan_id)` | Read | Original plan, interpretation, consent and current summary |
| `get_plan_summary(plan_id)` | Read | Short status, exact hash, tasks and missing prerequisites |
| `get_task_receipt(plan_id, task_id)` | Read | Completion report and prerequisite receipt hashes |
| `get_plan_id(creator, plan_key)` | Read | Recover a saved ID; `-1` means absent |
| `create_plan(plan_key, partner_wallet, rules_text)` | Write | Interpret and save a new plan |
| `accept_plan(plan_id, expected_plan_hash)` | Write | Named partner accepts the saved plan |
| `mark_done(plan_id, expected_plan_hash, task_id)` | Write | Assigned wallet reports completion when unblocked |

IDs start at 0 and follow successful saves. An invalid model response saves
nothing and does not consume the key or ID. A saved REVIEW_REQUIRED or
BLOCKED_CYCLE result is a valid recorded assessment, not a failed transaction.

## Consensus and model-output handling

The leader proposes a strict JSON interpretation. Supporting task definitions and
rule text are attached by code. Validators independently interpret the original
rules, compare every rule's normalized edges and global interpretation, then audit
the proposed reason and meaning. Explanatory wording need not be identical.
Unknown fields, missing rules, invented task IDs, duplicate JSON keys, invalid
edges and blank reasons fail structural validation. There is at most one format
retry per interpretation/audit; a negative audit is never retried into approval.
Provider errors propagate. Invalid output never becomes a successful fallback.

Maximum contract-level model requests: 2 on the leader path and 4 per validator
path (including malformed-output retries). Network/provider retries are outside
this code's control. Only creation calls AI; acceptance and completion are
deterministic. All storage writes occur after accepted interpretation returns.

## Verification

**94 local tests passed**, including one exhaustive comparison of all **512**
directed graphs on these three tasks against Python's independent cycle oracle.
The SDK linter passed three checks; SDK validation recognized eight methods.
See `VERIFICATION.md`, `local_test_results.txt`, and `sdk_check_results.json`.

Tests use authored model fixtures. They establish local code behavior and
validator-path behavior. The separate Studio walkthrough below records observed
hosted outcomes; neither check establishes general live-language accuracy.

## Reproduce locally

Python 3.12 was used. Create a virtual environment, activate it, then:

```bash
python -m pip install -r requirements-lock.txt
python prepare_test_sdk.py
python -m pytest test_precedeledger.py -q
GENVM_VERSION=v0.3.0-rc7 genvm-lint check precedeledger.py --json
```

On PowerShell, set `$env:GENVM_VERSION = 'v0.3.0-rc7'` before the linter command.
`requirements-dev.txt` lists the four direct development dependencies; the lock
file records the complete installed environment. The pinned runner is a tested
reproduction choice, not a claim to use the latest runner. The linter reported
a newer runner; it was not selected or tested here.

## Observed Studio walkthrough

User-reported contract: `0xb3FB34688208Ce42bB54D392f7B90DC397ae0C96`.
The abbreviated deployment label in the screenshots matches this address.

| Observed check | Result |
|---|---|
| Plan 0 interpretation | `VALID_ORDER`: tables and wording both precede cards |
| Partner acceptance | `ACTIVE`, `partner_accepted: true` |
| Early cards report | Execution error: prerequisites not yet reported done |
| Wording report | Cards waits only for tables |
| Tables report | Cards becomes `READY_TO_REPORT` |
| Cards report | Plan 0 `COMPLETE`; all three tasks `REPORTED_DONE` |
| Cards receipt | Two prerequisite receipt hashes; assigned-wallet self-report |
| Plan 1 circular rules | `BLOCKED_CYCLE`; all tasks `LOCKED_PLAN` |

The first early-cards attempt had an empty task ID and failed input validation.
Correcting that field reached the intended prerequisite rejection. Both attempts
are recorded in `HOSTED_RESULTS.json`; the source was unchanged.

Evidence is user-provided screenshots of Accepted-state reads and two rejected
transaction details, not an independent chain audit. The successful write
transaction receipts, chain ID, deployed-source comparison and full saved rule
text were not independently obtained. The cards receipt's two hashes were
counted; its predecessor receipts were not separately compared. Two observed
interpretation outcomes do not establish general model reliability or production
readiness. See `HOSTED_RESULTS.json` for the full evidence boundaries.

## GitHub and submission

The agreed Studio stop point has been reached. `PHONE_WALKTHROUGH.txt` remains a
reproduction checklist; do not rerun it on this deployment. Next, publish the
reviewed files to the `precedeledger` repository and use
`GITHUB_AND_SUBMISSION.txt` for the prepared description.

Repository URL and submission receipt remain pending. The package contains no
keys or account credentials. Keep real confidential work out of the public
prototype. Check current official submission requirements before submitting;
no contest eligibility or reward is promised.

## Related work and differentiation

The general ideas of dependency graphs and task coordination are established.
[MissionMesh](https://github.com/tanphung/missionmesh-genlayer) already describes
GenLayer task graphs, agent assignments and work acceptance. PrecedeLedger is a
narrower explicit-prerequisite and cycle-blocking experiment with fixed tasks,
partner consent and self-reported completion. It does not claim to invent these
concepts. See `IDEA_RESEARCH.md` for the three-idea comparison and search limits.

Earlier user-owned prototypes informed the SDK setup, storage, hash and validator
patterns. Previous contracts and deployments were not modified.
