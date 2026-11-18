import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import ts from "typescript";

const jsx=await readFile(fileURLToPath(new URL("./AtlasFlagship1529Panel.jsx",import.meta.url)),"utf8");
const css=await readFile(fileURLToPath(new URL("./atlas-flagship.css",import.meta.url)),"utf8");

test("V4.53 candidate React JSX transpiles without syntactic errors",()=>{
 const out=ts.transpileModule(jsx,{
  fileName:"AtlasFlagship1529Panel.jsx",
  reportDiagnostics:true,
  compilerOptions:{jsx:ts.JsxEmit.ReactJSX,target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ESNext}
 });
 const errors=(out.diagnostics||[]).filter(x=>x.category===ts.DiagnosticCategory.Error);
 assert.deepEqual(errors.map(d=>ts.flattenDiagnosticMessageText(d.messageText," ")),[]);
 assert.ok(out.outputText.includes("jsx"));
});
test("React candidate exposes evidence and edition comparison from the original scene model",()=>{
 assert.match(jsx,/setShowEditionCompare/);
 assert.match(jsx,/integrity\.events\.filter\(e=>e\.year>1529\)/);
 assert.match(jsx,/1530·1531·1540년 판본 비교/);
 assert.match(jsx,/showEditionCompare/);
 assert.match(jsx,/sourceUrl/);
 assert.match(jsx,/role="tabpanel"/);
 assert.match(jsx,/onKeyDown=\{handleReadingKeyDown\}/);
 assert.match(jsx,/useId\(\)/);
});
test("React candidate never bypasses host access and release holds",()=>{
 assert.match(jsx,/privatePreviewGranted=false/);
 assert.match(jsx,/!privatePreviewGranted\|\|!integrity/);
 assert.match(jsx,/atlas\.meta\.canShip!==false/);
 assert.match(jsx,/scene\.contentGate\?\.canShip!==false/);
 assert.doesNotMatch(jsx,/dangerouslySetInnerHTML|\bfetch\s*\(|localStorage|sessionStorage/);
});
test("candidate CSS stays scoped, mobile and edition compare controls exist",()=>{
 assert.match(css,/\.atlas-fp-compare\{/);
 assert.match(css,/\.atlas-fp-tabs/);
 assert.match(css,/@media\(max-width:720px\)/);
 assert.doesNotMatch(css,/(^|\n)body\s*\{|(^|\n)button\s*\{/);
});
