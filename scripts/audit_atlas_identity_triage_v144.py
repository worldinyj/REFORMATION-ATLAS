#!/usr/bin/env python3
"""Atlas V1.44: triage the actual data errors separately from audit-history mentions."""
import json
from pathlib import Path

def audit(root):
    files=sorted((root/"data").rglob("*.json"))
    records={}; errors=[]
    for f in files:
        try: records[f.relative_to(root).as_posix()]=json.loads(f.read_text(encoding="utf8"))
        except (ValueError,UnicodeError) as ex: errors.append({"file":str(f),"rule":"INVALID_JSON","detail":str(ex)})
    ov=records.get("data/overview/events_documents_v01.json",{})
    persons=records.get("data/overview/volumes_and_people_v01.json",{})
    canonical={"person":{x["id"] for x in persons.get("people",[]) if "id" in x},
               "document":{x["id"] for x in ov.get("documents",[]) if "id" in x},
               "event":{x["id"] for x in ov.get("events",[]) if "id" in x}}
    # Preserve research/audit records; a finding that quotes an error is not itself a new error.
    active={"data/contracts/atlas_person_document_witness_crosswalk_v119.json",
            "data/deep/vol03_wycliffe_hus_primary_witness_audit_v120.json"}
    seen=set()
    def visit(x,path,loc="$"):
        if isinstance(x,list):
            for i,y in enumerate(x):visit(y,path,f"{loc}[{i}]")
        elif isinstance(x,dict):
            if path in active and x.get("person_id")=="OV-P-009" and x.get("document_id")=="OV-D-005":
                issue=(path,loc,"WYC_HUS_TITLE_COLLISION")
                if issue not in seen:
                    seen.add(issue);errors.append({"file":path,"location":loc,"rule":issue[2],"status":"REQUIRES_EDITORIAL_REPAIR"})
            if path in active and x.get("person_id")=="OV-P-010" and x.get("document_id")=="OV-D-006" and x.get("relation") in ("authored","author"):
                errors.append({"file":path,"location":loc,"rule":"HUS_POSTHUMOUS_AUTHORSHIP"})
            for k,y in x.items():
                if path in active and k in ("person_id","document_id","event_id") and isinstance(y,str) and y.startswith("OV-"):
                    group=k[:-3]
                    if canonical[group] and y not in canonical[group]:
                        errors.append({"file":path,"location":loc+"."+k,"rule":"UNKNOWN_CANONICAL_ID","id":y})
                visit(y,path,loc+"."+k)
    for path,obj in records.items():visit(obj,path)
    return {"version":"1.44","files_found":len(files),"parsed":len(records),"errors":errors,
            "counts":{k:len(v) for k,v in canonical.items()},"limitation":"Provenance-aware targeted ID rules, not entire semantic verification"}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=Path("."));p.add_argument("--output",type=Path)
    a=p.parse_args();res=audit(a.root.resolve())
    output=json.dumps(res,ensure_ascii=False,indent=2)
    print(output)
    if a.output:a.output.write_text(output+"\n",encoding="utf8")
    raise SystemExit(bool(res["errors"]))
