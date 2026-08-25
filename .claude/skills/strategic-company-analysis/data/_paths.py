"""Where things are: this skill inside its project.

Adapted from finance-reports/_paths.py (2026-08-25), trimmed to the ascent —
this skill is SELF-CONTAINED on purpose and imports nothing from other skills.

ONE ASCENT, ONE MARKER: the `.claude` directory. The project root is derived
from it, so the files that need configuration cannot disagree about where the
project keeps it:

    <project>/                                    PROJECT_ROOT  config, secrets, environment
      .claude/skills/strategic-company-analysis/  SKILL_DIR     this skill
        data/                                     DATA_DIR      these files
"""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
SKILL_DIR = DATA_DIR.parent


def _ascend(start: Path, marker: str) -> Path:
    """Nearest ancestor of `start` containing `marker`. Hard error, no guess."""
    for directory in [start, *start.parents]:
        if (directory / marker).exists():
            return directory
    raise SystemExit(
        f"no {marker!r} directory above {start}.\n"
        f"This skill finds its configuration by locating the .claude directory "
        f"it lives in, so it must be installed as "
        f"<project>/.claude/skills/strategic-company-analysis/.")


PROJECT_ROOT = _ascend(SKILL_DIR, ".claude")
