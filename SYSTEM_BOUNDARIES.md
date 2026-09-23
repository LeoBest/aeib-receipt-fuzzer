# SMAOS Whole-System Transition Boundaries

This document defines the 4 falsifiable boundaries that SMAOS enforces in a multi-agent distributed system. 

SMAOS relies on explicit **negative state assertions** (e.g. `authority_created = false`) instead of assuming safety in the absence of failure logs.

## 1. Transport -> SDK Boundary
**Hazard:** Network drops (HTTP 504, TCP RST) occur, but the agent SDK assumes success or crashes, leaving the system in an unknown state.
**Assertion:** `unverified_state_promoted = false`
**Enforcement:** SMAOS operates on the 127.0.0.1 loopback interface. If the downstream socket drops, SMAOS forces the disposition to `dispatched_unconfirmed`.

## 2. Agent A -> Agent B Boundary (Handoff)
**Hazard:** An agent delegates a task to another agent, inadvertently escalating privileges beyond the delegator's ceiling.
**Assertion:** `delegation_ceiling_breached = false`
**Enforcement:** Trust Passports verify Identity (Actor), Delegation (On Behalf Of), and Authority (Ceiling Enforced).

## 3. Context -> Pipeline Boundary
**Hazard:** Agents ingest stale, tampered, or inadmissible context data (e.g. prompt injection, TTL expiration).
**Assertion:** `authority_created = false` (if context invalid)
**Enforcement:** Reject incoming context unless cryptographically signed and within TTL.

## 4. Outcome -> Witness Boundary
**Hazard:** An auditor cannot cryptographically prove the lineage of execution states.
**Assertion:** Cryptographic succession verified via `prior_state_hash`.
**Enforcement:** Each Trust Passport incorporates the hash of the preceding state.
