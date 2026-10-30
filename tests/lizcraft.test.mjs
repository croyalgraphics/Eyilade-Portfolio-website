import test from 'node:test';
import assert from 'node:assert/strict';
import {contourLevel} from '../src/lizcraft.js';

test('LizCraft contour progress stays bounded and advances in reading order across viewport sizes',()=>{
 for(const viewport of [568,844,900,1080]){
  const height=viewport<800?1100:800;
  assert.equal(contourLevel(viewport*2,height,viewport),1);
  assert.equal(contourLevel(-height,height,viewport),8);
  const levels=Array.from({length:30},(_,i)=>contourLevel(viewport-i*(height+viewport)/29,height,viewport));
  assert.ok(levels.every(n=>Number.isInteger(n)&&n>=1&&n<=8));
  assert.ok(levels.every((n,i)=>!i||n>=levels[i-1]));
 }
});
