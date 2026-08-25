"""check.py — is this skill internally consistent? Exit 1 if not.

Three checks, none of which a build step exists to make:

1. SKELETON — every file in modules/ and synthesis/ carries the seven
   headings from SKILL.md's "Module skeleton", in order, and its
   "What good looks like" section is non-empty. The skeleton is what makes
   modules separately runnable AND composable; a drifted module silently
   stops handing off.
2. REFERENCES — every `modules/…`, `synthesis/…`, `data/…` path (plus the
   named top-level files) mentioned in any of this skill's documents resolves
   to a real file. A routing table pointing at nothing fails quietly at the
   worst time: mid-analysis.
3. ROUTING — every module and synthesis file is mentioned in SKILL.md, so
   nothing is orphaned: a module the hub never routes to is dead weight that
   still costs maintenance.

No check reads the *quality* of a module — that has no engine and is found
only by using it. This is the skill's analogue of finance-reports' status.py:
structure by tool, substance by eye.
"""

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent

SKELETON = [
    "## Question this answers",
    "## When to run / when to skip",
    "## Inputs",
    "## Method",
    "## What good looks like",
    "## Hands off",
    "## Failure modes",
]

TOP_LEVEL = ["SKILL.md", "company-types.md", "output-forms.md", "check.py"]

REF_PATTERN = re.compile(r"(?:modules|synthesis|data)/[A-Za-z0-9_.-]+\.(?:md|py)")


def check_skeleton(path: Path, problems: list) -> None:
    text = path.read_text(encoding="utf-8")
    positions = []
    for heading in SKELETON:
        # Anchored to line start so prose mentioning a heading does not count.
        match = re.search(rf"^{re.escape(heading)}\s*$", text, re.MULTILINE)
        if not match:
            problems.append(f"{path.relative_to(SKILL_DIR)}: missing heading "
                            f"{heading!r}")
            return
        positions.append(match.start())
    if positions != sorted(positions):
        problems.append(f"{path.relative_to(SKILL_DIR)}: skeleton headings out "
                        f"of order")

    # "What good looks like" must hold an actual worked fragment. 80 chars is
    # not a quality bar — it is the difference between content and a stub.
    start = positions[SKELETON.index("## What good looks like")]
    end = positions[SKELETON.index("## Hands off")]
    body = text[start + len("## What good looks like"):end].strip()
    if len(body) < 80:
        problems.append(f"{path.relative_to(SKILL_DIR)}: 'What good looks "
                        f"like' is empty or a stub ({len(body)} chars)")


def main() -> int:
    problems = []

    modules = sorted((SKILL_DIR / "modules").glob("*.md"))
    synthesis = sorted((SKILL_DIR / "synthesis").glob("*.md"))
    if not modules:
        problems.append("modules/ holds no .md files")
    if not synthesis:
        problems.append("synthesis/ holds no .md files")

    # 1 — skeleton conformance
    for path in modules + synthesis:
        check_skeleton(path, problems)

    # 2 — every referenced path resolves
    documents = ([SKILL_DIR / name for name in TOP_LEVEL if name.endswith(".md")]
                 + modules + synthesis + [SKILL_DIR / "data" / "endpoints.md"])
    for doc in documents:
        if not doc.exists():
            problems.append(f"expected document missing: {doc.relative_to(SKILL_DIR)}")
            continue
        for ref in set(REF_PATTERN.findall(doc.read_text(encoding="utf-8"))):
            if not (SKILL_DIR / ref).exists():
                problems.append(f"{doc.relative_to(SKILL_DIR)}: references "
                                f"{ref}, which does not exist")

    # 3 — nothing orphaned: the hub routes to every module and synthesis file
    hub = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for path in modules + synthesis:
        rel = path.relative_to(SKILL_DIR).as_posix()
        if rel not in hub:
            problems.append(f"SKILL.md never mentions {rel} — orphaned module")
    for name in ("company-types.md", "output-forms.md", "data/fact_pack.py"):
        if name not in hub:
            problems.append(f"SKILL.md never mentions {name}")

    if problems:
        print(f"check: {len(problems)} problem(s)")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print(f"check: OK — {len(modules)} modules, {len(synthesis)} synthesis "
          f"files, all skeleton-conformant, all references resolve, "
          f"nothing orphaned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
