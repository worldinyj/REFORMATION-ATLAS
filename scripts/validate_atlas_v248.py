#!/usr/bin/env python3
"""Check catalogue attribution and prevent promotion to photographic evidence."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/deep/atlas_v248_hab_copy_state_catalogue_audit.json'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def validate(d):
    require((d['version'], d['status'], d['parent_commit']) == ('2.48', 'DRAFT', 'da5a3be06a6e1144b72d09a28314c365b917bcc1'), 'version/parent')
    require(len(d['preserved_files']) == 2, 'snapshots')
    for p in d['preserved_files']:
        require(hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest() == p['sha256'], 'preserved content')
    s = d['source']
    require(s['url'] == 'https://dev.hab.de/lutherkat/search.php?m1=jahr&st1=1524' and s['catalogue_entries'] == [1220, 1221], 'institutional source')
    require(s['retrieval'] == 'SEARCH_INDEX_TEXT_CONFIRMED_WITH_TWO_SEARCH_ENGINES' and s['direct_http_status'] == 403 and not s['full_page_downloaded'] and s['original_photographs_seen'] == 0, 'retrieval overclaim')
    h = d['holdings']
    expected = ['127.21 Theol. (15)', '148.26 Theol. (37)', '297 Theol. (28)', '147.5 Theol. (14)', '231.98 Theol. (1)', 'Li 5530 (55, 1069)', '151.37 Theol. (2)', 'QuN 135.1 (18)', 'QuN 282.2 (18)', '116.10 Theol. (11)', 'Ts 418 (2)']
    require([x['shelfmark'] for x in h] == expected and [x['id'] for x in h] == [f'H{i:02}' for i in range(1, 12)], 'holding identities')
    for i,x in enumerate(h):
        require(x['vd16'] == ('O90' if i < 3 else 'O91') and x['catalogue_entry'] == (1220 if i < 3 else 1221), 'VD16 grouping')
        require(x['original_photo_seen'] is False and x['other_readings'] is None, 'unseen readings invented')
        require(x['explicit_reading_profile'] == (i in [0, 3, 9]), 'profile scope')
    require(d['explicit_states'] == [
        {'holding':'H01','title':'TYPO','A3r_punctuation':'STRONG_COMMA','A4r_pair':['klosters','schrifftlich']},
        {'holding':'H04','title':'CORRECTED','A3r_punctuation':'WEAK_COMMA','A4r_pair':['kloisters','schrfftlich']},
        {'holding':'H10','title':'ENTRY_TITLE_NOT_INDIVIDUALLY_PHOTOCHECKED','A3r_punctuation':'STRONG_COMMA','A4r_pair':['klosters','schrifftlich']}], 'catalogue-specific profiles')
    require(all(v is False for k,v in d['guards'].items() if k != 'new_1526_faces') and d['guards']['new_1526_faces'] == 0, 'inference inflation')
    require(all(v is False for v in d['publication_gate'].values()), 'publication')
    require(d['access_attempt']['http_status'] == 200 and d['access_attempt']['response_kind'] == 'ACCESS_CHALLENGE_HTML' and d['access_attempt']['original_faces_seen'] == 0, 'HTML treated as book')
    require(d['metrics'] == {'listed_holdings':11,'O90_holdings':3,'O91_holdings':8,'explicit_reading_profiles':3,'new_original_faces':0,'core_essays':10,'core_sentences':543}, 'metrics')
    return True

if __name__ == '__main__':
    validate(json.loads(DATA.read_text()))
    print('PASS V248: HAB11 holdings/3 explicit profiles; catalogue not photographic collation; new faces0; publication HOLD')
