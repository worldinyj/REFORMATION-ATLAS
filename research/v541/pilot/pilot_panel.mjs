export function resolvePilot({pack,hostNamespace,kind,hostRecord,reviewEnabled=false}={}){
 if(reviewEnabled!==true||hostNamespace!=="ATLAS_OVERVIEW_V01"||pack?.namespace!==hostNamespace||pack?.mode!=="research_preview_only"||["can_ship","can_import_ai_studio","can_merge_main"].some(k=>pack[k]!==false))return null;
 if(pack.chapter?.id!=="L448-04-02"||!Array.isArray(pack.targets)||!Array.isArray(pack.cases)||!Array.isArray(pack.theology?.units)||!Array.isArray(pack.assets)||!hostRecord)return null;
 const target=pack.targets.find(t=>t.id===hostRecord.id&&t.kind===kind&&t.label===hostRecord.title);
 if(!target||!Array.isArray(target.case_ids)||!target.case_ids.every(id=>pack.cases.some(c=>c.case_id===id)))return null;
 return JSON.parse(JSON.stringify({target,chapter:pack.chapter,cases:pack.cases.filter(c=>target.case_ids.includes(c.case_id)),theology:pack.theology,assets:pack.assets,notice:pack.notice_ko,review_holds:pack.review_holds,can_ship:false}));
}

export function safeSource(url){return typeof url==="string"&&/^https:\/\/[a-z0-9.-]+(?::[0-9]+)?(?:[/?#][^\s<>"'\\]*)?$/i.test(url);}

export function mountPilot(container,options={}){
 if(!container||!container.ownerDocument||typeof container.appendChild!=="function")throw Error("A dedicated mount element is required");
 const model=resolvePilot(options);
 if(!model)return {status:"DISABLED",destroy(){}};
 const doc=container.ownerDocument,root=doc.createElement("section");root.setAttribute("aria-label","종교개혁 연구용 심화 읽기");root.className="atlas-pilot-v541";
 function add(p,tag,text){const e=doc.createElement(tag);if(text!==undefined)e.textContent=String(text);p.appendChild(e);return e;}
 function paragraphs(p,text){for(const x of String(text||"").split(/\n\s*\n/)){if(x.trim())add(p,"p",x);}}
 function references(p,links){const valid=[...new Set(links.filter(safeSource))];if(!valid.length)return;const details=add(p,"details");add(details,"summary","참고 자료 ("+valid.length+")");const ul=add(details,"ul");for(const url of valid){const a=add(add(ul,"li"),"a",url);a.href=url;a.rel="noopener noreferrer";}}
 add(root,"p",model.notice);add(root,"h2",model.chapter.title);add(root,"p",model.chapter.period);
 const tabs=add(root,"div");tabs.setAttribute("role","group");tabs.setAttribute("aria-label","읽기 깊이");const body=add(root,"div");
 const labels=[["overview","개요"],["intermediate","중간 해설"],["deep","심층 연구"]];const buttons=[];
 function render(level){body.replaceChildren();for(const b of buttons)b.setAttribute("aria-pressed",String(b.dataset.level===level));if(level==="overview"){paragraphs(body,model.chapter.overview.text);add(body,"p",model.chapter.overview.question);}else if(level==="intermediate"){add(body,"h3",model.chapter.intermediate.title);paragraphs(body,model.chapter.intermediate.text);add(body,"p",model.chapter.intermediate.question);for(const e of model.chapter.intermediate.evidence_ladder||[]){add(body,"h4",e.level||e.kind);paragraphs(body,e.claim);paragraphs(body,e.limit);}references(body,model.chapter.intermediate.supplemental_urls||[]);}else{paragraphs(body,model.chapter.deep.markdown);references(body,model.chapter.deep.source_urls||[]);}}
 for(const [level,label] of labels){const b=add(tabs,"button",label);b.type="button";b.dataset.level=level;b.addEventListener("click",()=>render(level));buttons.push(b);}
 render("overview");
 add(root,"h3","연결된 역사 사례");for(const c of model.cases){const box=add(root,"article");add(box,"h4",c.label);add(box,"p",c.period+" · "+c.region);add(box,"p",c.primary_evidence_genre);add(box,"p",c.interpretation_limit);}
 const theology=add(root,"details");add(theology,"summary","신학 비교 해설 ("+model.theology.units.length+")");for(const u of model.theology.units){add(theology,"h4",u.title);paragraphs(theology,u.body);add(theology,"p",u.boundary);add(theology,"p",u.source_scope);references(theology,(u.refs||[]).map(([k])=>model.theology.sources[k]?.url).filter(Boolean));}
 const figure=add(root,"figure");const asset=model.assets.find(a=>a.id==="asset:augsburg.svg");const path=options.diagramPath;
 // Host must supply its own relative asset route. Reject external, traversal, query, fragment and non-SVG paths.
 if(asset&&typeof path==="string"&&/^(?:\/)?(?:[A-Za-z0-9_-]+\/)*augsburg\.svg$/.test(path)){const img=add(figure,"img");img.alt=asset.caption;img.src=path;img.addEventListener("error",()=>{img.remove();add(figure,"p","문헌 도해를 불러오지 못했습니다. 아래 설명을 참조하세요.");},{once:true});}else add(figure,"p","문헌 도해 경로 미확정 — 텍스트 설명 제공");
 if(asset)add(figure,"figcaption",asset.caption);
 const holds=add(root,"details");add(holds,"summary","연구 검토 및 적용 제한");const ul=add(holds,"ul");for(const h of model.review_holds)add(ul,"li",h);
 container.appendChild(root);
 return {status:"REVIEW_PANEL_MOUNTED",destroy(){root.remove();}};
}
