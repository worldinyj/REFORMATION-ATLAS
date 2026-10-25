#!/usr/bin/env python3
"""Zwingli scholarly draft data integrity; PASS never approves web publication."""
from __future__ import annotations
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
read = lambda path: json.loads(path.read_text(encoding="utf-8"))

def main():
    doc = read(ROOT / "data/deep/vol04_zwingli_v01.json")
    baseline = read(ROOT / "data/overview/volumes_and_people_v01.json")
    status = read(ROOT / "data/deep/research_tracks_v01.json")
    manuscript = (ROOT / "docs/01_CONTENT/VOL04/ZWINGLI_DEEP_RESEARCH_V01.md").read_text(encoding="utf-8")
    sources,claims,events,media=doc["sources"],doc["claims"],doc["events"],doc["visual_candidates"]
    src_ids={s["id"] for s in sources}
    claim_ids={c["id"] for c in claims}
    n=fail=0
    def ck(ok, name):
        nonlocal n,fail
        n+=1
        if not ok:fail+=1
        print(("PASS " if ok else "FAIL ")+name)

    ck(doc["person_id"]=="OV-P-015" and any(p["id"]=="OV-P-015" and p["name_en"]=="Huldrych Zwingli" for p in baseline["people"]), "existing canonical person preserved")
    ck(doc["volume_id"]=="VOL-04" and doc["depth_block"]["id"]=="DEPTH-V04-P015-001", "volume and deep content block")
    ck(len(sources)==11 and len(src_ids)==11, "11 unique sources")
    ck(all(urlparse(s["url"]).scheme=="https" and not s["full_text_copied"] for s in sources), "linked source descriptions; no full-text copying")
    ck(all(s["review_status"] and s["evidence_type"] for s in sources), "source evidence categories and review state")
    ck(len(claims)==13 and len(claim_ids)==13, "13 claims unique")
    ck(all(c["source_ids"] and set(c["source_ids"]) <=src_ids for c in claims), "all claims tied to registered source")
    ck(all(c["review_status"]=="DRAFT" and c["publication_approved"] is False for c in claims), "claims stay unapproved")
    ck("SOURCE_DATE_CONFLICT_HOLD" in [c["confidence"] for c in claims] and "1월 29일" in manuscript and "1월 27일" in manuscript, "1523 disputation date uncertainty explicitly preserved")
    ck(len(events)==9 and len({e["id"] for e in events})==9, "9 new dated research anchors, no duplicate IDs")
    ck(all(e["related_claim_id"] in claim_ids and not e["public_visible"] for e in events), "no orphan or public research events")
    ck(len(media)==3 and {m["role"] for m in media}=={"portrait","scene","schematic_map"}, "portrait, scene and map candidates registered")
    ck(all(not m["approved"] and not m["publication_approved"] and not m["binary_in_github"] for m in media), "media binaries not claimed to be in GitHub nor approved")
    ck(len(doc["media_manifest_local_sha256"])==64, "local visual archive identified by hash")
    ck(not doc["release_gate"]["can_ship"] and not doc["release_gate"]["approved"], "web release gate denied")
    ck(all(s["id"] in manuscript for s in sources), "all source IDs included in manuscript bibliography")
    ck(all(phrase in manuscript for phrase in ["소시지","만츠","마르부르크","카펠","츠빙글리"]), "core history topics included")
    record=next((x for x in status["tracks"] if x["id"]=="TRACK-V04-ZWINGLI"),None)
    ck(record is not None and record["public_visible"] is False and record["sources"]==11, "research track registry updated")
    print(f"RESULT {n-fail}/{n}; deep scholarship remains draft, not historical peer review")
    return int(bool(fail))

if __name__=="__main__":
    raise SystemExit(main())
