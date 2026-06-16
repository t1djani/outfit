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
