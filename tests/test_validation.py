from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ContractValidationTests(unittest.TestCase):
    def test_contract_validation(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_contracts.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_openapi_reference_check(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/check_openapi_refs.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
