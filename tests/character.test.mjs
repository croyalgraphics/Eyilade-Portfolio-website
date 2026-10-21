import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';
const source=(await readFile(new URL('../src/character.js',import.meta.url),'utf8')).replace(/^import character[^\n]*\n/,'').replaceAll('export function ','function ');
const character=JSON.parse(await readFile(new URL('../content/character.json',import.meta.url)));
function fixture(){
 let time=0,next=0,intersection;const timers=new Map(),listeners=new Map();
 const classes=()=>{const set=new Set();return {add:c=>set.add(c),remove:c=>set.delete(c),contains:c=>set.has(c),toggle(c,value){value?set.add(c):set.delete(c);}};};
 const actor={addEventListener:(name,fn)=>listeners.set('actor:'+name,fn)};
 const poster={attrs:new Map([['srcset','idle responsive']]),getAttribute(n){return this.attrs.get(n);},setAttribute(n,v){this.attrs.set(n,v);},removeAttribute(n){this.attrs.delete(n);},addEventListener(){}};
 const canvas={getContext:()=>({clearRect(){},drawImage(){}})};const note={},status={};
 const root={classList:classes()};const host={dataset:{characterState:'idle'},classList:classes(),querySelector:q=>({'.illustration-button':actor,'.character-poster':poster,canvas,'.hello-note':note,'.hello-status':status})[q]};
 const document={documentElement:root,readyState:'complete',hidden:false,querySelector:q=>q==='.hero-figure'?host:null,addEventListener:(n,f)=>listeners.set(n,f)};
 const context={character,document,window:{IntersectionObserver:true},IntersectionObserver:class{constructor(fn){intersection=fn;}observe(){}},Image:class{set src(value){this.value=value;queueMicrotask(()=>this.onload());}},Math:{random:()=>0,floor:Math.floor},setTimeout(fn,delay){const id=++next;timers.set(id,{fn,at:time+delay});return id;},clearTimeout:id=>timers.delete(id),addEventListener:(n,f)=>listeners.set(n,f)};
 vm.runInNewContext(source+';mountHeroCharacter();',context);
 const settle=async()=>{for(let i=0;i<5;i++)await Promise.resolve();};
 async function advance(ms){const end=time+ms;for(let guard=0;guard<1000;guard++){const due=[...timers].filter(([,v])=>v.at<=end).sort((a,b)=>a[1].at-b[1].at)[0];if(!due)break;time=due[1].at;timers.delete(due[0]);due[1].fn();await settle();}time=end;await settle();}
 return {host,root,document,note,status,timers,async visible(value){intersection([{isIntersecting:value}]);await settle();},async click(){listeners.get('actor:click')();await settle();},async motion(value){root.classList.toggle('motion-off',value);listeners.get('portfolio:motion')();await settle();},async visibility(value){document.hidden=value;listeners.get('visibilitychange')();await settle();},advance};
}
test('accepted clicks alternate thumbs up then wave; rapid clicks do not overlap or consume the sequence',async()=>{const f=fixture();await f.visible(true);assert.equal(f.host.dataset.characterState,'idle');await f.click();assert.equal(f.host.dataset.characterState,'thumbs-up');await f.click();assert.equal(f.host.dataset.characterState,'thumbs-up');await f.advance(2400);assert.equal(f.host.dataset.characterState,'idle');await f.click();assert.equal(f.host.dataset.characterState,'wave');await f.advance(2000);assert.equal(f.host.dataset.characterState,'idle');assert.equal(f.note.textContent,'');});
test('automatic thinking is idle-only, shows a thought, and yields immediately to the user',async()=>{const f=fixture();await f.visible(true);await f.advance(14000);assert.equal(f.host.dataset.characterState,'thinking');assert.equal(f.note.textContent,'What if…');assert.equal(f.status.textContent,'');await f.click();assert.equal(f.host.dataset.characterState,'thumbs-up');assert.equal(f.status.textContent,'That’s a good idea.');await f.advance(2400);assert.equal(f.host.dataset.characterState,'idle');});
test('offscreen and hidden pages suspend timers; reduced motion uses still reactions',async()=>{const f=fixture();await f.visible(true);await f.visible(false);assert.equal(f.timers.size,0);await f.advance(40000);assert.equal(f.host.dataset.characterState,'idle');await f.visible(true);await f.visibility(true);assert.equal(f.timers.size,0);await f.visibility(false);await f.motion(true);assert.equal(f.timers.size,0);await f.click();assert.equal(f.host.dataset.characterState,'thumbs-up');assert.equal(f.host.dataset.characterPlaying,'false');await f.advance(1800);assert.equal(f.host.dataset.characterState,'idle');assert.equal(f.timers.size,0);});
