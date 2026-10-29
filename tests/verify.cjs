const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
const match=html.match(/<script id="lab-data" type="application\/json">([\s\S]*?)<\/script>/);
assert.ok(match,'Exercise data missing');
const labs=JSON.parse(match[1]);
assert.equal(labs.length,26);
assert.equal(labs.reduce((n,l)=>n+l.tests.length,0),68);
assert.equal(new Set(labs.map(l=>l.id)).size,labs.length);
for(const l of labs){assert.ok(l.tests.length>=2);assert.ok(l.solution&&l.starter&&l.hint);}
assert.ok(!html.includes('C:\\Users\\'));
assert.ok(!html.includes('wagwa'));
assert.ok(!html.includes('코드실습_시작.vbs'));
assert.ok(html.includes('https://atozuser0224.github.io/r-python-study-lab/'));
assert.ok(html.includes('worker.terminate()'));
assert.ok(html.includes('실행 시간 12초'));
console.log('PASS: 26 labs, 68 checks, portable links, and public-content boundary');
