import subprocess
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "validate-draft.sh"
FIX = Path(__file__).resolve().parent / "fixtures"


def _run(path):
    return subprocess.run(["bash", str(HOOK), str(path)], capture_output=True, text=True)


def test_good_skill_passes():
    assert _run(FIX / "good-skill.md").returncode == 0


def test_good_agent_passes():
    assert _run(FIX / "good-agent.md").returncode == 0


def test_no_frontmatter_fails():
    assert _run(FIX / "bad-no-frontmatter.md").returncode == 1


def test_empty_description_fails():
    assert _run(FIX / "bad-empty-description.md").returncode == 1


def test_missing_file_is_usage_error():
    assert _run(FIX / "does-not-exist.md").returncode == 2
