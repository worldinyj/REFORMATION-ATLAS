#!/usr/bin/env python3
"""Fail closed when an AI Studio code-sync diff changes protected research paths.

Run only AFTER a web app exists and git has fetched the reviewed base:
  python3 scripts/check_ai_studio_sync_paths.py --base origin/plan/atlas-ai-studio-build-v02

This is an extra guard; it cannot intercept Google AI Studio's direct push.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PREFIX = "apps/web/"
PROTECTED = ("data/", "docs/", "assets/", "scripts/", ".github/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="the reviewed base git reference")
    args = parser.parse_args()
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACDMRTUXB",
             f"{args.base}...HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        print("BLOCK unable to compare branch with base:", exc, file=sys.stderr)
        return 2
    changed = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not changed:
        print("WARN no committed changes compared with", args.base)
        return 0
    blocked = [x for x in changed if not x.startswith(ALLOWED_PREFIX)]
    secrets = [x for x in changed if x.startswith(ALLOWED_PREFIX) and (
        Path(x).name.startswith(".env")
        or Path(x).suffix.lower() in {".pem", ".p12", ".pfx", ".key"}
    )]
    print("BASE", args.base)
    print("ALLOWED APP FILES", len(changed) - len(blocked))
    print("CHANGED RESEARCH/GOVERNANCE/ROOT FILES", len(blocked))
    for path in blocked:
        print(("BLOCK PROTECTED " if path.startswith(PROTECTED) else "BLOCK OUTSIDE APP "), path)
    for path in secrets:
        print("BLOCK POTENTIAL SECRET", path)
    if blocked or secrets:
        print("RESULT BLOCK: review changes manually and keep app changes inside apps/web/")
        return 1
    print("RESULT PASS: changed paths are inside apps/web/. Still review source diffs, secrets and approval before pushing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
