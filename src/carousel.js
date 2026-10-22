export function carouselOffset(i,current,count){let offset=(i-current+count)%count;if(offset>count/2)offset-=count;return offset;}
export function shouldAutoplay({off,hover,focused,touching,visible,hidden,count}){return !off&&!hover&&!focused&&!touching&&visible&&!hidden&&count>1;}
export function carouselTiming(dwell,transition){return {dwell:Math.max(8000,Math.min(20000,Number(dwell)||10000)),transition:Math.max(200,Math.min(800,Number(transition)||500))};}
export function mountWorks(){
 const host=document.querySelector('.works-carousel');if(!host)return;
 const cards=[...host.querySelectorAll('.project-item')],stage=host.querySelector('.project-grid'),previous=host.querySelector('[data-project-step="-1"]'),next=host.querySelector('[data-project-step="1"]'),status=host.querySelector('.carousel-status');
 const timing=carouselTiming(host.dataset.dwellMs,host.dataset.transitionMs),delay=timing.dwell+timing.transition;
 host.style.setProperty('--carousel-transition',`${timing.transition}ms`);
 let keyboardMode=true,items=cards,index=0,hover=false,focused=false,touching=false,visible=false,timer=0,start=null,moved=false;
 const off=()=>document.documentElement.classList.contains('motion-off');
 host.classList.add('is-enhanced');stage.tabIndex=0;stage.setAttribute('aria-label','Project carousel. Use left and right arrow keys to browse.');host.querySelector('.carousel-controls').hidden=false;
 function schedule(){clearTimeout(timer);const play=shouldAutoplay({off:off(),hover,focused,touching,visible,hidden:document.hidden,count:items.length});host.dataset.autoplay=play?'playing':'paused';if(play)timer=setTimeout(()=>go(1,false),delay);}
 function render(){cards.forEach(c=>{const i=items.indexOf(c);c.hidden=i===-1;if(i===-1)return;const offset=carouselOffset(i,index,items.length),shown=Math.abs(offset)<=1;c.dataset.position=String(offset);c.style.setProperty('--card-position',offset);c.classList.toggle('is-current',offset===0);c.inert=!shown;c.setAttribute('aria-hidden',String(!shown));c.setAttribute('role','group');c.setAttribute('aria-roledescription','slide');c.setAttribute('aria-label',`${i+1} of ${items.length}`);});status.textContent=`${String(index+1).padStart(2,'0')} / ${String(items.length).padStart(2,'0')}`;previous.disabled=next.disabled=items.length<2;schedule();}
 function go(step,manual=true){if(items.length<2)return;index=(index+step+items.length)%items.length;render();if(manual)host.querySelector('.carousel-announcement').textContent=`Project ${index+1} of ${items.length}: ${items[index].querySelector('h3').textContent}`;}
 previous.addEventListener('click',()=>go(-1));next.addEventListener('click',()=>go(1));host.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();go(e.key==='ArrowRight'?1:-1);}});
 host.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'){hover=true;schedule();}});host.addEventListener('pointerleave',()=>{hover=false;schedule();});
 document.addEventListener('keydown',e=>{if(e.key==='Tab'||e.key.startsWith('Arrow')){keyboardMode=true;focused=host.contains(document.activeElement);schedule();}});
 host.addEventListener('pointerdown',()=>{keyboardMode=false;focused=false;schedule();});
 host.addEventListener('focusin',()=>{focused=keyboardMode;schedule();});host.addEventListener('focusout',e=>{focused=keyboardMode&&host.contains(e.relatedTarget);schedule();});
 stage.addEventListener('dragstart',e=>e.preventDefault());
 stage.addEventListener('pointerdown',e=>{if(e.isPrimary){touching=true;start={id:e.pointerId,x:e.clientX,y:e.clientY,captured:false};moved=false;schedule();}});
 stage.addEventListener('pointermove',e=>{if(!start||start.id!==e.pointerId)return;const dx=e.clientX-start.x,dy=e.clientY-start.y;if(!start.captured&&Math.abs(dx)>18&&Math.abs(dx)>Math.abs(dy)*1.3){start.captured=true;stage.setPointerCapture(e.pointerId);}if(start.captured)e.preventDefault();});
 function release(e){if(!start||start.id!==e.pointerId)return;const delta=e.clientX-start.x,captured=start.captured;if(stage.hasPointerCapture(e.pointerId))stage.releasePointerCapture(e.pointerId);start=null;touching=false;if(captured&&Math.abs(delta)>45){moved=true;go(delta<0?1:-1);}else schedule();}
 addEventListener('pointerup',release);addEventListener('pointercancel',e=>{if(!start||start.id!==e.pointerId)return;if(stage.hasPointerCapture(e.pointerId))stage.releasePointerCapture(e.pointerId);start=null;touching=false;schedule();});stage.addEventListener('click',e=>{if(moved){e.preventDefault();moved=false;}},true);
 document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{const filter=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});items=cards.filter(c=>filter==='all'||c.dataset.category===filter);index=0;render();document.querySelector('#filter-status').textContent=`Showing ${items.length} ${filter==='all'?'selected':filter} project${items.length===1?'':'s'}.`;}));
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;schedule();},{threshold:.2}).observe(host);else visible=true;
 document.addEventListener('portfolio:motion',schedule);document.addEventListener('visibilitychange',schedule);addEventListener('pagehide',()=>clearTimeout(timer),{once:true});render();
}
