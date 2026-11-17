// One shared subject vocabulary for every adapter and the saved library.
export const GTA_TOPICS = ['GTA VI','GTA V','GTA IV','GTA Online','San Andreas','Vice City','CJ','Big Smoke','Trevor','Wasted','Grove Street','FiveM','GTA III','GTA RP','Niko Bellic','Tommy Vercetti','Los Santos','Liberty City','Chinatown Wars'];
export const GTA_RE = /\b(?:gta\s*(?:[1-6]|vi|iv|v|iii)?|grand\s*theft\s*auto|gtavi|gtav|gtaiv|gtaonline|gtamemes|gta[ _-]?(?:iii|iv|vi|v|[1-6])|gta[ _-]?sa|gtarp|gta[ _-]?rp|chinatown[ _-]?wars|liberty[ _-]?city[ _-]?stories|vice[ _-]?city[ _-]?stories|san\s*andreas|sanandreas|vice\s*city|vicecity|grove\s*street|los\s*santos|liberty\s*city|leonida|fivem|carl\s*johnson|cj|big\s*smoke|trevor(?:\s*philips)?|tommy\s*vercetti|niko\s*bellic|franklin\s*clinton|michael\s*de\s*santa|lance\s*vance|ballas|wasted|ah\s*shit[,]?\s*here\s*we\s*go\s*again)\b|гта|гранд\s*тефт\s*авто|сиджей|биг\s*смоук|вайс\s*сити|сан[ -]*андреас|тревор|нико\s*беллик/i;
export function isGta(item) {
 const text=[item.title,item.description,item.body,item.text,...(item.tags||[])].filter(Boolean).join(' ');
 const community=/^(?:r\/|c\/)(?:gta\w*|grandtheftauto\w*|sanandreas|vicecity|fivem)(?:$|@)/i.test(item.path||'');
 return community || GTA_RE.test(text);
}
export function gtaQuery(q='') { const term=q.trim().replace(/^#/,''); return GTA_RE.test(term)?term:('GTA '+term).trim(); }
const GROUPS=[['GTA 6','GTA VI','GTAVI'],['GTA 5','GTA V','GTAV'],['GTA 4','GTA IV','GTAIV'],['GTA Online','GTAOnline'],['San Andreas','CJ','Big Smoke','Grove Street'],['Vice City','Tommy Vercetti'],['Trevor','Trevor Philips'],['Wasted','GTA wasted']];
export function gtaSearchTerms(q='',page=1) {
 if(!q.trim()) { const batches=[['GTA meme','GTA 6 meme','GTA Online meme','San Andreas meme','Vice City meme','GTA IV meme'],['CJ meme','Big Smoke meme','Trevor meme','Grove Street meme','FiveM meme','Wasted GTA'],['GTA V meme','Niko Bellic meme','Tommy Vercetti meme','Los Santos meme','Liberty City meme','GTA VI meme']]; return batches[(page-1)%batches.length]; }
 const clean=q.trim().replace(/^#/,'');
 const group=GROUPS.find(g=>g.some(t=>clean.toLowerCase().includes(t.toLowerCase())));
 const variants=group?group.map(t=>clean.replace(new RegExp(group.find(t=>clean.toLowerCase().includes(t.toLowerCase())).replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'i'),t)):[gtaQuery(clean)];
 return [...new Set([gtaQuery(clean),...variants])];
}
export const GTA_SEEDS = [
 {id:'gta-local-1',title:'GTA VI: me waiting for the next trailer',image:'assets/gta/meme-1.svg',tags:['GTA VI','GTA 6','Vice City']},
 {id:'gta-local-2',title:'CJ: Ah shit, here we go again',image:'assets/gta/meme-2.svg',tags:['CJ','San Andreas','Grove Street']},
 {id:'gta-local-3',title:'GTA Online: one peaceful drive',image:'assets/gta/meme-3.svg',tags:['GTA Online','GTA V','Wasted']},
 {id:'gta-local-4',title:'Big Smoke: I will have two number 9s',image:'assets/gta/meme-4.svg',tags:['Big Smoke','San Andreas']}
].map(item=>({...item,source:'original',kind:'image',thumb:item.image,body:item.title,text:item.title,url:item.image,site:'GTAXIOM',path:'Local originals',created:0,score:0,nsfw:false}));
