import * as THREE from 'three';
const stage=document.querySelector('.room-stage');
const host=document.querySelector('.room-canvas');
const logos=await fetch('/assets/logos.json').then(r=>r.json());
let selected=9,paused=false,off=document.documentElement.classList.contains('motion-off'),drag=false,lastX=0,startX=0,visible=true,mode='gallery';
const step=Math.PI*2/logos.length;
let current=-selected*step,target=current,frame=0,lastTime=0,settledAt=performance.now(),renderer,scene,camera;
const count=document.querySelector('#logo-count'),name=document.querySelector('#logo-name'),fallback=document.querySelector('#fallback-logo'),pause=document.querySelector('#room-pause');
const sculptures=[];
function updateCaption(index){selected=((index%logos.length)+logos.length)%logos.length;const l=logos[selected];count.textContent=`${String(selected+1).padStart(2,'0')} / ${logos.length}`;name.textContent=l.name;fallback.src=l.image;fallback.alt=l.name+' logo';}
function go(delta){target-=delta*step;target=Math.round(target/step)*step;updateCaption(Math.round(-target/step));settledAt=performance.now();start();}
document.querySelector('#logo-prev').addEventListener('click',()=>go(-1));
document.querySelector('#logo-next').addEventListener('click',()=>go(1));
document.querySelector('#inspect-logo').addEventListener('click',()=>{paused=true;pause.setAttribute('aria-pressed','true');pause.textContent='Resume movement';document.dispatchEvent(new CustomEvent('portfolio:logo-open',{detail:{index:selected}}));});
stage.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();go(e.key==='ArrowRight'?1:-1);}});
pause.addEventListener('click',()=>{paused=!paused;pause.setAttribute('aria-pressed',String(paused));pause.textContent=paused?'Resume movement':'Pause movement';settledAt=performance.now();start();});
document.addEventListener('portfolio:motion',e=>{off=e.detail.off;settledAt=performance.now();start();});
document.addEventListener('portfolio:room-mode',e=>{mode=e.detail.mode;if(mode==='gallery'){resize();start();}});
document.addEventListener('visibilitychange',()=>{if(!document.hidden){settledAt=performance.now();start();}});
new IntersectionObserver(([e])=>{visible=e.isIntersecting;if(visible){settledAt=performance.now();start();}},{threshold:.05}).observe(stage);
stage.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag=true;lastX=startX=e.clientX;stage.setPointerCapture(e.pointerId);});
stage.addEventListener('pointermove',e=>{if(!drag)return;target+=(e.clientX-lastX)*.006;lastX=e.clientX;start();});
function endDrag(){if(!drag)return;drag=false;target=Math.round(target/step)*step;updateCaption(Math.round(-target/step));settledAt=performance.now();start();}
stage.addEventListener('pointerup',endDrag);stage.addEventListener('pointercancel',endDrag);
function resize(){if(!renderer||!stage.clientWidth||!stage.clientHeight)return;const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.position.z=w<500?14.2:w<800?12:10.3;camera.updateProjectionMatrix();start();}
function start(){if(renderer&&!frame&&visible&&mode==='gallery'&&!document.hidden){lastTime=performance.now();frame=requestAnimationFrame(draw);}}
function draw(time){
  frame=0;if(!visible||mode!=='gallery'||document.hidden)return;
  const dt=Math.min((time-lastTime)/1000,.05);lastTime=time;
  if(!drag&&!paused&&!off&&time-settledAt>6500){target-=step;updateCaption(Math.round(-target/step));settledAt=time;}
  current=off?target:THREE.MathUtils.damp(current,target,8,dt);
  sculptures.forEach((group,i)=>{
    const a=i*step+current;
    group.position.set(Math.sin(a)*8.1,Math.sin(a*2)*.22+(off?0:Math.sin(time*.0008+i)*.045),Math.cos(a)*8.1-8.1);
    group.rotation.set(off?0:Math.sin(time*.0005+i)*.012,a,0);
  });
  renderer.render(scene,camera);
  if((!paused&&!off)||drag||Math.abs(current-target)>.0001)frame=requestAnimationFrame(draw);
}
try{
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.setClearColor(0xf4f2eb,0);
  scene=new THREE.Scene();scene.fog=new THREE.Fog(0xf4f2eb,17,36);
  camera=new THREE.PerspectiveCamera(32,1,.1,60);camera.position.set(0,.8,10.3);camera.lookAt(0,0,-2);
  scene.add(new THREE.AmbientLight(0xffffff,2.3));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(-3,6,8);scene.add(light);
  const rim=new THREE.DirectionalLight(0xffd5b8,1);rim.position.set(5,2,-4);scene.add(rim);
  const loader=new THREE.TextureLoader();
  const textures=await Promise.all(logos.map(l=>loader.loadAsync(l.image).catch(()=>null)));
  const geometry=new THREE.BoxGeometry(3.15,2.62,.065);
  const sideMaterial=new THREE.MeshStandardMaterial({color:0xe6e4d8,roughness:.75});
  for(const [i,l] of logos.entries()){
    const tex=textures[i];if(tex){tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=Math.min(4,renderer.capabilities.getMaxAnisotropy());}
    const body=new THREE.Mesh(geometry,sideMaterial);
    const face=new THREE.Mesh(new THREE.PlaneGeometry(3.13,2.6),new THREE.MeshBasicMaterial({map:tex,color:tex?0xffffff:0xf4f2eb,toneMapped:false}));face.position.z=.034;
    // Preserve each logo's original proportions; Natoral's original is square.
    if(l.slug==='natoral'){face.scale.x=2.6/3.13;const white=new THREE.Mesh(new THREE.PlaneGeometry(3.13,2.6),new THREE.MeshBasicMaterial({color:0xf4fffa}));white.position.z=.033;body.add(white);}
    const group=new THREE.Group();group.add(body,face);sculptures.push(group);scene.add(group);
  }
  host.append(renderer.domElement);resize();stage.classList.add('webgl-ready');start();
  new ResizeObserver(resize).observe(stage);
  renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();stage.classList.remove('webgl-ready');if(frame)cancelAnimationFrame(frame);frame=0;});
  renderer.domElement.addEventListener('webglcontextrestored',()=>{stage.classList.add('webgl-ready');start();});
}catch{
  renderer?.dispose();renderer=null;stage.classList.remove('webgl-ready');
  pause.hidden=true;document.querySelector('.room-bottom>span').textContent='USE PREVIOUS AND NEXT TO EXPLORE EACH IDENTITY';
}
