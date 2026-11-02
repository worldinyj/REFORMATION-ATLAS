#!/usr/bin/env python3
"""V233: indirect critical-letter Latin excerpt, handwriting provenance, K autography gate."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
v19=read("data/deep/atlas_v219_structured_ten_reader_critical_editions.json")
v27=read("data/deep/atlas_v227_melanchthon_conversation_original_eyewitness_comparison.json")
v32=read("data/deep/atlas_v232_marburg_1529_documentary_chronology_melanchthon_autograph.json")
d=read("data/deep/atlas_v233_mbw826_indirect_latin_folio_autography_and_mbw825_k_index.json")
assert d["version"]=="2.33"
assert d["parent_commit"]=="d6395b62b1b88c164dba311dfbc468f5c0cb78ad"
assert d["baseline_dataset"]=="data/deep/atlas_v232_marburg_1529_documentary_chronology_melanchthon_autograph.json"
assert all(x is False for x in d["publication_gate"].values())
assert (v19["metrics"]["chapters"],v19["metrics"]["sections"],v19["metrics"]["paragraphs"],v19["metrics"]["sentences"],v19["metrics"]["full_integrated_codepoints"])==(10,74,128,543,35102)
assert v27["metrics"]["original_manuscript_pages_visually_inspected"]==4
assert v32["metrics"]["new_original_1529_images_read"]==0
assert v32["metrics"]["new_1529_autograph_exemplar_located"]==1

def indexed(rows):
    x={r["id"]:r for r in rows}
    assert len(x)==len(rows),"duplicate item id"
    return x
src=indexed(d["sources"]);obs=indexed(d["historical_objects"])
phrases=indexed(d["short_philological_anchors"])
claims=indexed(d["interpretive_claims"])
sections=indexed(d["reader_draft"]["sections"])
issues=indexed(d["unresolved"])
assert (len(src),len(obs),len(phrases),len(claims),len(sections),len(issues))==(9,4,4,5,3,6)
assert all(x["url"].startswith("https://") and x["original_folio_read"] is False for x in src.values())
assert all(x["source_ids"] and set(x["source_ids"])<=src.keys() for x in obs.values())
assert all(x["autograph_image_seen"] is False for x in obs.values())
assert obs["OBJ-V233-MBW826"]["mbw_number"]==826
assert obs["OBJ-V233-MBW826"]["shelfmark"]=="Cod. hist. 2° 889–26, fol. 36r–36v"
assert obs["OBJ-V233-MBW825-K"]["mbw_number"]==825
assert obs["OBJ-V233-MBW825-K"]["shelfmark"]=="Best. 3 Nr. 245, fol. 60r–64v"
assert obs["OBJ-V233-MBW826"]["original_hand_scholarly_attributed"] is True
assert obs["OBJ-V233-MBW825-K"]["original_hand_scholarly_attributed"] is False
assert obs["OBJ-V233-CR1834"]["document_type"]=="1834_EDITORIAL_LETTER_PRINT"
assert obs["OBJ-V233-MBWT3"]["document_type"]=="MODERN_CRITICAL_TEXT_EDITION_MBW_T3"
assert set(phrases)=={"PHRASE-V233-CINGLII","PHRASE-V233-WORDS","PHRASE-V233-STRUGGLE","PHRASE-V233-PRESENCE"}
assert sum(x["words"] for x in phrases.values())==16
assert all(len(x["latin"].split())==x["words"] for x in phrases.values())
assert all(x["source_ids"]==["SRC-V233-ANDERSEN2011"] and x["status"]=="INDIRECT_CITATION_OF_MBW_T3" for x in phrases.values())
assert phrases["PHRASE-V233-STRUGGLE"]["latin"]=="non sine maximo certamine"
assert phrases["PHRASE-V233-PRESENCE"]["latin"]=="corpus Domini vere praesens in coena"
assert all(x["support_ids"] and set(x["support_ids"])<=src.keys() for x in claims.values())
assert all(set(x["supports"])<=claims.keys() and x["summary_ko"] for x in sections.values())
assert len(d["reader_draft"]["title_ko"])>5
assert all(x["question"] for x in issues.values())
protocol=d["edition_research_protocol"]
tiers=indexed(protocol["tiers"])
assert len(tiers)==5
assert all(t["completed"] is False for t in list(tiers.values())[:3])
assert tiers["T4"]["completed"] is True and tiers["T5"]["completed"] is True
assert protocol["autograph_17c_reverse_annotations_are_not_1529_letter_text"] is True
assert protocol["critical_edition_e_t_w_q_apparatus_required_for_publish"] is True
assert protocol["wlb_826_open_access_status"].startswith("NOT_ESTABLISHED")
assert protocol["hessian_825_digital_link_target_status"].startswith("ACADEMY_DIGITIZATION_INDEX_CONFIRMED")
assert d["metrics"]=={"source_records":9,"source_objects":4,"short_latin_anchors":4,
 "total_short_quoted_latin_words":16,"interpretive_claims":5,"reader_sections":3,
 "open_issues":6,"autograph_826_image_pages_read":0,"mbw_t3_826_pages_read":0,
 "cr1834_original_pages_proofread":0,"autograph_825_k_images_read":0,
 "cumulative_other_original_1529_manuscript_image_pages":4,
 "new_primary_pages_read":0,"published_items":0}
print("PASS V233: four short Latin anchors 16 words from later critical-text quotation; original letter unviewed")
print("PASS V233: 1529 WLB author autograph vs 17c ownership marks, HAdW signed-K original index; no original/modern edition conflation")
print("PASS V233: E/T/W/Q publication hold, 10-reader history corpus unchanged")
