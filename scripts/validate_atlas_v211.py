#!/usr/bin/env python3
"""V211: Verify two historical editorial replacements, full rebase and publication HOLD."""
import json,re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
x=load("data/deep/atlas_v211_ten_reader_hus_augsburg_revision.json")
old=load("data/deep/atlas_v209_unified_ten_revised_readers.json")
v10=load("data/deep/atlas_v210_reader_sentences_and_focus_anchors.json")
assert x["version"]=="2.11" and x["lineage"]["base_commit"]=="fb4f17605dc592ae068959370ec2eb2143946d9f"
assert all(v is False for v in x["publication_gate"].values())
m=x["metrics"]
assert (m["readers"],m["sections"],m["paragraphs"],m["changed_paragraphs"],m["changed_reader_chapters"])==(10,70,124,2,2)
assert m["previous_sentence_units"]==len(v10["sentences"])==518
assert m["reused_exact_sentences"]+m["retired_old_sentences"]==518
assert m["current_sentence_units"]==m["reused_exact_sentences"]+m["resegmented_new_sentences"]==len(x["sentences"])
assert (m["focus_anchors"],m["reanchored_focus"],m["rebased_unchanged_focus"])==(30,2,28)
assert m["source_records"]==len(x["source_register"])==4
assert m["source_dossiers"]==len(x["evidence_dossiers"])==2
assert m["primary_witness_images_checked"]==m["expert_approved"]==m["public_release_approved"]==0
chap={c["key"]:c for c in x["chapters"]}
before={c["key"]:c for c in old["chapters"]}
assert len(chap)==len(before)==10
edits={}
for e in x["edits"]:
    edits.setdefault(e["reader_key"],[]).append(e)
assert len(x["edits"])==2 and set(edits)=={"HUS","AUGSBURG"}
for key,oldc in before.items():
    body=oldc["body"]
    for e in sorted(edits.get(key,[]),key=lambda z:z["old_start"],reverse=True):
        assert body[e["old_start"]:e["old_end"]]==e["old_text"]
        body=body[:e["old_start"]]+e["new_text"]+body[e["old_end"]:]
    c=chap[key]
    assert body==c["body"] and c["review_status"]=="PENDING"
    assert c["source_version"]==("2.11" if key in edits else oldc["source_version"])
assert "게오르크 라우" in edits["AUGSBURG"][0]["new_text"]
assert "교회의 궁극적인 머리" in edits["HUS"][0]["new_text"]
def move(key,pos):
    delta=0
    for e in edits.get(key,[]):
        assert not (e["old_start"]<pos<e["old_end"])
        if pos>=e["old_end"]:delta+=e["delta"]
    return pos+delta
oldnav={q["reader_key"]:q["sections"] for q in old["section_navigation"]}
newnav={q["reader_key"]:q["sections"] for q in x["sections"]}
assert set(oldnav)==set(newnav)
for key in before:
    prev=0
    assert len(newnav[key])==len(oldnav[key])
    for n,o in zip(newnav[key],oldnav[key]):
        assert (n["start_char"],n["end_char"])==(move(key,o["start_char"]),move(key,o["end_char"]))
        assert n["id"]==o["id"].replace("SEC-V209-","SEC-V211-")
        assert prev==n["start_char"]
        prev=n["end_char"]
    assert prev==len(chap[key]["body"])
oldpar={p["id"]:p for p in old["paragraph_spans"]}
newpar={p["id"]:p for p in x["paragraphs"]}
assert len(newpar)==len(oldpar)==124
for op in oldpar.values():
    np=newpar[op["id"].replace("PAR-V209-","PAR-V211-")]
    key=op["reader_key"]
    assert (np["start_char"],np["end_char"])==(move(key,op["start_char"]),move(key,op["end_char"]))
    assert chap[key]["body"][np["start_char"]:np["end_char"]]==np["text_exact"]
    e=next((e for e in edits.get(key,[]) if e["old_paragraph_id"]==op["id"]),None)
    assert np["text_exact"]==(e["new_text"] if e else op["text_exact"])
