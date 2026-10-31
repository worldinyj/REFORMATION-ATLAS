export function safeText(value) {
 return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}
export function filterCards(cards, query) {
 const q=String(query ?? '').trim().toLocaleLowerCase('ko');
 return cards.filter(item => [item.heading,item.sub,item.body].join(' ').toLocaleLowerCase('ko').includes(q));
}
export function resultMessage(count) {
 return count ? count+'개 자료 표시' : '검색 결과가 없습니다. 다른 검색어를 입력해 주세요.';
}
export async function loadJson(fetcher,url) {
 const response=await fetcher(url);
 if(!response.ok) throw Error('JSON loading failed: '+url+' ('+response.status+')');
 return response.json();
}
