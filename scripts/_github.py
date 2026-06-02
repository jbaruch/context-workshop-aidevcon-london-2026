"""Shared helpers for the GitHub/git scripts.

Everything that touches the outside world goes through `run()`. The scripts
import and call it; the tests monkeypatch it. That single seam is what makes
these deterministic wrappers testable without a live GitHub.
"""

from __future__ import annotations

import json
import subprocess

# The login of GitHub's Copilot review bot. Used to request it as a reviewer
# and to recognise its reviews when polling.
COPILOT_BOT_LOGIN = "copilot-pull-request-reviewer"


class CommandError(RuntimeError):
    """A subprocess exited non-zero. Carries stdout/stderr for the caller."""

    def __init__(self, args: list[str], returncode: int, stdout: str, stderr: str):
        self.args_run = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(
            f"command {args!r} exited {returncode}: {stderr.strip() or stdout.strip()}"
        )


def run(args: list[str], *, check: bool = True, input_text: str | None = None) -> str:
    """Run a command and return stdout. The one boundary tests mock."""
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        input=input_text,
    )
    if check and proc.returncode != 0:
        raise CommandError(args, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout


def gh_graphql(query: str, **variables: object) -> dict:
    """Run a GraphQL query via `gh api graphql`. gh supplies auth, so there is
    no token to fumble. Returns the parsed `data` object."""
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for name, value in variables.items():
        flag = "-F" if isinstance(value, (int, bool)) else "-f"
        args += [flag, f"{name}={value}"]
    out = run(args)
    payload = json.loads(out)
    if "errors" in payload:
        raise CommandError(args, 0, out, json.dumps(payload["errors"]))
    return payload["data"]


def repo_owner_name() -> tuple[str, str]:
    """The current repo's owner and name, from gh."""
    out = run(["gh", "repo", "view", "--json", "owner,name"])
    data = json.loads(out)
    return data["owner"]["login"], data["name"]


def pr_node_id(pr_number: int) -> str:
    """Resolve a PR number to its GraphQL node id."""
    owner, name = repo_owner_name()
    data = gh_graphql(
        """
        query($owner:String!,$name:String!,$number:Int!){
          repository(owner:$owner,name:$name){
            pullRequest(number:$number){ id }
          }
        }
        """,
        owner=owner,
        name=name,
        number=pr_number,
    )
    return data["repository"]["pullRequest"]["id"]


def copilot_reviewer_id() -> str:
    """Resolve the Copilot review bot's node id for the current repo."""
    owner, name = repo_owner_name()
    data = gh_graphql(
        """
        query($owner:String!,$name:String!){
          repository(owner:$owner,name:$name){
            suggestedActors(capabilities:[CAN_BE_ASSIGNED], first:100){
              nodes{ login __typename ... on Bot { id } ... on User { id } }
            }
          }
        }
        """,
        owner=owner,
        name=name,
    )
    nodes = data["repository"]["suggestedActors"]["nodes"]
    for node in nodes:
        if node.get("login") == COPILOT_BOT_LOGIN:
            return node["id"]
    raise CommandError(
        ["copilot_reviewer_id"],
        0,
        "",
        f"Copilot reviewer ({COPILOT_BOT_LOGIN}) is not available on this repo. "
        "Is the Copilot code review feature enabled?",
    )
