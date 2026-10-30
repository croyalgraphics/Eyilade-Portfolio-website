import test from 'node:test';
import assert from 'node:assert/strict';
import {revealPercent} from '../src/purehive.js';

test('Pure Hive reveal remains bounded and advances across mobile and desktop reading positions',()=>{
 for(const viewport of [568,844,900,1080]){
  const height=viewport<800?1100:800;
  assert.equal(revealPercent(viewport*2,height,viewport),0);
  assert.equal(revealPercent(-height,height,viewport),100);
  const levels=Array.from({length:30},(_,i)=>revealPercent(viewport-i*(height+viewport)/29,height,viewport));
  assert.ok(levels.every(n=>n>=0&&n<=100));assert.ok(levels.every((n,i)=>!i||n>=levels[i-1]));
 }
});
