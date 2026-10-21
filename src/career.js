export function mountCareer(){
 const track=document.querySelector('.career-track');if(!track)return;
 const section=document.querySelector('.career-section'),events=[...track.querySelectorAll('[data-career-id]')],buttons=[...section.querySelectorAll('[data-career-step]')],pin=section.querySelector('.career-pin');
 const eligible=matchMedia('(min-width:1100px) and (min-height:900px)'),vertical=matchMedia('(max-width:600px)');let pinned=false,index=0,queued=false,storyProgress=0;
 track.tabIndex=0;section.querySelector('.career-navigation').hidden=false;
 const off=()=>document.documentElement.classList.contains('motion-off');
 function configure(){pinned=eligible.matches&&!off()&&!section.querySelector('details[open]');section.classList.toggle('career-scroll-story',pinned);section.style.setProperty('--career-travel',`${(events.length-1)*230}px`);track.style.scrollSnapType=pinned?'none':'';if(!pinned)track.scrollLeft=0;queue();}
 function paint(){
  const bounds=track.getBoundingClientRect();
  if(pinned){const start=section.getBoundingClientRect().top+scrollY-110;const travel=section.offsetHeight-pin.offsetHeight;const progress=Math.max(0,Math.min(1,(scrollY-start)/travel));storyProgress=progress*(events.length-1);index=Math.round(storyProgress);track.scrollLeft=progress*(track.scrollWidth-track.clientWidth);section.style.setProperty('--career-progress',progress);}
  else{let nearest=Infinity;events.forEach((el,i)=>{const r=el.getBoundingClientRect(),distance=vertical.matches?Math.abs(r.top-innerHeight*.3):Math.abs(r.left-bounds.left);if(distance<nearest){nearest=distance;index=i;}});}
  events.forEach((el,i)=>{el.style.setProperty('--segment-progress',String(Math.max(0,Math.min(1,(pinned?storyProgress:index)-i))));el.classList.toggle('is-active',i===index);el.classList.toggle('is-past',i<index);if(i===index)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');});
  section.querySelector('.career-position').textContent=`${String(index+1).padStart(2,'0')} / ${events.length}`;
  section.querySelector('.career-progress>span').style.transform=`scaleX(${(index+1)/events.length})`;
  buttons[0].disabled=index===0;buttons[1].disabled=index===events.length-1;queued=false;
 }
 function queue(){if(!queued){queued=true;requestAnimationFrame(paint);}}
 function go(step){const next=Math.max(0,Math.min(events.length-1,index+step));if(pinned){const start=section.getBoundingClientRect().top+scrollY-110,travel=section.offsetHeight-pin.offsetHeight;scrollTo({top:start+next/(events.length-1)*travel,behavior:'smooth'});}else{const left=events[next].getBoundingClientRect().left-track.getBoundingClientRect().left+track.scrollLeft;track.scrollTo({left,behavior:off()?'instant':'smooth'});}}
 buttons.forEach(b=>b.addEventListener('click',()=>go(Number(b.dataset.careerStep))));
 track.addEventListener('focusin',e=>{const event=e.target.closest('[data-career-id]');if(pinned&&event){const target=events.indexOf(event);if(target!==index){const start=section.getBoundingClientRect().top+scrollY-110,travel=section.offsetHeight-pin.offsetHeight;scrollTo({top:start+target/(events.length-1)*travel,behavior:'instant'});}}});
 track.addEventListener('keydown',e=>{if(vertical.matches||e.target!==track)return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();go(e.key==='ArrowRight'?1:-1);}});
 // Expanding details deliberately releases the sticky presentation for comfortable reading.
 section.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open&&pinned){pinned=false;section.classList.remove('career-scroll-story');track.style.scrollSnapType='';events[index].scrollIntoView({block:'center',inline:'start',behavior:'instant'});queue();}}));
 track.addEventListener('scroll',()=>{if(!pinned)queue();},{passive:true});addEventListener('scroll',queue,{passive:true});addEventListener('resize',configure,{passive:true});document.addEventListener('portfolio:motion',configure);configure();
}
