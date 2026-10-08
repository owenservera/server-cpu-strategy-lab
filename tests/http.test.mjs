import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { setTimeout as wait } from 'node:timers/promises';

test('built-in server returns static dashboard and JavaScript modules',async()=>{
  const port=51987;
  const child=spawn(process.execPath,['server.mjs'],{cwd:new URL('..',import.meta.url),env:{...process.env,PORT:String(port)},stdio:'ignore'});
  try{
    let response;
    for(let attempt=0;attempt<25;attempt++){
      try{response=await fetch(`http://127.0.0.1:${port}/`);break;}catch{await wait(70);}
    }
    assert.ok(response,'Server did not start');
    assert.equal(response.status,200);
    assert.match(response.headers.get('content-type'),/text\/html/);
    assert.match(await response.text(),/The compute/);
    const moduleResponse=await fetch(`http://127.0.0.1:${port}/data.js`);
    assert.equal(moduleResponse.status,200);
    assert.match(moduleResponse.headers.get('content-type'),/javascript/);
    assert.match(await moduleResponse.text(),/AMD6RAMP/);
    const bad=await fetch(`http://127.0.0.1:${port}/not-here`);
    assert.equal(bad.status,404);
  }finally{child.kill();}
});