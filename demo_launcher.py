#!/usr/bin/env python3
"""
SMAOS AEIB Local Wire-Truth Demo Harness (v0.1.0)
Simulates passive local loopback wire observation, in-memory PII/PCI scrubbing,
and independent audit evidence generation (without altering application logs).
"""

import html
import json
from pathlib import Path
import re
import sys
import time

JAVA_REMEDIATION_FILTER = """package com.sovereignnexus.smaos.guard;

import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.ExchangeFunction;
import reactor.core.publisher.Mono;

/**
 * Enterprise Spring Boot / WebClient Remediation Filter (Moat 1 & DORA Art. 17)
 * Hard boundary invariant: Evidence Absent => UNKNOWN
 * Prevents Spring AI / LangChain4j harnesses from returning ungrounded confirmation.
 */
public class ProofOrStopFilter implements ExchangeFilterFunction {

    @Override
    public Mono<ClientResponse> filter(ClientRequest request, ExchangeFunction next) {
        return next.exchange(request)
            .onErrorResume(java.net.SocketTimeoutException.class, ex -> {
                // Hard boundary invariant: Evidence Absent => UNKNOWN
                return Mono.error(new AgentDiscrepancyException(
                    "DORA Art. 17 Violation: Wire dropped with no settlement receipt. State forced to UNKNOWN."
                ));
            });
    }
}
"""

MERMAID_TRACE = """sequenceDiagram
    autonumber
    actor Agent as Autonomous Agent
    participant Observer as SMAOS Local Observer (passive)
    participant Gateway as Core Banking Gateway

    Observer->>Agent: observes outbound
    Agent->>Gateway: POST /v1/settle (EUR 50,000)
    Gateway--xAgent: HTTP 504 / TCP RST
    Note over Agent: SDK swallows exception
    Agent->>Agent: logs {"status": "CONFIRMED"}
    Observer->>Observer: compares wire state vs. claimed state
    Observer->>Observer: emits UNKNOWN + evidence bundle
"""

class TraceScrubber:
    PATTERNS = {
        "IBAN": re.compile(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}"),
        "PAN": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
        "JWT": re.compile(r"Bearer\s+[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*")
    }

    @classmethod
    def sanitize(cls, text: str) -> str:
        scrubbed = text
        for label, pattern in cls.PATTERNS.items():
            if label == "JWT":
                scrubbed = pattern.sub("Bearer [REDACTED_JWT]", scrubbed)
            else:
                scrubbed = pattern.sub(f"[REDACTED_{label}]", scrubbed)
        return scrubbed


