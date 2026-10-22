export function careerProgress(y,start,travel,count){
 const progress=Math.max(0,Math.min(1,travel>0?(y-start)/travel:0)),step=progress*Math.max(0,count-1);
 return {progress,step,index:Math.round(step)};
}
export function mountCareer(){
 const section=document.querySelector('.career-section');if(!section)return;
 const track=section.querySelector('.career-track'),viewport=section.querySelector('.career-viewport'),pin=section.querySelector('.career-pin'),events=[...track.querySelectorAll('[data-career-id]')],buttons=[...section.querySelectorAll('[data-career-step]')],dialog=section.querySelector('.career-dialog');
 const eligible=matchMedia('(min-width:1100px) and (min-height:840px)'),vertical=matchMedia('(max-width:900px)');
 let pinned=false,index=0,queued=false,offsets=[],lastOffset=0,pendingTarget=null,drag=null,moved=false,dialogTrigger=null;
 const off=()=>document.documentElement.classList.contains('motion-off');
 viewport.tabIndex=0;section.querySelector('.career-navigation').hidden=false;
 function geometry(){return {start:section.getBoundingClientRect().top+scrollY-96,travel:section.offsetHeight-pin.offsetHeight};}
 function configure(){
  const before=pinned?careerProgress(scrollY,geometry().start,geometry().travel,events.length).progress:null;
  const wasPinned=pinned;pinned=eligible.matches&&!off()&&!section.querySelector('details[open]');section.classList.toggle('career-scroll-story',pinned);section.classList.toggle('career-vertical',vertical.matches);
  section.style.setProperty('--career-travel',`${(events.length-1)*280}px`);viewport.scrollLeft=0;track.style.transform='';
  const lead=pinned?Math.max(0,(viewport.clientWidth-events[0].offsetWidth)/2):0;track.style.setProperty('--career-lead',`${lead}px`);
  offsets=events.map(el=>el.offsetLeft-events[0].offsetLeft);lastOffset=offsets.at(-1)||0;pendingTarget=null;
  if(wasPinned&&pinned&&before>0&&before<1){const g=geometry();scrollTo({top:g.start+before*g.travel,behavior:'instant'});}queue();
 }
 function paint(){
  let step=index;
  if(pinned){const g=geometry(),position=careerProgress(scrollY,g.start,g.travel,events.length);index=position.index;step=position.step;const base=Math.floor(step),fraction=step-base,camera=(offsets[base]||0)+((offsets[base+1]??lastOffset)-(offsets[base]||0))*fraction;track.style.transform=`translate3d(${-camera}px,0,0)`;section.style.setProperty('--career-progress',position.progress);if(pendingTarget!==null&&Math.abs(step-pendingTarget)<.025)pendingTarget=null;}
  else{const box=viewport.getBoundingClientRect();let nearest=Infinity;events.forEach((el,i)=>{const rect=el.getBoundingClientRect(),distance=vertical.matches?Math.abs(rect.top-innerHeight*.32):Math.abs(rect.left-box.left);if(distance<nearest){nearest=distance;index=i;}});step=index;}
  events.forEach((el,i)=>{el.style.setProperty('--segment-progress',String(Math.max(0,Math.min(1,step-i))));el.style.setProperty('--career-distance',String(Math.min(2,Math.abs(step-i))));el.classList.toggle('is-active',i===index);el.classList.toggle('is-past',i<index);if(i===index)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');});
  const label=section.querySelector('.career-position');label.textContent=`${String(index+1).padStart(2,'0')} / ${events.length}`;section.querySelector('.career-progress>span').style.transform=`scaleX(${(step+1)/events.length})`;buttons[0].disabled=index===0;buttons[1].disabled=index===events.length-1;queued=false;
 }
 function queue(){if(!queued){queued=true;requestAnimationFrame(paint);}}
 function visit(target,behavior=off()?'instant':'smooth'){
  if(pinned){const g=geometry();pendingTarget=target;scrollTo({top:g.start+target/(events.length-1)*g.travel,behavior});}
  else if(vertical.matches)events[target].scrollIntoView({block:'center',behavior});else viewport.scrollTo({left:offsets[target],behavior});
 }
 function go(step){visit(Math.max(0,Math.min(events.length-1,(pendingTarget??index)+step)));}
 buttons.forEach(b=>b.addEventListener('click',()=>go(Number(b.dataset.careerStep))));
 viewport.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();go(e.key==='ArrowRight'?1:-1);}});
 viewport.addEventListener('focusin',e=>{const event=e.target.closest('[data-career-id]');if(pinned&&event){viewport.scrollLeft=0;const target=events.indexOf(event);if(target!==index)visit(target,'instant');}});
 section.addEventListener('wheel',()=>pendingTarget=null,{passive:true});section.addEventListener('touchstart',()=>pendingTarget=null,{passive:true});
 viewport.addEventListener('dragstart',e=>e.preventDefault());
 viewport.addEventListener('pointerdown',e=>{if(e.isPrimary&&!vertical.matches){drag={id:e.pointerId,x:e.clientX,y:e.clientY,windowY:scrollY,left:viewport.scrollLeft,active:false};moved=false;}});
 viewport.addEventListener('pointermove',e=>{if(!drag||drag.id!==e.pointerId)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(!drag.active&&Math.abs(dx)>18&&Math.abs(dx)>Math.abs(dy)*1.3){drag.active=true;viewport.setPointerCapture(e.pointerId);pendingTarget=null;}if(!drag.active)return;e.preventDefault();moved=true;if(pinned){const g=geometry();scrollTo({top:Math.max(g.start,Math.min(g.start+g.travel,drag.windowY-dx/Math.max(1,lastOffset)*g.travel)),behavior:'instant'});}else viewport.scrollLeft=drag.left-dx;});
 const release=()=>{if(drag&&viewport.hasPointerCapture(drag.id))viewport.releasePointerCapture(drag.id);drag=null;};viewport.addEventListener('pointerup',release);viewport.addEventListener('pointercancel',release);viewport.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation();moved=false;}},true);
 // Keep the section's geometry stable while long descriptions are read.
 section.querySelectorAll('.career-detail summary').forEach(summary=>summary.addEventListener('click',e=>{if(!pinned||!dialog)return;e.preventDefault();const event=summary.closest('[data-career-id]');dialogTrigger=summary;dialog.querySelector('.career-dialog-company').textContent=event.querySelector('.career-company').textContent;dialog.querySelector('h2').textContent=event.querySelector('h3').textContent;dialog.querySelector('.career-dialog-description').textContent=summary.parentElement.querySelector('p').textContent;dialog.showModal();document.body.classList.add('viewer-open');}));
 dialog?.querySelector('.career-dialog-close').addEventListener('click',()=>dialog.close());dialog?.addEventListener('close',()=>{document.body.classList.remove('viewer-open');dialogTrigger?.focus({preventScroll:true});});dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 viewport.addEventListener('scroll',()=>{if(!pinned)queue();},{passive:true});addEventListener('scroll',queue,{passive:true});addEventListener('resize',configure,{passive:true});document.addEventListener('portfolio:motion',configure);document.fonts.ready.then(configure);configure();
}
