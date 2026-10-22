export function nextNavigationState(state,{y,threshold,locked}){
 if(locked||y<=Math.max(48,threshold))return {hidden:false,lastY:y,direction:0,distance:0};
 const delta=y-state.lastY;if(Math.abs(delta)<2)return {...state,lastY:y};
 const direction=Math.sign(delta),distance=direction===state.direction?state.distance+Math.abs(delta):Math.abs(delta);
 return {hidden:direction>0&&distance>=32?true:direction<0&&distance>=10?false:state.hidden,lastY:y,direction,distance};
}
export function mountNavigation(){
 const shell=document.querySelector('.navigation-shell');if(!shell)return;
 const intro=document.querySelector('.cv-hero,.about-hero,.work-intro,.logofolio-intro,.case-cover,.not-found');
 let threshold=innerHeight*.7,queued=false,state={hidden:false,lastY:scrollY,direction:0,distance:0};
 function measure(){threshold=intro?Math.max(160,intro.getBoundingClientRect().bottom+scrollY-Math.min(160,innerHeight*.2)):innerHeight*.7;update();}
 function update(){const locked=(shell.contains(document.activeElement)&&document.activeElement.matches(':focus-visible'))||Boolean(shell.querySelector('details[open]'));state=nextNavigationState(state,{y:Math.max(0,scrollY),threshold,locked});shell.classList.toggle('is-nav-hidden',state.hidden);queued=false;}
 function queue(){if(!queued){queued=true;requestAnimationFrame(update);}}
 addEventListener('scroll',queue,{passive:true});addEventListener('resize',measure,{passive:true});
 shell.addEventListener('focusin',()=>{state={...state,hidden:false,lastY:scrollY,distance:0};shell.classList.remove('is-nav-hidden');});shell.addEventListener('focusout',queue);shell.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',queue));
 // Keyboard navigation is never hidden beneath the viewport.
 document.addEventListener('keydown',e=>{if(e.key==='Tab'){state.hidden=false;shell.classList.remove('is-nav-hidden');}});
 if('ResizeObserver'in window&&intro)new ResizeObserver(measure).observe(intro);document.fonts.ready.then(measure);measure();
}
