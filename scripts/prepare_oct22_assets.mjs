/** Mechanical, local-only exports for the supplied 22 October asset additions.
 * Run: node scripts/prepare_oct22_assets.mjs
 * Uses the Codex bundled sharp runtime; override with SHARP_MODULE if required.
 * Originals are read only. Crops preserve logo pixels, colours and aspect ratios.
 */
import { createRequire } from 'node:module';
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const require = createRequire(import.meta.url);
const sharp = require(process.env.SHARP_MODULE || '/Users/joshuaoridamisi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = fileURLToPath(new URL('../', import.meta.url));
const out = path.join(root, 'dist/assets/master');
await mkdir(out, { recursive: true });
const jobs = [
  { group:'timelineLogos', slug:'citypartner', name:'Citypartner', source:'Citypartner healthcare.webp', file:'logo-citypartner.webp', crop:[160,138,322,358], box:[400,400] },
  { group:'timelineLogos', slug:'redot', name:'Redot Digital', source:'Redot-Icon.jpg', file:'logo-redot.webp', crop:[250,237,579,605], box:[400,400] },
  { group:'timelineLogos', slug:'ferman', name:'Ferman', source:'Ferman digital.jpeg', file:'logo-ferman.webp', crop:[0,62,400,275], box:[400,300] },
  { group:'timelineLogos', slug:'nysc', name:'NYSC', source:'NYSC_LOGO.svg', file:'logo-nysc.webp', trim:true, box:[320,400] },
  { group:'brands', slug:'carex', name:'Carex', source:'Carex-Logo.png', file:'brand-carex.webp', trim:true, box:[480,260] },
  { group:'brands', slug:'iosa-freight', name:'IOSA Freight', source:'IOSA-logo-1.png', file:'brand-iosa-freight.webp', trim:true, box:[480,260] },
  { group:'tools', slug:'canva', name:'Canva', source:'canva-icon-logo.png', file:'tool-canva.webp', trim:true, box:[192,192] },
];
const dataPath = path.join(root,'content/master-assets.json');
const master = JSON.parse(await readFile(dataPath,'utf8'));
const records = [];
for (const job of jobs) {
  const source = path.join(root,'Assets/Career and skills',job.source);
  const original = await readFile(source);
  if (job.source.endsWith('.svg')) {
    const xml = original.toString('utf8');
    if (/<(?:script|foreignObject|image)\b|(?:href|onload)\s*=/i.test(xml)) throw new Error(`SVG requires manual resource review: ${job.source}`);
  }
  const metadata = await sharp(original).metadata();
  const {data:raw,info} = await sharp(original,{density:144}).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  let crop = job.crop;
  if (job.trim) {
    let left=info.width, top=info.height, right=0, bottom=0;
    for(let y=0;y<info.height;y++) for(let x=0;x<info.width;x++) {
      if(raw[(y*info.width+x)*4+3]>4) {left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x+1);bottom=Math.max(bottom,y+1);}
    }
    if(right===0) throw new Error(`No visible artwork: ${job.source}`);
    const pad=Math.max(2,Math.round(Math.max(right-left,bottom-top)*.02));
    const x=Math.max(0,left-pad), y=Math.max(0,top-pad);
    crop=[x,y,Math.min(info.width,right+pad)-x,Math.min(info.height,bottom+pad)-y];
  }
  const target=path.join(out,job.file);
  const result=await sharp(raw,{raw:{width:info.width,height:info.height,channels:4}})
    .extract({left:crop[0],top:crop[1],width:crop[2],height:crop[3]})
    .resize({width:job.box[0],height:job.box[1],fit:'inside',withoutEnlargement:true,kernel:'lanczos3'})
    .webp({lossless:true,effort:6}).toFile(target);
  const item={name:job.name,slug:job.slug,image:'/assets/master/'+job.file,width:result.width,height:result.height,source:'Assets/Career and skills/'+job.source};
  if(job.group==='timelineLogos') master.timelineLogos[job.slug]={image:item.image,width:item.width,height:item.height,source:item.source};
  else {const index=master[job.group].findIndex(x=>x.slug===job.slug);if(index>=0)master[job.group][index]=item;else master[job.group].push(item);}
  records.push({...item,sha256:createHash('sha256').update(original).digest('hex'),sourceBytes:(await stat(source)).size,sourceWidth:metadata.width,sourceHeight:metadata.height,decodedWidth:info.width,decodedHeight:info.height,crop,bytes:result.size});
}
await writeFile(dataPath,JSON.stringify(master,null,2)+'\n');
let notes=`# Supplied asset additions — 22 October 2026\n\nPrepared with \`node scripts/prepare_oct22_assets.mjs\` using local Sharp. No external artwork or services were used. All seven originals remain unchanged. Exports use lossless WebP, Lanczos downsampling only where required, and no enlargement of raster sources. Original colours and the cropped artwork's aspect ratio are retained. Metadata is stripped.\n\nThe transparent sources are cropped to alpha bounds with a 2% safety margin. The opaque Citypartner, Redot and Ferman sources use visually reviewed explicit crops; no background replacement or logo recreation is performed. Citypartner's supplied pale gradient and the white backgrounds of the two JPEGs remain. The NYSC SVG is locally rasterised at 144 DPI before cropping/export.\n\n## Export record\n\nCrop notation: left, top, width, height in decoded source pixels. NYSC source dimensions in the table are its default 72 DPI raster bounds; it is decoded at 144 DPI.\n\n| Artwork | Source dimensions | Decoded crop | Export dimensions | Source / export bytes |\n|---|---|---|---|---|\n`;
for(const r of records)notes+=`| ${r.name} | ${r.sourceWidth} × ${r.sourceHeight} | ${r.crop.join(', ')} | ${r.width} × ${r.height} | ${r.sourceBytes.toLocaleString('en-US')} / ${r.bytes.toLocaleString('en-US')} |\n`;
notes+='\n## Provenance and original SHA-256\n\nAll source files were supplied by the site owner under `Assets/Career and skills/`. This export records provenance, not a new grant of trademark rights.\n\n';
for(const r of records)notes+=`- **${r.name}**: \`${r.source}\` → \`${r.image}\`\n  - SHA-256: \`${r.sha256}\`\n`;
notes+='\n## Artwork observations\n\n- The file `Ferman digital.jpeg` visibly spells **Feman Media Agency**. Its original lettering and artwork are preserved; the timeline label remains the approved career name Ferman. No spelling correction has been painted into the logo.\n- IOSA artwork visibly reads **iosa FREIGHT LIMITED**. It is mapped to the owner-requested display name IOSA Freight.\n- The supplied Ferman JPEG artwork touches its left and right image edges. The export keeps the entire original width and does not invent missing pixels.\n- Carex is the supplied Cussons Carex lockup; it is an additional brand entry alongside the separate PZ Cussons corporate mark.\n- Existing four brands and nine toolkit entries are retained, with Carex / IOSA Freight and Canva appended.\n';
await writeFile(path.join(root,'docs/OCT22_ASSET_NOTES.md'),notes);
console.log(JSON.stringify({exports:records.map(({name,image,width,height,bytes,crop})=>({name,image,width,height,bytes,crop})),brands:master.brands.length,tools:master.tools.length},null,2));