assert m["full_corpus_codepoints"]==sum(len(c["body"]) for c in chap.values())
oldsent={s["id"]:s for s in v10["sentences"]}
newseq=Counter()
newsent={}
count_reused=0
for s in x["sentences"]:
    key=s["reader_key"];newseq[key]+=1
    assert s["id"]==f"SNT-V211-{key}-{newseq[key]:04d}" and s["id"] not in newsent
    newsent[s["id"]]=s
    p=newpar[s["passage_id"]]
    assert p["reader_key"]==key and p["section_id"]==s["section_id"]
    assert p["start_char"]<=s["start_char"]<s["end_char"]<=p["end_char"]
    ss=chap[key]["body"][s["start_char"]:s["end_char"]]
    assert ss[:110]==s["excerpt"] and len(ss)==s["codepoints"]
    assert s["editorial_human_review"]=="PENDING"
    assert s["source_original_witness_checked"] is False and s["expert_approved"] is False and s["can_publish"] is False
    if s["previous_sentence_id"] is not None:
        os=oldsent[s["previous_sentence_id"]]
        assert s["start_char"]==move(key,os["start_char"])
        assert s["end_char"]==move(key,os["end_char"])
        count_reused+=1
    else:
        assert p["changed_by_v211_revision_id"] is not None
assert count_reused==m["reused_exact_sentences"]
for p in newpar.values():
    sentences=sorted((s for s in x["sentences"] if s["passage_id"]==p["id"]),key=lambda v:v["start_char"])
    assert sentences
    pos=p["start_char"]
    for s in sentences:
        assert not chap[p["reader_key"]]["body"][pos:s["start_char"]].strip()
        pos=s["end_char"]
    assert not chap[p["reader_key"]]["body"][pos:p["end_char"]].strip()
v10a={a["focus_id"]:a for a in v10["focus_anchors"]}
anchors={}
new_count=0
for a in x["focus_anchors"]:
    assert a["focus_id"] not in anchors and a["focus_id"] in v10a
    anchors[a["focus_id"]]=a
    p=newpar[a["passage_id"]]
    assert (p["reader_key"],p["section_id"])==(a["reader_key"],a["section_id"])
    assert p["start_char"]<=a["start_char"]<a["end_char"]<=p["end_char"]
    assert chap[a["reader_key"]]["body"][a["start_char"]:a["end_char"]]==a["exact_excerpt"]
    s=newsent[a["source_sentence_id"]]
    assert s["start_char"]<=a["start_char"]<a["end_char"]<=s["end_char"]
    assert a["id"] in s["v211_focus_anchor_ids"]
    if a["anchor_method"]=="NEW_V211_PARAGRAPH_EXACT_REANCHOR":
        new_count+=1
        assert a["focus_id"] in {"FOCUS-V204-HUS-01","FOCUS-V204-AUGSBURG-02"}
    else:
        olda=v10a[a["focus_id"]]
        assert a["exact_excerpt"]==olda["excerpt_exact"]
        assert (a["start_char"],a["end_char"])==(move(a["reader_key"],olda["start_char"]),move(a["reader_key"],olda["end_char"]))
    assert a["expert_claim_approved"] is False and a["original_source_collated"] is False and a["can_publish"] is False
assert len(anchors)==30 and new_count==2
assert all(s["v211_focus_anchor_ids"]==[a["id"] for a in x["focus_anchors"] if a["source_sentence_id"]==s["id"]] for s in x["sentences"])
for s in x["source_register"]:
    assert s["url"].startswith("https://") and s["original_historic_print_folio_opened"] is False
for record in x["evidence_dossiers"]:
    assert record["status"] and record["source_ids"]
    assert record["human_signoff"] is False
    assert all(k in {s["id"] for s in x["source_register"]} for k in record["source_ids"])
assert len(x["unresolved"])>=5
print(f"PASS V211: 10 readers, 2 substantive revisions, {len(x['sentences'])} revalidated sentences, 30 anchors; source/editorial release HOLD.")
