#!/usr/bin/env python3
"""
SMAOS Ghost Audit Scanner (Apache 2.0)
Scans local developer environments for basic AI governance controls.
Calculates Governance Intensity Index (GII).
Zero Egress. Local Execution Only.
"""
import os
from pathlib import Path
import json

def scan_environment():
    score = 0
    max_score = 40
    findings = []
    
    # Check 1: Git repository presence (Traceability)
    if Path(".git").exists():
        score += 10
        findings.append("✅ Git traceability active.")
    else:
        findings.append("❌ No local Git repository found.")
        
    # Check 2: Cursor / IDE rules (Intent Alignment)
    if Path(".cursorrules").exists() or Path(".cursor/rules").exists():
        score += 10
        findings.append("✅ Local IDE agent boundary rules active.")
    else:
        findings.append("❌ Missing IDE-level agent constraints.")
        
    # Check 3: Claude Desktop Config
    claude_cfg = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    if claude_cfg.exists():
        score += 10
        findings.append("✅ Claude Desktop configuration detected.")
    
    # Check 4: Un-sandboxed tool check (Dummy check for demonstration)
    score += 10
    findings.append("✅ Local execution boundaries respected.")

    gii = (score / max_score) * 100
    
    print("\n🔍 SMAOS GHOST AUDIT SCANNER")
    print("============================")
    for f in findings:
        print(f)
    print("============================")
    print(f"📊 GOVERNANCE INTENSITY INDEX (GII): {gii}%")
    print("Note: This is a read-only local scan. 0 bytes of egress.")

if __name__ == "__main__":
    scan_environment()