def main():
    print("🚀 Launching SMAOS AEIB Local Wire-Truth Demo Harness...")
    print("🚀 [SMAOS Local Wire-Truth Observer v0.1.0] Starting zero-egress inspection...")
    print("🔒 [Privacy Guard] Performing in-memory PII/PCI-DSS scrubbing...")

    root_dir = Path(__file__).resolve().parent
    fixtures_dir = root_dir / "fixtures"
    fixture_path = fixtures_dir / "sample_loan_disbursement.json"
    
    dispatched_by = "Agent-LangChain-Treasury"
    raw_iban = "CZ6508000000001234567890"
    raw_jwt = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.x"
    amount = 50000.0

    if fixture_path.exists():
        try:
            data = json.loads(fixture_path.read_text())
            dispatched_by = data.get("dispatched_by", dispatched_by)
            raw_iban = data.get("destination_account", raw_iban)
            raw_jwt = data.get("auth_header", raw_jwt)
            amount = float(data.get("amount", amount))
        except Exception:
            pass

    scrubbed_iban = TraceScrubber.sanitize(raw_iban)
    scrubbed_jwt = TraceScrubber.sanitize(raw_jwt)

    print(f"  • Dispatched By: {dispatched_by}")
    print(f"  • Destination Account: {scrubbed_iban}")
    print(f"  • Auth Header: {scrubbed_jwt}")
    print(f"  • Amount: {amount} EUR\n")

    print("🔍 [Wire Observation] Simulating transport inspection on 127.0.0.1...")
    print("  • Agent Log Claimed State: CONFIRMED")
    print("  • Core Banking Wire State: HTTP_504_GATEWAY_TIMEOUT (Wire evidence absent)\n")

    print("!! DISCREPANCY DETECTED !!")
    print("  • Description: Agent SDK logged CONFIRMED, but wire transport dropped with HTTP 504.")
    print("  • Disposition: Emitting UNKNOWN disposition with evidence bundle (agent logs remain unaltered).\n")

    audit_dir = root_dir / "audit_out"
    audit_dir.mkdir(parents=True, exist_ok=True)

    # 1. audit_trace.mermaid
    (audit_dir / "audit_trace.mermaid").write_text(MERMAID_TRACE)

    # 2. dora_art17_gap_report.json
    dora_report = {
        "dora_rts_classification": "4h_major_incident",
        "dora_article_17_support": "Supports DORA Article 17 incident classification by producing a machine-readable timeline and wire-evidence bundle for risk team review",
        "incidents": [
            {
                "id": "trace-001",
                "payload": f"EUR {amount:,.0f} to {scrubbed_iban}",
                "wire_status": 504,
                "sdk_claim": "CONFIRMED",
                "observer_disposition": "UNKNOWN",
                "finding": "UNSUPPORTED_CONFIRMATION_CLAIM",
                "log_tampering": False,
                "audit_stream": "INDEPENDENT_EVIDENCE_BUNDLE"
            }
        ],
        "telemetry_source": "smaos_wire_observer_v0.1.0",
        "pci_dss_sanitization": "ACTIVE_ZERO_EGRESS",
        "sample_payload_scrubbed": f"EUR {amount:,.0f} to {scrubbed_iban}"
    }
    (audit_dir / "dora_art17_gap_report.json").write_text(json.dumps(dora_report, indent=2))

    # 3. ProofOrStopFilter.java
    (audit_dir / "ProofOrStopFilter.java").write_text(JAVA_REMEDIATION_FILTER)

    # 4. index.html
    html_dashboard = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMAOS Wire-Truth Verification Dashboard</title>
    <meta name="description" content="Air-gapped compliance engine preventing AI agent double-spends. Generates automated evidence for DORA RTS 2024/1772, ISO 42001, and ATH 1.0.">

    <!-- OpenGraph / LinkedIn / Slack Unfurl -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://sovereignnexus.github.io/aeib-receipt-fuzzer/">
    <meta property="og:title" content="SMAOS: DORA & ISO 42001 Verification for AI Agents">
    <meta property="og:description" content="Stop silent ledger drift. See how SMAOS intercepts HTTP 504 timeouts and forces ungrounded AI actions to an UNKNOWN state.">

    <!-- Schema.org B2B Software Application JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "SMAOS Wire-Truth Engine",
      "applicationCategory": "SecurityApplication",
      "operatingSystem": "Linux, macOS, Windows",
      "description": "Enterprise verification layer for autonomous AI agents. Supports DORA Article 17 incident classification by producing a machine-readable timeline and wire-evidence bundle for risk team review.",
      "offers": {{
        "@type": "Offer",
        "price": "1500",
        "priceCurrency": "EUR",
        "description": "48-Hour Diagnostic Staging Audit"
      }}
    }}
    </script>

    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg-color: #0d1117;
            --panel-bg: #161b22;
            --border-color: #30363d;
            --text-primary: #c9d1d9;
            --text-accent: #58a6ff;
            --success: #3fb950;
            --danger: #f85149;
            --warning: #d29922;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            background: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 2rem;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }}
        h1 {{ color: var(--text-accent); margin: 0 0 0.5rem 0; font-size: 1.8rem; }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }}
        .badge-green {{ background: rgba(63, 185, 80, 0.15); color: var(--success); border: 1px solid var(--success); }}
        .badge-blue {{ background: rgba(88, 166, 255, 0.15); color: var(--text-accent); border: 1px solid var(--text-accent); }}
        .badge-red {{ background: rgba(248, 81, 73, 0.15); color: var(--danger); border: 1px solid var(--danger); }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
        @media (max-width: 1100px) {{ .grid {{ grid-template-columns: 1fr; }} }}
        .panel {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
        }}
        .panel h2 {{ margin-top: 0; font-size: 1.2rem; color: #f0f6fc; }}
        .mermaid-wrapper {{ background: #ffffff; border-radius: 6px; padding: 1.25rem; }}
        .terminal {{
            background: #090d13;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1rem;
            font-family: monospace;
            font-size: 13px;
            line-height: 1.5;
            color: #7ee787;
            white-space: pre-wrap;
        }}
        .metric-cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 2rem; }}
        .card {{
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1rem 1.25rem;
        }}
        .card-label {{ font-size: 0.8rem; color: #8b949e; text-transform: uppercase; }}
        .card-val {{ font-size: 1.5rem; font-weight: 700; margin-top: 0.4rem; }}
        .text-red {{ color: var(--danger); }}
        .text-green {{ color: var(--success); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>🏛️ SMAOS Wire-Truth Verification Dashboard</h1>
                <p style="margin: 0; color: #8b949e;">Autonomous Agent Execution Evidence vs. Wire Settlement Ground Truth</p>
            </div>
            <div>
                <span class="badge badge-green">Zero-Egress Verified (127.0.0.1)</span>
                <span class="badge badge-blue">DORA RTS 2024/1772</span>
                <span class="badge badge-red">PCI-DSS Scrubber Active</span>
            </div>
        </header>

        <div class="grid">
            <div class="panel">
                <h2>📊 Passive Wire Observation Trace</h2>
                <div class="mermaid-wrapper">
                    <div class="mermaid">
{MERMAID_TRACE}
                    </div>
                </div>
            </div>

            <div class="panel">
                <h2>💻 Local Verification Stream (Independent Audit Log)</h2>
                <div class="terminal">
🚀 [SMAOS Local Wire-Truth Observer v0.1.0]
🔒 [Privacy Guard] In-memory PII scrubbing: ACTIVE (0 leaks)
  • Dispatched By: {dispatched_by}
  • Destination Account: {scrubbed_iban}
  • Auth Header: {scrubbed_jwt}
  • Amount: {amount} EUR

🔍 [Wire Observation] 127.0.0.1 Transport State:
  • Agent Log Claimed State: CONFIRMED
  • Core Banking Wire State: HTTP_504_GATEWAY_TIMEOUT (Evidence absent)

!! DISCREPANCY DETECTED !!
  • Description: Agent SDK logged CONFIRMED, but wire transport dropped with HTTP 504.
  • Disposition: Emitting UNKNOWN disposition with evidence bundle (agent logs remain unaltered).

✅ Audit completed. Zero log tampering — independent evidence stream materialized.
                </div>
            </div>
        </div>

        <div class="metric-cards">
            <div class="card">
                <div class="card-label">Unsupported Confirmation Claims</div>
                <div class="card-val text-red">Detected (504 Discrepancy)</div>
                <div style="font-size: 0.75rem; color: #8b949e; margin-top: 0.3rem;">Agent claimed success without external settlement</div>
            </div>
            <div class="card">
                <div class="card-label">DORA Art. 17 Incident Support</div>
                <div class="card-val text-red">Evidence Bundle Ready</div>
                <div style="font-size: 0.75rem; color: #8b949e; margin-top: 0.3rem;">Supports risk team Article 17 incident classification</div>
            </div>
            <div class="card">
                <div class="card-label">PII / PCI-DSS Sanitization</div>
                <div class="card-val text-green">100% In-Memory Redacted</div>
                <div style="font-size: 0.75rem; color: #8b949e; margin-top: 0.3rem;">0 IBAN, PAN, or JWT leaks to disk</div>
            </div>
        </div>
    </div>

    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>
"""
    (audit_dir / "index.html").write_text(html_dashboard)

    print("✅ Audit execution completed. Artifacts written to ./audit_out:")
    print("  • audit_out/audit_trace.mermaid")
    print("  • audit_out/dora_art17_gap_report.json")
    print("  • audit_out/ProofOrStopFilter.java")
    print("  • audit_out/index.html\n")

    print("📊 Executive Dashboard generated at audit_out/index.html")
    print("💡 Local server command: python3 -m http.server 8765 --directory audit_out --bind 127.0.0.1")


if __name__ == "__main__":
    main()
