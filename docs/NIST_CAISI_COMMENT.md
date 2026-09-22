# Formal Comment: NIST AI Agent Standards Initiative (CAISI)

**Date:** September 2026
**To:** National Institute of Standards and Technology (NIST)
**Subject:** Separation of Agent Evidence Handling from Model Capability (The Overclaim Risk)

**Executive Summary:**
Current evaluation frameworks for autonomous agents focus heavily on reasoning capability and benchmark success. We submit that **evidence handling and incident reporting** must be evaluated as an orthogonal vector to capability.

**The Container Fallacy & Empirical Data:**
As demonstrated by the DEMM-Bench diagnostics (arXiv:2606.20634), state-of-the-art agent baselines exhibit a **75% Overclaim Rate** when transport faults (e.g., HTTP 504 Gateway Timeout, TCP RST) occur mid-flight. Standard SDKs prioritize continuity over ledger truth, leading the agent to hallucinate a `CONFIRMED` state when the physical wire evidence is absent.

**Recommendation:**
NIST standards should require agents operating in high-risk environments (finance, critical infrastructure) to emit "Decision Reproducibility" receipts (aligning with IETF AAT draft-03) and explicitly distinguish between a *dispatched* intent and a *wire-confirmed* effect. Self-attestation by closed-model APIs is mathematically insufficient for auditability.
