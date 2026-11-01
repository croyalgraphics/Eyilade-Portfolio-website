import { readFile, readdir, stat, access } from 'node:fs/promises';
import { resolve, extname } from 'node:path';
import { gzipSync } from 'node:zlib';
import { createHash } from 'node:crypto';
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
if(assets.tools.map(t=>t.slug).join(',')!=='photoshop,illustrator,indesign,after-effects,premiere-pro,codex,figma,github,leonardo-ai,canva')errors.push('Expected the ten supplied tools, including Canva.');
if(/class="project-item|class="logo-flow|class="logo-index/.test(home))errors.push('Home may not embed project or logo galleries.');
if((folio.match(/class="logo-lane"/g)||[]).length!==3)errors.push('Expected exactly three logo lanes.');
if(folio.includes('data-room-mode="gallery"'))errors.push('Paused 3D gallery must not be exposed.');
for(const font of ['beach-sound.woff2','rubik-variable.woff2'])try{await access(resolve(root,'assets/fonts',font));}catch{errors.push(`Missing supplied font ${font}`);}
for(const l of logos){if(!l.width||!l.height)errors.push(`Logo dimensions missing: ${l.name}`);if(l.project)try{await access(resolve(root,'.'+l.project,'index.html'));}catch{errors.push(`Invalid logo project: ${l.name}`);}}
if(assets.brands.length!==6||!['PwC','Dabur','PZ Cussons','Sandtex','Carex','IOSA Freight'].every(name=>assets.brands.some(b=>b.name===name)))errors.push('Expected all six supplied brand logos.');
if(!assets.timelineLogos.pwc||(home.match(/class="career-logo"[^>]*src="\/assets\/master\/brand-pwc.webp"/g)||[]).length!==1)errors.push('PwC must appear in one consolidated milestone.');
if(career.map(c=>c.id).join(',')!=='intelligentsia,nysc,running-jack,citypartner,ferman,redot,pwc')errors.push('Career consolidation/order does not match the approved directive.');
const pwc=career.find(c=>c.id==='pwc');
if(pwc.start!=='2022-02'||pwc.end!==null||pwc.role!=='Senior Graphic Designer'||pwc.progression?.length!==3||!pwc.progression[2].current)errors.push('PwC period/current position/progression incorrect.');
if(home.includes('character-reactions'))errors.push('Visible character controls must be removed.');
const works=await readFile(resolve(root,'work/index.html'),'utf8');
if(!works.includes('works-carousel')||(works.match(/class="project-item/g)||[]).length!==11)errors.push('Works carousel must retain all eleven projects.');
for(const path of pages){const html=await readFile(path,'utf8');if(html.includes('href="/#about" data-nav="about"')||!html.includes('href="/about/" data-nav="about"'))errors.push(`${path}: About must link to its dedicated route.`);if(!html.includes('class="footer-character"')||!html.includes('/assets/icons/linkedin-in.svg')||!html.includes('https://behance.net/eyiladeoridamisi'))errors.push(`${path}: shared contact/footer missing.`);}
if(career.find(c=>c.id==='nysc').company!=='Federal government of Nigeria')errors.push('NYSC organization correction missing.');
for(const key of ['citypartner','redot','ferman','nysc']){if(!assets.timelineLogos[key]||career.find(c=>c.id===key)?.logoKey!==key)errors.push(`Missing supplied career mark ${key}`);}
if(works.includes('carousel-toggle')||works.includes('class="project-caption"><div><h3')&&/<h3>[^<]*<\/h3><p>/.test(works))errors.push('Carousel pause control or short descriptions must not remain.');
for(const path of pages){const html=await readFile(path,'utf8');if(!html.includes('class="utility-controls"')||!html.includes('theme-toggle')||!html.includes('>Eyilade<span'))errors.push(`${path}: shared utility controls or wordmark missing.`);const footer=html.slice(html.indexOf('<footer'),html.indexOf('</footer>'));if(footer.includes('More about me')||!footer.includes('Get my Portfolio')||!footer.includes('Get my CV'))errors.push(`${path}: revised download actions missing.`);if(!footer.includes('aria-label="LinkedIn profile"')||!footer.includes('aria-label="Behance portfolio"')||!footer.includes('aria-label="Copy email address"'))errors.push(`${path}: icon action labels missing.`);}
const character=JSON.parse(await readFile('content/character.json','utf8'));
const allowed=['idle','wave','thinking','thumbs-up'];
if(Object.keys(character.states).join(',')!==allowed.join(','))errors.push('Hero must use exactly four approved states; blink is excluded.');
for(const state of allowed){const a=character.states[state];if(!a||a.sequence.length!==a.durations.length||a.sequence.some(f=>!Number.isInteger(f)||f<0||f>5)||a.durations.some(d=>d<60))errors.push(`Invalid hero playback: ${state}`);for(const file of [a.atlas,a.poster])try{await access(resolve(root,'.'+file));}catch{errors.push(`Missing hero asset ${file}`);}}
const runtime=await readFile(resolve(root,'main.js'),'utf8');
if(/blink/i.test(home+runtime)||files.some(p=>p.includes('/assets/character/')&&/blink/i.test(p)))errors.push('Blink must not appear in the public hero, runtime or character assets.');
if(!home.includes('character-canvas')||!home.includes('character-poster'))errors.push('Hero needs both sprite canvas and static fallback.');
if(!home.includes('tel:+2348119995647'))errors.push('Exact authorised phone missing.');
// Latest refinement contract: remove redundant controls while preserving their content and destinations.
const hero=home.slice(home.indexOf('<section class="cv-hero"'),home.indexOf('</section>'));
if(/<a\b|hero-actions|hero-download|Meet the person/.test(hero))errors.push('Homepage hero must contain no redundant CTA links or wrappers.');
if(/career-detail|career-dialog|What I did|My work at PwC/.test(home))errors.push('Career-detail actions/dialog must be removed from all milestones.');
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const c of career)if(c.description&&!home.includes(`<p class="career-description">${escapeHTML(c.description)}</p>`))errors.push(`Approved career description must remain directly readable: ${c.id}`);
for(const path of pages){const html=await readFile(path,'utf8');if(/class="(?:discipline-number|pathway-number|project-index|case-number|career-order)"|class="section-kicker"><span>\d/.test(html))errors.push(`${path}: decorative numerical identifier remains.`);const footer=html.slice(html.indexOf('<footer'),html.indexOf('</footer>'));if(!footer.includes('Have a project/role in mind?')||!footer.includes('Let’s make<br><em>something together.</em>'))errors.push(`${path}: revised footer invitation missing.`);}
if(/Brand identities, visual stories,<br>and considered experiences\.|Explore logofolio/.test(works.slice(works.indexOf('<main'),works.indexOf('works-carousel'))))errors.push('Redundant Work intro content remains.');
if(!works.includes('data-dwell-ms="10000" data-transition-ms="500"'))errors.push('Carousel hold and transition must be configured independently.');
for(const direction of ['-1','1'])if(!new RegExp(`data-career-step="${direction}"[^>]*><svg`).test(home))errors.push(`Career navigation ${direction} must use an accessible icon.`);
if(!home.includes('2022–')||!home.includes('01 / 7')||!works.includes('01 / 11'))errors.push('Meaningful dates and navigation counts must be preserved.');
// Beans Central: the expanded project must remain a complete, original-asset-led case study.
const beans=await readFile(resolve(root,'work/beans-central/index.html'),'utf8');
const beansManifest=JSON.parse(await readFile(resolve(root,'assets/beans-central/artwork-manifest.json'),'utf8'));
for(const dish of beansManifest.dishes){
 for(const file of [`food-${dish.slug}.webp`,...['640','1280','1600'].map(size=>`campaign-${dish.slug}-${size}.webp`)])try{await access(resolve(root,'assets/beans-central',file));}catch{errors.push(`Missing Beans Central dish artwork: ${file}`);}
 if(!beans.includes(`data-dish="${dish.slug}"`)||!beans.includes(`campaign-${dish.slug}-1280.webp`))errors.push(`Beans Central dish missing from case study: ${dish.name}`);
}
for(const a of beansManifest.artworks)for(const size of [640,1280,1600])try{await access(resolve(root,'assets/beans-central',`${a.name}-${size}.webp`));}catch{errors.push(`Missing Beans Central responsive export: ${a.name}-${size}`);}
if(beansManifest.dishes.length!==6||!beans.includes('AI-assisted photography and mockups')||!beans.includes('data-beans-player'))errors.push('Beans Central must contain six dishes, truthful concept context and the motion sequence.');
if(/09076468999|fast delivery|healthy|nutritiously/i.test(beans))errors.push('Unverified original business claims/order number may not appear in the new Beans Central case.');
const liz=await readFile(resolve(root,'work/lizcraft/index.html'),'utf8');
const lizManifest=JSON.parse(await readFile(resolve(root,'assets/lizcraft/artwork-manifest.json'),'utf8'));
for(const a of lizManifest.artworks)for(const size of [640,1280,1800])try{await access(resolve(root,'assets/lizcraft',`${a.name}-${size}.webp`));}catch{errors.push(`Missing LizCraft responsive export: ${a.name}-${size}`);}
if((liz.match(/class="lc-contour-ring"/g)||[]).length!==8)errors.push('LizCraft must animate the eight actual original contour paths.');
for(const text of ['Hand wash gently','Use mild soap','Do not bleach','Do not machine wash','Do not iron'])if(!liz.includes(`<li>${text}</li>`))errors.push(`LizCraft care instruction missing: ${text}`);
if(!liz.includes('data-parcel-select="parcel-closed-modern"')||!liz.includes('data-parcel-select="parcel-open-modern"')||!liz.includes('AI-assisted visualisations'))errors.push('LizCraft parcel controls or truthful concept context missing.');
if(files.some(p=>p.includes('/assets/lizcraft/')&&/sf.?compact/i.test(p)))errors.push('SF Compact may not be redistributed with the new LizCraft assets.');
const pure=await readFile(resolve(root,'work/purehive/index.html'),'utf8');
const pureManifest=JSON.parse(await readFile(resolve(root,'assets/purehive/artwork-manifest.json'),'utf8'));
for(const a of pureManifest.artworks)for(const size of [640,1280,1800])try{await access(resolve(root,'assets/purehive',`${a.name}-${size}.webp`));}catch{errors.push(`Missing Pure Hive responsive export: ${a.name}-${size}`);}
if(!pure.includes('AI-assisted visualisations with fictional models')||[0,1,2].some(i=>!pure.includes(`data-ph-scene-select="${i}"`)))throw Error('Pure Hive concept context or scene controls missing');
for(const name of ['dress-modern','woman-modern','man-modern','family-modern','objects-modern','making-modern'])if(!liz.includes(`/assets/lizcraft/${name}-1280.webp`))throw Error(`Missing LizCraft human or collection scene: ${name}`);
if(files.some(p=>p.includes('/assets/purehive/')&&/american.?typewriter/i.test(p)))throw Error('Apple font may not be redistributed');
const feasts=await readFile(resolve(root,'work/feasts-and-flavours/index.html'),'utf8');
const feastsManifest=JSON.parse(await readFile(resolve(root,'assets/feasts/artwork-manifest.json'),'utf8'));
for(const a of feastsManifest.artworks)for(const size of [640,1280,1800])try{await access(resolve(root,'assets/feasts',`${a.name}-${size}.webp`));}catch{errors.push(`Missing Feasts responsive export: ${a.name}-${size}`);}
for(const name of ['owanbe-service','wedding-reception','birthday-celebration','professional-service','shared-table','pass-a-bowl','curry-bowl','rice-chicken','crispy-chicken','guest-table','takeaway-service'])if(!feasts.includes(`/assets/feasts/${name}-1280.webp`))errors.push(`Missing Feasts event or preserved lifestyle scene: ${name}`);
if(!feasts.includes('Professional catering')||!feasts.includes('fictional models')||[0,1,2].some(i=>!feasts.includes(`data-ff-select="${i}"`)))errors.push('Feasts catering context, scene controls or concept provenance missing.');
if((feasts.match(/class="ff-rosette-part"/g)||[]).length!==8)errors.push('Feasts must preserve the eight original rosette paths.');
if(/09076468999|fast delivery|healthy|nutritiously/i.test(feasts))errors.push('Unverified business claims or old ordering number in new Feasts case.');
if(files.some(p=>p.includes('/assets/feasts/')&&/funky.?bird.*\.(ttf|otf|woff2?)$/i.test(p)))errors.push('Personal-use Funky Bird font may not be redistributed.');
const natoral=await readFile(resolve(root,'work/natoral/index.html'),'utf8');
const natoralManifest=JSON.parse(await readFile(resolve(root,'assets/natoral-supplied/artwork-manifest.json'),'utf8'));
for(const a of natoralManifest.artworks)for(const size of [640,1280,1800])try{await access(resolve(root,'assets/natoral-supplied',`${a.name}-${size}.webp`));}catch{errors.push(`Missing Natoral responsive export: ${a.name}-${size}`);}
for(const name of ['Dewskin','Softmelt','Root Ritual','Curl Veil','First Spoon','Little Drops','Form Daily'])if(!natoral.includes(name))errors.push(`Natoral proposed product name missing: ${name}`);
for(const range of ['body','hair','baby','active'])if(!natoral.includes(`data-nt-range-select="${range}"`))errors.push(`Natoral range control missing: ${range}`);
if(!natoral.includes('proposed concepts')||!natoral.includes('fictional models')||!natoral.includes('data-nt-view-select="artwork"'))errors.push('Natoral concept context or artwork view missing.');
if(natoralManifest.revision!=='owner-supplied-N1-N8'||natoralManifest.sources?.length!==8)errors.push('Natoral must use all eight supplied packaging masters.');
for(const source of natoralManifest.sources||[]){
 const bytes=await readFile(resolve(root,'assets/natoral-supplied',source.file));
 if(createHash('sha256').update(bytes).digest('hex')!==source.sha256)errors.push(`Supplied Natoral original changed: ${source.file}`);
}
if(/\/assets\/natoral(?:-v2)?\/(?:body|hair|baby|active|family|campaign|dispatch|label|type|range|digital|project)-/.test(natoral))errors.push('Superseded Natoral packaging imagery remains in the project.');

if(errors.length){console.error(errors.join('\n'));process.exit(1);}
console.log(`PASS: ${pages.length} pages, ${links} internal references, 19 unique logo assets, image dimensions, page metadata and private-content boundary.`);
