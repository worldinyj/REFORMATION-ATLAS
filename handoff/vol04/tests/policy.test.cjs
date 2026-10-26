const test = require('node:test');
const assert = require('node:assert/strict');
const { validatedPublicPayload } = require('../.policy-build/editionPolicy.js');
const { getApprovedDocumentEdition } = require('../.policy-build/approvedEditions.js');
const documentId = 'OV-D-011';
function good() { return {
  workId: documentId, releaseManifestRef: 'approved-release-fixture', editorialApprovalRef: 'editor-fixture',
  releaseApproved: true, workApproved: true, sourceEvidenceApproved: true, rightsApproved: true,
  editions: [{ id: 'EDN-V04-9999', label:'test-only edition', yearLabel:'1540', language:'la',
    materialKind:'print', approved:true, publicationApproved:true }],
  comparisons: [{ id:'COM-V04-9999', kind:'structure', observationKo:'fixture observation',
    sourceLabels:['fixture cited source'], approved:true, publicationApproved:true,
    textCollated:false, mediaRightsApproved:false }]
}; }
test('production input remains empty', () => {
  assert.equal(getApprovedDocumentEdition(documentId), null);
  assert.equal(validatedPublicPayload(getApprovedDocumentEdition(documentId), documentId), null);
});
test('synthetic reviewed fixture passes shape only, not release authentication', () => {
  assert.ok(validatedPublicPayload(good(), documentId));
});
test('reject mismatched work, missing manifest, draft edition, and fake canonical identifier', () => {
  const mutations = [
    p => p.workId = 'OV-D-012', p => p.releaseManifestRef = '',
    p => p.editions[0].approved = false, p => p.editions[0].id = 'EDN-CANDIDATE',
    p => p.comparisons[0].sourceLabels = [], p => p.sourceEvidenceApproved = false,
    p => p.comparisons[0].id = 'WRONG', p => p.releaseApproved = false,
    p => p.rightsApproved = false,
  ];
  mutations.forEach(m => { const p = good(); m(p); assert.equal(validatedPublicPayload(p, documentId), null); });
});
test('reject wording comparison without original collation', () => {
  const p = good(); p.comparisons[0].kind='textual_wording';
  assert.equal(validatedPublicPayload(p, documentId), null);
  p.comparisons[0].textCollated = true;
  assert.ok(validatedPublicPayload(p, documentId));
});
test('reject iconography without rights approval', () => {
  const p = good(); p.comparisons[0].kind='iconography';
  assert.equal(validatedPublicPayload(p, documentId), null);
  p.comparisons[0].mediaRightsApproved = true;
  assert.ok(validatedPublicPayload(p, documentId));
});
test('reject duplicates and empty edition list', () => {
  const p = good(); p.editions.push({...p.editions[0]});
  assert.equal(validatedPublicPayload(p, documentId), null);
  const q = good(); q.editions = [];
  assert.equal(validatedPublicPayload(q, documentId), null);
});
