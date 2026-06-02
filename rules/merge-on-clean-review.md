# Rule: merge a code PR only on a clean Copilot review

**Scope:** code PRs (the `code-ticket` workflow).

The Copilot review is the gate, not a formality. Therefore:

- You **MUST** obtain the review verdict from
  `python3 scripts/await_copilot_review.py <pr-number>`, which prints JSON
  including a `clean` boolean.
- You **MUST NOT** call `scripts/merge_pr.py` unless that JSON reports
  `"clean": true` (Copilot approved with **no** outstanding comments).
- If `clean` is `false`, you **MUST** address **every** comment, push the fix,
  re-request the review, and wait again — repeating until it is clean.
- You **MUST NOT** merge while even one comment is unresolved, even if you judge
  it unimportant. "I think it's fine" is not clean.

`clean` is computed deterministically in `scripts/await_copilot_review.py`
(`summarize`); this rule forbids merging until it is `true`.
