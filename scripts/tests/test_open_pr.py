import open_pr


class FakeRun:
    def __init__(self, branch, untracked=""):
        self.branch = branch
        self.untracked = untracked
        self.calls = []

    def __call__(self, args, **kw):
        self.calls.append(args)
        if args[:4] == ["git", "rev-parse", "--abbrev-ref", "HEAD"]:
            return self.branch + "\n"
        if args[:4] == ["git", "ls-files", "--others", "--exclude-standard"]:
            return self.untracked
        if args[:3] == ["gh", "pr", "create"]:
            return "https://github.com/o/r/pull/7\n"
        return ""

    def has(self, prefix):
        return any(c[: len(prefix)] == prefix for c in self.calls)


def test_creates_branch_when_on_base(monkeypatch, capsys):
    fake = FakeRun(branch="main")
    monkeypatch.setattr(open_pr, "run", fake)

    rc = open_pr.main(["--title", "Add widget", "--body", "b"])

    assert rc == 0
    assert fake.has(["git", "switch", "-c", "add-widget"])
    assert fake.has(["gh", "pr", "create"])
    assert "pull/7" in capsys.readouterr().out


def test_keeps_existing_feature_branch(monkeypatch):
    fake = FakeRun(branch="feature/x")
    monkeypatch.setattr(open_pr, "run", fake)

    open_pr.main(["--title", "Add widget", "--body", "b"])

    assert not fake.has(["git", "switch", "-c"])
    # pushes the branch we were already on
    assert ["git", "push", "-u", "origin", "feature/x"] in fake.calls


def test_explicit_branch_name_used(monkeypatch):
    fake = FakeRun(branch="main")
    monkeypatch.setattr(open_pr, "run", fake)

    open_pr.main(["--title", "Add widget", "--branch", "custom/name"])

    assert fake.has(["git", "switch", "-c", "custom/name"])


def test_specific_paths_staged(monkeypatch):
    fake = FakeRun(branch="feature/x")
    monkeypatch.setattr(open_pr, "run", fake)

    open_pr.main(["--title", "t", "--add", "a.py", "b.py"])

    assert ["git", "add", "--", "a.py", "b.py"] in fake.calls
    assert not fake.has(["git", "add", "-A"])
    assert not fake.has(["git", "add", "-u"])


def test_default_stages_tracked_modifications_only(monkeypatch):
    fake = FakeRun(branch="feature/x")
    monkeypatch.setattr(open_pr, "run", fake)

    open_pr.main(["--title", "t"])

    assert ["git", "add", "-u"] in fake.calls
    assert not fake.has(["git", "add", "-A"])


def test_warns_on_untracked_files(monkeypatch, capsys):
    fake = FakeRun(branch="feature/x", untracked="new.py\nsecret.env\n")
    monkeypatch.setattr(open_pr, "run", fake)

    rc = open_pr.main(["--title", "t"])

    assert rc == 0
    assert ["git", "add", "-u"] in fake.calls
    err = capsys.readouterr().err
    assert "new.py" in err
    assert "secret.env" in err


def test_no_warning_when_no_untracked(monkeypatch, capsys):
    fake = FakeRun(branch="feature/x")
    monkeypatch.setattr(open_pr, "run", fake)

    open_pr.main(["--title", "t"])

    assert capsys.readouterr().err == ""


def test_untracked_not_checked_when_paths_explicit(monkeypatch, capsys):
    fake = FakeRun(branch="feature/x", untracked="new.py\n")
    monkeypatch.setattr(open_pr, "run", fake)

    open_pr.main(["--title", "t", "--add", "a.py"])

    assert not fake.has(["git", "ls-files", "--others", "--exclude-standard"])
    assert capsys.readouterr().err == ""


def test_slugify():
    assert open_pr.slugify("Fix the Login Bug!") == "fix-the-login-bug"
