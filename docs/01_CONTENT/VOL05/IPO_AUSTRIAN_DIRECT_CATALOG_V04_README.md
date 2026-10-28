# VOL05 IPO/IPM Austrian direct catalogs V0.4 — Research review handoff

Branch: research/vol05-ipo-austria-direct-catalog-v04. **DRAFT_RESEARCH_NOT_PUBLIC**. Google AI Studio and main unchanged.

## Verified at institution-catalog level

The Austrian State Archive's publicly accessible individual pages, not just Spanish PARES secondary cross references, distinguish:
- IPO imperial copy (ID **2594303**, catalog date October 14 old style, 41 seals, 117 image-index entries, **Kaiserliches Exemplar**).
- IPO Mainz copy (ID **2594304**, catalog date October 24 new style, 35 seals, 79 image-index entries, **Mainzer Exemplar**).
- IPM Mainz copy (ID **2594302**, catalog date October 24, 34 seals, 51 image-index entries, **Mainzer Exemplar**).

All pages give the shared date-series label **AT-OeStA/HHStA UR AUR 1648 X 14/24**. Thus the shared label is *not* a unique individual-copy identifier. The separate public item IDs and differences in seal count and item-index count support distinct catalog objects. The number of image-index entries is NOT a count of physical sheets or folios.

All three detailed record pages were directly accessed and read as catalogs. Their image link numbers are visible, but image pixel data could not be retrieved for source-text reading, so **original manuscript folio/Latin text collation remains false**. The publicly listed access status does not establish online picture republication rights.

## Related IDs, not merged by assumption

Older Austrian record IDs in Spanish PARES (**IPO 393786**, **IPM 1252067**) and LWL que2599/2595 require object-identity reconciliation. A similar title does not guarantee a one-to-one mapping to Austrian ID 2594303 or 2594304.

APW Antje Oschmann 1998 III B 1/1, pp.95–170 is a separate edited book. The secondary scholarly citations of IPO V §34 on p.121 and IPO VII §1 on p.129 have been cross-checked in search excerpts (a 2009 study and a 2022 Christian Witt work plus an EKD source). **The APW book's actual pages remain unread**, hence scholarly page leads cannot be promoted to verified critical-edition collation.

## Artifacts and evidence gates

- docs/01_CONTENT/VOL05/IPO_AUSTRIAN_DIRECT_CATALOG_AUDIT_V04.md — Korean history report and explicit observation boundaries.
- data/deep/vol05_ipo_direct_austrian_catalog_v04.json — exact catalog copies, 4 unresolved older-ID crosslinks, 2 secondary scholarly page leads.
- scripts/validate_vol05_ipo_austria_direct_catalog_v04.py — preserve copies, count/party/date distinctions, scholarly evidence and public=false.
- scripts/test_vol05_ipo_austria_catalog_negative_v04.py — 33 hypothetical incorrect modifications must fail.
- .github/workflows/vol05-ipo-austria-catalog-qa.yml — run prior V0.3 and new V0.4 QA.

## Next precise research steps

(1) Access image **bytes** for the two Austrian IPO records, carefully inspect which frame shows each IPO clause, and register image index ↔ manuscript folio. (2) Directly open APW pp.121 and 129 and compare with their independently identified 1648 manuscript leaves. (3) Establish physical object identity through archive entry codes, seals, archival history rather than titles. (4) Obtain licenses for public use of photographed documents. Only after scholarly and editorial review create a separate publication-ready data snapshot; do not import this research JSON into the parallel AI Studio app yet.
