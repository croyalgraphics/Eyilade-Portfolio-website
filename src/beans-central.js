export function mountBeansSequence(){
 const player=document.querySelector('[data-beans-player]');if(!player)return;
 const frames=[...player.querySelectorAll('.bc-dish-frame')],choices=[...player.querySelectorAll('[data-dish-select]')],toggle=player.querySelector('.bc-motion-toggle'),status=player.querySelector('.bc-dish-status');
 let current=0,paused=false,visible=false,timer=null,hovering=false,explicitPlay=false,motionOff=document.documentElement.classList.contains('motion-off');
 const stop=()=>{clearTimeout(timer);timer=null;};
 function schedule(){stop();if(!paused&&!motionOff&&visible&&!document.hidden&&(explicitPlay||(!hovering&&!player.contains(document.activeElement))))timer=setTimeout(()=>{show((current+1)%frames.length,false);},4400);}
 function show(index,announce=true){current=index;frames.forEach((f,i)=>f.hidden=i!==index);choices.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));status.setAttribute('aria-live',announce?'polite':'off');status.textContent=`${choices[index].textContent} · ${index+1} of ${frames.length}`;schedule();}
 function update(){toggle.disabled=motionOff;toggle.textContent=motionOff?'Motion off':paused?'Play sequence':'Pause sequence';toggle.setAttribute('aria-pressed',String(paused||motionOff));schedule();}
 choices.forEach((b,i)=>b.addEventListener('click',()=>{paused=true;show(i);update();}));
 toggle.addEventListener('click',()=>{paused=!paused;explicitPlay=!paused;update();});
 player.addEventListener('focusin',()=>{explicitPlay=false;stop();});player.addEventListener('focusout',()=>queueMicrotask(schedule));
 player.addEventListener('pointerenter',()=>{hovering=true;explicitPlay=false;stop();});player.addEventListener('pointerleave',()=>{hovering=false;explicitPlay=false;schedule();});
 document.addEventListener('portfolio:motion',e=>{motionOff=e.detail.off;update();});document.addEventListener('visibilitychange',schedule);
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;schedule();},{threshold:.25}).observe(player);
 addEventListener('pagehide',stop,{once:true});update();
}
