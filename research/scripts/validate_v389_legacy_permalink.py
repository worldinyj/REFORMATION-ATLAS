#!/usr/bin/env python3
"""Verify V3.89's recovered, currently broken historical Rott article route.

Usage: python3 validate_v389_legacy_permalink.py PATH_TO_V389_JSON [--self-test]
No network, dependencies, or writes.
"""
import copy
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

OLD = 'https://www.zwingliana.ch/index.php/zwa/article/view/910/820'
CORRECT_ZURICH = 'CH-002121-2-991170608445805501'


def validate(data):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    d = data.get('discovery', {})
    g = data.get('link_quality_gates', {})
    s = data.get('correspondence_constraints', {})
    url = d.get('historical_ojs_link', '')
    parts = urlsplit(url)
    check(data.get('version') == 'V3.89', 'version')
    check(parts.scheme == 'https' and parts.hostname == 'www.zwingliana.ch', 'source hostname')
    check(parts.path == '/index.php/zwa/article/view/910/820', 'literal link path')
    check(url == OLD, 'historical URL')
    check(d.get('parsed_old_article_token') == '910', 'old article token')
    check(d.get('parsed_old_second_token') == '820', 'old route suffix')
    check(d.get('second_token_semantics') == 'UNKNOWN_FROM_LINK_ALONE', 'unproven suffix')
    check(d.get('historical_link_probe', {}).get('result') == 'HTTP 404 NOT FOUND', 'current 404')
    check(d.get('current_pdf_url') is None and d.get('current_article_url') is None, 'no invented active URL')
    check(not d.get('original_pdf_opened') and not d.get('printed_489_image_seen') and not d.get('printed_491_image_seen'), 'no original inspection')
    check(g.get('mapping_of_legacy_910_to_new_article_id') is None and g.get('mapping_of_legacy_820_to_new_galley_id') is None, 'no speculative migration')
    check(g.get('present_day_pdf_link_verified') is False, 'pdf not verified')
    check(s.get('july23_vs_july25_identity') == 'UNRESOLVED', 'letter collision still unresolved')
    check(s.get('correct_zurich_catalog_identifier') == CORRECT_ZURICH, 'correct Zurich catalog id')
    check(data.get('deployment', {}).get('can_ship') is False, 'no release')
    sources = data.get('sources', [])
    check(len({x.get('id') for x in sources}) == len(sources), 'source IDs unique')
    check(d.get('source') in {x.get('id') for x in sources}, 'linked source')
    return errors


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 validate_v389_legacy_permalink.py PATH_TO_V389_JSON [--self-test]')
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    problems = validate(data)
    result = {'version': data.get('version'), 'checks': 17, 'problems': problems}
    if '--self-test' in sys.argv[2:]:
        mutations = [
            ('claim_pdf', lambda x: x['discovery'].update(current_pdf_url='https://example.org/guess.pdf')),
            ('erase_404', lambda x: x['discovery']['historical_link_probe'].update(result='200 OK')),
            ('assume_820_galley', lambda x: x['discovery'].update(second_token_semantics='VERIFIED_PDF_GALLEY')),
            ('promote_original', lambda x: x['discovery'].update(printed_489_image_seen=True)),
            ('merge_july_letters', lambda x: x['correspondence_constraints'].update(july23_vs_july25_identity='SAME')),
            ('publish', lambda x: x['deployment'].update(can_ship=True)),
        ]
        result['negative_tests'] = []
        for name, modify in mutations:
            candidate = copy.deepcopy(data)
            modify(candidate)
            result['negative_tests'].append({'name': name, 'rejected': bool(validate(candidate))})
        if not all(t['rejected'] for t in result['negative_tests']):
            problems.append('mutation failed')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(bool(problems))


if __name__ == '__main__':
    raise SystemExit(main())
