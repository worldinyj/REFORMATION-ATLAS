# V1.25 검증 재현 안내

실행 명령:

```bash
python3 scripts/validate_vol03_v125.py
python3 -m unittest discover -s tests -p 'test_vol03_v125.py' -v
```

검사 영역은 ID 중복, 출처 링크, 공개 게이트, 사본 포함/제외, 비교 절 미교감 상태, 후스 기록 장르 구분. 이는 사학적 판정 자동화가 아니라 데이터 구조의 일관성 검증이다.
