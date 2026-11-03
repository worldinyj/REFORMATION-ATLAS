#!/usr/bin/env python3
"""Validate V247 provenance and limits; does not certify historical readings."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = 'data/deep/atlas_v247_o90_o91_paired_loci_wa15_printed_apparatus_audit.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(d):
    require((d['version'], d['status'], d['parent_commit']) ==
            ('2.47', 'DRAFT', 'c3079778ed33415bcaa48d721e44e330c106e025'), 'version/parent')
    require(all(v is False for v in d['publication_gate'].values()), 'publication gate')
    expected_hashes = ['0fea005d6592dbc976b46da1d1d9d6f217b4390a2708b304968648a64ad82efb',
                       '7cbe9c0318673b53fd8bc5edab47c41319133075079bc6b237153c09ad295e97']
    require([x['sha256'] for x in d['preserved_files']] == expected_hashes, 'baseline digests')
    for row in d['preserved_files']:
        require(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256'], 'inherited file changed')
    sources = {x['id']: x for x in d['sources']}
    require(len(sources) == len(d['sources']) == 8, 'source uniqueness/count')
    for row in sources.values():
        require(row['url'].startswith('https://') and row['reading'] and row['scope'], 'source provenance')
    assets = {x['filename']: x for x in d['retrieved_artifacts']}
    require(len(assets) == len(d['retrieved_artifacts']) == 19, 'artifact count')
    for row in assets.values():
        require(row['bytes'] > 0 and len(row['sha256']) == 64 and
                all(c in '0123456789abcdef' for c in row['sha256']), 'artifact checksum')
    o = d['o90']
    require((o['vd16'], o['vd16_basis'], o['record'], o['barcode'], o['shelfmark']) ==
            ('O90', 'OFFICIAL_GATEWAY_HOLDING_LINK', 'AC10086742', 'Z182122003', '*35.R.59'), 'holding identity')
    require(o['manifest_canvases'] == 20 and o['inspected_canvases'] == list(range(5, 19)), 'image scope')
    require(o['title_canvases'] == [5] and o['body_canvases'] == list(range(7, 15)) and
            o['blank_canvases'] == [6, 15, 16, 17, 18], 'face partition')
    require(o['folio_map'] == dict(zip(map(str, range(5, 15)),
            ['A1r', 'A1v', 'A4r', 'A4v', 'B1r', 'B1v', 'B2r', 'B2v', 'B3r', 'B3v'])), 'Vienna-specific folios')
    require(o['missing_leaves'] == ['A2', 'A3'] and
            o['A4_signature_basis'] == 'INFERRED_FROM_SEQUENCE_AND_SIGNED_B_LEAVES', 'lacuna/signatures')
    require(not o['same_copy_as_WA1899_proven'] and not o['full_collation_complete'] and
            o['halle_faces_seen'] == 0, 'scope expansion')
    loci = d['paired_loci']
    require([x['id'] for x in loci] == [f'P{i:02}' for i in range(1, 9)], 'locus IDs')
    require([(x['o90_canvas'], x['o91_canvas']) for x in loci] ==
            [(5, 5), (7, 11), (7, 11), (13, 17), (13, 17), (13, 17), (14, 18), (14, 18)], 'paired witness offsets')
    for row in loci:
        require(o['folio_map'][str(row['o90_canvas'])] == row['folio'], 'paired folio')
    require((loci[0]['o90_token'], loci[0]['o91_token'], loci[0]['result']) ==
            ('geschihct', 'geschicht', 'DIFFERENT'), 'title variant')
    require([(x['o90_token'], x['o91_token'], x['result']) for x in loci[1:3]] ==
            [('klosters', 'klosters', 'SAME'), ('schrifftlich', 'schrifftlich', 'SAME')], 'A4 readings')
    require(all(loci[n]['scope'] == 'SELF_REPORT_NOT_INDEPENDENT_PROOF' for n in [3, 4, 6]), 'self-report distinction')
    require(loci[5]['o90_token'] == loci[5]['o91_token'] == 'Jhesus' and
            loci[5]['result'] == 'SAME_NO_EY', 'marginal reading')
    require(loci[7]['o90_token'] == loci[7]['o91_token'] == 'Martinus Luther', 'speaker heading')
    require(d['unavailable_loci'] == [{'id': 'U01', 'folio': 'A3r', 'topic': 'punctuation',
            'o90_canvas': None, 'o91_canvas': 9, 'complete': False, 'reason': 'O90_VIENNA_LACUNA'}], 'missing A3 treated as read')
    w = d['wa15']
    require((w['actual_volume'], w['actual_year'], w['title_pdf_page'], w['pdf_pages']) ==
            (15, 1899, 7, 844), 'actual WA title')
    require(w['metadata_volume'] == 'v.1, pt.5' and w['metadata_date'] == '1883' and
            not w['metadata_adopted_as_edition_identity'], 'metadata disagreement suppressed')
    require(w['selected_print_pages'] == [81, 82, 83, 93, 94] and w['printed_to_pdf'] ==
            {'81': 95, '82': 96, '83': 97, '93': 107, '94': 108} and
            w['apparatus_pages'] == [81, 82, 83], 'WA page offsets')
    require(w['printed_Aa_Ab_inconsistency_confirmed'] and not w['online_transcription_only_error'] and
            not w['silent_siglum_emendation'] and not w['printing_order_resolved'], 'siglum uncertainty erased')
    require(w['p81_reports_vienna_A2_A3_missing'] and w['p93_Ey_attributed_to'] == 'Ax' and
            w['p83_stemma_status'] == 'EDITORIAL_HYPOTHESIS', 'editorial layer')
    require(d['inference_guards'] == {'independent_event_corroboration': False,
            'all_O90_O91_states_collated': False, 'new_1526_original_faces': 0,
            'new_approved_sophia_numeric_readings': 0, 'sophia_numeric_status': 'PENDING',
            'sophia_inherited_print_values': [14, 16, 17, 5]}, 'historical overclaim')
    require(d['rights'] == {'ONB_manifest_license': 'http://rightsstatements.org/vocab/NoC-NC/1.0/',
            'ONB_reported_commercial_reuse_restriction_expiry': '2029-10-31T23:46:33',
            'PDM_claim': False, 'commercial_clearance_granted': False,
            'image_binaries_added_to_repository': False}, 'rights expansion')
    require(len(d['reader_sections']) == len({x['id'] for x in d['reader_sections']}) == 8, 'reader sections')
    for row in d['reader_sections']:
        require(len(row['body']) > 150 and set(row['sources']) <= sources.keys(), 'reader references')
    require(d['metrics'] == {'source_records': 8, 'retrieved_artifacts': 19,
            'new_O90_inspected_faces': 14, 'new_O90_title_faces': 1, 'new_O90_body_faces': 8,
            'new_O90_blank_faces': 5, 'selected_WA_faces': 6, 'WA_apparatus_faces': 3,
            'paired_loci': 8, 'unavailable_loci': 1, 'reader_sections': 8, 'old_core_essays': 10,
            'old_core_sentences': 543, 'new_approved_numeric_readings': 0,
            'new_1526_original_faces': 0, 'published_web_items': 0}, 'scope metrics')
    return assets


def verify_downloads(directory, assets, d):
    for name, row in assets.items():
        p = directory / name
        require(p.stat().st_size == row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256'],
                'source bytes: ' + name)
    m = json.loads((directory / 'onb_o90_manifest.json').read_text())
    require(len(m['sequences'][0]['canvases']) == 20, 'manifest extent')
    meta = ' '.join(str(x['value']) for x in m['metadata'])
    require(all(x in meta for x in ['AC10086742', 'Z182122003', '*35.R.59', '2029-10-31T23:46:33']), 'manifest identity/rights')
    require(m['license'] == d['rights']['ONB_manifest_license'], 'manifest rights')
    ia = json.loads((directory / 'wa15_ia_metadata.json').read_text())['metadata']
    require(ia['volume'] == d['wa15']['metadata_volume'] and ia['date'] == d['wa15']['metadata_date'], 'IA discrepancy')
    require('VD0076310' in (directory / 'o90_gateway.html').read_text(), 'VD16 official record')
    print('PASS V247: 19 source files SHA256/size; ONB20-canvas identity and rights; IA metadata discrepancy')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence-dir', type=Path)
    args = parser.parse_args()
    d = json.loads((ROOT / DATA_PATH).read_text())
    assets = validate(d)
    if args.evidence_dir:
        verify_downloads(args.evidence_dir, assets, d)
    print('PASS V247: O90 title1/body8/blank5; 8 paired loci; A3r unavailable; no full-edition claim')
    print('PASS V247: WA15 actual1899 title; printed Aa/Ab conflict preserved; Ax editorial Ey distinguished')
    print('PASS V247: immutable V219/V246; Sophia numerals pending; core10/543 and publication HOLD')
