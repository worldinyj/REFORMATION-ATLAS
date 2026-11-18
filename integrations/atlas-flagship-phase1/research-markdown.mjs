function tokenizeInline(value) {
  const tokens=[];const pattern=/\*\*([^*\n]+)\*\*|\*([^*\n]+)\*/g;
  let last=0;let match;
  while((match=pattern.exec(value))!==null){
    if(match.index>last)tokens.push({kind:"text",text:value.slice(last,match.index)});
    tokens.push({kind:match[1]!==undefined?"strong":"em",text:match[1]??match[2]});
    last=pattern.lastIndex;
  }
  if(last<value.length)tokens.push({kind:"text",text:value.slice(last)});
  return tokens;
}
function parseResearchMarkdown(source) {
  return String(source??"").replace(/\r\n?/g,"\n").trim().split(/\n\s*\n/g).filter(Boolean).map(raw=>{
    const part=raw.trim();
    if(part==="---")return {kind:"rule",tag:"hr",segments:[]};
    const heading=part.match(/^(#{1,4})[ \t]+([^\n]+)$/);
    const text=heading?heading[2]:part.replace(/\n/g," ");
    return {kind:"block",tag:heading?"h"+heading[1].length:"p",segments:tokenizeInline(text)};
  });
}

export {parseResearchMarkdown};
