export const revealPercent=(top,height,viewport)=>Math.max(0,Math.min(100,100*(viewport*.9-top)/(height+viewport*.1)));

export function mountPurehive(){
 const page=document.querySelector('.purehive-case');if(!page)return;
 let off=document.documentElement.classList.contains('motion-off');
 const flow=page.querySelector('[data-ph-flow]'),range=flow.querySelector('input'),output=flow.querySelector('output'),colour=flow.querySelector('.ph-mark-colour'),replay=flow.querySelector('.ph-replay');
 let inView=false,manual=false,raf=0,play=0,start=0,playing=false,playbackDelay=0;
 const show=n=>{const value=Math.round(Math.max(0,Math.min(100,n)));range.value=String(value);output.value=`${value}%`;colour.style.setProperty('--ph-clip',`${100-value}%`);};
 const stop=()=>{cancelAnimationFrame(play);play=0;playing=false;start=0;replay.textContent='Replay the reveal';};
 const scroll=()=>{raf=0;if(off||manual||playing||!inView||document.hidden)return;const r=flow.getBoundingClientRect();show(revealPercent(r.top,r.height,innerHeight));};
 const schedule=()=>{if(!raf&&inView&&!off&&!manual&&!playing&&!document.hidden)raf=requestAnimationFrame(scroll);};
 const animate=t=>{if(off||!inView||document.hidden||!playing){stop();return;}if(!start)start=t+playbackDelay;const progress=Math.max(0,Math.min(1,(t-start)/2200));show(progress*100);if(progress<1)play=requestAnimationFrame(animate);else stop();};
 range.addEventListener('input',()=>{manual=true;stop();show(Number(range.value));});
 replay.addEventListener('click',()=>{if(playing){stop();return;}const art=flow.querySelector('.ph-flow-art'),bounds=art.getBoundingClientRect();playbackDelay=bounds.top<80||bounds.bottom>innerHeight-70?350:0;if(playbackDelay)art.scrollIntoView({behavior:'smooth',block:'center'});manual=true;playing=true;start=0;replay.textContent='Pause the reveal';play=requestAnimationFrame(animate);});
 const reveals=[...page.querySelectorAll('.ph-reveal')];
 if('IntersectionObserver'in window){
  new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(!inView)stop();schedule();},{rootMargin:'80px'}).observe(flow);
  const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-arrived');observer.unobserve(e.target);}}),{threshold:.1});
  if(!off)reveals.forEach(el=>{el.classList.add('is-waiting');observer.observe(el);});
 }
 addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
 document.addEventListener('portfolio:motion',e=>{off=e.detail.off;stop();replay.disabled=off;if(off){show(100);reveals.forEach(el=>el.classList.add('is-arrived'));}else{manual=false;schedule();}});
 document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();cancelAnimationFrame(raf);raf=0;}else schedule();});
 addEventListener('pagehide',()=>{stop();cancelAnimationFrame(raf);},{once:true});replay.disabled=off;show(100);
 const choices=[...page.querySelectorAll('[data-ph-scene-select]')],frames=[...page.querySelectorAll('[data-ph-scene]')];
 choices.forEach(button=>button.addEventListener('click',()=>{choices.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));frames.forEach(f=>f.hidden=f.dataset.phScene!==button.dataset.phSceneSelect);page.querySelector('.ph-scene-status').textContent=`${button.textContent} scene selected`; }));
}
