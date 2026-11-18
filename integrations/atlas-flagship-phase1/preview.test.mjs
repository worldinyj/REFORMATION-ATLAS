import test from "node:test";
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";

const path=fileURLToPath(new URL("./preview-1529-1540.html",import.meta.url));
const html=await readFile(path,"utf8");
const js=html.split("<script>")[1]?.split("</script>")[0];
const payload=html.split('id="data">')[1]?.split("</script>")[0];
assert.ok(js,"inline application script present");
assert.ok(payload,"embedded research data present");

class FakeElement {
 constructor(tag){this.tag=tag;this.children=[];this.attrs={};this.handlers={};this.textContent="";this.hidden=false;}
 append(...elements){this.children.push(...elements)}
 appendChild(element){this.children.push(element);return element}
 replaceChildren(...elements){this.children=[...elements]}
 setAttribute(key,value){this.attrs[key]=value}
 addEventListener(key,fn){this.handlers[key]=fn}
 click(){this.handlers.click?.()}
}
function runtime(){
 const nodes=new Map();
 const document={
  getElementById(id){if(!nodes.has(id))nodes.set(id,new FakeElement(id));return nodes.get(id)},
  createElement(tag){return new FakeElement(tag)}
 };
 document.getElementById("data").textContent=payload;
 new Function("document","URL",js)(document,URL);
 return {node:id=>document.getElementById(id),content:JSON.parse(payload)};
}

test("offline research preview includes four sourced events and no automatic exfiltration",()=>{
 const d=JSON.parse(payload);
 assert.equal(d.events.length,4);
 assert.equal(d.docs.length,2);
 assert.equal(d.canShip,false);
 assert.equal(d.sourceSha.length,3);
 assert.doesNotMatch(html,/<script\s+src=/i);
 assert.doesNotMatch(js,/\bfetch\s*\(|XMLHttpRequest|localStorage|sessionStorage|sendBeacon/);
 assert.doesNotMatch(js,/innerHTML/);
});
test("initial navigation shows 1529, complete L0 body and a linked source",()=>{
 const {node,content}=runtime();
 assert.equal(node("steps").children.length,4);
 assert.equal(node("eventTitle").textContent,content.events[0].title);
 assert.equal(node("steps").children[0].attrs["aria-current"],"step");
 assert.equal(node("reader").textContent,content.l0.text);
 assert.equal(node("docs").children.length,1);
 assert.ok(node("docs").children[0].children[2].href.startsWith("https://"));
});
test("event selection changes document cards, chapter text toggles and compare expands",()=>{
 const {node,content}=runtime();
 node("steps").children[3].click();
 assert.equal(node("eventTitle").textContent,content.events[3].title);
 assert.match(node("docs").children[0].children[2].href,/gruber/);
 node("l1").click();
 assert.equal(node("reader").textContent,content.l1.text);
 assert.equal(node("l1").attrs["aria-selected"],"true");
 node("compare").click();
 assert.equal(node("comparison").hidden,false);
 assert.equal(node("comparisonRows").children.length,3);
});
test("source panel can collapse and restart resets all panels to first reading",()=>{
 const {node,content}=runtime();
 node("steps").children[2].click();
 node("l1").click();
 node("compare").click();
 node("sourcesBtn").click();
 assert.equal(node("sources").hidden,true);
 node("restart").click();
 assert.equal(node("eventTitle").textContent,content.events[0].title);
 assert.equal(node("reader").textContent,content.l0.text);
 assert.equal(node("comparison").hidden,true);
 assert.equal(node("sources").hidden,false);
});
