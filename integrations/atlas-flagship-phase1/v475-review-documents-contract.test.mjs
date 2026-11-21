import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
const read=path=>readFile(fileURLToPath(new URL(path,import.meta.url)),"utf8");
const html=await read("./V475_READER_PILOT_WORKSHEET.html");
const bundle=JSON.parse(await read("../../research/data/ATLAS_V475_CROSS_VOLUME_REVIEW_BUNDLE.json"));
const dossier=await read("./V475_HISTORIAN_SOURCE_REVIEW_DOSSIER_KO.md");
const spec=await read("./V475_CROSS_VOLUME_CONTENT_REVIEW_STANDARD_KO.md");
test("Print-ready participant page contains all nine questions and choices, zero answer keys",()=>{
 assert.equal((html.match(/class="question"/g)||[]).length,9);
 assert.equal((html.match(/class="task"/g)||[]).length,3);
 for(const q of bundle.participant.questions){
  assert.match(html,new RegExp('id="'+q.id+'"'));
  for(const c of q.choices) assert.ok(html.includes('name="'+q.id+'" value="'+c.id+'"'));
 }
 assert.ok(html.includes("여러 사료 카드"));
 assert.doesNotMatch(html,/"answerKey"|data-correct|정답은\s*[A-D]/);
});
test("HTML is offline, print-accessible, no submissions, scripts, tracking or personal detail requests",()=>{
 assert.match(html,/<html lang="ko">/);
 assert.match(html,/@page\{size:A4/);
 assert.match(html,/<fieldset class="question"/);
 assert.doesNotMatch(html,/<script|onload=|onsubmit=|fetch\(|XMLHttpRequest|localStorage|sessionStorage|form action=|navigator\.sendBeacon|mailto:/i);
 assert.match(html,/응답.*저장하거나 전송하지 않습니다/);
 assert.match(html,/이름·이메일·로그인 정보·종교적 신념·의료 정보를 적지 마세요/);
});
test("Historian dossier links all 14 claims, explicitly distinguishes original/print/translation and no actual approvals",()=>{
 assert.equal((dossier.match(/\| V457-C\d{2} \|/g)||[]).length,14);
 assert.match(dossier,/고위험 \*\*10건\*\*/);
 assert.match(dossier,/W2119 인쇄본/);
 assert.match(dossier,/K·Z/);
 assert.match(dossier,/실제 요청 발송 0건/);
 for(const id of bundle.sources.map(s=>s.id))assert.ok(dossier.includes("["+id+"]"));
});
test("Cross-volume standard defines 9 meaningful schema stages and no automatic production promotion",()=>{
 for(const term of ["신원","L0","L1","시간","사료","이본","전문가","독자","출시"])assert.ok(spec.includes(term));
 assert.match(spec,/실제 전문가 검토/);
 assert.match(spec,/can_ship=false/);
});
test("Bundled reviewer source remains research-only, not a fictitious pilot or signature",()=>{
 assert.equal(bundle.expertReview.reviewersEngaged,0);
 assert.equal(bundle.participant.actualParticipants,0);
 assert.equal(bundle.participant.actualSessions,0);
 assert.equal(bundle.privacy.blindPilotClaimPermitted,false);
 assert.equal(bundle.releaseGate.canShip,false);
});
