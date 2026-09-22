from pathlib import Path

run_py = Path("/Users/andriileukhin/Documents/SovereignNexus/aeib-receipt-fuzzer/run.py")
src = run_py.read_text()

if "signature_bbs_plus" not in src:
    src = src.replace(
        '"signature_ed25519": "ed25519:e58e93e6b76a1b1bed74a6ed7836ca362"',
        '"signature_ed25519": "ed25519:e58e93e6b76a1b1bed74a6ed7836ca362",\n        "signature_bbs_plus": "bbs_plus:mock_selective_disclosure_signature"'
    )
    run_py.write_text(src)
    print("Added BBS+ signature scaffold to run.py")
