from pathlib import Path
p=Path(__file__).resolve().parents[1]/'integrations/atlas-explorer-v168'
h=(p/'index.html').read_text();j=(p/'explorer.mjs').read_text();css=(p/'mobile.css').read_text()
assert all((p/f).exists() for f in ('index.html','explorer.mjs','mobile.css','ux-helpers.mjs','ux-helpers.test.mjs'))
assert all('data-tab="'+x+'"' in h for x in ('readers','editions','claims','cities'))
assert 'buildAtlasPreview(input)' in j and 'loadJson(fetch' in j
assert "setAttribute('role','alert')" in j
assert 'resultMessage(items.length)' in j
assert 'noopener noreferrer' in j and 'safeText(item.body)' in j
assert '@media(max-width:380px)' in css and 'min-height:44px' in css
print('PASS V168B responsive UX and safe data rendering')
