#!/usr/bin/env python3
"""Merge a PR.

Replaces the merge mechanics (code-ticket step 9, documentation-ticket step 7).
The *gate* — only merge on a clean Copilot review / human approval — is a rule
the skill enforces; this script just performs the merge once told to.

Usage:
  merge_pr.py <pr-number> [--method squash|merge|rebase] [--delete-branch]
"""

from __future__ import annotations

import argparse
import sys

from _github import run


def merge(pr_number: int, *, method: str = "squash", delete_branch: bool = True) -> None:
    args = ["gh", "pr", "merge", str(pr_number), f"--{method}"]
    if delete_branch:
        args.append("--delete-branch")
    run(args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr_number", type=int)
    parser.add_argument("--method", choices=["squash", "merge", "rebase"], default="squash")
    parser.add_argument("--no-delete-branch", dest="delete_branch", action="store_false")
    args = parser.parse_args(argv)
    merge(args.pr_number, method=args.method, delete_branch=args.delete_branch)
    print(f"merged PR #{args.pr_number}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
