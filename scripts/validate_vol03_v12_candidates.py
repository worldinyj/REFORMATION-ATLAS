#!/usr/bin/env python3
"""VOL-03 V1.2 candidate review checks; read-only, Python 3.11+ standard library."""
import argparse,hashlib,json,sys,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--scene-zip",type=Path)
    args=ap.parse_args()
    errors=[]
    def check(ok,label):
        print(("PASS " if ok else "FAIL ")+label)
        if not ok:errors.append(label)
    obj=load("data/vol03_visual_candidates_v12.json")
    graph=load("data/vol03_integrated_catalog_v08.json")
    claims=load("data/vol03_primary_claims.json")
    presentation=load("data/vol03_presentation_index.json")
    staged=load("assets/illustrations/vol03/ILLUSTRATION_STAGE.json")
    manifest=load("assets/asset_manifest.json")
    check(not obj["publication_gate"]["approved"] and not obj["publication_gate"]["can_ship"],"V1.2 release gate disabled")
    check(len(graph["nodes"])==182 and len(graph["edges"])==365,"original research graph 182/365")
    check(len(claims["claims"])==14,"14 canonical claims")
    check((len(obj["inherited_portrait_candidates"]),len(obj["scene_candidates"]),len(obj["maps"]))==(4,2,2),"4 portraits + 2 scenes + 2 maps")
    check(all(not x["public_visible"] and x["review_status"]=="DRAFT" for x in obj["scene_candidates"]),"two scenes unpublished drafts")
    check(not presentation["publication_gate"]["approved"] and not presentation["publication_gate"]["can_ship"],"existing presentation unpublished")
    check(all(not x.get("media_safe_to_display",False) for x in presentation["people_pages"]+presentation["visual_story_pages"]),"all page media display gates closed")
    stage_ids={x["id"] for x in staged["assets"]}
    manifest_ids={x["asset_id"] for x in manifest}
    check(all(x["original_id"] in stage_ids for x in obj["scene_candidates"]),"scene links to canonical staged IDs")
    check(all(x["original_id"] in manifest_ids for x in obj["maps"]),"map links to original manifest")
    check(all(x["id"] not in manifest_ids for x in obj["maps"]),"map candidates not promoted")
    for x in obj["maps"]:
        path=ROOT/x["git_path"]
        check(path.is_file(),x["id"]+" exists")
        if path.is_file():
            try:
                root=ET.parse(path).getroot()
                visible=" ".join(t.text or "" for t in root.iter())
                check("DRAFT" in visible,x["id"]+" DRAFT caption")
                check("아님" in visible or "미복원" in visible,x["id"]+" conceptual-route caption")
            except ET.ParseError:
                check(False,x["id"]+" XML")
    if args.scene_zip:
        archive=args.scene_zip
        check(archive.is_file(),"scene ZIP available")
        if archive.is_file():
            check(hashlib.sha256(archive.read_bytes()).hexdigest()==obj["scene_zip"]["sha256"],"scene ZIP sha256")
            with zipfile.ZipFile(archive) as z:
                check(z.testzip() is None,"scene ZIP CRC")
                for scene in obj["scene_candidates"]:
                    suffix="hus_sermon_nonspecific" if scene["original_id"]=="ILL-V03-01" else "bohemia_council_discussion"
                    for ext in ("png","webp"):
                        name=scene["id"]+"_"+suffix+"."+ext
                        match=[p for p in z.namelist() if p.endswith("/"+name)]
                        check(len(match)==1,name+" single member")
                        if len(match)==1:
                            check(hashlib.sha256(z.read(match[0])).hexdigest()==scene[ext+"_sha256"],name+" checksum")
    print("VOL03 V1.2 QA", "FAIL" if errors else "PASS", "issues="+str(len(errors)))
    return bool(errors)
if __name__=="__main__":sys.exit(main())
