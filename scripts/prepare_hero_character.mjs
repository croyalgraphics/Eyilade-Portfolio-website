import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createRequire} from 'node:module';import {resolve} from 'node:path';import {createHash} from 'node:crypto';
const require=createRequire(import.meta.url);const sharp=require('/Users/joshuaoridamisi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const source=resolve('artwork/eyilade-smooth-v2');const target=resolve('dist/assets/character');await mkdir(target,{recursive:true});
const original=JSON.parse(await readFile(source+'/manifest.json','utf8'));const allowed=['idle','wave','thinking','thumbs-up'];const stillFrame={idle:0,wave:2,thinking:3,'thumbs-up':3};
const output={version:2,style:'smooth-illustration',width:512,height:768,columns:3,states:{}};const provenance=[];
for(const name of allowed){
 const a=original.animations[name];const sheet=await readFile(source+'/'+a.sheet);const atlas=name+'-atlas.webp';await sharp(sheet).webp({quality:88,alphaQuality:100,effort:6}).toFile(target+'/'+atlas);
 const frame=a.frames[stillFrame[name]];const still=await readFile(source+'/'+frame.file);const poster=name+'-still.webp';await sharp(still).webp({quality:90,alphaQuality:100,effort:6}).toFile(target+'/'+poster);
 output.states[name]={atlas:'/assets/character/'+atlas,poster:'/assets/character/'+poster,sequence:a.playback.sequence,durations:a.playback.durations};
 provenance.push({state:name,sourceSheet:'artwork/eyilade-smooth-v2/'+a.sheet,sourceSha256:createHash('sha256').update(sheet).digest('hex'),sourceStill:frame.file,frameCount:a.frames.length,atlasBytes:(await readFile(target+'/'+atlas)).length,posterBytes:(await readFile(target+'/'+poster)).length});
}
await sharp(source+'/frames/idle/idle_01.png').resize(320,480,{kernel:'lanczos3'}).webp({quality:90,alphaQuality:100,effort:6}).toFile(target+'/idle-still-320.webp');
await writeFile('content/character.json',JSON.stringify(output,null,2)+'\n');await writeFile('docs/HERO_CHARACTER_ASSETS.json',JSON.stringify({allowedStates:allowed,excludedState:'blink',exports:provenance},null,2)+'\n');console.log(provenance.map(p=>({state:p.state,atlasKB:Math.round(p.atlasBytes/1024),posterKB:Math.round(p.posterBytes/1024)})));
