from pathlib import Path
r=Path(__file__).resolve().parents[1]
chapter=(r/'docs/01_CONTENT/V172_LUTHER_1517_1521_FULL_READER.md').read_text()
report=(r/'docs/00_GOVERNANCE/V172_PLAN_VS_ACTUAL_AND_NEXT_PRIORITIES.md').read_text()
assert chapter.count('## 1장.')==1 and chapter.count('## 2장.')==1
assert len(chapter)>3000\nprint('Current chapter draft character count:',len(chapter))
assert all(x in chapter for x in ['1517년','1521년','면벌부','보름스','원문','미완료'])
assert all(f'G{x}' in report for x in range(8))
assert '평균 58.7자' in report and '평균 364.6자' in report
assert '남은 6편' in report and '미완' in report
print('PASS V172: substantial Luther chapters, G0-G7 reconciliation, six pending essays')
