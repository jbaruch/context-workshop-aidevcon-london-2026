import pytest

import await_copilot_review as acr


def _review(state, comments=(), login=acr.COPILOT_BOT_LOGIN, submitted="2026-01-01T00:00:00Z"):
    return {
        "author": {"login": login},
        "state": state,
        "submittedAt": submitted,
        "comments": {"nodes": [dict(c) for c in comments]},
    }


def _data(reviews):
    return {"repository": {"pullRequest": {"reviews": {"nodes": reviews}}}}


def test_summarize_clean_approval():
    out = acr.summarize(_review("APPROVED"))
    assert out == {"state": "APPROVED", "clean": True, "comments": []}


def test_summarize_changes_requested_is_not_clean():
    review = _review("CHANGES_REQUESTED", [{"path": "a.py", "line": 3, "body": "fix"}])
    out = acr.summarize(review)
    assert out["clean"] is False
    assert out["comments"] == [{"path": "a.py", "line": 3, "body": "fix"}]


def test_approved_with_comments_is_not_clean():
    review = _review("APPROVED", [{"path": "a.py", "line": 1, "body": "nit"}])
    assert acr.summarize(review)["clean"] is False


def test_latest_picks_most_recent_copilot_review(monkeypatch):
    monkeypatch.setattr(acr, "repo_owner_name", lambda: ("o", "r"))
    reviews = [
        _review("COMMENTED", submitted="2026-01-01T00:00:00Z"),
        _review("APPROVED", submitted="2026-02-01T00:00:00Z"),
        _review("CHANGES_REQUESTED", login="someone-else", submitted="2026-03-01T00:00:00Z"),
    ]
    monkeypatch.setattr(acr, "gh_graphql", lambda *a, **k: _data(reviews))
    assert acr.latest_copilot_review(1)["state"] == "APPROVED"


def test_returns_none_when_copilot_has_not_reviewed(monkeypatch):
    monkeypatch.setattr(acr, "repo_owner_name", lambda: ("o", "r"))
    monkeypatch.setattr(acr, "gh_graphql", lambda *a, **k: _data([_review("APPROVED", login="human")]))
    assert acr.latest_copilot_review(1) is None


def test_await_polls_until_review_lands(monkeypatch):
    monkeypatch.setattr(acr, "repo_owner_name", lambda: ("o", "r"))
    responses = iter([_data([]), _data([_review("APPROVED")])])
    monkeypatch.setattr(acr, "gh_graphql", lambda *a, **k: next(responses))
    sleeps = []

    result = acr.await_review(1, interval=0, timeout=100, sleep=lambda s: sleeps.append(s))

    assert result["clean"] is True
    assert sleeps == [0]  # slept once between the empty poll and the hit


def test_await_times_out(monkeypatch):
    monkeypatch.setattr(acr, "repo_owner_name", lambda: ("o", "r"))
    monkeypatch.setattr(acr, "gh_graphql", lambda *a, **k: _data([]))
    with pytest.raises(TimeoutError):
        acr.await_review(1, interval=0, timeout=0, sleep=lambda s: None)
