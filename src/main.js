import {mountHeroCharacter,mountFooterCharacter} from './character.js';
import {mountCareer} from './career.js';
import {mountWorks} from './carousel.js';
const root=document.documentElement;
const systemMotion=matchMedia('(prefers-reduced-motion: reduce)');
let preference;try{preference=localStorage.getItem('eyilade-motion');}catch{}
let motionOff=systemMotion.matches||preference==='off';
const motionButton=document.querySelector('.motion-toggle');
function setMotion(off,save=false){
 motionOff=systemMotion.matches||off;root.classList.toggle('motion-off',motionOff);
 motionButton?.setAttribute('aria-pressed',String(motionOff));
 motionButton?.setAttribute('aria-label',systemMotion.matches?'Reduced motion follows your device setting':`Turn motion ${motionOff?'on':'off'}`);
 if(motionButton){motionButton.disabled=systemMotion.matches;motionButton.querySelector('.motion-label').textContent=systemMotion.matches?'Reduced motion':`Motion ${motionOff?'off':'on'}`;}
 if(save){preference=off?'off':'on';try{localStorage.setItem('eyilade-motion',preference);}catch{}}
 document.dispatchEvent(new CustomEvent('portfolio:motion',{detail:{off:motionOff}}));
}
setMotion(motionOff);motionButton?.addEventListener('click',()=>setMotion(!motionOff,true));
systemMotion.addEventListener('change',()=>setMotion(preference==='off'));
const menu=document.querySelector('.mobile-nav');
const closeMenu=()=>{if(menu)menu.open=false;};
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
menu?.addEventListener('toggle',()=>menu.querySelector('summary').setAttribute('aria-label',`${menu.open?'Close':'Open'} navigation menu`));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.open){closeMenu();menu.querySelector('summary').focus();}});
document.addEventListener('click',e=>{if(menu?.open&&!menu.contains(e.target))closeMenu();});
matchMedia('(min-width:901px)').addEventListener('change',e=>{if(e.matches)closeMenu();});
const nav=document.querySelector('.desktop-nav');const navLinks=[...nav.querySelectorAll('.nav-link')];
function highlight(link){if(!link)return;nav.style.setProperty('--nav-x',`${link.offsetLeft}px`);nav.style.setProperty('--nav-w',`${link.offsetWidth}px`);navLinks.forEach(a=>a.classList.toggle('is-highlighted',a===link));}
const currentNav=()=>nav.querySelector('[aria-current]')||navLinks[0];
function restoreNav(){nav.classList.remove('is-tracking');highlight(currentNav());}
navLinks.forEach(a=>{for(const type of ['pointerenter','focus'])a.addEventListener(type,()=>{nav.classList.add('is-tracking');highlight(a);});});
nav.addEventListener('pointerleave',()=>{if(!nav.contains(document.activeElement))restoreNav();});
nav.addEventListener('focusout',e=>{if(!nav.contains(e.relatedTarget))restoreNav();});
restoreNav();document.fonts.ready.then(restoreNav);addEventListener('resize',restoreNav,{passive:true});
const progress=document.querySelector('.scroll-progress');let scrollPending=false;
function updateScroll(){
 const max=root.scrollHeight-innerHeight;progress.style.transform=`scaleX(${max>0?scrollY/max:0})`;
 scrollPending=false;
}
addEventListener('scroll',()=>{if(!scrollPending){scrollPending=true;requestAnimationFrame(updateScroll);}},{passive:true});updateScroll();
if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');observer.unobserve(e.target);}}),{threshold:.07});
 document.querySelectorAll('.project-item,.section-heading,.about-introduction,.brand-lineup,.tool-system,.pathway,.case-details>div,.mark-note').forEach(el=>{if(!motionOff){el.classList.add('will-reveal');observer.observe(el);}});}
