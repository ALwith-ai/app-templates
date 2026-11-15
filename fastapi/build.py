"""Check the service and write what a deployment runs to dist/.

The build fails on a lint, format or type error. dist/ then holds the source the service runs from,
the locked dependencies, the migrations and the API contract, and nothing else.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
# Development-only entries; everything else at the top level is part of the service.
EXCLUDED = {"__pycache__", "build.py", "dist", "README.md", "ruff.toml", "tests"}


def check() -> None:
    for arguments in (["ruff", "check"], ["ruff", "format", "--check"], ["ty", "check"]):
        subprocess.run([sys.executable, "-m", *arguments], cwd=ROOT, check=True)


def write_dist() -> None:
    if not (ROOT / "openapi.json").is_file():
        msg = "openapi.json, the API contract, is missing"
        raise FileNotFoundError(msg)
    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    for entry in sorted(ROOT.iterdir()):
        if entry.name.startswith(".") or entry.name in EXCLUDED:
            continue
        if entry.is_dir():
            shutil.copytree(entry, DIST / entry.name, ignore=ignore)
        else:
            shutil.copy2(entry, DIST / entry.name)


if __name__ == "__main__":
    check()
    write_dist()
