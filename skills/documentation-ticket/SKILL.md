---
name: documentation-ticket
description: Workflow for a documentation-only ticket — one that changes only the README, files under docs/, any .md file, or a plain text/typo fix, with no source-code changes. Covers the branch, commit, push, PR, human-review, and merge steps.
---

# Documentation ticket workflow

Use this when a ticket changes **only** documentation: the README, files inside `docs/`, any file ending in `.md`, or a plain text/typo fix — and touches no source code.

The deterministic PR mechanics live in `scripts/` (run from the repo root). This skill is the judgment; the mandatory gate is [docs are reviewed by a human, never the bot](../../rules/docs-need-human-review.md).

## Steps

1. Make the requested documentation change.
2. Open the PR: `python3 scripts/open_pr.py --title "<title>" --body "<body>"`. You supply the title and body; the script creates the branch, commits, pushes, and opens the PR against `main`, printing the URL.
3. **Human-review gate** ([rule](../../rules/docs-need-human-review.md)). Leave it for a **human** to review — do **not** request the Copilot reviewer.
4. Once a human approves it, merge: `python3 scripts/merge_pr.py <pr-number>`.

Keep it simple — do not add extra steps.
