#!/usr/bin/env python3
"""Branch (if needed), commit, push, and open a PR against the base branch.

Replaces the deterministic git/gh plumbing shared by both skills. The judgment
parts (the title, body, branch name, what to stage) are inputs the skill
supplies; the mechanics live here.

Usage:
  open_pr.py --title T --body B [--branch NAME] [--base main] [--add PATH ...]

Prints the PR URL on success.
"""

from __future__ import annotations

import argparse
import re
import sys

from _github import run


def current_branch() -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:50] or "change"


def ensure_branch(base: str, fallback_name: str) -> str:
    """Make sure we're on a feature branch, not the base. Returns its name.

    If already off the base branch, keep that branch. Otherwise create one.
    """
    cur = current_branch()
    if cur != base:
        return cur
    run(["git", "switch", "-c", fallback_name])
    return fallback_name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--base", default="main")
    parser.add_argument("--branch", default=None, help="branch name if one must be created")
    parser.add_argument(
        "--add",
        nargs="*",
        default=None,
        help="paths to stage (default: tracked modifications only)",
    )
    args = parser.parse_args(argv)

    branch = ensure_branch(args.base, args.branch or slugify(args.title))

    if args.add:
        run(["git", "add", "--", *args.add])
    else:
        run(["git", "add", "-u"])
        untracked = [
            line
            for line in run(["git", "ls-files", "--others", "--exclude-standard"]).splitlines()
            if line.strip()
        ]
        if untracked:
            print(
                "warning: leaving untracked files out of the commit "
                "(pass --add to include them):\n  " + "\n  ".join(untracked),
                file=sys.stderr,
            )
    run(["git", "commit", "-m", args.title] + (["-m", args.body] if args.body else []))
    run(["git", "push", "-u", "origin", branch])

    url = run(
        ["gh", "pr", "create", "--base", args.base, "--head", branch,
         "--title", args.title, "--body", args.body]
    ).strip()
    print(url)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # surface the failing command cleanly to the skill
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
