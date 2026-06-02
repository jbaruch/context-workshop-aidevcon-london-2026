import request_copilot_review as rcr


def test_request_review_wires_resolved_ids(monkeypatch):
    captured = {}

    monkeypatch.setattr(rcr, "pr_node_id", lambda n: f"PR_{n}")
    monkeypatch.setattr(rcr, "copilot_reviewer_id", lambda: "BOT_1")

    def fake_graphql(query, **variables):
        captured["query"] = query
        captured["vars"] = variables
        return {}

    monkeypatch.setattr(rcr, "gh_graphql", fake_graphql)

    rcr.request_review(42)

    assert captured["vars"] == {"prId": "PR_42", "reviewerId": "BOT_1"}
    assert "requestReviews" in captured["query"]


def test_main_prints_confirmation(monkeypatch, capsys):
    monkeypatch.setattr(rcr, "pr_node_id", lambda n: "PR")
    monkeypatch.setattr(rcr, "copilot_reviewer_id", lambda: "BOT")
    monkeypatch.setattr(rcr, "gh_graphql", lambda *a, **k: {})

    assert rcr.main(["42"]) == 0
    assert "#42" in capsys.readouterr().out
