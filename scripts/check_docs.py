"""Check required planning documents and local Markdown links; no dependencies."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("README.md", "PROJECT_SPEC.md", "ARCHITECTURE.md", "ROADMAP.md",
            "EVALUATION.md", "AGENTS.md", "docs/API.md", "docs/SCHEMA.md",
            "docs/DEPLOYMENT.md", "docs/SECURITY.md", "docs/LEARNING.md")
errors = []
for name in REQUIRED:
    path = ROOT / name
    if not path.is_file() or not path.read_text().strip():
        errors.append(f"Missing or empty required document: {name}")
paths = list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md"))
for path in paths:
    text = path.read_text()
    if sum(line.startswith("```") for line in text.splitlines()) % 2:
        errors.append(f"Unclosed code fence: {path.relative_to(ROOT)}")
    for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if target and not (path.parent / target).exists():
            errors.append(f"Broken file link in {path.relative_to(ROOT)}: {target}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Documentation checks passed: {len(paths)} Markdown files; required files and local links exist.")
