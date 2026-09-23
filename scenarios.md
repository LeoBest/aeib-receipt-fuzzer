# SMAOS Scenarios (v0.3.0 / v0.3.1)

This document lists the eight wire-fault conformance scenarios shipped with SMAOS.
They are the canonical inputs for `verify.sh`, `docker compose up`, and the
`GET /api/scorecard` endpoint.

## What This Tests

Whether an agent harness correctly preserves uncertainty (`dispatched_unconfirmed`),
detects idempotency/mutation conflicts (`CONFLICT`), and enforces response schema
contracts (`INVALID_INPUT`) when external settlement evidence is absent or corrupted —
preventing the "Container Fallacy" measured by DEMM-Bench (arXiv:2606.20634).

## What This Does NOT Test

LLM intelligence, prompt toxicity, model capability, or internal policy routing
logic. See `LIMITATIONS.md` for the full scope boundary.

## Scenario Table (8 Scenarios)

| Scenario ID                    | Transport / Wire Event                     | Agent SDK Claim   | Expected Disposition     | Control Type     | Failure Mode Addressed |
|:-------------------------------|:-------------------------------------------|:------------------|:-------------------------|:-----------------|:-----------------------|
| `504_timeout`                  | HTTP 504 Gateway Timeout                   | `CONFIRMED`       | `dispatched_unconfirmed` | Fault Injection  | Silent timeout drop & false confirmation |
| `tcp_reset`                    | TCP RST mid-flight                         | `CONFIRMED`       | `dispatched_unconfirmed` | Fault Injection  | Mid-stream socket abort |
| `confirmed`                    | HTTP 200 OK, normal flow                   | `CONFIRMED`       | `CONFIRMED`              | Negative Control | Clean settlement baseline |
| `refused`                      | HTTP 403 Forbidden (policy)                | `REFUSED`         | `REFUSED`                | Negative Control | Downstream policy rejection |
| `delayed_confirmation`         | HTTP 200 arrived post-deadline (t+65s)     | `CONFIRMED`       | `dispatched_unconfirmed` | Fault Injection  | Late-arriving orphan settlement |
| `duplicate_retry_same_payload` | HTTP 409 duplicate retry in-flight         | `RETRY_DISPATCH`  | `CONFLICT`               | Fault Injection  | Unverified duplicate retry storm |
| `payload_mutation_on_retry`    | HTTP 409 payload mismatch on retry         | `CONFIRMED`       | `CONFLICT`               | Fault Injection  | Mutation under reused idempotency key |
| `malformed_response`           | HTTP 200 with truncated / corrupted JSON   | `CONFIRMED`       | `INVALID_INPUT`          | Fault Injection  | Downstream schema contract violation |

## Scoring Rubric

- **PASS**: `evaluated_disposition` in `disposition_report.json` matches Expected Disposition exactly.
- **FAIL**: Any deviation, including a promoted `CONFIRMED` on a fault scenario or failure to detect schema violations.

The `confirmed` and `refused` negative controls are essential: they prove the engine
distinguishes verified settlement from unconfirmed drops — not a blanket rejection machine.

## Artifact Bundle (per scenario run)

Each `python3 run.py --scenario <id>` writes to `./audit_out/<id>/`:

| File                          | Purpose                                             |
|:------------------------------|:----------------------------------------------------|
| `disposition_report.json`     | IETF-aligned receipt with `evaluated_disposition`   |
| `audit_trace.mermaid`         | Visual sequence diagram of wire event vs SDK claim  |
| `dora_art17_gap_report.json`  | Machine-readable DORA Art. 17 evidence dossier      |
| `ProofOrStopFilter.java`      | Drop-in Spring Boot fail-closed remediation filter  |
