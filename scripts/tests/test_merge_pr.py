import merge_pr


class Recorder:
    def __init__(self):
        self.calls = []

    def __call__(self, args, **kw):
        self.calls.append(args)
        return ""


def test_default_squash_and_delete_branch(monkeypatch):
    rec = Recorder()
    monkeypatch.setattr(merge_pr, "run", rec)

    merge_pr.main(["7"])

    assert rec.calls == [["gh", "pr", "merge", "7", "--squash", "--delete-branch"]]


def test_method_override(monkeypatch):
    rec = Recorder()
    monkeypatch.setattr(merge_pr, "run", rec)

    merge_pr.main(["7", "--method", "merge", "--no-delete-branch"])

    assert rec.calls == [["gh", "pr", "merge", "7", "--merge"]]
