#!/usr/bin/env python3
"""Repository-wide structural JSON and canonical identity audit."""
import json
from pathlib import Path
from collections import Counter

def audit(root):
    files=sorted((root/"data").rglob("*.json"))
    db, issues={},[]
    for p in files:
        path=p.relative_to(root).as_posix()
        try: db[path]=json.loads(p.read_text(encoding="utf8"))
        except (ValueError,UnicodeError) as e: issues.append(dict(path=path,rule="INVALID_JSON",detail=str(e)))
    ov=db.get("data/overview/events_documents_v01.json",{})
    people=db.get("data/overview/volumes_and_people_v01.json",{})
    keys={"person":{x["id"] for x in people.get("people",[]) if "id" in x},"document":{x["id"] for x in ov.get("documents",[]) if "id" in x},"event":{x["id"] for x in ov.get("events",[]) if "id" in x}}
    def walk(v,path,loc="$"):
        if isinstance(v,list):
            for n,x in enumerate(v):walk(x,path,f"{loc}[{n}]")
        elif isinstance(v,dict):
            if v.get("person_id")=="OV-P-009" and v.get("document_id")=="OV-D-005":
                issues.append(dict(path=path,at=loc,rule="WYCLIFFE_HUS_DE_ECCLESIA_MIXUP"))
            if v.get("person_id")=="OV-P-010" and v.get("document_id")=="OV-D-006" and v.get("relation") in ("authored","author","authored_work"):
                issues.append(dict(path=path,at=loc,rule="HUS_FOUR_ARTICLES_MISATTRIBUTION"))
            for k,x in v.items():
                if k in ("person_id","document_id","event_id") and isinstance(x,str) and x.startswith("OV-"):
                    kind=k[:-3]
                    if keys[kind] and x not in keys[kind]:
                        issues.append(dict(path=path,at=f"{loc}.{k}",rule="UNKNOWN_CANONICAL_REF",id=x))
                walk(x,path,f"{loc}.{k}")
    for p,v in db.items():walk(v,p)
    return dict(version="1.43",files_found=len(files),files_parsed=len(db),canonical_counts={k:len(v) for k,v in keys.items()},issues=issues,issue_counts=dict(Counter(x["rule"] for x in issues)),limitations="Structural audit only; no historical semantic or manuscript verification")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("."))
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=audit(a.root.resolve())
    out=json.dumps(result,indent=2,ensure_ascii=False)
    if a.output:a.output.write_text(out+"\n",encoding="utf8")
    print(out)
    raise SystemExit(1 if result["issues"] else 0)
