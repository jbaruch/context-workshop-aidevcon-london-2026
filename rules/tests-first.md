# Rule: no tests, no PR

**Scope:** any ticket that touches source code (the `code-ticket` workflow).

A project with no tests gives a code change nothing to stand on. Therefore:

- Before implementing a code ticket, you **MUST** run the deterministic gate:
  `python3 scripts/run_tests.py --check`.
- If it exits non-zero (no test runner detected), you **MUST NOT** implement the
  change and **MUST NOT** open a PR. Write tests first, then re-run the gate.
- You **MUST NOT** rationalise around this ("it's a tiny change", "I'll add tests
  later"). No tests means no PR, full stop.

The check is mechanical and lives in `scripts/run_tests.py` (`--check`); this
rule is the obligation to honour its exit code.
