import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const html=await readFile(new URL('./index.html',import.meta.url),'utf8');
const app=await readFile(new URL('./app.js',import.meta.url),'utf8');
const css=await readFile(new URL('./studio.css',import.meta.url),'utf8');
test('every direct DOM id used by the app exists in the studio HTML',()=>{const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]));for(const [,id] of app.matchAll(/\$\(['"]([^'"]+)['"]\)/g))assert.ok(ids.has(id),`Missing DOM id #${id}`)});
test('studio has no remote origins or runtime service calls',()=>{assert.doesNotMatch(html,/https?:\/\//i);assert.doesNotMatch(app,/https?:\/\//i);assert.doesNotMatch(css,/https?:\/\//i);assert.match(app,/fetch\(`samples\//);assert.doesNotMatch(app,/fetch\(['"]https?:/i)});
test('required UI areas, local import and export controls are present',()=>{for(const label of ['Story','Direction','Sound &amp; voice','Assets','Import project','Export project JSON','Export video','Download blank story template'])assert.ok(html.includes(label),`Missing UI action: ${label}`)});
