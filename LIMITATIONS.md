# SMAOS Limitations (v0.3.0)

This document states what SMAOS does not measure, does not claim, and does not
provide. Read this before citing SMAOS results in regulatory submissions.

## Scope Boundary

### What SMAOS Measures

- Whether an agent harness preserves uncertainty (`dispatched_unconfirmed`) when
  a wire call produces no settlement confirmation.
- Whether the harness correctly records a `CONFIRMED` state only when HTTP 200
  with valid evidence is received.
- Whether PII is scrubbed before local file writes.

### What SMAOS Does NOT Measure

- **Model intelligence or capability**: SMAOS does not evaluate LLM reasoning,
  task completion rate, or answer quality.
- **Prompt safety or toxicity**: SMAOS does not evaluate prompt injection,
  jailbreaks, or adversarial inputs.
- **Memory poisoning**: SMAOS does not detect contaminated context windows
  prior to execution.
- **Production traffic**: SMAOS runs on synthetic local fixtures. It does not
  observe live production wire traffic.
- **External system truth**: SMAOS proves whether the harness's claimed
  disposition is justified by the wire evidence it received. It cannot prove
  what the downstream system actually did.

## What SMAOS Does NOT Claim

- **No regulatory certification**: SMAOS does not certify compliance with
  EU DORA, ISO/IEC 42001, EU AI Act, GDPR, or any other regulation.
  Evidence bundles are inputs to your organization's human risk classification
  and reporting processes.
- **No legal advice**: Results are engineering measurements, not legal opinions.
- **No production proxy guarantee**: The engine is designed for local staging
  diagnostics. Running it in production requires your own security review.
- **No model-level audit**: SMAOS does not replace model audits, red-teaming,
  or penetration testing.

## Known Constraints

- **Loopback only**: All execution is on `127.0.0.1`. Results reflect local
  staging behavior, not live cloud or on-premises production conditions.
- **Four baseline scenarios**: The current release ships four scenarios. Real
  client environments will have additional fault modes not covered here.
- **Synthetic fixtures**: Payloads use representative but synthetic data.
  Real-client staging diagnostics use anonymized client traces under NDA.
- **No continuous monitoring**: SMAOS is a point-in-time diagnostic tool,
  not a continuous observability platform.

## Responsible Use

Results from SMAOS should be reviewed by a qualified engineer and risk officer
before being included in regulatory submissions or board reports.
