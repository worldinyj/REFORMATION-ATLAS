#!/usr/bin/env python3
"""Austrian IPO/IPM direct catalog evidence, edition and publication gate.

Confirms copy-level catalog metadata only, not image content, Latin original
text, transcription accuracy, historical image rights or APW line collation.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
REG="data/deep/vol05_ipo_direct_austrian_catalog_v04.json"
PARENT="data/deep/vol05_ipo_archive_id_apw_page_leads_v03.json"
REPORT="docs/01_CONTENT/VOL05/IPO_AUSTRIAN_DIRECT_CATALOG_AUDIT_V04.md"
EXPECTED={
2594303:("WAR-TREATY-IPO-1648","Kaiserliches Exemplar","1648-10-14",41,117,"Queen Christina of Sweden"),
2594304:("WAR-TREATY-IPO-1648","Mainzer Exemplar","1648-10-24",35,79,"Queen Christina of Sweden"),
2594302:("WAR-TREATY-IPM-1648","Mainzer Exemplar","1648-10-24",34,51,"King Louis XIV of France"),
}
EXPECTED_CROSS={"IPO-PARES-393786","IPM-PARES-1252067","IPO-LWL-QUE2599","IPO-LWL-QUE2595"}
EXPECTED_CITATIONS={"IPO-LAT-V-34":121,"IPO-LAT-VII-1":129}

def read(relative):
    return json.loads((ROOT/relative).read_text(encoding="utf-8"))

def reject(reason):
    raise ValueError(reason)

def validate(d=None):
    d=read(REG) if d is None else d
    if d["kind"]!="VOL05_IPO_IPM_AUSTRIAN_DIRECT_CATALOG_EVIDENCE" or d["status"]!="DRAFT_RESEARCH_NOT_PUBLIC":
        reject("wrong unpublished research kind")
    if (d["volume_id"],d["canonical_event_id"],d["canonical_document_id"])!=("VOL-05","OV-E-024","OV-D-015"):
        reject("canonical mapping drift")
    if d["parent_research"]!=PARENT or d["app_modified"] is not False or d["overview_modified"] is not False or d["canonical_ids_minted"]!=0:
        reject("public/app/ID mutation")
    gates=d["publication_gate"]
    expected_gates={"scholarly_approved","editorial_approved","physical_folios_collated",
                    "apw_original_page_collated","archive_photo_reuse_approved","publish_approved","can_ship"}
    if set(gates)!=expected_gates or any(gates.values()):
        reject("publication, folio collation or photo rights falsely granted")
    parent=read(PARENT)
    if parent["canonical_event_id"]!=d["canonical_event_id"] or parent["canonical_work_id"]!=d["canonical_document_id"]:
        reject("existing source crosswalk mismatch")
    entries=d["direct_archival_catalogs"]
    if len(entries)!=3 or {x["archive_item_id"] for x in entries}!=set(EXPECTED):
        reject("need exactly three directly read original catalog records")
    shared="AT-OeStA/HHStA UR AUR 1648 X 14/24"
    for e in entries:
        id=e["archive_item_id"]
        ref=EXPECTED[id]
        fields=(e["treaty_key"],e["copy_designation"],e["original_catalog_date"],e["seal_count"],e["listed_image_count"],e["counterparty"])
        if fields!=ref:
            reject("archival item treaty/date/sigils/count mismatch "+str(id))
        if e["uri"]!="https://www.archivinformationssystem.at/detail.aspx?ID="+str(id):
            reject("archival URL does not match catalog identifier")
        if e["archive"]!="Österreichisches Staatsarchiv / HHStA" or e["series_or_shared_signature"]!=shared or e["material"]!="Papier":
            reject("archive institution or material not supported")
        if e["historical_calendar_interpretation"] not in {"OLD_STYLE_LABEL_IN_ARCHIVE_LISTING","NEW_STYLE_LABEL_IN_ARCHIVE_LISTING"}:
            reject("unrecorded dating inference")
        if (id==2594303)!=(e["historical_calendar_interpretation"]=="OLD_STYLE_LABEL_IN_ARCHIVE_LISTING"):
            reject("old/new style calendar label lost")
        if e["record_page_direct_read"] is not True or e["image_index_direct_read"] is not True:
            reject("official metadata access provenance changed")
        if e["image_pixels_read"] is not False or e["text_from_original_manuscript_read"] is not False:
            reject("false image viewing or Latin text reading")
        if e["item_archival_id_uniquely_identifies_catalog_record"] is not True or e["shared_signature_uniquely_identifies_physical_copy"] is not False:
            reject("duplicate date-series label misused as copy-specific signature")
        if e["rights_to_republish_images"] is not False:
            reject("publication rights not granted by public catalog")
    references=d["indirect_catalogs_preserved"]
    if len(references)!=4 or {x["key"] for x in references}!=EXPECTED_CROSS:
        reject("PARES and LWL preliminary records must remain")
    for x in references:
        if x["related_treaty_key"] not in {"WAR-TREATY-IPO-1648","WAR-TREATY-IPM-1648"}:
            reject("wrong related treaty")
        if urlparse(x["source_url"]).scheme!="https":
            reject("unsecured supporting source")
        status=x.get("crosswalk_status",x.get("relationship_to_direct_items"))
        if status != "UNRESOLVED":
            reject("physical witness relationship not yet proven")
    edition=d["critical_edition"]
    if (edition["key"],edition["editor"],edition["edition_year"],edition["ipo_page_span"])!=("IPO-EDN-APW-1998","Antje Oschmann",1998,"95–170"):
        reject("critical book bibliography drift")
    if edition["text_page_photographed_or_direct_read"] is not False:
        reject("critical edition falsely read")
    evidence=d["secondary_page_corroborations"]
    if len(evidence)!=2 or {x["clause_anchor"] for x in evidence}!=set(EXPECTED_CITATIONS):
        reject("two distinct secondary page leads necessary")
    for x in evidence:
        if x["reported_apw_page"] != EXPECTED_CITATIONS[x["clause_anchor"]]:
            reject("incorrect APW book page lead")
        if x["apw_page_direct_read"] is not False or x["original_latin_verified"] is not False:
            reject("secondary footnote falsely upgraded to original text")
        if "SECONDARY" not in x["level"] or x["footnote_quote_length"]!="SHORT_METADATA_ONLY":
            reject("secondary source class/quote caution lost")
    holds=d["unresolved"]
    if len(holds)!=6 or any(x["status"]!="OPEN" for x in holds):
        reject("original identity/copyright scholarship issues prematurely closed")
    md=(ROOT/REPORT).read_text(encoding="utf-8")
    if len(md)<4800 or md.count("\n## ")<6 or "DRAFT_RESEARCH_NOT_PUBLIC" not in md:
        reject("reader report incomplete")
    for part in ("2594303","2594304","2594302","41개","35개","34개","117","79","51","APW","121쪽","129쪽"):
        if part not in md:
            reject("report lacks critical observation "+part)
    return {"catalogs":3,"copy_images_listed":sum(x["listed_image_count"] for x in entries),
            "indirect_catalogs":4,"apw_secondary_footnotes":2,"public":0}

if __name__=="__main__":
    x=validate()
    print(f"PASS: IPO Austrian direct catalogs {x['catalogs']}, image-index entries {x['copy_images_listed']}, indirect links {x['indirect_catalogs']}, secondary APW pages {x['apw_secondary_footnotes']}, PUBLIC 0")
