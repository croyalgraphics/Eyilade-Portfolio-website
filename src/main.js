import {mountHeroCharacter,mountFooterCharacter} from './character.js';
import {mountCareer} from './career.js';
import {mountWorks} from './carousel.js';
import {mountPreferences} from './preferences.js';
import {mountNavigation} from './navigation.js';
import {mountToolkit} from './toolkit.js';
import {mountBeansSequence} from './beans-central.js';
import {mountLizcraft} from './lizcraft.js';
import {mountPurehive} from './purehive.js';
import {mountFeasts} from './feasts.js';
import {mountNatoral} from './natoral.js';
const root=document.documentElement;
let motionOff=root.classList.contains('motion-off');
document.addEventListener('portfolio:motion',e=>motionOff=e.detail.off);
mountPreferences();
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
 document.querySelectorAll('.discipline,.section-heading,.about-introduction,.brand-lineup,.tool-system,.pathway,.case-details>div,.mark-note').forEach(el=>{if(!motionOff){el.classList.add('will-reveal');observer.observe(el);}});}
mountNavigation();
mountToolkit();
mountHeroCharacter();
mountCareer();
mountWorks();
mountFooterCharacter();
mountBeansSequence();
mountLizcraft();
mountPurehive();
mountFeasts();
mountNatoral();
const copy=document.querySelector('.copy-email');let copyTimer;
copy?.addEventListener('click',async()=>{clearTimeout(copyTimer);copy.classList.remove('is-copied','has-copy-error');try{await navigator.clipboard.writeText('eyilade@gmail.com');copy.classList.add('is-copied');copy.setAttribute('title','Email copied');copy.querySelector('.copy-feedback').textContent='Copied';document.querySelector('.copy-status').textContent='Email address copied.';}catch{copy.classList.add('has-copy-error');copy.querySelector('.copy-feedback').textContent='Select the email to copy';document.querySelector('.copy-status').textContent='Clipboard unavailable. Select and copy eyilade@gmail.com.';}copyTimer=setTimeout(()=>{copy.classList.remove('is-copied','has-copy-error');copy.setAttribute('title','Copy email address');document.querySelector('.copy-status').textContent='';},2500);});
addEventListener('pagehide',()=>clearTimeout(copyTimer),{once:true});
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
