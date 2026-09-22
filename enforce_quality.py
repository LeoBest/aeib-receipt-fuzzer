import os
import sys
from pathlib import Path

ROOT = Path("/Users/andriileukhin/Documents/SovereignNexus/aeib-receipt-fuzzer")

APACHE_HEADER = """#!/usr/bin/env python3
# Copyright 2026 SovereignNexus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

# 1. Rename smaos-dora-compiler/compiler.py to validate_dora_register.py
old_dora = ROOT / "smaos-dora-compiler/compiler.py"
new_dora = ROOT / "validate_dora_register.py"
if old_dora.exists():
    dora_src = old_dora.read_text()
    if not dora_src.startswith("# Copyright"):
        dora_src = dora_src.replace("#!/usr/bin/env python3\n", APACHE_HEADER)
    new_dora.write_text(dora_src)
    import shutil
    shutil.rmtree(ROOT / "smaos-dora-compiler")
    print("Renamed DORA compiler -> validate_dora_register.py")

# 2. Add Apache Headers to all Python scripts
for script_name in ["run.py", "demo_launcher.py", "ghost_audit_scanner.py"]:
    f = ROOT / script_name
    if f.exists():
        src = f.read_text()
        if "Copyright" not in src:
            src = src.replace("#!/usr/bin/env python3\n", APACHE_HEADER)
            f.write_text(src)
            print(f"Added Apache 2.0 header to {script_name}")

# 3. Add tests for the new scripts
test_engine = ROOT / "tests/test_engine.py"
test_src = test_engine.read_text()
if "test_ghost_audit_scanner" not in test_src:
    new_tests = """
def test_ghost_audit_scanner():
    cmd = [sys.executable, str(ROOT / "ghost_audit_scanner.py")]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    assert res.returncode == 0
    assert "GOVERNANCE INTENSITY INDEX (GII)" in res.stdout
    assert "0 bytes of egress" in res.stdout

def test_validate_dora_register():
    cmd = [sys.executable, str(ROOT / "validate_dora_register.py")]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    assert res.returncode == 0
    assert "SMAOS DORA xBRL-CSV Compiler" in res.stdout
    assert "R0010" in res.stdout
"""
    test_engine.write_text(test_src + new_tests)
    print("Added tests for Ghost Scanner and DORA Validator")

