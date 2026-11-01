import test from 'node:test';
import assert from 'node:assert/strict';
import {rangeState} from '../src/natoral.js';

test('range browsing keeps artwork choice when changing category and safely normalises invalid state',()=>{
 assert.deepEqual(rangeState('hair','artwork'),{range:'hair',view:'artwork'});
 assert.deepEqual(rangeState('baby','artwork'),{range:'baby',view:'artwork'});
 assert.deepEqual(rangeState('active','photo'),{range:'active',view:'photo'});
 assert.deepEqual(rangeState('missing','invalid'),{range:'body',view:'photo'});
});
