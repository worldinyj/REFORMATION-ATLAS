# V3.51 | Wittenberg Concord: critical witness and subscription collation

**Date:** 2026-11-09  
**Parent:** V3.50 / `research/atlas-v350-wittenberg-manuscript-witnesses`  
**State:** DRAFT · RESEARCH_ONLY · NOT_APPROVED · CAN_SHIP=false

## Goal
Distinguish the *document date*, the *critical editor's date*, copy-specific *subscription lists*, and subsequent endorsements. Avoid representing a catalogue description or OCR transcription as a direct reading from a sixteenth-century manuscript.

## Sources rechecked in this cycle
1. BDS 6/1 (Gütersloh 1988), item 10, pp. 114–134; contents heading dates *Formula Concordiae Lutherj et Bucerj* **28 May 1536**. https://digi.hadw-bw.de/view/bds6_1/0009
2. BDS 6/1, p. 131 (digital page /0135), editorial apparatus lists order of signatories for witnesses A/B, C/D/E, G, H, I, J, L; footnote 34 describes later signatures of Urbanus Rhegius, Spalatin, and Melander. **Access type: online edition text/OCR, not visual inspection of the actual page image.** https://digi.hadw-bw.de/view/bds6_1/0135
3. *Melanchthons Briefwechsel* regest 1744: **29 May 1536**, list of named participants, conditional approval required from absent preachers and authorities. **Access: scholarly regest**. https://melanchthon.hadw-bw.de/regest.html?reg_nr=1744
4. Gotha Chart. A 396, fol. 53r–54v: copy, Communion arts. 1–4 only; catalogue explicitly notes Jonas absent in *this copy*. **Access: library catalogue, not manuscript image.** https://kalliope.staatsbibliothek-berlin.de/de/ead?ead.id=DE-611-HS-3411111
5. Gotha Chart. B 28, fol. 34r/v: copy, Communion arts. 1–4 only; catalogue explicitly notes additional Johannes Zwick; metadata anomaly 'Datum der Vorlage: 1526'. **Access: library catalogue, not manuscript image.** https://kalliope.staatsbibliothek-berlin.de/de/ead?ead.id=DE-611-HS-3421004

## Critical apparatus: subscription witness matrix
The lists below follow the BDS 6/1 p. 131 editorial summary, *not* autographs examined by this project.

| Witness grouping | Jonas | Zwick | Upper German list | Special note |
|---|---|---|---|---|
| A, B | included | not listed | present | Schuler before Musculus |
| C, D, E | included | not listed | present | Musculus before Schuler |
| G | omitted | not listed | present | Schuler ahead of Otter |
| H | omitted | not listed | absent | only Wittenberg-side names listed, plus Menius and Myconius |
| I | omitted | included | present | Alber and Schradin at end |
| J | included | included | present | Alber and Schradin at end |
| L | omitted | not listed | present | order variation |

Important: 'not listed' only means absent from this editorial enumeration. It does **not** establish that an individual did not approve the agreement, was absent from Wittenberg, or was not involved in another documentary witness.

## Additional downstream signers
BDS p. 131 n. 34 distinguishes Urbanus Rhegius, Spalatin, and Melander, whose names are added in CR III col. 77 and both Weimar textual forms. The editors say these persons **were not in Wittenberg** and subsequently signed the formula (place tentatively *Naumburg?*). In the user-facing historical narrative, classify as `later_subscription`, **not** `on_site_1536_signatory`. The proposed location is uncertain.

## Dating
- `edition_date = 1536-05-28` for BDS heading, specifically labelled editorial.
- `regest_date = 1536-05-29` for MBW 1744.
- `catalogue_assigned_date = 1536-05-29` for Gotha A 396 and B 28.
- Do not treat the conflicting dates as proof of two separate signings without examining the critical introduction, source variants, and provenance.
- The isolated '1526' in Chart. B 28 catalogue metadata remains unresolved and must not silently override the 1536 historical date.

## Historical interpretation (preliminary)
The agreement was a process of doctrinal formulation and ecclesial reception, not necessarily a single immutable signature sheet. The editorial apparatus documents variation in copied lists and records later endorsement. It does **not** by itself establish when or why each copy diverged.

The doctrinal content (Lord's Supper, unworthy recipients, infant baptism, absolution) must be studied separately from signatures: copied article text, editorial variants, and participant assent are three distinct evidence objects.

## Structured records proposed for app ingestion (not published)
- `source_id`, `witness_siglum`, `shelfmark`, `folio`, `edition_page`, `source_access`, `date_text`, `date_role`
- `person_id`, `subscription_status` (listed / omitted_in_list / later_subscription / not_assessed), `evidence_basis`, `certainty`
- `article_id`, `diplomatic_reading`, `normalized_reading`, `editorial_variant`, `verified_from_manuscript_image`
- `public_release_gate` fixed false until primary witness review and historical expert QA.

## Next gate: V3.52
1. Inspect accessible BDS pp. 114–134 image by image (where supported), separating article text and footnotes.
2. Locate the preface/editorial notes explaining the choice of the 28 May date.
3. Crosswalk sigla A–S to shelfmarks; avoid assuming that a same-looking signer list proves identical manuscript.
4. Mark each signed-name item as *witness attestation*, *later endorsement*, or *unresolved*.
5. Provide only verified explanatory content to the history app after review.

## QA checklist
- [x] Dates kept source-specific
- [x] Subscription witness matrix derived from edition apparatus
- [x] Subsequent signatories separated from original attendee list
- [x] Catalogue/OCR evidence not relabelled as manuscript inspection
- [ ] Manuscript folio images verified
- [ ] Date discrepancy resolved
- [ ] Full article collation completed
- [ ] Expert release approval

**Publishing action:** none. **Main edits:** none.
