/* REFORMATION ATLAS V1.66 - pure read-only, fail-closed adapter.
 * Consumes imported JSON objects; never fetches or changes application state.
 */
export const CONTRACT_VERSION = "1.66";
export function buildAtlasPreview({manifest, narratives, cities, geoLinks, editions, evidence, navigation}) {
  if (!manifest || manifest.publication_gate?.can_ship !== false) throw Error("Missing research hold");
  const pages = narratives?.pages ?? [];
  const places = cities?.places ?? [];
  const links = geoLinks?.links ?? [];
  const works = editions?.works ?? [];
  const claims = evidence?.cards ?? [];
  const paths = navigation?.claims ?? [];
  const pageIds = new Set(pages.map(x => x.id));
  const placeIds = new Set(places.map(x => x.id));
  const editionIds = new Set(works.flatMap(x => x.editions.map(e=>e.id)));
  const evidenceIds = new Set(claims.map(x=>x.id));
  if (pages.length !== 10 || places.length !== 11 || claims.length !== 8) throw Error("Incomplete source dataset");
  if (!links.every(x=>pageIds.has(x.reader_page_id) && placeIds.has(x.place_id))) throw Error("Invalid map linkage");
  if (!paths.every(x=>evidenceIds.has(x.claim_id) && pageIds.has(x.reader_page_id) && x.edition_ids.every(id=>editionIds.has(id)))) throw Error("Invalid evidence linkage");
  return Object.freeze({
    contractVersion:CONTRACT_VERSION,
    mode:"RESEARCH_PREVIEW_ONLY",
    canPublish:false,
    readerCards:pages.map(p=>({id:p.id,title:p.title,period:p.period,sections:p.segments.map(s=>({heading:s.heading,text:s.text})),sourceUrls:[...p.source_urls],isVerifiedPrimary:false})),
    mapPins:places.map(x=>({id:x.id,name:x.name,lat:x.lat,lon:x.lon,accuracy:"CITY_APPROXIMATE",pageId:x.reader_page_id})),
    datedLinks:links.map(x=>({pageId:x.reader_page_id,placeId:x.place_id,period:x.period,relation:x.relation})),
    editionCards:works.flatMap(w=>w.editions.map(e=>({editionId:e.id,workId:w.work_id,title:w.title_ko,year:e.year,kind:e.kind,language:[...e.language],canPublishImage:false}))),
    claimCards:paths.map(p=>({id:p.claim_id,editionIds:[...p.edition_ids],readerPageId:p.reader_page_id,evidenceLevel:claims.find(x=>x.id===p.claim_id)?.proof_level??"UNKNOWN",originalVerified:false})),
    mediaPolicy:"NO_IMAGE_EMBEDDING"
  });
}
