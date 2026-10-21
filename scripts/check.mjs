import { readFile, readdir, stat, access } from 'node:fs/promises';
import { resolve, extname } from 'node:path';
import { gzipSync } from 'node:zlib';
const root=resolve('dist');
const files=[];
async function walk(path){for(const entry of await readdir(path,{withFileTypes:true})){const p=resolve(path,entry.name);if(entry.isDirectory())await walk(p);else files.push(p);}}
await walk(root);
let errors=[];let links=0;const pages=files.filter(p=>p.endsWith('.html'));
for(const path of pages){
  const html=await readFile(path,'utf8');
  if((html.match(/<h1[ >]/g)||[]).length!==1)errors.push(`${path}: expected one H1`);
  if(!html.includes('<meta name="description"'))errors.push(`${path}: description missing`);
  for(const tag of html.matchAll(/<img\b[^>]*>/g)){
    if(!/\balt="[^"]*"/.test(tag[0]))errors.push(`${path}: image missing alt`);
    if(!/\bwidth="\d+"/.test(tag[0])||!/\bheight="\d+"/.test(tag[0]))errors.push(`${path}: image dimensions missing`);
  }
  for(const match of html.matchAll(/(?:href|src|data-image)="(\/[^"#?]*)/g)){
    const url=decodeURIComponent(match[1]);if(url.startsWith('//'))continue;
    let dest=resolve(root,'.'+url);if(url.endsWith('/'))dest=resolve(dest,'index.html');
    try{await access(dest);}catch{errors.push(`${path}: missing ${url}`);}links++;
  }
  // The explicitly selected logo art is allowed; private software plans are not.
  if(/Up2Date|SupaChef|Golden Whisper|Boxed Pace|Car Poool|WorkOS|private workplace mobility|recyclable pickup/i.test(html))errors.push(`${path}: private product detail found`);
}
const logos=JSON.parse(await readFile('content/logos.json','utf8'));
if(logos.length!==19||new Set(logos.map(l=>l.slug)).size!==19)errors.push('Logofolio must contain 19 distinct original identities.');
for(const l of logos)try{await access(resolve(root,'.'+l.image));}catch{errors.push(`Missing logo ${l.name}`);}
for(const file of ['main.js','styles.css']){
 const data=await readFile(resolve(root,file));console.log(`${file}: ${(data.length/1024).toFixed(1)} KB / ${(gzipSync(data).length/1024).toFixed(1)} KB gzip`);
}
const home=await readFile(resolve(root,'index.html'),'utf8');
const folio=await readFile(resolve(root,'logofolio/index.html'),'utf8');
const assets=JSON.parse(await readFile('content/master-assets.json','utf8'));
const career=JSON.parse(await readFile('content/career.json','utf8'));
if(career.length!==7||(home.match(/data-career-id=/g)||[]).length!==7)errors.push('Expected exactly seven consolidated career milestones.');
if(career.some((c,i)=>i&&c.start<career[i-1].start))errors.push('Career records must be chronological.');
if(assets.tools.map(t=>t.slug).join(',')!=='photoshop,illustrator,indesign,after-effects,premiere-pro,codex,figma,github,leonardo-ai')errors.push('Expected the nine supplied tools.');
if(/class="project-item|class="logo-flow|class="logo-index/.test(home))errors.push('Home may not embed project or logo galleries.');
if((folio.match(/class="logo-lane"/g)||[]).length!==3)errors.push('Expected exactly three logo lanes.');
if(folio.includes('data-room-mode="gallery"'))errors.push('Paused 3D gallery must not be exposed.');
for(const font of ['beach-sound.woff2','rubik-variable.woff2'])try{await access(resolve(root,'assets/fonts',font));}catch{errors.push(`Missing supplied font ${font}`);}
for(const l of logos){if(!l.width||!l.height)errors.push(`Logo dimensions missing: ${l.name}`);if(l.project)try{await access(resolve(root,'.'+l.project,'index.html'));}catch{errors.push(`Invalid logo project: ${l.name}`);}}
if(assets.brands.length!==4||!['PwC','Dabur','PZ Cussons','Sandtex'].every(name=>assets.brands.some(b=>b.name===name)))errors.push('Expected all four supplied brand logos.');
if(!assets.timelineLogos.pwc||(home.match(/class="career-logo"[^>]*src="\/assets\/master\/brand-pwc.webp"/g)||[]).length!==1)errors.push('PwC must appear in one consolidated milestone.');
if(career.map(c=>c.id).join(',')!=='intelligentsia,nysc,running-jack,citypartner,ferman,redot,pwc')errors.push('Career consolidation/order does not match the approved directive.');
const pwc=career.find(c=>c.id==='pwc');
if(pwc.start!=='2022-02'||pwc.end!==null||pwc.role!=='Senior Graphic Designer'||pwc.progression?.length!==3||!pwc.progression[2].current)errors.push('PwC period/current position/progression incorrect.');
if(home.includes('character-reactions'))errors.push('Visible character controls must be removed.');
const works=await readFile(resolve(root,'work/index.html'),'utf8');
if(!works.includes('works-carousel')||(works.match(/class="project-item/g)||[]).length!==11)errors.push('Works carousel must retain all eleven projects.');
for(const path of pages){const html=await readFile(path,'utf8');if(html.includes('href="/#about" data-nav="about"')||!html.includes('href="/about/" data-nav="about"'))errors.push(`${path}: About must link to its dedicated route.`);if(!html.includes('class="footer-character"')||!html.includes('/assets/icons/linkedin-in.svg')||!html.includes('https://behance.net/eyiladeoridamisi'))errors.push(`${path}: shared contact/footer missing.`);}
const character=JSON.parse(await readFile('content/character.json','utf8'));
const allowed=['idle','wave','thinking','thumbs-up'];
if(Object.keys(character.states).join(',')!==allowed.join(','))errors.push('Hero must use exactly four approved states; blink is excluded.');
for(const state of allowed){const a=character.states[state];if(!a||a.sequence.length!==a.durations.length||a.sequence.some(f=>!Number.isInteger(f)||f<0||f>5)||a.durations.some(d=>d<60))errors.push(`Invalid hero playback: ${state}`);for(const file of [a.atlas,a.poster])try{await access(resolve(root,'.'+file));}catch{errors.push(`Missing hero asset ${file}`);}}
const runtime=await readFile(resolve(root,'main.js'),'utf8');
if(/blink/i.test(home+runtime)||files.some(p=>p.includes('/assets/character/')&&/blink/i.test(p)))errors.push('Blink must not appear in the public hero, runtime or character assets.');
if(!home.includes('character-canvas')||!home.includes('character-poster'))errors.push('Hero needs both sprite canvas and static fallback.');
if(!home.includes('tel:+2348119995647'))errors.push('Exact authorised phone missing.');
if(errors.length){console.error(errors.join('\n'));process.exit(1);}
console.log(`PASS: ${pages.length} pages, ${links} internal references, 19 unique logo assets, image dimensions, page metadata and private-content boundary.`);
