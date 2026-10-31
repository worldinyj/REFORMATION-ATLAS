#!/usr/bin/env python3
"""Validate V1.66 preview adapter contract and upstream integrity; fail closed."""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
load=lambda name:json.loads((r/name).read_text(encoding='utf8'))
m=load("data/contracts/atlas_v165_integration_readiness_manifest.json")
p=load("data/deep/atlas_v156_extended_narratives.json")
cities=load("data/contracts/atlas_v157_historical_city_map.json")
nav=load("data/contracts/atlas_v164_evidence_navigation.json")
assert m['publication_gate']=={'approved':False,'can_ship':False}
assert len(p['pages'])==10 and len(cities['places'])==11 and len(nav['claims'])==8
code=(r/"integrations/ai-studio-readonly-v166/adapter.mjs").read_text(encoding="utf8")
assert 'canPublish:false' in code and 'RESEARCH_PREVIEW_ONLY' in code
assert 'fetch(' not in code and 'localStorage' not in code
assert 'throw Error' in code
print("PASS V1.66: no external fetch or state mutation; fail-closed preview contract")
