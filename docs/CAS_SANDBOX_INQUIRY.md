# Pre-Submission Inquiry: Czech AI Sandbox

**To:** Czech Agency for Standardisation (ČAS) / MPO
**CC:** ČNB, ÚOOÚ, NÚKIB
**Subject:** Pre-Submission Inquiry: Governance Sidecar for Regulated Financial AI

Dear Sandbox Operators,

We are developing the SMAOS Wire-Truth Observer, a passive, local-first governance sidecar designed to prevent autonomous agents from hallucinating `CONFIRMED` transaction states during transport faults (e.g., HTTP 504 timeouts).

Before submitting a formal application to the Czech AI Sandbox, we seek clarification on four regulatory questions:

1. **Classification:** Does a passive, non-mutating pre-execution governance sidecar constitute a "governance component" of a high-risk AI system, or is it evaluated as an independent AI system?
2. **DORA Coordination:** How does the Sandbox coordinate with ČNB regarding DORA Article 28 Register inputs for experimental financial AI participants?
3. **Eligibility:** Is a transaction-governance sidecar for regulated financial use cases within the active scope of the Sandbox cohorts?
4. **Evidence Format:** What format does ČAS require for sandbox execution plans and telemetry exit reports (e.g., JSON-LD, xBRL)?

We believe our integration of W3C BBS+ selective disclosure and Ed25519 cryptography provides a verifiable mechanism to satisfy both EU AI Act Article 12 (immutable logging) and GDPR Article 17 (Right to Erasure).

We look forward to your guidance.
