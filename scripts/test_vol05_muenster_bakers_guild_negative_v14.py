#!/usr/bin/env python3
"""Reject changes that promote archival regests into original-text inspections."""
from __future__ import annotations
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_vol05_muenster_bakers_guild_v14 import load,validate,REG

def test_rejected(data,name,change):
    d=copy.deepcopy(data);change(d)
    try:validate(d)
    except (ValueError,KeyError,TypeError,IndexError,StopIteration):return
    raise AssertionError("unsafe historical mutation accepted: "+name)

def main():
    d=load(REG)
    assert validate(d)["public"]==0
    tests=[
      ("release",lambda x:x["gate"].__setitem__("can_publish",True)),
      ("historian approval",lambda x:x["gate"].__setitem__("historian_approved",True)),
      ("guild book original read",lambda x:x["gate"].__setitem__("original_baker_book_read",True)),
      ("1661 original found",lambda x:x["gate"].__setitem__("original_1661_guild_regulament_found",True)),
      ("Bischof p22 read",lambda x:x["gate"].__setitem__("Bischof_1926_p22_read",True)),
      ("1681 original read",lambda x:x["gate"].__setitem__("AAII0_1681_folio_read",True)),
      ("V35 lawsuit invented",lambda x:x["gate"].__setitem__("individual_V35_case_proved",True)),
      ("media rights invented",lambda x:x["gate"].__setitem__("media_rights_approved",True)),
      ("main changed",lambda x:x.__setitem__("main_modified",True)),
      ("app changed",lambda x:x.__setitem__("ai_studio_modified",True)),
      ("canonical record created",lambda x:x.__setitem__("new_canonical_ids",1)),
      ("wrong treaty",lambda x:x.__setitem__("canonical_document_id","OV-D-014")),
      ("source dropped",lambda x:x["sources"].pop()),
      ("insecure archive URL",lambda x:x["sources"][0].__setitem__("url","http://example.com")),
      ("1639 paper original read claimed",lambda x:x["sources"][0].__setitem__("original_document_read",True)),
      ("modern art rights fabricated",lambda x:x["sources"][1].__setitem__("media_rights_approved",True)),
      ("1639 book relabelled 1660",lambda x:x["documents"][0].__setitem__("date","1660-01-12")),
      ("1639 catalog swapped",lambda x:x["documents"][0].__setitem__("shelfmark","Nr. 1627")),
      ("1639 booklet split into originals",lambda x:x["documents"][0].__setitem__("witness_type","THREE_ORIGINALS")),
      ("1661 guild rule forged shelfmark",lambda x:x["documents"][1].__setitem__("shelfmark","MLA 413–4")),
      ("1661 confusion with council",lambda x:x["documents"][1].__setitem__("date","1661-08-18")),
      ("1681 council folio wrong",lambda x:x["documents"][2].__setitem__("shelfmark","AA II 0 fol. 95r")),
      ("1718 confused 1790",lambda x:x["documents"][3].__setitem__("date","1790-04-23")),
      ("1718 source lost",lambda x:x["documents"][3].__setitem__("source_key","S1")),
      ("guild folio itself read",lambda x:x["documents"][0].__setitem__("firsthand_original_read",True)),
      ("1660 Jan12 shifted",lambda x:x["claims"][1].__setitem__("date","1660-01-18")),
      ("1660 election amount changed",lambda x:x["claims"][1].__setitem__("claim","an unspecified cash demand")),
      ("1660 Jan18 shifted",lambda x:x["claims"][2].__setitem__("date","1661-08-18")),
      ("1641 Beckmann turned confessional",lambda x:x["claims"][3].__setitem__("IPO_V35_enforcement_proved",True)),
      ("1661 original falsely read",lambda x:x["claims"][4].__setitem__("original_text_read",True)),
      ("Bischof 1926 omitted",lambda x:x["bibliography"].__setitem__("year",1927)),
      ("Bischof 1926 read fictitiously",lambda x:x["bibliography"].__setitem__("book_1926_read",True)),
      ("Bischof 1661 original guessed",lambda x:x["bibliography"].__setitem__("original_1661_archival_signature","A II 0 96r")),
      ("three paper booklets incorrectly asserted",lambda x:x["grouping"].__setitem__("nr1527_physical_booklets",3)),
      ("Jan18 1660 dropped",lambda x:x["grouping"]["appendix_dates"].pop()),
      ("V35 false proof",lambda x:x["grouping"].__setitem__("NOT_PROOF_OF_1648_V35_APPLICATION",False)),
      ("uncertainty erased",lambda x:x["uncertainties"].clear())
    ]
    for name,change in tests:test_rejected(d,name,change)
    print(f"PASS: {len(tests)} forbidden archival booklet, 1926 citation, 1661 ordinance, 1681 election and V35 publication mutations rejected; PUBLIC 0")
if __name__=="__main__":main()
