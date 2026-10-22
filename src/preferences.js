export function resolveMotionPreference(stored,systemReduced){return stored==='off'?true:stored==='on'?false:Boolean(systemReduced);}
export function resolveThemePreference(stored,systemDark){return stored==='light'||stored==='dark'?stored:systemDark?'dark':'light';}

export function mountPreferences(){
 const root=document.documentElement,motionQuery=matchMedia('(prefers-reduced-motion: reduce)'),themeQuery=matchMedia('(prefers-color-scheme: dark)');
 const motionButton=document.querySelector('.motion-toggle'),themeButton=document.querySelector('.theme-toggle');
 let motionStored,themeStored;
 function read(){try{motionStored=localStorage.getItem('eyilade-motion');themeStored=localStorage.getItem('eyilade-theme');}catch{}}
 function apply(){
  const off=resolveMotionPreference(motionStored,motionQuery.matches),theme=resolveThemePreference(themeStored,themeQuery.matches);
  root.dataset.motion=off?'off':'on';root.classList.toggle('motion-off',off);root.dataset.theme=theme;
  const motionLabel=`Turn animations ${off?'on':'off'}`;motionButton?.setAttribute('aria-label',motionLabel);motionButton?.setAttribute('title',motionLabel);motionButton?.setAttribute('aria-pressed',String(off));
  const themeLabel=`Switch to ${theme==='dark'?'light':'dark'} mode`;themeButton?.setAttribute('aria-label',themeLabel);themeButton?.setAttribute('title',themeLabel);themeButton?.setAttribute('aria-pressed',String(theme==='dark'));
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content',theme==='dark'?'#161b18':'#f6f3ea');
  document.dispatchEvent(new CustomEvent('portfolio:motion',{detail:{off}}));document.dispatchEvent(new CustomEvent('portfolio:theme',{detail:{theme}}));
 }
 function save(key,value){try{localStorage.setItem(key,value);}catch{}}
 read();apply();
 motionButton?.addEventListener('click',()=>{motionStored=root.classList.contains('motion-off')?'on':'off';save('eyilade-motion',motionStored);apply();});
 themeButton?.addEventListener('click',()=>{themeStored=root.dataset.theme==='dark'?'light':'dark';save('eyilade-theme',themeStored);apply();});
 motionQuery.addEventListener('change',apply);themeQuery.addEventListener('change',apply);addEventListener('storage',e=>{if(e.key===null||e.key==='eyilade-theme'||e.key==='eyilade-motion'){read();apply();}});
 return ()=>root.classList.contains('motion-off');
}
