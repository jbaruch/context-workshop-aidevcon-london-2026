#!/usr/bin/env python3
"""Detect the project's test runner and run the whole suite.

Replaces the prose in code-ticket steps 1 and 3. Detection is a pure
filesystem decision, so it is fully deterministic and easy to test for real.

Usage:
  run_tests.py            run the full suite; exit with the suite's code
  run_tests.py --check    only detect; exit 0 if tests exist (print runner),
                          exit 3 if the project has no tests at all
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

NO_TESTS_EXIT = 3


def detect_runner(root: Path) -> list[str] | None:
    """Return the command to run the suite, or None if the project has no tests.

    Order matters: an explicit `test` script in package.json wins over a guess.
    """
    pkg = root / "package.json"
    if pkg.is_file():
        try:
            scripts = json.loads(pkg.read_text()).get("scripts", {})
        except json.JSONDecodeError:
            scripts = {}
        if "test" in scripts:
            return ["npm", "test"]

    makefile = root / "Makefile"
    if makefile.is_file() and _make_has_test_target(makefile):
        return ["make", "test"]

    if _glob_any(root, ["test_*.py", "*_test.py"]) or (root / "tests").is_dir():
        return [sys.executable, "-m", "pytest"]

    if _glob_any(root, ["*_test.go"]):
        return ["go", "test", "./..."]

    if _glob_any(root, ["*.test.ts", "*.test.tsx", "*.test.js", "*.test.jsx"]):
        return ["npm", "test"]

    return None


def _glob_any(root: Path, patterns: list[str]) -> bool:
    return any(next(root.rglob(p), None) is not None for p in patterns)


def _make_has_test_target(makefile: Path) -> bool:
    for line in makefile.read_text().splitlines():
        if line.startswith("test:") or line.startswith("test "):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="detect only, don't run")
    parser.add_argument("--root", default=".", help="project root (default: cwd)")
    args = parser.parse_args(argv)

    runner = detect_runner(Path(args.root))
    if runner is None:
        print("no tests found", file=sys.stderr)
        return NO_TESTS_EXIT

    print(" ".join(runner))
    if args.check:
        return 0
    return subprocess.run(runner, cwd=args.root).returncode


if __name__ == "__main__":
    raise SystemExit(main())
