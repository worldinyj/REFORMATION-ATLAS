#!/usr/bin/env python3
"""Read-only structured check for VOL-04 Luther deep research, no web publishing.

Usage: python3 scripts/validate_vol04_luther_deep_v01.py
Standard Python 3 library. A PASS is structural QA, not primary-source collation.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/deep/vol04_luther_v01.json"
ARTICLE = ROOT / "docs/01_CONTENT/VOL04/LUTHER_DEEP_RESEARCH_V01.md"
OVERVIEW = ROOT / "data/overview"
DATE_ENUM = {"year","day","period","range","approximate_year","approximate_period"}

def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    n,fail=0,0
    def ck(ok: bool, message: str):
        nonlocal n,fail
        n+=1
        if not ok:fail+=1
        print(("PASS " if ok else "FAIL ")+message)
    data=read(DATA)
    txt=ARTICLE.read_text(encoding="utf-8")
    ppl=read(OVERVIEW/"volumes_and_people_v01.json")
    events=read(OVERVIEW/"events_documents_v01.json")
    related=read(OVERVIEW/"relationships_and_themes_v01.json")
    sources=data["sources"]; claims=data["claims"]; timeline=data["timeline"]
    known={x["id"] for x in ppl["people"]+ppl["volumes"]+events["events"]+events["documents"]+related["ideas"]}
    srcIDs={s["id"] for s in sources}; claimIDs={c["id"] for c in claims}

    ck(data["parent_person_id"]=="OV-P-013" and "OV-P-013" in known,
       "existing Luther person ID preserved; no duplicate person")
    ck(data["parent_volume_id"]=="VOL-04","VOL-04 volume retained")
    ck(data["content_block"]["entity_id"]==data["parent_person_id"] and
       data["content_block"]["depth"]=="DEEP_RESEARCH","deep block attached to original entity")
    ck(len(sources)==17 and len(srcIDs)==17,"17 source IDs unique")
    ck(len(claims)==16 and len(claimIDs)==16,"16 historical claims unique")
    ck(len(timeline)==11 and len({x["id"] for x in timeline})==11,
       "11 additional dated anchors unique")
    ck(all(urlparse(s["url"]).scheme=="https" for s in sources),"all sources HTTPS")
    ck(all(s["rights"]=="LINK_AND_OWN_SUMMARY_ONLY" and not s["full_text_copied"]
           for s in sources),"no primary/full-text content copied")
    ck(all("access_status" in s and s["access_status"] for s in sources),
       "source verification limitations recorded")
    ck(all(c["source_ids"] and set(c["source_ids"])<=srcIDs for c in claims),
       "all claims have grounded sources")
    ck(all(c["related_ids"] and set(c["related_ids"])<=known for c in claims),
       "claim cross-entity references resolve")
    ck(all(c["review_status"]=="DRAFT_EDITORIAL" and
           not c["approved"] and not c["publication_approved"] for c in claims),
       "each claim explicitly draft and unapproved")
    ck(all(t["date_precision"] in DATE_ENUM and
           t["claim_id"] in claimIDs and t["public_visible"] is False for t in timeline),
       "timelines retain year precision and point to valid claims")
    ck(all(s["id"] in txt for s in sources),
       "manuscript source appendix accounts for all registered sources")
    ck(txt.startswith("# VOL-04") and txt.count("## ")>=10,
       "full chapter draft and editorial section structure present")
    ck("반유대주의" in txt and "농민전쟁" in txt and "마르부르크" in txt,
       "difficult Luther historical topics included")
    ck(data["public_release"]["approved"] is False and
       data["public_release"]["can_ship"] is False and
       data["content_block"]["publication_approved"] is False,
       "research dataset not publishable")
    ck(not data["media_policy"]["images"] and not data["media_policy"]["map_pins"],
       "no unauthorized images or historical map pins")
    ck(data["ui_handoff"]["no_web_push"] is True,
       "web app and research kept separate")
    ck("자동" in txt or "공개" in txt,"publishing limitations stated in manuscript")
    print(f"RESULT {n-fail}/{n} | sources={len(sources)} claims={len(claims)} timeline={len(timeline)} errors={fail}")
    return 1 if fail else 0

if __name__=="__main__":
    raise SystemExit(main())
