#!/usr/bin/env python3
"""Request a Copilot review on a PR.

Replaces code-ticket step 5: the prose that told the model to hand-build a
GraphQL POST with a bearer token, look up node ids, and "if GitHub returns an
error, correct whatever field was wrong and send it again until it goes
through." That trial-and-error is gone — the ids are resolved deterministically
and the mutation is fired once.

Usage:
  request_copilot_review.py <pr-number>
"""

from __future__ import annotations

import argparse
import sys

from _github import copilot_reviewer_id, gh_graphql, pr_node_id

MUTATION = """
mutation($prId:ID!,$reviewerId:ID!){
  requestReviews(input:{pullRequestId:$prId, userIds:[$reviewerId], union:true}){
    pullRequest{ number }
  }
}
"""


def request_review(pr_number: int) -> None:
    pr_id = pr_node_id(pr_number)
    reviewer_id = copilot_reviewer_id()
    gh_graphql(MUTATION, prId=pr_id, reviewerId=reviewer_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr_number", type=int)
    args = parser.parse_args(argv)
    request_review(args.pr_number)
    print(f"requested Copilot review on PR #{args.pr_number}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
