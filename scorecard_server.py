#!/usr/bin/env python3
# Copyright 2026 SovereignNexus
# Apache License 2.0
"""
scorecard_server.py — Zero-dependency live scorecard API (v0.3.0)

Reads disposition_report.json from ./audit_out/<scenario_id>/ and exposes
a structured JSON scorecard at GET /api/scorecard on 127.0.0.1:8766.

Zero external dependencies — runs on Python 3 stdlib only.

Usage:
    # First run the scenarios:
    for s in 504_timeout tcp_reset confirmed refused; do
        python3 run.py --scenario $s --export-dir ./audit_out/$s
    done
    # Then start the server:
    python3 scorecard_server.py
    # Query:
    curl http://127.0.0.1:8766/api/scorecard
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

AUDIT_DIR = Path("./audit_out")
HOST = "127.0.0.1"
PORT = 8766

EXPECTED = {
    "504_timeout":                  "dispatched_unconfirmed",
    "tcp_reset":                    "dispatched_unconfirmed",
    "confirmed":                    "CONFIRMED",
    "refused":                      "REFUSED",
    "delayed_confirmation":         "dispatched_unconfirmed",
    "duplicate_retry_same_payload": "CONFLICT",
    "payload_mutation_on_retry":    "CONFLICT",
    "malformed_response":           "INVALID_INPUT",
}


def build_scorecard() -> dict:
    scenarios = []
    total = 0
    passed = 0

    for scenario_id, expected in EXPECTED.items():
        report_path = AUDIT_DIR / scenario_id / "disposition_report.json"
        if not report_path.exists():
            scenarios.append({
                "scenario_id": scenario_id,
                "status": "NOT_RUN",
                "evaluated_disposition": None,
                "expected_disposition": expected,
            })
            total += 1
            continue

        data = json.loads(report_path.read_text())
        got = data.get("evaluated_disposition", "")
        status = "PASS" if got == expected else "FAIL"

        scenarios.append({
            "scenario_id": scenario_id,
            "status": status,
            "evaluated_disposition": got,
            "expected_disposition": expected,
            "discrepancy_detected": data.get("discrepancy_detected"),
            "transport_fault": data.get("transport_fault"),
        })
        total += 1
        if status == "PASS":
            passed += 1

    overclaim_scenarios = [
        s for s in scenarios
        if s["status"] == "FAIL" and s.get("discrepancy_detected")
    ]

    return {
        "version": "v0.3.0",
        "measurement": "not certification — human review required before regulatory use",
        "scenarios_total": total,
        "scenarios_passed": passed,
        "scenarios_failed": total - passed,
        "overclaim_detected": len(overclaim_scenarios) > 0,
        "board_implication": (
            "Agent harness swallowed transport fault and promoted unconfirmed effect "
            "to CONFIRMED. Silent reconciliation drift risk detected."
            if overclaim_scenarios else
            "No overclaims detected in tested scenarios."
        ),
        "scenarios": scenarios,
        "evidence_artifacts": [
            "audit_out/<scenario_id>/disposition_report.json",
            "audit_out/<scenario_id>/audit_trace.mermaid",
            "audit_out/<scenario_id>/dora_art17_gap_report.json",
            "audit_out/<scenario_id>/ProofOrStopFilter.java",
        ],
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/scorecard":
            body = json.dumps(build_scorecard(), indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass  # suppress access logs for demo cleanliness


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Scorecard API  →  http://{HOST}:{PORT}/api/scorecard")
    print(f"Health check   →  http://{HOST}:{PORT}/health")
    print("Zero external dependencies. Ctrl+C to stop.")
    server.serve_forever()
