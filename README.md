# 🛡️ SMAOS | Air-Gapped AI Agent Wire-Truth Engine (`v0.1.0`)

> **Prevent silent ledger drift and HTTP 504 double-spend hazards in autonomous AI payment agent workflows.**

[![Release](https://img.shields.io/badge/release-v0.1.0-blue.svg)](https://github.com/sovereignnexus/aeib-receipt-fuzzer/releases/tag/v0.1.0)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Egress](https://img.shields.io/badge/egress-0%20bytes%20(air--gapped)-success.svg)](#privacy--zero-egress-invariant)
[![Compliance](https://img.shields.io/badge/compliance-DORA%20Art.%2017%20%7C%20ISO%2042001-orange.svg)](#regulatory-compliance-mapping)

---

## 🏛️ The Problem: The "Container Fallacy"

When an autonomous payment agent dispatches a mutating tool call and the gateway drops with an **HTTP 504 Gateway Timeout**, standard agent SDKs (LangChain, Spring AI) catch the transport exception and falsely log **`CONFIRMED`**.

* **The Result:** The AI agent claims success, the database records the transfer, but the clearing ledger never moved the money.
* **The Systemic Risk:** Triggers 4:00 AM reconciliation drift and mandatory 4-hour **DORA Article 17 EBA incident reporting clocks**.

---

## ⚡ 60-Second Quickstart (100% Local / Air-Gapped)

### Option 1: Native Python (Zero Dependencies)
```bash
git clone https://github.com/sovereignnexus/aeib-receipt-fuzzer.git
cd aeib-receipt-fuzzer
python3 run.py
```

### Option 2: Air-Gapped Docker Container
```bash
docker compose up
```
*Navigates to local dashboard at `http://127.0.0.1:8765`.*

---

## 🛒 The "Container Shop" Menu (`docker-compose.yml`)

Configure your target stack and fault profiles locally via simple environment variables:

```yaml
services:
  smaos-audit:
    image: sovereignnexus/aeib-receipt-fuzzer:v0.1.0
    ports:
      - "127.0.0.1:8765:8765"
    environment:
      RUNTIME: "java21"             # java21 | python
      FRAMEWORK: "spring-boot"      # spring-boot | langchain4j | fastapi
      FAULT_MODES: "504,TCP_RST"    # 504 | TCP_RST
      PRIVACY_GUARD: "true"         # In-memory IBAN/PAN/JWT scrubbing
      COMPLIANCE_EXPORT: "DORA,ISO42001,ATH"
```

---

## 🛡️ Key Safety Invariants

1. **In-Memory Privacy Scrubber:** IBANs (`[REDACTED_IBAN]`), card PANs, and JWT bearer tokens (`[REDACTED_JWT]`) are scrubbed in-memory *before* any disk writes.
2. **Proof-or-Stop Invariant:** Hard precedence override forcing unconfirmed state transitions:
   $$\text{Evidence Absent} \implies \text{UNKNOWN}$$
3. **Polyglot Remediation:** Exports `ProofOrStopFilter.java` for Spring Boot `WebClient` and `fix.patch` for Python.

---

## 📊 Audit Deliverable Bundle (`./audit_out/`)

Every local run outputs:
* `dora_art17_gap_report.json` — EBA RTS 2024/1772 major incident JSON report.
* `audit_trace.mermaid` — Visual sequence diagram mapping wire drops vs. SDK overclaims.
* `ProofOrStopFilter.java` — Drop-in fail-closed filter for Spring Boot microservices.
* `index.html` — Interactive dark-mode dashboard for local CISO review.

---

## 💼 Commercial Diagnostic Engagement

Need to audit your staging logs before DORA enforcement?
* **48-Hour Staging Diagnostic Audit (€1,500 / ~38,000 CZK):** Ingestion of 250+ staging execution traces, calculation of your Toxic Receipt Index (TRI %), and delivery of the full DORA Article 17 gap report.

See [`SPECS.md`](SPECS.md) or [`docs/sow-diagnostic-audit.pdf`](docs/sow-diagnostic-audit.pdf) for the full Statement of Work.

---

## 📜 License & Author

Apache License 2.0. Built by **SovereignNexus s.r.o.** (`andrii@sovereignnexus.org`).
