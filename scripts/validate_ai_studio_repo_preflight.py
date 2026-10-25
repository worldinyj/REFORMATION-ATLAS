#!/usr/bin/env python3
"""Read-only REFORMATION ATLAS GitHub/AI Studio preflight.

This proves the research repository's documented safety prerequisites, not
Google OAuth connection, branch protection or a running AI Studio application.
Standard Python 3 library only.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/03_PRODUCT/AI_STUDIO_BUILD_V02"
DATA = ROOT / "data/overview"


def get(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    checks = 0

    def check(ok: bool, detail: str) -> None:
        nonlocal checks
        checks += 1
        print(("PASS " if ok else "FAIL ") + detail)
        if not ok:
            errors.append(detail)

    required = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / ".gitignore",
        ROOT / ".github/CODEOWNERS",
        ROOT / ".github/pull_request_template.md",
        ROOT / ".github/workflows/ai-studio-repo-preflight.yml",
        DESIGN / "09_GITHUB_CONNECTION_SETUP.md",
        DESIGN / "06_MASTER_BUILD_PROMPT.md",
        DESIGN / "01_PROJECT_PLAN.md",
        DESIGN / "02_PRD.md",
        DESIGN / "03_TRD.md",
        DESIGN / "04_UXUI.md",
        DESIGN / "05_TASKLIST.md",
        DESIGN / "DESIGN_TOKENS.json",
        DESIGN / "SCREEN_CONTRACT.json",
        DESIGN / "TASKLIST.json",
        DATA / "legacy_person_crosswalk_v01.json",
    ]
    check(all(x.is_file() for x in required), "all readiness, design and review assets exist")

    v = get(DATA / "volumes_and_people_v01.json")
    e = get(DATA / "events_documents_v01.json")
    p = get(DATA / "places_v01.json")
    r = get(DATA / "relationships_and_themes_v01.json")
    s = get(DATA / "source_register_v01.json")
    crosswalk = get(DATA / "legacy_person_crosswalk_v01.json")
    screen = get(DESIGN / "SCREEN_CONTRACT.json")
    tasks = get(DESIGN / "TASKLIST.json")

    check(
        (len(v["volumes"]), len(v["people"]), len(e["events"]),
         len(e["documents"]), len(p["places"]), len(r["ideas"]),
         len(r["relationships"]), len(s["sources"]))
        == (8, 33, 34, 20, 22, 10, 32, 23),
        "source inventory 8/33/34/20/22/10/32/23 unchanged",
    )
    check(len(crosswalk["pairs"]) == 3, "canonical identity crosswalk maps 3 earlier persons")
    check(
        all(item["historical_site_confirmed"] is False for item in p["places"]),
        "all 22 places explicitly unverified for historical map pins",
    )
    check(
        len(tasks["tasks"]) == 36
        and all(task["status"] == "NOT_STARTED" for task in tasks["tasks"])
        and tasks["release_gate"]["can_ship"] is False,
        "36 implementation tasks unstarted and publication blocked",
    )
    check(
        len(screen["screens"]) == 14 and screen["release_approved"] is False,
        "14 planned screens, no web publication approval",
    )
    check(
        all(d["publication_gate"]["can_ship"] is False for d in (v, e, p, r)),
        "all overview release gates remain closed",
    )

    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    check(all(pattern in ignore for pattern in (".env", "node_modules/", "dist/")),
          "ignore file covers secrets and Node build output")
    check("@worldinyj" in (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8"),
          "GitHub code review ownership documented")
    check("main" in (DESIGN / "09_GITHUB_CONNECTION_SETUP.md").read_text(encoding="utf-8"),
          "manual branch protection instructions exist")

    try:
        ls = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
        ).stdout.decode("utf-8").split("\0")
        tracked = [p for p in ls if p]
    except (OSError, subprocess.CalledProcessError):
        tracked = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file()]
        print("WARN git unavailable; checking local files instead of tracked git paths")

    def forbidden_path(path: str) -> bool:
        file = Path(path).name
        return (
            file in {".env", ".env.local", ".env.production", ".env.development",
                     "id_rsa", "id_ed25519"}
            or (file.startswith(".env.") and file != ".env.example")
            or file.endswith((".pem", ".p12", ".pfx", ".key"))
        )

    forbidden = [item for item in tracked if forbidden_path(item)]
    check(not forbidden, "no common secret/private-key paths tracked by git")
    if forbidden:
        for item in forbidden:
            print("FAIL forbidden tracked path:", item)

    bad_public = [f for f in tracked if f.startswith("apps/web/public/")
                  and any(x in f.lower() for x in ("candidate", "pending", ".env"))]
    check(not bad_public, "no unapproved candidate names in app public media directory")

    app = ROOT / "apps/web/package.json"
    root_app = ROOT / "package.json"
    print("INFO research_repository=PUBLIC (externally verified; not checked by this script)")
    print("INFO main_branch_protected=NOT_VERIFIED_BY_SCRIPT")
    print("INFO ai_studio_oauth_connected=NOT_VERIFIED_BY_SCRIPT")
    print("INFO app_repository_created=NOT_VERIFIED_BY_SCRIPT")
    print("INFO existing_app_import_ready=" + ("POSSIBLE_VERIFY_RUNTIME" if (app.exists() or root_app.exists()) else "NO_NO_PACKAGE_JSON"))
    print("INFO next_step=CREATE_AI_STUDIO_APP_THEN_LINK_SEPARATE_REPOSITORY")
    print("INFO local_safety_checks=" + ("PASS" if not errors else "FAIL"))
    print("RESULT %d/%d passed" % (checks - len(errors), checks))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
