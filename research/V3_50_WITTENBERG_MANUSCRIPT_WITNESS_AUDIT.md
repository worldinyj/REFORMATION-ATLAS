# ATLAS V3.50 — 1536 Wittenberg Concord: manuscript witness audit (DRAFT)

Date: 2026-11-09
Parent: V3.49.1 (1836 CR III, pp. 75–78 print audit)
Status: RESEARCH_ONLY / NOT_APPROVED / CAN_SHIP=false
Scope: new research note only. Do not modify 513 historical articles, main, Google AI Studio application, or published assets.

## Research question
How do dated manuscript witnesses, signer lists, and the 1988 critical edition qualify readings inherited from the 1836 Corpus Reformatorum printing?

## Witness/source register (access type separated)
| ID | Evidence | Locator | Observed level | Note |
|---|---|---|---|---|
| W350-01 | Melanchthons Briefwechsel, MBW 1744 | https://melanchthon.hadw-bw.de/regest.html?reg_nr=1744 | scholarly regest accessed | heading identifies Wittenberg, 29 May 1536; records signatories and assent conditions |
| W350-02 | Martin Bucers Deutsche Schriften 6/1 (1988), critical edition | https://doi.org/10.11588/diglit.29831#0118 | search-index OCR excerpt only; image currently access-blocked | heading 'Formula Concordiae Lutherj et Bucerj (28. Mai 1536)'; lists MS A/B/C/D etc; must verify scan before promoting exact date interpretation |
| W350-03 | Thüringer Universitäts- und Landesbibliothek, Rörer collection Ms. Bos. q. 24b | https://flugschriften.reformationsportal.de/ | archival search record, not manuscript facsimile inspected | 29 May 1536; Communion portion, fols. 234v–235r; CR III 75–76 |
| W350-04 | Thüringer Universitäts- und Landesbibliothek, Rörer collection Ms. Bos. q. 24c | https://flugschriften.reformationsportal.de/ | archival search record, not manuscript facsimile inspected | 29 May 1536; Baptism and absolution, fols. 290v–291r; CR III 77–78 |
| W350-05 | Forschungsbibliothek Gotha, Chart. B 28, fol. 34r/v | https://kalliope.staatsbibliothek-berlin.de/de/ead?ead.id=DE-611-HS-3421004 | manuscript catalogue accessed, not facsimile | copy in Conrad Meusel collection, Communion arts. 1–4 only, 29 May 1536 assigned, 'additional signatory Johannes Zwick' |
| W350-06 | Forschungsbibliothek Gotha, Chart. A 91 | https://kalliope.staatsbibliothek-berlin.de/de/findingaid?fa.enum=182&fa.id=DE-611-BF-80453&lastparam=true | catalogue search excerpt | multiple folio ranges catalogued under Wittenberger Konkordie, dated 29 May 1536 |
| W350-07 | Amy Nelson Burnett, 'The Wittenberg Concord 1536' (2016) | https://doi.org/10.1080/14622459.2016.1157339 | article metadata and notes accessed | cites CR III 75–77 and BDS 6/1 120–132; reference correlation, not independent manuscript transcription |

## Findings, with explicit limits
1. **Date labels differ across materials.** MBW 1744 and manuscript catalogues assign **29 May 1536**. The digitally indexed heading of BDS 6/1 describes **28 May 1536**. It is not yet established here whether that represents text composition, meeting/drafting, a distinct documentary witness, or an editorial dating distinction. Preserve both with source labels; do not silently normalize to one date.
2. **Signers are witness-sensitive.** MBW 1744 includes Capito, Bucer, Frecht, Otter, Wolfhart, Musculus, Schuler, Bernhardi, German, Alber, Schradin; Luther, Jonas, Cruciger, Bugenhagen, Melanchthon, Menius, Myconius. Gotha Chart. B 28 specifically notes **Johannes Zwick as additional signatory**. Do not label every name an autograph on every extant copy; the Gotha record explicitly identifies a *copy*.
3. **Fragment completeness matters.** The Rörer witness Ms. Bos. q. 24b covers Communion; q. 24c covers Baptism/Absolution. A single fragment cannot establish the whole accord's wording or its global subscription list.
4. **Do not conflate editorship and autograph.** The catalogue's attribution of Melanchthon and designation 'Abschrift, Autograph Konrad Meusels' means the hand of the copyist Conrad Meusel is not Melanchthon's original autograph.
5. **Spurious metadata warning:** Gotha catalogue notes 'Datum der Vorlage: 1526' alongside an assigned 1536 date. Treat the anomalous 1526 entry as unresolved catalogue metadata, not historical proof that the 1536 accord was signed in 1526.
6. **Lexical carry-forward:** V3.49.1 directly established in the 1836 printing '29. Maii', 'cum pane et vino', 'vere et substantialiter', 'vere exhiberi', 'etiam indignis'. None of these is hereby confirmed through direct image-level reading of the 1536 manuscript. Label them **CR-1836 verified only**.

## Proposed cross-edition data contract
Each article quote/claim must carry: `claim_id`, `witness_id`, `source_type` (manuscript_image/manuscript_catalogue/critical_edition_image/edition_OCR/regest/modern_study), `folio_or_page`, `reading`, `normalization`, `date_as_given`, `certainty`, `verified_from_image`, `variant_group`, `editorial_note`. No automatic transfer of a verified reading to another witness.

## Next gated actions
- Obtain authorized facsimile images of Rörer Ms. Bos. q. 24b fol. 234v–235r and q. 24c fol. 290v–291r and document provenance/folios before transcription.
- Inspect BDS 6/1 pp. 120–132 images and introduction to resolve **28 versus 29 May** as a genuine documentary dating distinction, not merely OCR.
- Compare each signing list at the *same textual unit*; separate copy annotations from signatures of the 1536 participants.
- Only then collate the five V3.49.1 lexical anchors against actual manuscript images and produce diplomatic vs normalized transcriptions.
- Maintain DRAFT; scholarly and historical QA required before publication.

## QA
- [x] Scholarly regest / archival catalogue sources identified
- [x] Partial witness limits explicitly recorded
- [x] Variant/dating discrepancy quarantined
- [ ] Primary manuscript images directly inspected
- [ ] 1988 critical edition scan directly inspected
- [ ] Diplomatic transcription verified
- [ ] Publication approval

No merges, no public content changes.
