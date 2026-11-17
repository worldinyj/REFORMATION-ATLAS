/**
 * REFORMATION ATLAS V4.29 - private preview read-only content adapter.
 *
 * NO network, no storage, no external libraries and no application mutations.
 * This module does NOT authorize public publishing.
 */
const VOL_IDS = Object.freeze(Array.from({ length: 8 }, (_, i) => "VOL-" + String(i + 1).padStart(2, "0")));
const THEME_IDS = Object.freeze(Array.from({ length: 6 }, (_, i) => "T415-" + String(i + 1).padStart(2, "0")));
const SAFE_BANNER = "내부 검토용 · 교회사·독자·권리 검증 미완료 · 공개 금지";

function ensure(condition, reason) {
  if (!condition) throw new Error("ATLAS_PRIVATE_STAGING_CONTRACT: " + reason);
}
function unique(items) { return new Set(items).size === items.length; }
function allowedRoute(path) {
  return typeof path === "string" && /^\/atlas-preview\/(?:volumes(?:\/VOL-0[1-8])?|themes(?:\/T415-0[1-6])?|read\/[1-6]|search)$/.test(path);
}

/** Throws unless data is self-consistent and restricted to private staging. */
export function validatePrivateAtlasPayload(pack) {
  ensure(pack && typeof pack === "object", "missing payload");
  ensure(pack.schema === "reformation-atlas-l0-private-stage-v1", "unexpected schema");
  ensure(pack.version === "V4.29", "unexpected version");
  ensure(pack.source?.version === "V4.23", "source version mismatch");
  ensure(pack.access?.environment === "PRIVATE_STAGING_ONLY", "must be private");
  ensure(pack.access?.can_ship === false && pack.access?.allow_public_indexing === false && pack.access?.allow_public_export === false, "publication or indexing must be disabled");
  ensure(pack.access?.requires_authentication === true, "private preview needs access control");
  ensure(pack.constraints?.editor_only_review_notes_included === false, "editor notes must not ship");
  const vols = pack.content?.volumes, themes = pack.content?.themes;
  const chapters = pack.content?.reading?.chapters;
  ensure(Array.isArray(vols) && vols.length === 8, "expected eight volume cards");
  ensure(Array.isArray(themes) && themes.length === 6, "expected six themes");
  ensure(Array.isArray(chapters) && chapters.length === 6, "expected six reader scenes");
  ensure(vols.every((v, i) => v.id === VOL_IDS[i] && v.order === i + 1 && typeof v.body_markdown === "string" && v.body_markdown.length > 250), "volume order or narrative missing");
  ensure(vols.every(v => allowedRoute(v.display?.route)), "unsafe volume route");
  ensure(vols.filter(v => v.type === "THEMATIC_INDEX").length === 1 && vols[7].type === "THEMATIC_INDEX" && vols.slice(0, 7).every(v => v.type === "HISTORY"), "VOL-08 must be the thematic index");
  ensure(themes.every((t, i) => t.id === THEME_IDS[i] && Array.isArray(t.anchors) && t.anchors.length === 7 && typeof t.body_markdown === "string" && t.body_markdown.length > 250), "missing theme or anchor");
  ensure(themes.every(t => allowedRoute(t.display?.route)), "unsafe thematic route");
  ensure(chapters.every((c, i) => c.order === i + 1 && c.route === "/atlas-preview/read/" + (i + 1) && c.body_markdown.length > 150), "reader order");
  const anchors = themes.flatMap(t => t.anchors.map(a => ({ ...a, theme_id: t.id })));
  ensure(anchors.length === 42 && unique(anchors.map(a => a.theme_id + "/" + a.volume_id)), "42 unique theme-history links required");
  ensure(anchors.every(a => VOL_IDS.slice(0, 7).includes(a.volume_id) && a.target_route === "/atlas-preview/volumes/" + a.volume_id && typeof a.label === "string"), "orphan or unsafe anchor");
  ensure(vols.every(v => typeof v.question === "string" && typeof v.summary === "string"), "volume summary missing");
  const readerText = chapters.map(x => x.body_markdown).join("\n");
  ensure(!/C417-\d+|SRC421-\d+|Q419-\d+|정답표/.test(readerText), "internal answer key visible");
  const bodyText = vols.map(v => v.body_markdown).concat(themes.map(t => t.body_markdown), chapters.map(c => c.body_markdown)).join("\n");
  ensure(!/!\[[^\]]*\]\([^)]+\)/.test(bodyText), "third-party inline media not permitted");
  return Object.freeze({ valid: true, volumes: vols.length, themes: themes.length, anchors: anchors.length, reader_scenes: chapters.length, can_ship: false });
}

export function createPrivateAtlasNavigator(pack) {
  const integrity = validatePrivateAtlasPayload(pack);
  const volumeMap = new Map(pack.content.volumes.map(v => [v.id, v]));
  const themeMap = new Map(pack.content.themes.map(t => [t.id, t]));
  const readerMap = new Map(pack.content.reading.chapters.map(c => [c.order, c]));
  const locked = () => Object.freeze({ banner: pack.access.render_banner || SAFE_BANNER, publication_allowed: false, indexable: false });

  /** An app-router adapter; paths are logical candidates, not actual deployed URLs. */
  function resolve(path) {
    if (!allowedRoute(path)) return null;
    if (path === pack.routes.volumes_index) return Object.freeze({ kind: "volume-index", volumes: pack.content.volumes, ...locked() });
    if (path === pack.routes.themes_index) return Object.freeze({ kind: "theme-index", themes: pack.content.themes, ...locked() });
    if (path === pack.routes.search) return Object.freeze({ kind: "search", ...locked() });
    const v = path.match(/^\/atlas-preview\/volumes\/(VOL-0[1-8])$/);
    if (v) return Object.freeze({ kind: "volume", item: volumeMap.get(v[1]), related_themes: pack.content.themes.filter(t => t.anchors.some(a => a.volume_id === v[1])), ...locked() });
    const t = path.match(/^\/atlas-preview\/themes\/(T415-0[1-6])$/);
    if (t) return Object.freeze({ kind: "theme", item: themeMap.get(t[1]), ...locked() });
    const c = path.match(/^\/atlas-preview\/read\/([1-6])$/);
    if (c) return Object.freeze({ kind: "reader", item: readerMap.get(Number(c[1])), all_chapters: readerMap.size, ...locked() });
    return null;
  }

  /** Search only the twenty frozen text units. No user query is logged or uploaded. */
  function search(query, limit = 30) {
    const term = String(query ?? "").trim().toLocaleLowerCase("ko");
    if (!term) return [];
    const units = [
      ...pack.content.volumes.map(v => ({ kind: "volume", id: v.id, title: v.title, summary: v.summary, content: v.body_markdown, route: v.display.route })),
      ...pack.content.themes.map(t => ({ kind: "theme", id: t.id, title: t.title, summary: t.question, content: t.body_markdown, route: t.display.route })),
      ...pack.content.reading.chapters.map(c => ({ kind: "reader", id: c.id, title: c.title, summary: pack.content.reading.title, content: c.body_markdown, route: c.route }))
    ];
    return units.filter(x => (x.title + " " + x.summary + " " + x.content).toLocaleLowerCase("ko").includes(term))
      .slice(0, Math.max(0, Math.min(30, Number(limit) || 30)))
      .map(({ content, ...record }) => Object.freeze(record));
  }

  return Object.freeze({ integrity, resolve, search, listVolumeIds: () => [...VOL_IDS], listThemeIds: () => [...THEME_IDS], release: locked });
}
