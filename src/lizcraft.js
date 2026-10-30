export const contourLevel=(top,height,viewport)=>Math.max(1,Math.min(8,Math.ceil(8*(viewport*.9-top)/(height+viewport*.15))));

export function mountLizcraft(){
 const page=document.querySelector('.lizcraft-case');if(!page)return;
 let off=document.documentElement.classList.contains('motion-off');
 const thread=page.querySelector('[data-liz-thread]'),rings=[...thread.querySelectorAll('.lc-contour-ring')].reverse(),range=thread.querySelector('input'),count=thread.querySelector('output'),replay=thread.querySelector('.lc-replay');
 let manual=false,inView=false,scrollFrame=0,playFrame=0,playing=false,started=0,playbackDelay=0;
 function show(n){n=Math.max(1,Math.min(rings.length,n));rings.forEach((p,i)=>p.style.opacity=i<n?'1':'.08');range.value=String(n);count.value=`${n} of ${rings.length}`;}
 function cancelPlay(){cancelAnimationFrame(playFrame);playFrame=0;playing=false;started=0;replay.textContent='Replay the unfolding';}
 function updateScroll(){scrollFrame=0;if(off||manual||playing||!inView||document.hidden)return;const r=thread.getBoundingClientRect();show(contourLevel(r.top,r.height,innerHeight));}
 function schedule(){if(!scrollFrame&&inView&&!off&&!manual&&!playing&&!document.hidden)scrollFrame=requestAnimationFrame(updateScroll);}
 function animate(time){if(!playing||off||!inView||document.hidden){cancelPlay();return;}if(!started)started=time+playbackDelay;const progress=Math.max(0,Math.min(1,(time-started)/2300));show(1+Math.floor(progress*7));if(progress<1)playFrame=requestAnimationFrame(animate);else cancelPlay();}
 range.addEventListener('input',()=>{manual=true;cancelPlay();show(Number(range.value));});
 replay.addEventListener('click',()=>{if(playing){cancelPlay();manual=true;return;}const art=thread.querySelector('.lc-thread-art'),bounds=art.getBoundingClientRect();playbackDelay=bounds.top<80||bounds.bottom>innerHeight-70?350:0;if(playbackDelay)art.scrollIntoView({behavior:'smooth',block:'center'});manual=true;playing=true;started=0;replay.textContent='Pause unfolding';playFrame=requestAnimationFrame(animate);});
 const reveal=[...page.querySelectorAll('.lc-reveal')];
 if('IntersectionObserver'in window){
  new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(!inView)cancelPlay();schedule();},{rootMargin:'80px'}).observe(thread);
  const revealObserver=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-arrived');revealObserver.unobserve(e.target);}}),{threshold:.12});
  if(!off)reveal.forEach(el=>{el.classList.add('is-waiting');revealObserver.observe(el);});
 }
 addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
 document.addEventListener('portfolio:motion',e=>{off=e.detail.off;cancelPlay();replay.disabled=off;if(off){show(8);reveal.forEach(el=>el.classList.add('is-arrived'));}else{manual=false;schedule();}});
 document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelPlay();cancelAnimationFrame(scrollFrame);scrollFrame=0;}else schedule();});
 addEventListener('pagehide',()=>{cancelPlay();cancelAnimationFrame(scrollFrame);},{once:true});
 replay.disabled=off;show(8);
 const parcel=page.querySelector('[data-liz-parcel]'),choices=[...parcel.querySelectorAll('[data-parcel-select]')],frames=[...parcel.querySelectorAll('[data-parcel-frame]')];
 choices.forEach(button=>button.addEventListener('click',()=>{const target=button.dataset.parcelSelect;choices.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));frames.forEach(f=>f.hidden=f.dataset.parcelFrame!==target);parcel.querySelector('.lc-parcel-status').textContent=`${button.textContent} parcel`; }));
}
