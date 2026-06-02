import json
import sys

import run_tests
from run_tests import NO_TESTS_EXIT, detect_runner


def test_package_json_test_script_wins(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
    assert detect_runner(tmp_path) == ["npm", "test"]


def test_pytest_detected_from_tests_dir(tmp_path):
    (tmp_path / "tests").mkdir()
    assert detect_runner(tmp_path) == [sys.executable, "-m", "pytest"]


def test_pytest_detected_from_test_file(tmp_path):
    (tmp_path / "test_thing.py").write_text("def test_x(): pass")
    assert detect_runner(tmp_path) == [sys.executable, "-m", "pytest"]


def test_go_detected(tmp_path):
    (tmp_path / "main_test.go").write_text("package main")
    assert detect_runner(tmp_path) == ["go", "test", "./..."]


def test_makefile_test_target(tmp_path):
    (tmp_path / "Makefile").write_text("test:\n\techo hi\n")
    assert detect_runner(tmp_path) == ["make", "test"]


def test_no_tests_returns_none(tmp_path):
    (tmp_path / "README.md").write_text("# docs only")
    assert detect_runner(tmp_path) is None


def test_check_exits_3_when_no_tests(tmp_path, capsys):
    assert run_tests.main(["--check", "--root", str(tmp_path)]) == NO_TESTS_EXIT


def test_check_exits_0_and_prints_runner(tmp_path, capsys):
    (tmp_path / "tests").mkdir()
    rc = run_tests.main(["--check", "--root", str(tmp_path)])
    assert rc == 0
    assert "pytest" in capsys.readouterr().out


def test_run_returns_suite_exit_code(tmp_path, monkeypatch):
    (tmp_path / "tests").mkdir()

    class FakeProc:
        returncode = 5

    monkeypatch.setattr(run_tests.subprocess, "run", lambda *a, **k: FakeProc())
    assert run_tests.main(["--root", str(tmp_path)]) == 5
