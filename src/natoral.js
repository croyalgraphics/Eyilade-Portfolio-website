export const rangeState=(range,view)=>({range:['body','hair','baby','active'].includes(range)?range:'body',view:view==='artwork'?'artwork':'photo'});

export function mountNatoral(){
 const page=document.querySelector('.natoral-case');if(!page)return;
 const browser=page.querySelector('[data-nt-range-browser]'),rangeButtons=[...browser.querySelectorAll('[data-nt-range-select]')],viewButtons=[...browser.querySelectorAll('[data-nt-view-select]')],frames=[...browser.querySelectorAll('[data-nt-range]')];
 let state=rangeState('body','photo');
 const render=()=>{rangeButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ntRangeSelect===state.range)));viewButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ntViewSelect===state.view)));frames.forEach(f=>{f.hidden=f.dataset.ntRange!==state.range;f.querySelectorAll('[data-nt-view]').forEach(v=>v.hidden=v.dataset.ntView!==state.view);});browser.querySelector('.nt-range-status').textContent=`${rangeButtons.find(b=>b.dataset.ntRangeSelect===state.range).textContent} · ${state.view==='photo'?'Photography':'Face artwork'} view`;};
 rangeButtons.forEach(b=>b.addEventListener('click',()=>{state=rangeState(b.dataset.ntRangeSelect,state.view);render();}));
 viewButtons.forEach(b=>b.addEventListener('click',()=>{state=rangeState(state.range,b.dataset.ntViewSelect);render();}));
 let off=document.documentElement.classList.contains('motion-off'),inView=false,raf=0;
 const mark=page.querySelector('.nt-mark-story'),image=mark.querySelector('.nt-mark-art');
 const showMark=()=>{raf=0;if(off||!inView||document.hidden){image.style.setProperty('--nt-scale','1');return;}const r=mark.getBoundingClientRect(),p=Math.max(0,Math.min(1,(innerHeight-r.top)/(innerHeight+r.height)));image.style.setProperty('--nt-scale',String(.88+p*.12));};
 const schedule=()=>{if(!raf&&inView&&!document.hidden)raf=requestAnimationFrame(showMark);};
 const reveals=[...page.querySelectorAll('.nt-reveal')];
 if('IntersectionObserver'in window){
  new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{rootMargin:'40px'}).observe(mark);
  const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-arrived');observer.unobserve(e.target);}}),{threshold:.1});
  if(!off)reveals.forEach(el=>{el.classList.add('is-waiting');observer.observe(el);});
 }
 addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
 document.addEventListener('portfolio:motion',e=>{off=e.detail.off;if(off){image.style.setProperty('--nt-scale','1');reveals.forEach(el=>el.classList.add('is-arrived'));}else schedule();});
 document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;}else schedule();});
 addEventListener('pagehide',()=>cancelAnimationFrame(raf),{once:true});render();
}