mountHeroCharacter();
mountCareer();
mountWorks();
mountFooterCharacter();
const copy=document.querySelector('.copy-email');let copyTimer;
copy?.addEventListener('click',async()=>{clearTimeout(copyTimer);try{await navigator.clipboard.writeText('eyilade@gmail.com');copy.querySelector('span').textContent='Copied';document.querySelector('.copy-status').textContent='Email address copied.';copyTimer=setTimeout(()=>copy.querySelector('span').textContent='Copy email',2500);}catch{document.querySelector('.copy-status').textContent='Copy unavailable. Email: eyilade@gmail.com';copy.querySelector('span').textContent='eyilade@gmail.com';}});
const lightbox=document.querySelector('.lightbox');const imageButtons=[...document.querySelectorAll('.image-zoom')];let currentImage=0,lightboxTrigger=null;
function showImage(index){if(!imageButtons.length)return;currentImage=(index+imageButtons.length)%imageButtons.length;const button=imageButtons[currentImage];const image=lightbox.querySelector('img');lightbox.classList.add('is-loading');lightbox.classList.remove('has-error');lightbox.querySelector('.image-status').textContent='Loading artwork…';image.alt=button.dataset.caption;lightbox.querySelector('#lightbox-caption').textContent=`${button.dataset.caption} · ${currentImage+1} of ${imageButtons.length}`;lightbox.querySelector('.lightbox-original').href=button.dataset.image;image.src=button.dataset.image;}
if(lightbox){const img=lightbox.querySelector('img');img.addEventListener('load',()=>{lightbox.classList.remove('is-loading');lightbox.querySelector('.image-status').textContent='';});img.addEventListener('error',()=>{lightbox.classList.remove('is-loading');lightbox.classList.add('has-error');lightbox.querySelector('.image-status').textContent='This image could not load. Try opening the full image below.';});
 imageButtons.forEach((b,i)=>b.addEventListener('click',()=>{lightboxTrigger=b;showImage(i);lightbox.showModal();document.body.classList.add('viewer-open');}));
 lightbox.querySelector('.lightbox-close').addEventListener('click',()=>lightbox.close());lightbox.querySelector('.lightbox-prev').addEventListener('click',()=>showImage(currentImage-1));lightbox.querySelector('.lightbox-next').addEventListener('click',()=>showImage(currentImage+1));
 lightbox.addEventListener('close',()=>{document.body.classList.remove('viewer-open');lightboxTrigger?.focus({preventScroll:true});});lightbox.addEventListener('click',e=>{if(e.target===lightbox){const r=lightbox.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)lightbox.close();}});lightbox.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();showImage(currentImage+(e.key==='ArrowRight'?1:-1));}});
}
const flows=[...document.querySelectorAll('.logo-flow')];
if('IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(e=>e.target.classList.toggle('flow-sleeping',!e.isIntersecting)),{rootMargin:'100px'});flows.forEach(flow=>observer.observe(flow));}
function updateFlows(){flows.forEach(flow=>{const button=flow.querySelector('.flow-pause');const paused=flow.classList.contains('flow-paused');button.disabled=motionOff;button.textContent=motionOff?'Motion off':paused?'Resume movement':'Pause movement';button.setAttribute('aria-pressed',String(motionOff||paused));});}
flows.forEach(flow=>flow.querySelector('.flow-pause').addEventListener('click',()=>{flow.classList.toggle('flow-paused');updateFlows();}));
document.addEventListener('portfolio:motion',updateFlows);updateFlows();
document.addEventListener('visibilitychange',()=>flows.forEach(flow=>flow.classList.toggle('flow-tab-hidden',document.hidden)));
document.querySelectorAll('[data-room-mode]').forEach(button=>button.addEventListener('click',()=>{const mode=button.dataset.roomMode;document.querySelector('#room-flow').hidden=mode!=='flow';document.querySelector('#logo-index').hidden=mode!=='index';document.querySelectorAll('[data-room-mode]').forEach(b=>{const active=b===button;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});}));
