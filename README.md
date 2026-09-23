# 🛡️ SMAOS AEIB Wire-Truth Verifier (`v0.3.0`)
> **Air-Gapped, Zero-Egress Wire-Truth Verification Engine for Autonomous Agent Harnesses** 
> *Enforcing the IETF `dispatched_unconfirmed` invariant, DORA Article 17 compliance, and Post-Quantum Cryptographic Receipts.*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Standard](https://img.shields.io/badge/IETF-AAT_draft--03-green.svg)](docs/CRYPTOGRAPHY.md)
[![DORA](https://img.shields.io/badge/EBA_DORA-Article_17_Ready-red.svg)](docs/DORA_ARTICLE_17_COMPLIANCE.md)
[![PQC](https://img.shields.io/badge/PQC-ML--DSA--65_(FIPS_204)-purple.svg)](docs/CRYPTOGRAPHY.md)
[![Egress](https://img.shields.io/badge/Data_Egress-0_Bytes_(127.0.0.1)-brightgreen.svg)](#privacy--zero-egress-guarantee)

---

## 🚨 The Core Problem: The Container Fallacy

Autonomous agents in financial and regulated environments suffer from the **Container Fallacy** ([DEMM-Bench, arXiv:2606.20634](https://arxiv.org)):
* When a mutating API call (e.g., payment disbursement or database commit) is dispatched and the network drops with an **HTTP 504 Gateway Timeout** or **TCP RST**, standard agent SDKs swallow the exception.
* The agent SDK logs `{"status": "CONFIRMED"}` internally, even though **no settlement receipt was ever received** from the core banking gateway.
* **Impact**: Silent ledger drift, double-disbursements, and major compliance failures under **EBA DORA RTS 2024/1772 Article 17** (exposing institutions to periodic penalties up to 1% of average daily worldwide turnover).

---

## 💡 The Solution: Local Wire-Truth Observation

`aeib-receipt-fuzzer` is a zero-dependency, local-first verification engine that operates passively on loopback (`127.0.0.1`). It compares claimed application SDK logs against actual wire transport states, intercepts false confirmations, redacts sensitive data in-memory, and emits an independent, cryptographically signed evidence bundle.

```text
┌──────────────────────────────────────┐
│ 1. AUTONOMOUS AGENT (Model/SDK)      │
│    LangChain / Spring AI / Custom LLM│
└──────────────────────────────────────┘
                   │ Outbound Request
                   │ (POST /v1/settle)
                   ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 2. SMAOS LOCAL WIRE OBSERVER (Passive / Loopback)                                │
├──────────────────────────────────────────────────────────────────────────────────┤
│ • PII/PCI-DSS In-Memory Scrubber: Redacts IBANs & JWTs prior to disk writes      │
│ • State Evaluator: Compares claimed SDK state vs. actual wire transport status   │
│ • IETF Capsule Engine: Emits dispatched_unconfirmed + independent evidence       │
└──────────────────────────────────────────────────────────────────────────────────┘
                   │ Transport Exception
                   │ (HTTP 504 / TCP RST)
                   ▼
┌──────────────────────────────────────┐
│ 3. CORE BANKING / CLEARING           │
│ ❌ Wire Dropped / Unconfirmed        │
└──────────────────────────────────────┘
```

---

## ✨ Key Features & Capability Suite

### 1. Passive Wire Observation & Zero Application Log Tampering
* Intercepts transport state passively on loopback (`127.0.0.1`).
* **Zero Log Tampering**: The agent's internal application logs remain 100% untouched; SMAOS emits an independent, parallel audit stream.

### 2. Active In-Memory PII/PCI-DSS Scrubbing
* Scrubbing rules redact IBANs (`[REDACTED_IBAN]`), credit card PANs (`[REDACTED_PAN]`), and Bearer JWTs (`[REDACTED_JWT]`) in-memory before writing any logs to disk.

### 3. IETF Standard Vocabulary (`dispatched_unconfirmed`)
* Replaces ambiguous statuses with the exact terminology defined in **IETF Agent Action Capsule (draft-02)**. Unconfirmed mutations resolve strictly to `dispatched_unconfirmed`.

### 4. Moat 1: Attestation Closure (IETF AAT draft-03)
* Binds 5 exact cryptographic digests to every audit receipt to guarantee decision reproducibility:
  1. `model_weights_digest`
  2. `tokenizer_digest`
  3. `chat_template_digest`
  4. `engine_build_digest`
  5. `numeric_environment_digest`

### 5. Moat 2: Post-Quantum Cryptographic Envelope
* Dual-signs audit receipts using classical **Ed25519** and post-quantum **ML-DSA-65 (FIPS 204)** signatures, securing 6–12 month evidence pack durability for CISO and insurance underwriting review.

### 6. Standalone Offline WASM Verifier (`smaos_verify.wasm`)
* A pure Rust WebAssembly binary (186 KB) compiled to `wasm32-unknown-unknown`. Allows CISOs and auditors to drag-and-drop receipts into an air-gapped browser with Wi-Fi disabled to verify RFC 8785 JCS canonicalization and cryptographic proofs locally.

### 7. Governance Intensity Index (GII) Scanner (`ghost_audit_scanner.py`)
* Read-only CLI utility that crawls local developer profiles (`~/.claude/settings.json`, `.cursor/`), git commit histories, and environment variables for swallowed commits, un-sandboxed permissions, or OWASP vulnerabilities.

### 8. Drop-In Spring Boot Remediation Filter (`ProofOrStopFilter.java`)
* A 15-line fail-closed Spring `WebClient` filter that enforces `Evidence Absent ⟹ UNKNOWN`, immediately eliminating false-success receipts in enterprise Java applications.

---

## Why SMAOS is Unique

### 1. Wire-Truth Observation vs. Application Log Lies ("The Container Fallacy")
* **Competitors (LangSmith, Datadog, Braintrust, AgentOps)**: Read what the agent *says* happened from application logs or API responses. When an HTTP 504 Gateway Timeout or TCP RST occurs, standard SDKs swallow the exception and falsely record `CONFIRMED`.
* **Only SMAOS**: Observes raw network physics on `127.0.0.1` loopback. We prove the **Container Fallacy** (backed by **DEMM-Bench, arXiv:2606.20634**, showing a 75% overclaim rate in standard baselines). We intercept the fault and force the state to the IETF standard **`dispatched_unconfirmed`**.

### 2. Zero-Egress, Air-Gapped Verification (0 Bytes Cloud Leak)
* **Competitors**: Require streaming client staging traces, prompts, or sensitive payloads to third-party cloud servers, introducing massive data governance and GDPR risks.
* **Only SMAOS**: Operates 100% locally on `127.0.0.1` under `--network none`. In-memory regex scrubbing redacts IBANs (`[REDACTED_IBAN]`), PANs, and Bearer JWTs before anything touches disk.

### 3. Cryptographic Decision Reproducibility & Post-Quantum Proofs
* **Competitors**: Offer plaintext logs, internal database records, or basic signed JWTs that fail replay-attack checks.
* **Only SMAOS**: Binds 5 IETF AAT draft-03 digests (`model_weights`, `tokenizer`, `chat_template`, `engine_build`, `numeric_environment`) and dual-signs receipts with **Ed25519 + ML-DSA-65 (FIPS 204)**. We deliver a standalone **186 KB WASM verifier (`smaos_verify.wasm`)** so CISOs can drag and verify receipts offline in a disconnected browser with Wi-Fi turned off.

### 4. Instant Code Fix, Not Just "Compliance Theater"
* **Competitors**: Deliver generic policy PDFs or dashboards showing "your model failed."
* **Only SMAOS**: Delivers the exact 15-line Spring Boot / WebClient fail-closed Java filter (**`ProofOrStopFilter.java`**) that engineering teams drop into production on day 1 to enforce `Evidence Absent ⟹ UNKNOWN`.

---

## 📊 Institutional Comparison: The Honest Calibration

| Capability / Dimension | Standard SaaS Loggers & Evals | Generic DORA Auditors | **SMAOS 48-Hour Staging Diagnostic** |
| :--- | :---: | :---: | :---: |
| **Observation Layer** | Application SDK / API Layer | Static Policy Checklists | **Physical Wire Transport (`127.0.0.1`)** |
| **504 Timeout Detection** | ❌ Records what SDK claims | ❌ Cannot detect runtime drops | **✅ Forces `dispatched_unconfirmed`** |
| **Data Privacy & Egress** | ❌ High Egress (SaaS Cloud) | ⚠️ Manual Sample Intake | **✅ 0 Bytes Egress + In-Memory Scrubbing** |
| **Attestation Binding** | ❌ Text logs / Prompts only | ❌ None | **✅ IETF AAT 5-Digest Decision Binding** |
| **Post-Quantum Crypto** | ❌ None | ❌ None | **✅ Dual Ed25519 + ML-DSA-65 (FIPS 204)** |
| **Offline Verification** | ❌ Requires Cloud Dashboard | ❌ Static PDF Report | **✅ Standalone WASM Verifier (`smaos_verify.wasm`)** |
| **Remediation Delivery** | ❌ None | ❌ Generic recommendations | **✅ Drop-In Java Patch (`ProofOrStopFilter.java`)** |

> *"Existing tools ask: 'What did the LLM say?'  
> SMAOS asks: 'What actually moved on the wire, and can you prove it in court 5 years from now?'  
>  
> We don't sell another monitoring dashboard. We deliver a zero-egress wire-truth verifier that catches false payment confirmations, generates DORA Article 17 incident dossiers, and gives your developers the exact 15 lines of Java code to fix the bug."*


--- | :---: | :---: | :---: | :---: |
| **Wire-Truth Verification** | ❌ None (Swallows 504) | ❌ Text-log based | ⚠️ HTTP Status only | **✅ Physical Wire vs Log Comparison** |
| **Data Egress & Privacy** | ❌ Sends data to Cloud | ❌ High Egress (SaaS) | ❌ Cloud-bound proxy | **✅ 0 Bytes Egress (127.0.0.1)** |
| **PII/PCI Sanitization** | ❌ None / Client-side | ⚠️ Post-hoc masking | ⚠️ Header-only | **✅ Active In-Memory Regex Redaction** |
| **State Vocabulary** | ❌ False `CONFIRMED` | ❌ Ambiguous text | ❌ Standard HTTP | **✅ IETF `dispatched_unconfirmed`** |
| **Attestation Closure** | ❌ None | ❌ None | ❌ API Key only | **✅ IETF AAT draft-03 (5 Digests)** |
| **Cryptographic Proofs** | ❌ Plaintext JSON | ❌ Database ID | ❌ JWT Bearer | **✅ Dual Ed25519 + ML-DSA-65 (FIPS 204)** |
| **Offline Verification** | ❌ Impossible | ❌ Requires SaaS UI | ❌ Requires Cloud | **✅ Standalone Offline WASM Verifier** |
| **DORA Article 17 Support** | ❌ Non-compliant | ⚠️ Manual Export | ⚠️ Partial Logs | **✅ Machine-Readable JSON Dossier** |
| **Remediation Code** | ❌ None | ❌ None | ❌ None | **✅ Drop-In Spring Boot Java Filter** |

---

## 🚀 Quick Start

### 1. Single Scenario Verification
Run a specific fault injection scenario and generate an audit evidence bundle:
```bash
python3 run.py --scenario 504_timeout --export-dir ./audit_out
```

### 2. Multi-Scenario Matrix Execution
Run the full test suite across all four conformance vectors:
```bash
for s in confirmed refused 504_timeout tcp_reset; do
  python3 run.py --scenario $s --export-dir "./audit_out/$s"
done
```

### 3. Interactive Local Executive Dashboard
Launch the zero-egress, dark-mode browser dashboard on loopback:
```bash
python3 demo_launcher.py
# View dashboard locally at http://127.0.0.1:8765/
```

### 4. Run via Air-Gapped Docker Container
Build and execute the zero-network containerized verifier:
```bash
docker build -t smaos-demo:0.2.0 .
docker run --rm -p 127.0.0.1:8765:8765 --network none smaos-demo:0.2.0
```

---

## 🛡️ Intellectual Property & Architecture ("One Core, Two Doors")

SMAOS adheres strictly to the One Core, Two Doors dual-licensing architecture:

```text
┌──────────────────────────────────────────────────┐   ┌──────────────────────────────────────────────────┐
│ DOOR 1: PUBLIC TRUST                             │   │ DOOR 2: PRIVATE IP (COMMERCIAL)                  │
│ (Apache License 2.0)                             │   │ (Closed Source)                                  │
├──────────────────────────────────────────────────┤   ├──────────────────────────────────────────────────┤
│ • Local Wire-Truth Engine (`run.py`)             │   │ • Continuous eBPF Kernel Event Drivers           │
│ • Standalone Rust WASM Verifier (`smaos_verify`) │   │ • Real-time Neural Routing & Context Compaction  │
│ • GII Audit Scanner (`ghost_audit_scanner.py`)   │──►│ • Multi-Node Enterprise Consensus Engine         │
│ • DORA Register Validator                        │   │ • Automated State-Machine Synthesis & Recovery   │
│ • IETF AAT / PQC Conformance Test Vectors        │   │ • Enterprise Governance Platform (SMAOS Fortress)│
└──────────────────────────────────────────────────┘   └──────────────────────────────────────────────────┘
```

* **Door 1 (Open Source):** Provides developers, auditors, and CISOs with 100% transparent, local verification tools to test agent harnesses and verify cryptographic receipts offline.
* **Door 2 (Commercial):** Powers real-time, continuous production governance and automated state reconciliation at enterprise scale.

---

## 📜 Standards & Regulatory Mapping

* **EBA DORA RTS 2024/1772 Article 17:** Major ICT Incident Classification support.
* **EU AI Act Article 12 & 14:** Automatic logging and human oversight readiness.
* **ISO/IEC 42001 Clause 9:** Runtime verification and continuous auditability.
* **IETF AAT (draft-03):** Agent Audit Trail Decision Reproducibility.
* **NIST FIPS 204:** Module-Lattice-Based Digital Signature Standard (ML-DSA-65).

## 📄 License

This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
