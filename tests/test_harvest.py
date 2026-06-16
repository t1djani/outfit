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
