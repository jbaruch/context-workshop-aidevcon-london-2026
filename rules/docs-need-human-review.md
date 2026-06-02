# Rule: documentation PRs are reviewed by a human, never the bot

**Scope:** documentation-only PRs (the `documentation-ticket` workflow) — changes
confined to the README, `docs/`, any `.md` file, or plain text/typo fixes, with
no source-code changes.

Prose is judged by people, not by a code reviewer. Therefore, for a docs PR:

- You **MUST** leave the review to a **human**.
- You **MUST NOT** request the Copilot reviewer
  (`scripts/request_copilot_review.py`) on a documentation PR.
- You **MUST NOT** merge until a human has approved it.

If you are unsure whether a ticket is documentation or code, it is **not** a docs
ticket — treat it as code and follow [tests-first](tests-first.md) and
[merge-on-clean-review](merge-on-clean-review.md) instead.
