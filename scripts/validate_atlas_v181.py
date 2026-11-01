import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
data=json.loads((R/"data/contracts/atlas_v181_textual_variant_comparisons.json").read_text())
ed=json.loads((R/"data/contracts/atlas_v161_edition_comparison_cards.json").read_text())
ids={e["id"] for w in ed["works"] for e in w["editions"]}
assert len(data["comparisons"])==3
assert data["publication_gate"]["can_ship"] is False
for v in data["comparisons"]:
 assert v["reference"] and v["source_url"].startswith("https://")
 assert v["original_imprint_collated"] is False
 assert v["evidence_class"] and len(v["witnesses"])==2
 for witness in v["witnesses"]:
  assert witness.get("edition_id") is None or witness["edition_id"] in ids
ac=next(x for x in data["comparisons"] if x["id"]=="CMP-V181-AC10")
assert {"vere adsint","distribuantur vescentibus"}<=set(ac["witnesses"][0]["latin_key_phrases"])
assert {"cum pane et vino","vere exhibeantur"}<=set(ac["witnesses"][1]["latin_key_phrases"])
assert next(x for x in data["comparisons"] if x["id"]=="CMP-V181-INST")["witnesses"][1]["chapter_count"]==80
print("PASS V181: 3 comparisons, registered edition IDs, no original collation or publication permission")
