import test from 'node:test';
import assert from 'node:assert/strict';
import {nextNavigationState} from '../src/navigation.js';
import {resolveMotionPreference,resolveThemePreference} from '../src/preferences.js';
import {careerProgress} from '../src/career.js';
import {carouselOffset,shouldAutoplay,carouselTiming} from '../src/carousel.js';

test('preferences use system defaults, while explicit choices survive differing systems',()=>{
 assert.equal(resolveMotionPreference(null,true),true);
 assert.equal(resolveMotionPreference('on',true),false);
 assert.equal(resolveMotionPreference('off',false),true);
 assert.equal(resolveThemePreference(null,true),'dark');
 assert.equal(resolveThemePreference('light',true),'light');
 assert.equal(resolveThemePreference('dark',false),'dark');
 assert.equal(resolveThemePreference('invalid',false),'light');
});
test('navigation protects introductions, ignores jitter and reveals promptly on reversal',()=>{
 let state={hidden:false,lastY:0,direction:0,distance:0};
 const move=(y,locked=false)=>state=nextNavigationState(state,{y,threshold:400,locked});
 assert.equal(move(390).hidden,false);
 assert.equal(move(410).hidden,false);
 assert.equal(move(411).hidden,false);
 assert.equal(move(430).hidden,true);
 assert.equal(move(425).hidden,true);
 assert.equal(move(419).hidden,false);
 assert.equal(move(600,true).hidden,false);
 assert.equal(move(640).hidden,true);
 assert.equal(move(0).hidden,false);
});
test('all seven career milestones are reachable in both scroll directions without boundary overflow',()=>{
 for(const i of [0,1,2,3,4,5,6,5,4,3,2,1,0]){
  const position=careerProgress(900+i*280,900,1680,7);
  assert.equal(position.index,i);
  assert.equal(position.step,i);
 }
 assert.equal(careerProgress(-100,900,1680,7).index,0);
 assert.equal(careerProgress(9000,900,1680,7).index,6);
 assert.equal(careerProgress(900,900,0,1).index,0);
});
test('carousel pauses for each interaction, visibility and motion condition independently',()=>{
 const ready={off:false,hover:false,focused:false,touching:false,visible:true,hidden:false,count:11};
 assert.equal(shouldAutoplay(ready),true);
 for(const key of ['off','hover','focused','touching','hidden'])assert.equal(shouldAutoplay({...ready,[key]:true}),false,key);
 assert.equal(shouldAutoplay({...ready,visible:false}),false);
 assert.equal(shouldAutoplay({...ready,count:1}),false);
 assert.equal(shouldAutoplay({...ready,count:0}),false);
});
test('carousel wraparound keeps adjacent projects on the correct side',()=>{
 assert.equal(carouselOffset(10,0,11),-1);
 assert.equal(carouselOffset(0,10,11),1);
 assert.equal(carouselOffset(5,5,11),0);
 assert.equal(carouselOffset(0,0,1),0);
});
test('carousel viewing time and movement time are independent and bounded',()=>{
 assert.deepEqual(carouselTiming(undefined,undefined),{dwell:10000,transition:500});
 assert.deepEqual(carouselTiming('12000','300'),{dwell:12000,transition:300});
 assert.deepEqual(carouselTiming('90000','50'),{dwell:20000,transition:200});
});
