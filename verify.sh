#!/usr/bin/env bash
# verify.sh — SMAOS Artifact Verification Script (v0.3.0 / v0.3.1)
# Re-runs all 8 scenarios and asserts expected dispositions.
# Usage: ./verify.sh
# Exit code 0 = all PASS. Exit code 1 = one or more FAIL.

set -euo pipefail

EXPORT_DIR="${EXPORT_DIR:-./audit_out_verify}"
mkdir -p "$EXPORT_DIR"

SCENARIOS=(
  504_timeout
  tcp_reset
  confirmed
  refused
  delayed_confirmation
  duplicate_retry_same_payload
  payload_mutation_on_retry
  malformed_response
)

EXPECTED=(
  dispatched_unconfirmed
  dispatched_unconfirmed
  CONFIRMED
  REFUSED
  dispatched_unconfirmed
  CONFLICT
  CONFLICT
  INVALID_INPUT
)

pass=0
fail=0

echo ""
echo "🔒 SMAOS Verification Run (8 Scenarios)"
echo "   Engine  : python3 run.py"
echo "   Egress  : 127.0.0.1 loopback only"
echo "   Out dir : $EXPORT_DIR"
echo ""

for i in "${!SCENARIOS[@]}"; do
  s="${SCENARIOS[$i]}"
  exp="${EXPECTED[$i]}"
  out_dir="$EXPORT_DIR/$s"

  python3 run.py --scenario "$s" --export-dir "$out_dir" > /dev/null 2>&1

  report="$out_dir/disposition_report.json"
  if [ ! -f "$report" ]; then
    echo "  ✗ $s  — FAIL (disposition_report.json not found)"
    fail=$((fail + 1))
    continue
  fi

  got=$(python3 -c "import json; print(json.load(open('$report'))['evaluated_disposition'])")

  if [ "$got" = "$exp" ]; then
    echo "  ✓ $s  → $got"
    pass=$((pass + 1))
  else
    echo "  ✗ $s  → $got  (expected: $exp)"
    fail=$((fail + 1))
  fi
done

# PII scrubbing check on fault scenarios
echo ""
echo "🔍 PII Scrubbing Check (across scenarios)"
for s in "${SCENARIOS[@]}"; do
  report="$EXPORT_DIR/$s/disposition_report.json"
  if grep -qE '\bCZ[0-9]{2}[A-Z0-9]{16,}\b|\b[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}\b' "$report" 2>/dev/null; then
    echo "  ✗ $s  — FAIL (raw IBAN or PAN detected in output)"
    fail=$((fail + 1))
  else
    echo "  ✓ $s  — PII clean"
  fi
done

# Summary
echo ""
if [ "$fail" -eq 0 ]; then
  echo "✅ ALL PASS  ($pass/$((pass + fail)) scenarios)"
  echo "   Measurement, not certification. Human review required before regulatory use."
  exit 0
else
  echo "❌ FAILURES  ($fail/$((pass + fail)) scenarios failed)"
  exit 1
fi
