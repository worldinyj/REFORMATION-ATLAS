#!/usr/bin/env python3
"""VOL05 V1.7: avoid fabricated woman-guild admission, manuscript identity or IPO V35 lawsuit."""
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_kramergilde_three_people_v17.json"
PARENT="data/deep/vol05_kramergilde_1931_edition_access_audit_v16.json"
ARTICLE="docs/01_CONTENT/VOL05/MUENSTER_KRAMERGILDE_THREE_PEOPLE_1670_1720_V17.md"
GATE_KEYS={"historian_approved","Ketteler_1931_p270_read","original_1719_register_read",
"Geisberg_1934_p256_direct_read","Geisberg_book_equated_to_Ketteler_original",
"individual_IPO_V35_case_verified","art_rights_approved","can_publish"}
P_MAP={
"P1670":(1670,"Maria Schürman","S1","CANDIDATE_WIDOW_ROLE_UNCERTAIN"),
"P1719":(1719,"Anton Reinhard Neuhaus","S2","REPORTED_ADMITTED_SECONDARY_ACADEMIC"),
"P1720":(1720,"Gerhard Henrich Bußman","S1","CANDIDATE_LOCAL_HISTORICAL_EXTRACTION")}
BOOK_MAP={"L1":("S5","Gildebuch der Kramergilde im Stadtarchive"),
"L2":("S3","Ketteler 1931 Die Aufnahmen in die Kramergilde 1662–1797"),
"L3":("S7","Das Rote Buch der Gesamtgilde")}
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def fail(message):raise ValueError(message)
def validate(d=None):
    d=load(REG) if d is None else d
    if (d["kind"],d["status"],d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=(
        "VOL05_MUENSTER_KRAMERGILDE_THREE_PERSON_CANDIDATES",
        "DRAFT_RESEARCH_NOT_PUBLIC","VOL-05","OV-E-024","OV-D-015"):
        fail("research-only record and canonical source identity changed")
    if d["parent"]!=PARENT or d["new_canonical_ids"]!=0 or d["main_modified"] is not False or d["overview_modified"] is not False or d["ai_studio_modified"] is not False:
        fail("main/overview/app or parent research changed")
    if set(d["publication_gate"])!=GATE_KEYS or any(d["publication_gate"].values()):
        fail("original evidence or approval status falsely released")
    par=load(PARENT)
    if par["canonical_event_id"]!=d["canonical_event_id"] or par["canonical_document_id"]!=d["canonical_document_id"]:
        fail("V1.6 lineage incompatible")
    sources=d["sources"]
    if len(sources)!=9 or len({s["id"] for s in sources})!=9:
        fail("nine unique evidence records required")
    ss={s["id"]:s for s in sources}
    for s in sources:
        p=urlparse(s["url"])
        if p.scheme!="https" or not p.hostname or not s["type"] or not s["claim"]:
            fail("invalid evidence URL or scope")
        if s["direct_1931_page_read"] is not False or s["direct_1719_original_read"] is not False or s["media_rights_approved"] is not False:
            fail("unread exact printed page/original or art reuse falsely approved")
    if "heimatvereinsendenhorst.de" not in ss["S1"]["url"] or "saw-leipzig.de" not in ss["S2"]["url"]:
        fail("secondary local candidates and academic Neuhaus evidence substituted")
    if "8315820.pdf" not in ss["S5"]["url"] or "exponate.html" not in ss["S7"]["url"]:
        fail("Geisberg original printed excerpt or museum artifact index replaced")
    people=d["person_candidates"]
    if len(people)!=3 or {p["id"] for p in people}!=set(P_MAP):
        fail("precisely three people at their separate source grades required")
    for person in people:
        y,n,s,grade=P_MAP[person["id"]]
        if (person["year"],person["name"],person["source_id"],person["evidence_grade"])!=(y,n,s,grade):
            fail("secondary person, year or provenance changed")
        if person["confession"]!="UNKNOWN" or person["individual_IPO_V35_court_verdict"] is not False:
            fail("unknown religion or unproved religious lawsuit fabricated")
        if person["actual_original_member_row_read"] is not False or person["printed_1931_member_row_read"] is not False or person["original_archive_shelfmark"] is not None:
            fail("unread 17th/18th century original or Ketteler 1931 row fabricated")
    if "Wwe" not in next(p for p in people if p["id"]=="P1670")["context"]:
        fail("Maria widow status or uncertain membership meaning erased")
    if "Amtsohn" not in next(p for p in people if p["id"]=="P1719")["context"]:
        fail("Neuhaus 1719 admissions category lost")
    books=d["archival_book_leads"]
    if len(books)!=3 or {b["key"] for b in books}!=set(BOOK_MAP):
        fail("guild book, edited register and older corporate book must remain separate")
    for b in books:
        src,title=BOOK_MAP[b["key"]]
        if b["source_id"]!=src or b["title"]!=title:
            fail("old corporate guild book substituted for later member register")
        if b["modern_shelfmark"] is not None or b["proven_same_as_Ketteler_original"] is not False or b["book_directly_read"] is not False:
            fail("hypothetical original accession or same-manuscript identity invented")
    artworks=d["museum_objects"]
    if len(artworks)!=3 or {x["key"] for x in artworks}!={"M1","M2","M3"}:
        fail("historic artifacts list changed")
    if any(x["source_id"]!="S7" or x["downloaded"] is not False or x["publishing_rights"] is not False for x in artworks):
        fail("museum image rights and publication not verified")
    checks=d["remaining_checks"]
    if len(checks)!=5 or {x["key"] for x in checks}!={"R1","R2","R3","R4","R5"}:
        fail("five precise research items needed")
    if any(x["completed"] is not False for x in checks):
        fail("unread source steps falsely completed")
    if len(d["editorial_limits"])<10:
        fail("source uncertainty and widow inference warnings removed")
    story=(ROOT/ARTICLE).read_text(encoding="utf-8")
    if len(story)<6800 or story.count("\n## ")<8 or "DRAFT_RESEARCH_NOT_PUBLIC" not in story:
        fail("substantive Korean reader chapter absent")
    for x in ("Maria Schürman","Gerhard Henrich Bußman","Anton Reinhard Neuhaus","1670","1719","1720","Geisberg","Gesamtgilde","§35","미확인"):
        if x not in story:fail("critical source fact or uncertainty omitted: "+x)
    return {"sources":9,"person_candidates":3,"manuscript_leads":3,"museum_metadata":3,"direct_1931_rows_read":0,"individual_V35_verdicts":0,"published":0}
if __name__=="__main__":
    x=validate()
    print("PASS VOL05 V1.7: 9 sources, 3 individual candidates, 3 distinct books; Ketteler direct rows 0, §35 rulings 0, PUBLIC 0")
