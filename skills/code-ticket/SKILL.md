---
name: code-ticket
description: Workflow for a ticket that touches real source code (anything that is not purely documentation). Use when a ticket changes code, or when you cannot tell whether it is docs or code (default to this). Covers tests-first gating, implementation, running the full suite, PR, Copilot review, and merge-on-clean-review.
---

# Code ticket workflow

Use this when a ticket touches any real source code (anything that is not purely documentation). If you genuinely cannot tell whether a ticket is documentation or code, treat it as a code ticket — code changes are the riskier ones, so it is always safer to take the more careful path.

The deterministic mechanics live in `scripts/` (run them from the repo root). This skill is the judgment: deciding *what* to build and *how* to fix failures and review comments. Two mandatory gates apply — [no tests, no PR](../../rules/tests-first.md) and [merge only on a clean review](../../rules/merge-on-clean-review.md); follow them exactly.

## Steps

1. **Tests-first gate** ([rule](../../rules/tests-first.md)). Run `python3 scripts/run_tests.py --check`. If it exits non-zero, stop here — write tests first before implementing or opening a PR.
2. Implement what the ticket asked for.
3. Run the whole suite with `python3 scripts/run_tests.py`. If it exits non-zero, read the failures, fix the code, and run it again. Repeat until it exits 0 — do not move on while even one test fails.
4. Open the PR: `python3 scripts/open_pr.py --title "<title>" --body "<body>"`. You supply the title and body (judgment); the script creates the branch if needed, commits, pushes, and opens the PR against `main`. It prints the PR URL.
5. Request a Copilot review: `python3 scripts/request_copilot_review.py <pr-number>`. (The script resolves the PR and reviewer ids and fires the request — no manual GraphQL.)
6. Wait for the review: `python3 scripts/await_copilot_review.py <pr-number>`. It blocks until Copilot has reviewed, then prints JSON: `{"state", "clean", "comments"}`.
7. If `clean` is `false`, address **every** comment in the JSON: fix the code, push, then re-run step 5 and step 6. Repeat this fix-summon-wait loop as many times as needed.
8. **Merge gate** ([rule](../../rules/merge-on-clean-review.md)). Only proceed once the review JSON reports `"clean": true`.
9. When the review is clean, merge: `python3 scripts/merge_pr.py <pr-number>`.
