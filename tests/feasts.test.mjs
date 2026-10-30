import test from 'node:test';
import assert from 'node:assert/strict';
import {occasionIndex,canAdvanceOccasion} from '../src/feasts.js';

test('occasion navigation wraps in both directions, including rapid repeated steps',()=>{
 assert.equal(occasionIndex(0,-1,3),2);
 assert.equal(occasionIndex(2,1,3),0);
 assert.equal(occasionIndex(1,8,3),0);
 assert.equal(occasionIndex(0,1,0),0);
});
test('optional playback only advances while visible, permitted and not being read',()=>{
 const ready={playing:true,inView:true,hidden:false,motionOff:false,interacting:false};
 assert.equal(canAdvanceOccasion(ready),true);
 for(const [key,value] of [['playing',false],['inView',false],['hidden',true],['motionOff',true],['interacting',true]])assert.equal(canAdvanceOccasion({...ready,[key]:value}),false,key);
});
