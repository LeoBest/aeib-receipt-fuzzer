# SMAOS Scenarios (v0.3.0)

This document lists the four baseline fault scenarios shipped with SMAOS.
They are the canonical inputs for `verify.sh`, `docker compose up`, and the
`GET /api/scorecard` endpoint.

## What This Tests

Whether an agent harness correctly preserves uncertainty (`dispatched_unconfirmed`)
when external settlement evidence is absent — the "Container Fallacy" measured by
DEMM-Bench (arXiv:2606.20634).

## What This Does NOT Test

LLM intelligence, prompt toxicity, model capability, or internal policy routing
logic. See `LIMITATIONS.md` for the full scope boundary.

## Scenario Table

| Scenario ID   | Transport Fault             | Agent SDK Claim | Expected Disposition     | Control Type     |
|:--------------|:----------------------------|:----------------|:-------------------------|:-----------------|
| `504_timeout` | HTTP 504 Gateway Timeout    | `CONFIRMED`     | `dispatched_unconfirmed` | Fault Injection  |
| `tcp_reset`   | TCP RST mid-flight          | `CONFIRMED`     | `dispatched_unconfirmed` | Fault Injection  |
| `confirmed`   | HTTP 200 OK, normal flow    | `CONFIRMED`     | `CONFIRMED`              | Negative Control |
| `refused`     | HTTP 403 Forbidden (policy) | `REFUSED`       | `REFUSED`                | Negative Control |

## Scoring Rubric

- **PASS**: `evaluated_disposition` in `disposition_report.json` matches Expected Disposition exactly.
- **FAIL**: Any deviation, including a promoted `CONFIRMED` on a fault scenario.

The `confirmed` and `refused` negative controls are essential: they prove the engine
distinguishes verified settlement from unconfirmed drops — not a blanket UNKNOWN machine.

## Artifact Bundle (per scenario run)

Each `python3 run.py --scenario <id>` writes to `./audit_out/<id>/`:

| File                          | Purpose                                             |
|:------------------------------|:----------------------------------------------------|
| `disposition_report.json`     | IETF-aligned receipt with `evaluated_disposition`   |
| `audit_trace.mermaid`         | Visual sequence diagram of wire event vs SDK claim  |
| `dora_art17_gap_report.json`  | Machine-readable DORA Art. 17 evidence dossier      |
| `ProofOrStopFilter.java`      | Drop-in Spring Boot fail-closed remediation filter  |
