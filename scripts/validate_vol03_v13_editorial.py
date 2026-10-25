#!/usr/bin/env python3
"""Read-only V1.3 editorial and publication gate checks."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1]
def j(p):return json.loads((R/p).read_text(encoding="utf-8"))
errors=[]
def chk(ok,label):
    print(("PASS " if ok else "FAIL ")+label)
    if not ok: errors.append(label)
d=j("data/vol03_v13_review_gates.json")
v=j("data/vol03_visual_candidates_v12.json")
g=j("data/vol03_integrated_catalog_v08.json")
claims=j("data/vol03_primary_claims.json")
index=j("data/vol03_presentation_index.json")
chk(len(d["candidates"])==8 and all(not c["historian_approved"] and not c["public_visible"] for c in d["candidates"]),"eight candidates require human review")
chk({c["id"] for c in d["candidates"]}=={x["candidate_id"] for x in v["inherited_portrait_candidates"]}|{x["id"] for x in v["scene_candidates"]}|{x["id"] for x in v["maps"]},"candidate ID links")
chk(any(x["decision"]=="REVISE_HIGH" and x["id"]=="ILL-V03-02-R2C01" for x in d["candidates"]),"negotiation image risk hold")
chk(len(g["nodes"])==182 and len(g["edges"])==365 and len(claims["claims"])==14,"original graph/claims counts")
chk(all(not x["approved"] and not x["can_ship"] for x in [d["publication_gate"],v["publication_gate"],g["publication_gate"],index["publication_gate"]]),"every publication gate closed")
chk(all(not item["media_safe_to_display"] for item in index["people_pages"]+index["visual_story_pages"]),"no web image exposure")
import hashlib
expected={x["path"]:x["sha256"] for x in d["installation"]["expected_media"]}
staging=R/"assets/illustrations/vol03/candidates"
actual=[p for p in staging.glob("*.webp")] if staging.exists() else []
chk(len(actual) in (0,6),"candidate assets either not installed or complete six-file set")
chk(all(str(p.relative_to(R)) in expected for p in actual),"no unexpected candidate WebP assets")
for path in actual:
    rel=str(path.relative_to(R))
    if rel in expected:
        chk(hashlib.sha256(path.read_bytes()).hexdigest()==expected[rel],"candidate SHA256 "+rel)
for part in ["01_WALDENSIANS.md","02_WYCLIF_LOLLARDS.md","03_HUS_AND_PRAGUE.md","04_HUSSITE_MOVEMENTS.md","09_PRAGUE_ARTICLES_AND_COMPACTATA.md"]:
    chk("## V1.3 편집 보강" in (R/"docs/01_CONTENT/VOL03"/part).read_text(encoding="utf-8"),"edited "+part)
text=(R/"docs/01_CONTENT/VOL03/06_TIMELINE.md").read_text(encoding="utf-8")
chk(all(marker in text for marker in ["1432-05-18","1433-11-30","1435년 7월","1436년 7월","1437-12-23"]),"five negotiation milestones")
chk("## V1.3 추가 검증" in (R/"docs/01_CONTENT/VOL03/07_FACTCHECK_MATRIX.md").read_text(encoding="utf-8"),"visual factcheck supplement")
print(("PASS" if not errors else "FAIL")+" V1.3 editorial QA; issues="+str(len(errors)))
sys.exit(bool(errors))
