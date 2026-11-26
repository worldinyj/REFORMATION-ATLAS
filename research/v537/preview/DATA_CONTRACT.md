# ATLAS preview data contract v1.0.0

Status: RESEARCH PREVIEW ONLY. All release flags must remain false.

| Root field | Meaning / rule |
|---|---|
| volumes | 8 records; id, title, subtitle, intro, outro, chapter_ids, map_asset_id, kind |
| chapters | 24 records; stable id, volume_id, title, period; overview.text, intermediate.text, deep.markdown; transition.next_chapter_id |
| cases | 52 records; case_id, chapter_id, period, region, locations, interpretation_limit; null coordinate is intentional |
| points | GeoJSON FeatureCollection; 36 points; coordinates are longitude, latitude |
| people | 10 records; symbol_asset_id always resolves; portrait_asset_id null, use symbolic card |
| theology.units / global_units | 5 / 6 records; home and related chapter IDs; keep boundary/limit/source_scope visible |
| assets | 23 records; id, source_path, preview_path, blob_sha, media_type, status |
| timeline | asset_id and comparative rows, not a proportional chronology |
| review_holds | outstanding validation requirements |
| provenance | source path and Git blob SHA |

Asset resolution: join asset ID to assets[].id, then read preview_path relative to package root. Never use source_path as a public web URL. The builder copies only manifest-listed SVGs and verifies Git blob SHA; no pending WebP files are included.

Render Markdown using a sanitizing renderer; do not execute embedded HTML, external scripts, or untrusted links. Preserve text, evidence limitations, and source attribution. Treat period strings as display labels, not sortable dates. The final volume is thematic. Modern coastline and approximate locations are not historical borders or exact itineraries.

No schema migration to the production app is authorized. Unknown optional fields may be ignored, but all release flags, evidence limitations, source links and asset disclosures must be preserved. This contract is a written field specification plus builder assertions; it is not a complete JSON Schema.
