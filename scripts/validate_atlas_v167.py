#!/usr/bin/env python3
from pathlib import Path
r=Path(__file__).resolve().parents[1]
base=r/"integrations/atlas-explorer-v167"
html=(base/"index.html").read_text(encoding="utf8")
js=(base/"explorer.mjs").read_text(encoding="utf8")
assert all(f'data-tab="{x}"' in html and f'id="{x}"' in html for x in ('readers','editions','claims','cities'))
assert 'buildAtlasPreview' in js and "if(vm.canPublish!==false)" in js
assert 'replaceChildren()' in js and 'noopener noreferrer' in js
assert "localStorage" not in js and "innerHTML=item.body" not in js
assert 'external' not in html.lower() or '외부 이미지' in html
assert (base/"README.md").is_file()
print("PASS V1.67: four tab shells, escaped reader content, read-only adapter and release gate")
