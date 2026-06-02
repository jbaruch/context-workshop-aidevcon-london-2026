#!/usr/bin/env python3
"""Poll a PR until Copilot's review lands, then print it as JSON.

Replaces code-ticket step 6: the "wait ~10s, query, check, loop" prose. The
loop is pure mechanism. The script blocks until Copilot has reviewed, then
emits the verdict and comments so the skill can decide what to fix.

Output (stdout, JSON):
  {"state": "<APPROVED|CHANGES_REQUESTED|COMMENTED>",
   "clean": <bool>,
   "comments": [{"path": ..., "line": ..., "body": ...}, ...]}

`clean` is true when Copilot approved with no review comments — the merge gate.

Usage:
  await_copilot_review.py <pr-number> [--interval 10] [--timeout 300]
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from _github import COPILOT_BOT_LOGIN, gh_graphql, repo_owner_name

REVIEW_QUERY = """
query($owner:String!,$name:String!,$number:Int!){
  repository(owner:$owner,name:$name){
    pullRequest(number:$number){
      reviews(last:20){
        nodes{
          author{ login }
          state
          submittedAt
          comments(first:100){ nodes{ path line body } }
        }
      }
    }
  }
}
"""


def latest_copilot_review(pr_number: int) -> dict | None:
    """Return Copilot's most recent review on the PR, or None if it hasn't
    reviewed yet."""
    owner, name = repo_owner_name()
    data = gh_graphql(REVIEW_QUERY, owner=owner, name=name, number=pr_number)
    reviews = data["repository"]["pullRequest"]["reviews"]["nodes"]
    copilot = [r for r in reviews if (r.get("author") or {}).get("login") == COPILOT_BOT_LOGIN]
    if not copilot:
        return None
    return max(copilot, key=lambda r: r.get("submittedAt") or "")


def summarize(review: dict) -> dict:
    comments = [
        {"path": c.get("path"), "line": c.get("line"), "body": c.get("body")}
        for c in review.get("comments", {}).get("nodes", [])
    ]
    state = review.get("state")
    return {
        "state": state,
        "clean": state == "APPROVED" and not comments,
        "comments": comments,
    }


def await_review(
    pr_number: int, *, interval: float = 10.0, timeout: float = 300.0, sleep=time.sleep
) -> dict:
    """Block until Copilot has reviewed, returning the summary. Raises on
    timeout."""
    deadline = time.monotonic() + timeout
    while True:
        review = latest_copilot_review(pr_number)
        if review is not None:
            return summarize(review)
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Copilot did not review PR #{pr_number} within {timeout:.0f}s"
            )
        sleep(interval)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr_number", type=int)
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args(argv)
    result = await_review(args.pr_number, interval=args.interval, timeout=args.timeout)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
