import os
import sys
import subprocess
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import harvest  # noqa: E402


def _make_repo(tmp):
    root = Path(tmp)
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("print('hi')\n")
    (root / "README.md").write_text("# Demo\nA demo project.\n")
    (root / "node_modules").mkdir()
    (root / "node_modules" / "junk.js").write_text("x\n")
    (root / ".git").mkdir()
    return root


def test_build_tree_lists_files_and_skips_noise():
    with tempfile.TemporaryDirectory() as tmp:
        root = _make_repo(tmp)
        tree = harvest.build_tree(root, max_depth=3)
        assert "src" in tree
        assert "app.py" in tree
        assert "README.md" in tree
        # noise dirs are skipped
        assert "node_modules" not in tree
        assert ".git" not in tree


def test_read_key_files_returns_present_manifests_bounded():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text("# Demo\n" + "x\n" * 50)
        (root / "package.json").write_text('{"name":"demo"}\n')
        (root / "CLAUDE.md").write_text("project rules\n")
        found = harvest.read_key_files(root, max_bytes=40)
        names = {name for name, _ in found}
        assert "README.md" in names
        assert "package.json" in names
        assert "CLAUDE.md" in names
        # absent manifests are simply not present
        assert "pyproject.toml" not in names
        # content is byte-bounded (slice + truncation suffix, measured in bytes)
        suffix = "\n… (truncated)".encode("utf-8")
        for _, content in found:
            assert len(content.encode("utf-8")) <= 40 + len(suffix)


def test_git_summary_handles_non_git_dir():
    with tempfile.TemporaryDirectory() as tmp:
        # not a git repo
        summary = harvest.git_summary(Path(tmp))
        assert "no git history" in summary.lower()


def test_find_docs_lists_markdown_under_docs():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs").mkdir()
        (root / "docs" / "guide.md").write_text("guide\n")
        (root / "docs" / "deep").mkdir()
        (root / "docs" / "deep" / "spec.md").write_text("spec\n")
        docs = harvest.find_docs(root)
        joined = "\n".join(docs)
        assert "guide.md" in joined
        assert "spec.md" in joined


def test_detect_resources_flags_known_artifacts():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".servo").mkdir()
        (root / ".servo" / "manifest.yaml").write_text("experts: []\n")
        (root / ".mcp.json").write_text('{"mcpServers":{"linear":{}}}\n')
        (root / ".claude").mkdir()
        (root / ".claude" / "skills").mkdir()
        res = harvest.detect_resources(root)
        assert ".servo/manifest.yaml" in res
        assert ".mcp.json" in res
        assert ".claude/skills" in res


def test_main_emits_all_sections():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "README.md").write_text("# Demo\n")
        (root / "src").mkdir()
        (root / "src" / "app.py").write_text("x=1\n")
        out = harvest.render(root)
        for header in [
            "# outfit · evidence dossier",
            "## TREE",
            "## KEY FILES",
            "## GIT",
            "## DOCS",
            "## RESOURCES",
            "## NEXT",
        ]:
            assert header in out
        # NEXT must remind the reader that decisions are the agent's job
        assert "decides nothing" in out.lower()


def test_script_runs_as_subprocess():
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "README.md").write_text("# Demo\n")
        script = Path(__file__).resolve().parent.parent / "scripts" / "harvest.py"
        r = subprocess.run(
            [sys.executable, str(script), tmp],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode == 0
        assert "# outfit · evidence dossier" in r.stdout
