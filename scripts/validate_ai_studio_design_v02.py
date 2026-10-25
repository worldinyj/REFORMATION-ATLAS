#!/usr/bin/env python3
"""Validate the Google AI Studio V0.2 design package only; read-only."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "docs/03_PRODUCT/AI_STUDIO_BUILD_V02"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def fail(message, faults):
    print("FAIL", message)
    faults.append(message)

def main():
    faults = []
    required = [
        "01_PROJECT_PLAN.md", "02_PRD.md", "03_TRD.md", "04_UXUI.md",
        "05_TASKLIST.md", "00_GITHUB_DESIGN_PREFLIGHT.md",
        "06_MASTER_BUILD_PROMPT.md", "06_AI_STUDIO_MASTER_PROMPT.md",
        "07_AI_STUDIO_ITERATION_PROMPTS.md", "08_BUILD_CHECKLIST.md",
        "DESIGN_TOKENS.json", "SCREEN_CONTRACT.json", "README.md",
    ]
    for name in required:
        file = BUNDLE / name
        if not file.is_file() or file.stat().st_size < 200:
            fail("missing/empty "+name, faults)
        else:
            print("PASS doc", name)
    if faults:
        return 1
    data = load(ROOT / "data/overview/ai_studio_tasklist_v02.json")
    canonical = load(BUNDLE / "TASKLIST.json")
    base_prd = load(ROOT / "data/overview/prd_acceptance_v01.json")
    screens = load(BUNDLE / "SCREEN_CONTRACT.json")
    tokens = load(BUNDLE / "DESIGN_TOKENS.json")
    tasks = data["tasks"]
    task_ids = [task["id"] for task in tasks]
    fr_ids = {req["id"] for req in base_prd["requirements"]}
    present_fr = {rid for task in tasks for rid in task["fr_ids"]}
    if len(tasks) != 36 or len(set(task_ids)) != 36:
        fail("36 unique task IDs", faults)
    if len(fr_ids) != 18 or not fr_ids.issubset(present_fr):
        fail("PRD FR-001 through FR-018 fully traced", faults)
    if len(canonical["tasks"]) != 36 or canonical["stats"]["p0"] != 33 or canonical["stats"]["p1"] != 3:
        fail("canonical 36-task package mismatch", faults)
    if data["statistics"]["tasks"] != len(tasks):
        fail("mirror count mismatched", faults)
    if data["statistics"]["p0"] != sum(t["priority"] == "P0" for t in tasks):
        fail("mirror P0 count mismatched", faults)
    if data["statistics"]["p1"] != sum(t["priority"] == "P1" for t in tasks):
        fail("mirror P1 count mismatched", faults)
    canonical_index = {t["id"]:t for t in canonical["tasks"]}
    for task in tasks:
        mirror = canonical_index.get(task["id"])
        if not mirror or task["fr_ids"] != mirror["prd_ids"] or task["depends_on"] != mirror["depends_on"] or task["priority"] != mirror["priority"] or task["status"] != mirror["status"]:
            fail("canonical-vs-mirror task divergence " + task["id"], faults)
    if data.get("canonical_source") != "docs/03_PRODUCT/AI_STUDIO_BUILD_V02/TASKLIST.json":
        fail("mirror has no canonical source", faults)
    if any(task["status"] != "NOT_STARTED" for task in tasks):
        fail("all implementation tasks initially unstarted", faults)
    if any(task["priority"] not in ("P0","P1") for task in tasks):
        fail("invalid priority", faults)
    index = {task["id"]:task for task in tasks}
    for task in tasks:
        if any(dep not in index for dep in task["depends_on"]):
            fail("missing task dependency "+task["id"], faults)
        if any(fr not in fr_ids for fr in task["fr_ids"]):
            fail("unknown requirement "+task["id"], faults)

    marked = set()
    active = set()
    def walk(node):
        if node in active:
            fail("task dependency cycle "+node, faults)
            return
        if node in marked:
            return
        active.add(node)
        for dep in index[node]["depends_on"]:
            if dep in index:
                walk(dep)
        active.remove(node)
        marked.add(node)
    for node in task_ids:
        walk(node)

    if len(screens["screens"]) != 14:
        fail("14 design routes", faults)
    normalize = lambda path: re.sub(r":[a-zA-Z_][a-zA-Z_0-9]*", ":param", path)
    if {normalize(s["path"]) for s in screens["screens"]} != {normalize(p["path"]) for p in base_prd["information_pages"]}:
        fail("screen paths do not match PRD after parameter normalization", faults)
    if tokens["palette"]["accent"] != "#205F50" or tokens["palette"]["canvas"] != "#F7F8F5":
        fail("Quiet Editorial color tokens missing", faults)

    def luminance(c):
        vals = [int(c[i:i+2],16)/255 for i in (1,3,5)]
        vals = [v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in vals]
        return .2126*vals[0]+.7152*vals[1]+.0722*vals[2]
    bg = luminance(tokens["palette"]["canvas"])
    for k in ("ink","muted","accent"):
        fg = luminance(tokens["palette"][k])
        contrast = (max(fg,bg)+.05)/(min(fg,bg)+.05)
        if contrast < 4.5:
            fail("insufficient normal text contrast "+k, faults)
        else:
            print("PASS contrast", k, "%.2f:1"%contrast)

    master = (BUNDLE/"06_AI_STUDIO_MASTER_PROMPT.md").read_text(encoding="utf-8")
    for text in ("PROMPT START","PROMPT END","VOL-01","VOL-08","React","TypeScript","Do NOT try to implement all features"):
        if text not in master:
            fail("master prompt missing "+text, faults)
    status = load(ROOT / "data/overview/ai_studio_design_readiness_v02.json")
    if status["publication_gate"]["can_ship"] or status["website_built"] or status["approved_by_user"]:
        fail("design package incorrectly marked published/approved", faults)
    expected_widths = [320, 360, 375, 390, 430, 768, 1024, 1440]
    if screens["responsive"] != expected_widths or tokens["layout"]["breakpoints_preview_px"] != expected_widths:
        fail("responsive breakpoints must agree for mobile/tablet/desktop", faults)
    if not screens.get("mobile_first") or not screens.get("parity_required") or not tokens["layout"].get("mobile_primary"):
        fail("mobile-first and feature parity contract missing", faults)
    if screens["content_update_contract"]["initial"] != "OVERVIEW" or screens["content_update_contract"]["follow_up"] != "DEEP_RESEARCH":
        fail("overview-to-depth update contract missing", faults)
    if not status["prebuild_gate"]["required"] or status["prebuild_gate"]["status"] != "NOT_RUN_IN_AI_STUDIO":
        fail("prebuild audit incorrectly marked completed or missing", faults)
    if status["content_expansion"]["initial"] != "OVERVIEW" or not status["content_expansion"]["preserve_existing_urls_and_ids"]:
        fail("content depth stability missing", faults)
    must_contain = {
        "00_GITHUB_DESIGN_PREFLIGHT.md": ("PREBUILD_GATE", "NO BUILD", "36", "320/360/375/390/430", "DEEP_RESEARCH"),
        "01_PROJECT_PLAN.md": ("PREBUILD_GATE", "DEEP_RESEARCH", "320/360/375/390/430"),
        "02_PRD.md": ("PREBUILD_GATE", "DEEP_RESEARCH", "320/360/375/390/430"),
        "03_TRD.md": ("PREBUILD_GATE", "DEEP_RESEARCH", "320/360/375/390/430"),
        "04_UXUI.md": ("모바일", "DEEP_RESEARCH", "320/360/375/390/430"),
        "05_TASKLIST.md": ("AT-001", "PREBUILD_GATE", "DEEP_RESEARCH", "320/360/375/390/430"),
        "06_MASTER_BUILD_PROMPT.md": ("PREBUILD_GATE", "NO BUILD", "DEEP_RESEARCH", "320/360/375/390/430"),
        "06_AI_STUDIO_MASTER_PROMPT.md": ("PREBUILD_GATE", "NO BUILD", "DEEP_RESEARCH", "320/360/375/390/430"),
        "07_ITERATION_PROMPTS.md": ("PREBUILD_GATE", "DEEP_RESEARCH", "320/360/375/390/430"),
        "07_AI_STUDIO_ITERATION_PROMPTS.md": ("PREBUILD_GATE", "DEEP_RESEARCH", "320/360/375/390/430"),
        "08_BUILD_CHECKLIST.md": ("PREBUILD_GATE", "320/360/375/390/430"),
        "08_GITHUB_HANDOFF.md": ("PREBUILD_GATE", "320/360/375/390/430"),
    }
    for name, markers in must_contain.items():
        body = (BUNDLE / name).read_text(encoding="utf-8")
        if not all(mark in body for mark in markers):
            fail("inconsistent mandatory lifecycle/audit/mobile contract in " + name, faults)
    by_id = {t["id"]: t for t in canonical["tasks"]}
    if "PREBUILD_GATE" not in by_id["AT-001"]["acceptance"] or "PREBUILD_GATE" not in by_id["AT-004"]["verification"]:
        fail("AT-001 / AT-004 not gated by GitHub prebuild audit", faults)
    if not all(str(w) in by_id["AT-026"]["acceptance"] for w in expected_widths):
        fail("AT-026 mobile and desktop acceptance widths missing", faults)
    if "DEEP_RESEARCH" not in by_id["AT-035"]["acceptance"]:
        fail("AT-035 must preserve incremental historical depth", faults)
    if status["tasks"] != 36 or status["task_priority"] != {"P0":33,"P1":3}:
        fail("readiness file has outdated task count", faults)
    if (ROOT / "apps/web").exists():
        fail("app code detected despite design-only scope", faults)
    print("PASS" if not faults else "FAIL","AI Studio V0.2 package",len(tasks),"tasks",len(screens["screens"]),"screens",len(faults),"issues")
    return bool(faults)

if __name__ == "__main__":
    sys.exit(main())
