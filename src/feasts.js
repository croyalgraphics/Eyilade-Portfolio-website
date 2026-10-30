export const occasionIndex=(index,direction,count)=>count>0?((index+direction)%count+count)%count:0;
export const canAdvanceOccasion=({playing,inView,hidden,motionOff,interacting})=>playing&&inView&&!hidden&&!motionOff&&!interacting;

export function mountFeasts(){
 const page=document.querySelector('.feasts-case');if(!page)return;
 const player=page.querySelector('[data-ff-player]'),choices=[...player.querySelectorAll('[data-ff-select]')],frames=[...player.querySelectorAll('[data-ff-scene]')],play=player.querySelector('.ff-play'),status=player.querySelector('.ff-player-status');
 let index=0,playing=false,inView=false,motionOff=document.documentElement.classList.contains('motion-off'),hovered=false,timer=0;
 const allowed=()=>canAdvanceOccasion({playing,inView,hidden:document.hidden,motionOff,interacting:hovered||player.contains(document.activeElement)||document.querySelector('.lightbox[open]')!==null});
 const label=()=>{const paused=playing&&!allowed();status.textContent=`${choices[index].textContent} selected · ${motionOff?'Motion off':playing?(paused?'Playback paused':'Playing occasions'):'Manual browsing'}`;play.textContent=playing?'Pause occasions':'Play occasions';play.setAttribute('aria-pressed',String(playing));play.disabled=motionOff;};
 const schedule=()=>{clearTimeout(timer);timer=0;label();if(allowed())timer=setTimeout(()=>{if(allowed()){show(occasionIndex(index,1,frames.length));}else schedule();},6500);};
 const show=n=>{index=n;choices.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===n)));frames.forEach((f,i)=>f.hidden=i!==n);schedule();};
 const manual=n=>{playing=false;show(n);};
 choices.forEach((b,i)=>b.addEventListener('click',()=>manual(i)));
 player.querySelector('.ff-prev').addEventListener('click',()=>manual(occasionIndex(index,-1,frames.length)));
 player.querySelector('.ff-next').addEventListener('click',()=>manual(occasionIndex(index,1,frames.length)));
 play.addEventListener('click',()=>{playing=!playing;schedule();});
 player.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'){hovered=true;schedule();}});
 player.addEventListener('pointerleave',()=>{hovered=false;schedule();});
 player.addEventListener('focusin',schedule);player.addEventListener('focusout',()=>queueMicrotask(schedule));
 const motif=page.querySelector('.ff-motif'),replay=motif.querySelector('.ff-replay');
 const revealMotif=()=>{motif.classList.remove('is-arrived');requestAnimationFrame(()=>requestAnimationFrame(()=>{if(!motionOff)motif.classList.add('is-arrived');}));};
 replay.addEventListener('click',revealMotif);
 const reveals=[...page.querySelectorAll('.ff-reveal')];
 if('IntersectionObserver'in window){
  new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{threshold:.12}).observe(player);
  const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-arrived');observer.unobserve(e.target);}}),{threshold:.1});
  if(!motionOff){reveals.forEach(el=>{el.classList.add('is-waiting');observer.observe(el);});motif.classList.add('is-waiting');observer.observe(motif);}
 }else{inView=true;motif.classList.add('is-arrived');}
 const dialog=document.querySelector('.lightbox');if(dialog)new MutationObserver(schedule).observe(dialog,{attributes:true,attributeFilter:['open']});
 document.addEventListener('visibilitychange',schedule);
 document.addEventListener('portfolio:motion',e=>{motionOff=e.detail.off;if(motionOff){playing=false;reveals.forEach(el=>el.classList.add('is-arrived'));motif.classList.add('is-arrived');}replay.disabled=motionOff;schedule();});
 addEventListener('pagehide',()=>{clearTimeout(timer);playing=false;},{once:true});
 replay.disabled=motionOff;schedule();
}
