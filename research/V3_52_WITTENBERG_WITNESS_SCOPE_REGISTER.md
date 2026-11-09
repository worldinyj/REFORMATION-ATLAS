# V3.52 — Wittenberg Concord, source scope and collation eligibility register

**Date:** 2026-11-09  
**Predecessor:** V3.51 (`research/atlas-v351-wittenberg-critical-witness-register`)  
**Status:** RESEARCH_ONLY / DRAFT / NOT_APPROVED / CAN_SHIP=false

## What was newly checked
The online full text of the 1988 edition *Martin Bucers Deutsche Schriften*, volume 6/1, **printed pp. 114–115** (digital frames /0118 and /0119) explicitly distinguishes manuscripts A–S, printing T, **manuscripts not considered in collation**, and additional printings. This classification determines what evidence can count as an apparatus witness in the planned doctrinal-text comparison.

Access level throughout: **edition digital OCR/transcribed web text**. No manuscript facsimile inspection is claimed. OCR-corrupted shelfmarks must not be treated as precise archive identifiers without image-level checking.

## Editorial inventory by original siglum
The following geographic/collection identification is readable in the edition's online text. For shelfmark characters, return to the actual scan before using them as exact citations.

| Siglum | City | Institution | Portion represented | Evidence |
|---|---|---|---|---|
| A | Zürich | Staatsarchiv | complete | BDS p.114 online OCR |
| B | Konstanz | Stadtarchiv | complete | same |
| C | Strasbourg | Archives de Strasbourg (AST) | Communion only | same |
| D | Vienna | Österreichische Nationalbibliothek | Communion and Baptism/Absolution in separate folio spans | same |
| E | Heidelberg | Universitätsbibliothek, Cod. Pal. Germ. 684 | complete | same |
| F | Nuremberg | Staatsarchiv | complete | same |
| G | Wolfenbüttel | Herzog August Bibliothek | complete | same |
| H | Wolfenbüttel | Herzog August Bibliothek | complete | same |
| I | Wolfenbüttel | Herzog August Bibliothek | Communion only | same |
| J | Wolfenbüttel | Herzog August Bibliothek | Communion only | same |
| K | Wolfenbüttel | Herzog August Bibliothek | Communion only | same |
| L | Wolfenbüttel | Herzog August Bibliothek | Communion only | same |
| M | Ulm | Stadtarchiv | complete | same |
| N | Gotha | Forschungsbibliothek, Chart. A 346 | Communion only | same |
| O | Gotha | Forschungsbibliothek, Chart. A 41 | complete | same |
| P | Gotha | Forschungsbibliothek, Chart. A 41 | complete | same |
| Q | Strasbourg | AST | Communion only | same |
| R | Hamburg | Staats- und Universitätsbibliothek | Communion only | same |
| S | Frankfurt a.M. / Zerbst archival holding as specified by editors | historical Bundesarchiv Außenstelle reference | Communion only | same |
| T | Ingolstadt print (1545) | Johannes Cochlaeus edition | complete | printed witness, not manuscript |

**Counting rule:** A–S = 19 lettered manuscript entries; T = 1 separately described *printed* witness. The manuscript inventory does **not** mean that all 19 were independently inspected for the present project. BDS also has an additional list of manuscripts *not considered in collation*; do not add them to the 19 source sigla or claim they were collated.

## Excluded from edition's collation (selected)
On printed p.115, BDS records several copies in Dresden, Lindau, Schwäbisch Hall, Strasbourg, Weimar, Vienna, and Zürich under the distinct heading *Bei der Kollationierung nicht berücksichtigte Handschriften*. These may be valuable for future manuscript study, but they must have `collation_in_1988_edition=false` and `not_same_as_siglum_A_to_S=true` until independently linked. Avoid treating this exclusion as historical inauthenticity; it is a decision of the edition.

## Important new analytical distinction
- **Complete manuscript**: may potentially support articles on Lord's Supper, infant baptism, and absolution, once folios actually verified.
- **Communion-only copy**: cannot directly support assertions about the baptism or absolution text.
- **D with divided folios**: separate source segment references required for Communion vs Baptism/Absolution.
- **Printed witness T (1545)**: a distinct published transmission layer; do not refer to it as a manuscript.
- **Excluded manuscripts**: library/research source candidates, not witnesses of the existing BDS collation.
- **Signatory sequence**: BDS p.131 groups A/B, C/D/E, G, H, I, J, L; lack of a signatory matrix row for another manuscript is `not_assessed`, not `name_absent`.

## Digital integration schema proposal
```json
{
  "witness_id": "BDS-1988-A",
  "edition": "BDS_6_1_1988",
  "siglum": "A",
  "format": "manuscript",
  "text_coverage": ["communion", "baptism", "absolution"],
  "collation_in_edition": true,
  "direct_manuscript_image_checked": false,
  "edition_page_source": "114",
  "source_access": "edition_OCR",
  "shelfmark_verified": false,
  "publication_gate": "DRAFT"
}
```

## Recommended next research gate (V3.53)
1. Review the original facsimile images of BDS pages 114–115 and 131 to correct OCR-distorted folio/shelfmark numbers.
2. Match Gotha Chart. A 396 / Chart. B 28 catalogue entries to BDS sigla only after shelfmark equivalence is demonstrated. **Do not automatically equate Chart. A 396 with siglum N (Chart. A 346).**
3. Build article-by-article lexical alignment across complete witnesses A/B/D/E and limited communion-only witnesses I/J/L.
4. Keep BDS heading 28 May and MBW 1744 regest 29 May as distinct labels pending source-critical dating analysis.
5. No public app integration before QA approval.

## Source URLs
- BDS printed p.114: https://digi.hadw-bw.de/view/bds6_1/0118
- BDS printed p.115: https://digi.hadw-bw.de/view/bds6_1/0119
- BDS printed p.131: https://digi.hadw-bw.de/view/bds6_1/0135
- MBW 1744: https://melanchthon.hadw-bw.de/regest.html?reg_nr=1744

## Gate
[x] Witness categories separated.  
[x] 19 manuscript sigla and print T inventoried at geographic level.  
[x] Incomplete vs complete witnesses distinguished.  
[x] OCR uncertainty flagged for shelfmarks.  
[ ] Actual facsimile and diplomatic reading completed.  
[ ] Manuscript-source images examined.  
[ ] Expert approval obtained.

**Explicit exclusions:** No edits to 513 historical essays, no edits to `main`, no AI Studio changes, no PR merge, no publication.
