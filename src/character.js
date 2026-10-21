import character from '../content/character.json';

// One active drawing timer. User gestures supersede automatic thought; blink is excluded.
export function mountHeroCharacter(){
 const host=document.querySelector('.hero-figure');if(!host)return;
 const actor=host.querySelector('.illustration-button'),poster=host.querySelector('.character-poster'),canvas=host.querySelector('canvas'),note=host.querySelector('.hello-note'),status=host.querySelector('.hello-status');
 let context;try{context=canvas.getContext('2d');}catch{}
 if(context){context.imageSmoothingEnabled=true;context.imageSmoothingQuality='high';}
 const cache=new Map(),originalSrcset=poster.getAttribute('srcset');
 let timer=0,thoughtTimer=0,stillTimer=0,generation=0,visible=!('IntersectionObserver'in window),ready=false,userBusy=false,clicks=0;
 const messages={wave:'Good to meet you.',thinking:'What if…','thumbs-up':'That’s a good idea.'};
 const motionOff=()=>document.documentElement.classList.contains('motion-off');
 const canPlay=()=>Boolean(context&&ready&&visible&&!document.hidden&&!motionOff());
 function stop(){clearTimeout(timer);generation++;host.dataset.characterPlaying='false';}
 function dismiss(){host.classList.remove('character-reacting');note.textContent='';status.textContent='';}
 function bubble(state,user){note.textContent=messages[state]||'';host.classList.toggle('character-reacting',state!=='idle');if(user)status.textContent=messages[state];}
 function showStill(state){stop();host.dataset.characterState=state;canvas.hidden=true;host.classList.remove('character-ready');if(state==='idle'&&originalSrcset)poster.setAttribute('srcset',originalSrcset);else poster.removeAttribute('srcset');poster.src=character.states[state].poster;}
 function scheduleThought(){clearTimeout(thoughtTimer);if(canPlay()&&!userBusy&&host.dataset.characterState==='idle')thoughtTimer=setTimeout(()=>{if(canPlay()&&!userBusy){bubble('thinking',false);play('thinking');}},14000+Math.random()*12000);}
 function loadAtlas(state){if(cache.has(state))return cache.get(state);const p=new Promise((resolve,reject)=>{const image=new Image();image.decoding='async';image.onload=()=>resolve(image);image.onerror=()=>reject(new Error('Character artwork unavailable'));image.src=character.states[state].atlas;});cache.set(state,p);p.catch(()=>cache.delete(state));return p;}
 function idle(){userBusy=false;dismiss();play('idle');}
 async function play(state){
  stop();clearTimeout(thoughtTimer);host.dataset.characterState=state;const token=generation;
  if(!canPlay()){showStill(state);if(state!=='idle')stillTimer=setTimeout(idle,1800);return;}
  let atlas;try{atlas=await loadAtlas(state);}catch{if(token===generation){showStill(state);if(state!=='idle')stillTimer=setTimeout(idle,1800);}return;}
  if(token!==generation||!canPlay())return;
  const {sequence,durations}=character.states[state];let cursor=0;canvas.hidden=false;host.classList.add('character-ready');host.dataset.characterPlaying='true';
  if(state==='idle')scheduleThought();
  function draw(){if(token!==generation||!canPlay())return;const frame=sequence[cursor];context.clearRect(0,0,character.width,character.height);context.drawImage(atlas,frame%character.columns*character.width,Math.floor(frame/character.columns)*character.height,character.width,character.height,0,0,character.width,character.height);host.dataset.characterFrame=String(frame);timer=setTimeout(()=>{cursor++;if(cursor===sequence.length){if(state==='idle')cursor=0;else{idle();return;}}draw();},durations[cursor]);}draw();
 }
 actor.addEventListener('click',()=>{if(userBusy)return;clearTimeout(stillTimer);clearTimeout(thoughtTimer);userBusy=true;clicks++;const state=clicks%2?'thumbs-up':'wave';bubble(state,true);play(state);});
 function reconcile(){clearTimeout(stillTimer);clearTimeout(thoughtTimer);userBusy=false;dismiss();if(canPlay())play('idle');else showStill('idle');}
 document.addEventListener('portfolio:motion',reconcile);document.addEventListener('visibilitychange',reconcile);
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;reconcile();},{threshold:.08}).observe(host);
 function loaded(){ready=true;reconcile();}if(document.readyState==='complete')loaded();else addEventListener('load',loaded,{once:true});
 addEventListener('pagehide',()=>{stop();clearTimeout(stillTimer);clearTimeout(thoughtTimer);});
 poster.addEventListener('error',()=>{if(poster.getAttribute('src')!==character.states.idle.poster){poster.removeAttribute('srcset');poster.src=character.states.idle.poster;}});
}

export function mountFooterCharacter(){
 const actor=document.querySelector('.footer-character');if(!actor)return;let timer;
 actor.addEventListener('pointermove',e=>{if(document.documentElement.classList.contains('motion-off')||e.pointerType!=='mouse')return;const r=actor.getBoundingClientRect();actor.style.setProperty('--footer-tilt',`${(e.clientX-r.left-r.width/2)/r.width*5}deg`);});
 actor.addEventListener('pointerleave',()=>actor.style.setProperty('--footer-tilt','0deg'));
 actor.addEventListener('click',()=>{clearTimeout(timer);actor.classList.remove('is-greeting');requestAnimationFrame(()=>actor.classList.add('is-greeting'));document.querySelector('.footer-character-status').textContent='Let’s talk ideas. Get in touch using the links below.';timer=setTimeout(()=>{actor.classList.remove('is-greeting');document.querySelector('.footer-character-status').textContent='';},2400);});
 addEventListener('pagehide',()=>clearTimeout(timer),{once:true});
}
