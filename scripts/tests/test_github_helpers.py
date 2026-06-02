import json

import pytest

import _github
from _github import CommandError


class Dispatcher:
    """Stand-in for `run` that answers by command shape."""

    def __init__(self, graphql_payloads):
        self._graphql = list(graphql_payloads)

    def __call__(self, args, **kw):
        if args[:3] == ["gh", "repo", "view"]:
            return json.dumps({"owner": {"login": "o"}, "name": "r"})
        if args[:3] == ["gh", "api", "graphql"]:
            return json.dumps({"data": self._graphql.pop(0)})
        raise AssertionError(f"unexpected command {args}")


def test_repo_owner_name(monkeypatch):
    monkeypatch.setattr(_github, "run", Dispatcher([]))
    assert _github.repo_owner_name() == ("o", "r")


def test_gh_graphql_raises_on_errors(monkeypatch):
    monkeypatch.setattr(_github, "run", lambda *a, **k: json.dumps({"errors": [{"message": "bad"}]}))
    with pytest.raises(CommandError):
        _github.gh_graphql("query{}")


def test_pr_node_id(monkeypatch):
    payload = {"repository": {"pullRequest": {"id": "PR_node_1"}}}
    monkeypatch.setattr(_github, "run", Dispatcher([payload]))
    assert _github.pr_node_id(7) == "PR_node_1"


def test_copilot_reviewer_id_found(monkeypatch):
    payload = {
        "repository": {
            "suggestedActors": {
                "nodes": [
                    {"login": "someone", "__typename": "User", "id": "U1"},
                    {"login": _github.COPILOT_BOT_LOGIN, "__typename": "Bot", "id": "BOT_1"},
                ]
            }
        }
    }
    monkeypatch.setattr(_github, "run", Dispatcher([payload]))
    assert _github.copilot_reviewer_id() == "BOT_1"


def test_copilot_reviewer_id_missing_raises(monkeypatch):
    payload = {"repository": {"suggestedActors": {"nodes": [{"login": "human", "id": "U1"}]}}}
    monkeypatch.setattr(_github, "run", Dispatcher([payload]))
    with pytest.raises(CommandError):
        _github.copilot_reviewer_id()


def test_run_raises_command_error_on_nonzero(monkeypatch):
    class FakeProc:
        returncode = 1
        stdout = ""
        stderr = "boom"

    monkeypatch.setattr(_github.subprocess, "run", lambda *a, **k: FakeProc())
    with pytest.raises(CommandError) as exc:
        _github.run(["false"])
    assert "boom" in str(exc.value)
