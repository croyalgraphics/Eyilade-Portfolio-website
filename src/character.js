import character from '../content/character.json';

// One timer, four approved states, no continuous render loop.
export function mountHeroCharacter(){
 const host=document.querySelector('.hero-figure');if(!host)return;
 const actor=host.querySelector('.illustration-button');const poster=host.querySelector('.character-poster');const canvas=host.querySelector('.character-canvas');
 const controls=host.querySelector('.character-reactions');const actions=[...host.querySelectorAll('[data-character-action]')];const status=host.querySelector('.hello-status');const note=host.querySelector('.hello-note');
 let context;try{context=canvas.getContext('2d');}catch{}
 if(context){context.imageSmoothingEnabled=true;context.imageSmoothingQuality='high';}
 const cache=new Map();let timer=0,noteTimer=0,generation=0,visible=!('IntersectionObserver'in window),pageReady=false;
 const originalSrcset=poster.getAttribute('srcset');
 controls.hidden=false;
 const messages={wave:'Good to meet you.',thinking:'Thinking it through.','thumbs-up':'That’s a good idea.'};
 const motionOff=()=>document.documentElement.classList.contains('motion-off');
 const canPlay=()=>Boolean(context&&pageReady&&visible&&!document.hidden&&!motionOff());
 function stop(){clearTimeout(timer);generation++;host.dataset.characterPlaying='false';}
 function select(state){host.dataset.characterState=state;actions.forEach(b=>{if(b!==actor)b.setAttribute('aria-pressed',String(b.dataset.characterAction===state));});}
 function showStill(state){
  stop();select(state);canvas.hidden=true;host.classList.remove('character-ready');
  if(state==='idle'&&originalSrcset)poster.setAttribute('srcset',originalSrcset);else poster.removeAttribute('srcset');
  poster.src=character.states[state].poster;host.dataset.characterFrame=String(state==='idle'?0:state==='wave'?2:3);
 }
 function loadAtlas(state){
  if(cache.has(state))return cache.get(state);
  const promise=new Promise((resolve,reject)=>{const image=new Image();image.decoding='async';image.onload=()=>resolve(image);image.onerror=()=>reject(new Error('Character artwork unavailable'));image.src=character.states[state].atlas;});
  cache.set(state,promise);promise.catch(()=>cache.delete(state));return promise;
 }
 async function play(state){
  if(!character.states[state])return;
  stop();select(state);const token=generation;
  if(!canPlay()){showStill(state);return;}
  let atlas;try{atlas=await loadAtlas(state);}catch{if(token===generation)showStill(state);return;}
  if(token!==generation||!canPlay())return;
  const {sequence,durations}=character.states[state];let cursor=0;
  canvas.hidden=false;host.classList.add('character-ready');host.dataset.characterPlaying='true';
  function draw(){
   if(token!==generation||!canPlay()){stop();return;}
   const frame=sequence[cursor];context.clearRect(0,0,character.width,character.height);
   context.drawImage(atlas,frame%character.columns*character.width,Math.floor(frame/character.columns)*character.height,character.width,character.height,0,0,character.width,character.height);
   host.dataset.characterFrame=String(frame);
   timer=setTimeout(()=>{cursor++;if(cursor===sequence.length){if(state==='idle')cursor=0;else{play('idle');return;}}draw();},durations[cursor]);
  }
  draw();
 }
 function reconcile(){if(motionOff()||!context){showStill('idle');return;}if(canPlay())play('idle');else stop();}
 actions.forEach(button=>button.addEventListener('click',()=>{
  const state=button.dataset.characterAction;play(state);clearTimeout(noteTimer);note.textContent=messages[state];host.classList.add('character-reacting');status.textContent=messages[state];
  noteTimer=setTimeout(()=>{host.classList.remove('character-reacting');status.textContent='';},2600);
 }));
 document.addEventListener('portfolio:motion',reconcile);document.addEventListener('visibilitychange',reconcile);
 if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;reconcile();},{threshold:.08});observer.observe(host);}
 function ready(){pageReady=true;reconcile();}
 if(document.readyState==='complete')ready();else addEventListener('load',ready,{once:true});
 addEventListener('pagehide',()=>{stop();clearTimeout(noteTimer);});
 poster.addEventListener('error',()=>{if(poster.getAttribute('src')!==character.states.idle.poster){poster.removeAttribute('srcset');poster.src=character.states.idle.poster;}});
}
