export function mountToolkit(){
 document.querySelectorAll('.tool-trigger').forEach(button=>{
  let timer,frame=0;const off=()=>document.documentElement.classList.contains('motion-off');
  button.addEventListener('pointermove',e=>{if(e.pointerType!=='mouse'||off()||frame)return;const x=e.clientX;frame=requestAnimationFrame(()=>{const r=button.getBoundingClientRect();button.style.setProperty('--tool-tilt',`${(x-r.left-r.width/2)/r.width*7}deg`);frame=0;});});
  button.addEventListener('pointerleave',()=>button.style.setProperty('--tool-tilt','0deg'));
  button.addEventListener('click',()=>{clearTimeout(timer);button.classList.remove('is-tool-reacting');if(off())return;requestAnimationFrame(()=>button.classList.add('is-tool-reacting'));timer=setTimeout(()=>button.classList.remove('is-tool-reacting'),650);});
  addEventListener('pagehide',()=>{clearTimeout(timer);cancelAnimationFrame(frame);},{once:true});
 });
}
