# ATLAS V4.84 — Volume VIII integration gate and claim provenance

Date: 2026-11-21
Status: RESEARCH_DRAFT
can_ship: false

## Scope
V4.83 Volume VIII research draft: "Scripture and Authority" (A1-A7) and "State, Conflict and Coexistence" (B1-B8). Plan to connect to V4.82 "Translation and Local Reception" (10 reported sections).

**Important**: V4.82 full source and final research branch could not be verified in this session. This file is not a completed merge, does not replace the master Volume VIII, and must not be promoted to the production app.

## Historical editorial decisions
- C-V484-001 [supported] Augsburg Confession, Article XXVIII (1530), distinguishes ecclesiastical and temporal authority. It does not amount to a modern separation of church and state.
- C-V484-002 [supported] The 1530 confession and the 1555 Religious Peace of Augsburg are distinct events and documents.
- C-V484-003 [supported] 1555 regulates peace between Catholic estates and estates adhering to the Augsburg Confession, not universal freedom of religion.
- C-V484-004 [supported_interpretive] Legal coexistence in 1555 must not be equated with modern universal individual religious freedom.
- C-V484-005 [supported] The 1648 settlement included the Reformed in the imperial settlement.
- C-V484-006 [supported] The 1648 settlement uses 1624 as a normative year for several religious property and exercise provisions, subject to specifics and exceptions.
- C-V484-007 [reject] "1648 instantly created the modern sovereign state system."
- C-V484-008 [hold] The exact bibliographical relationship of the 1715 Tamil New Testament printing and 1719 records remains to be settled from witness-level source work.
- C-V484-009 [review] Local agency in global translation needs additional anchored case evidence, not an assertion of one-way European transmission.

## Sources reviewed
- S1530: https://thebookofconcord.org/augsburg-confession-single-page/
- S1555: https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/ghdi%3Adocument-4386
- S1648: https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/peace-treaties-of-westphalia-october-14-24-1648

These are online text/translated-primary readings. Original printed witnesses and all edition-level claims are NOT marked as visually collated.

## Navigation contract proposal
P01: Scripture authority -> public confession (A2, A3, B2)
P02: Confession -> imperial religious law (B2, B3)
P03: Limited imperial coexistence -> 1648 religious settlement (B3, B5, B6)
P04: Print -> multilingual translation and local reception (A5, A6)
P05: Local reception -> global Christianity and colonial asymmetries (A6, B7)

## Blocking gates
- Recover V4.82 exact source, path, SHA before actual merging; perform duplicate/content-ID audit.
- Separate 1530 presented confession, 1531 printed edition, and 1540 Variata.
- Resolve Tamil 1715 / 1719 bibliographic questions from original witnesses and library correspondence.
- Complete human historical editorial review, reader testing, content contract and app integration validations.
- Keep can_ship=false and do NOT update main, production app, or master Volume VIII.

Companion research artifacts created within the 2026-11-21 chat:
REFORMATION_ATLAS_V484_제8권_통합검토_연구본.md
REFORMATION_ATLAS_V484_제8권_연결계약.json
These local deliverables are NOT represented as committed copies by this tracker.
