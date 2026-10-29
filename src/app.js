(() => {
  'use strict';
  const labs = JSON.parse(document.getElementById('lab-data').textContent);
  const homepage = 'https://atozuser0224.github.io/r-python-study-lab/';
  const storageKey = 'practice-code-labs-v1';
  const records = new Map(), engines = new Map();
  let saved = {}, storageOK = true, active = null;
  try {
    const stored=JSON.parse(localStorage.getItem(storageKey) || '{}');
    if(stored && typeof stored==='object' && !Array.isArray(stored))saved=stored;
  } catch { storageOK = false; }
  let importedId=null;
  if(location.hash.startsWith('#practice=')) {
    try {
      const imported=JSON.parse(decodeURIComponent(location.hash.slice(10)));
      if(labs.some(l=>l.id===imported.id) && typeof imported.code==='string' && imported.code.length<=100000) {
        saved[imported.id]={code:imported.code,stdin:typeof imported.stdin==='string'?imported.stdin.slice(0,10000):'',passed:false};
        importedId=imported.id;
        history.replaceState(null,'','#lab-'+imported.id);
      }
    } catch { /* Ignore malformed exercise links. No code runs automatically. */ }
  }
  const el = (tag, cls, text) => { const x=document.createElement(tag); if(cls)x.className=cls; if(text!==undefined)x.textContent=text; return x; };
  const persist = () => {
    for (const [id,r] of records) saved[id]={code:r.editor.value,stdin:r.input?.value || '',passed:r.passed};
    try { localStorage.setItem(storageKey, JSON.stringify(saved)); } catch { storageOK=false; }
    document.querySelector('.storage-note').hidden = storageOK;
  };
  const progress = () => { document.querySelector('.lab-progress').textContent=`연습 ${labs.length}개 · 통과 ${[...records.values()].filter(r=>r.passed).length}개`; };
  const setStatus = (r,text,kind='') => { r.status.textContent=text; r.status.dataset.kind=kind; };
  function lock(on) {
    for(const r of records.values()) {
      r.run.disabled=on; r.reset.disabled=on; r.apply.disabled=on;
      r.editor.readOnly=on; if(r.input)r.input.readOnly=on;
      r.stop.hidden=!(on && active?.record===r);
    }
  }
  function dispose(lang) { const e=engines.get(lang); if(e) { e.worker.terminate(); engines.delete(lang); } }
  function finish(job) {
    clearTimeout(job.timer); if(active===job) active=null; lock(false);
  }
  function abort(job, text) {
    if(active!==job)return;
    dispose(job.lang); job.record.passed=false; setStatus(job.record,text,'error');
    finish(job); persist(); progress();
  }
  function engine(lang) {
    if(engines.has(lang))return engines.get(lang);
    const source=document.getElementById(lang==='r'?'r-worker':'python-worker').textContent;
    const url=URL.createObjectURL(new Blob([source],{type:'text/javascript'}));
    const worker=new Worker(url,{type:'module'});
    URL.revokeObjectURL(url);
    const state={worker,ready:false}; engines.set(lang,state);
    worker.onmessage=({data})=>{
      const job=active; if(!job || job.lang!==lang)return;
      if(data.type==='phase')setStatus(job.record,data.text);
      else if(data.type==='running') {
        state.ready=true; clearTimeout(job.timer);
        setStatus(job.record,'실행·채점 중…');
        job.timer=setTimeout(()=>abort(job,'실행 시간 12초를 넘겨 중지했습니다. 반복문의 종료 조건을 확인한 뒤 다시 실행하세요.'),12000);
      } else if(data.type==='result') {
        const r=job.record;
        r.output.textContent=data.output || (data.error?'출력 전에 오류가 발생했습니다.':'화면 출력이 없습니다. print()를 넣어 보세요.');
        if(data.error)r.output.textContent+='\n\n'+data.error;
        r.tests.replaceChildren();
        for(const t of data.tests || []) {
          const li=el('li',t.ok?'ok':'bad',(t.ok?'✓ 통과 · ':'✗ 실패 · ')+t.name);
          if(!t.ok && t.detail)li.append(el('small','',t.detail));
          r.tests.append(li);
        }
        for(const image of data.images || []) {
          const canvas=el('canvas');canvas.width=image.width;canvas.height=image.height;
          canvas.setAttribute('role','img');canvas.setAttribute('aria-label',r.lab.title+' 실행 그래프');
          canvas.getContext('2d').drawImage(image,0,0);image.close();r.plots.append(canvas);
        }
        const passed=(data.tests || []).filter(t=>t.ok).length;
        r.passed=!data.error && passed===r.lab.tests.length;
        setStatus(r,data.error?'실행 오류 · 아래 내용을 확인하세요.':`${passed}/${r.lab.tests.length} 통과${r.passed?' · 완료!':' · 틀린 항목을 수정해 보세요.'}`,data.error?'error':r.passed?'pass':'fail');
        if(data.error && !state.ready)dispose(lang);
        finish(job);persist();progress();
      }
    };
    worker.onerror=(event)=>{ if(active?.lang===lang)abort(active,'엔진을 불러오지 못했습니다. 인터넷 연결을 확인한 뒤 다시 실행하세요. '+(event.message || '')); };
    return state;
  }
  function run(r) {
    if(location.protocol==='file:') {
      location.href=homepage+'#practice='+encodeURIComponent(JSON.stringify({id:r.lab.id,code:r.editor.value,stdin:r.input?.value || ''}));
      return;
    }
    if(active)return;
    r.output.textContent='';r.tests.replaceChildren();r.plots.replaceChildren();r.passed=false;
    const job={record:r,lang:r.lab.lang};active=job;lock(true);progress();
    setStatus(r,'실행 엔진을 준비하고 있습니다. 첫 실행은 다운로드 때문에 시간이 걸릴 수 있습니다.');
    job.timer=setTimeout(()=>abort(job,'엔진 준비가 지연돼 중지했습니다. 인터넷 연결을 확인한 뒤 다시 실행하세요.'),180000);
    try {
      const e=engine(job.lang);
      e.worker.postMessage({code:r.editor.value,stdin:r.input?.value || '',tests:r.lab.tests});
    } catch(error) { abort(job,'실행 엔진을 시작하지 못했습니다. '+String(error)); }
  }
  const intro=el('aside','practice-intro');
  intro.innerHTML='<h2>읽고, 직접 쓰고, 실행해 보세요</h2><p>각 단원의 연습칸에서 코드를 작성한 뒤 <strong>실행·채점</strong>을 누르세요. 출력과 테스트 결과가 바로 아래에 나타납니다. <kbd>Ctrl+Enter</kbd>로도 실행할 수 있습니다.</p><p class="note">Python·R은 이 브라우저에서 실행됩니다. 처음에는 인터넷으로 실행 엔진을 불러옵니다. 입력값이 필요한 Python 코드는 입력칸을 사용하세요. R은 미리 제공한 데이터와 벡터로 연습합니다. 각 실행의 변수는 새로 시작합니다.</p><p class="note">힌트와 예시 답안은 펼쳐서 확인할 수 있습니다. 채점은 표시된 연습 테스트 기준이며, 통과가 모든 입력의 정답을 보장하지는 않습니다.</p><p class="lab-progress" role="status"></p><p class="storage-note" hidden>브라우저 저장을 사용할 수 없어 이번 작성 내용은 새로고침하면 사라질 수 있습니다.</p><p class="lab-jump"><a href="#lab-r-ops">첫 R 연습으로</a> · <a href="#lab-py-input">첫 Python 연습으로</a></p><p class="lab-sources">실행 엔진: <a href="https://docs.r-wasm.org/webr/latest/" target="_blank" rel="noopener">webR</a> · <a href="https://pyodide.org/en/stable/usage/quickstart.html" target="_blank" rel="noopener">Pyodide</a></p>';
  document.querySelector('main h1').after(intro);
  if(location.protocol==='file:') {
    const notice=el('div','file-notice');
    const p=el('p','','다운로드한 HTML은 바로 읽을 수 있습니다. 실제 코드 실행은 아래 웹 실습 페이지를 사용하세요. 실행 버튼을 누르면 작성한 코드를 웹 실습 페이지로 가져옵니다. 인터넷 연결이 필요합니다.');
    const a=el('a','','웹 코드 실습 페이지 열기 →');a.href=homepage;
    notice.append(p,a);intro.prepend(notice);
  }
  for(const lab of labs) {
    const card=el('section','lab');card.id='lab-'+lab.id;card.setAttribute('aria-labelledby',card.id+'-title');
    const header=el('div','lab-header');header.append(el('span','lab-tag',lab.lang==='r'?'R':'Python'));
    const title=el('h3','',lab.title);title.id=card.id+'-title';header.append(title);card.append(header,el('p','lab-task',lab.task));
    const label=el('label','', '직접 코드 작성');label.htmlFor=card.id+'-code';card.append(label);
    const editor=el('textarea');editor.id=label.htmlFor;editor.spellcheck=false;editor.wrap='off';editor.value=saved[lab.id]?.code ?? lab.starter;
    editor.style.height=Math.min(420,Math.max(180,(editor.value.split('\n').length+1)*23))+'px';
    card.append(editor,el('p','editor-note','Ctrl+Enter: 실행 · 들여쓰기: 공백 4개 · 작성 내용은 이 브라우저에 자동 저장'));
    let input;
    if(lab.stdin) {
      const inputLabel=el('label','','입력값 · input()이 한 줄씩 읽습니다');inputLabel.htmlFor=card.id+'-stdin';
      input=el('textarea','lab-stdin');input.id=inputLabel.htmlFor;input.value=saved[lab.id]?.stdin ?? lab.stdin;
      card.append(inputLabel,input);
    }
    const actions=el('div','lab-actions'),runButton=el('button','primary','실행·채점'),stop=el('button','stop','실행 중지'),reset=el('button','','시작 코드로 초기화');
    stop.hidden=true;actions.append(runButton,stop,reset);card.append(actions);
    const hint=el('details'),hs=el('summary','','힌트 보기');hint.append(hs,el('p','',lab.hint));card.append(hint);
    const answer=el('details'),as=el('summary','','예시 답안 보기'),pre=el('pre'),code=el('code','',lab.solution);pre.append(code);
    const apply=el('button','','이 답안을 편집기에 넣기');answer.append(as,pre,apply);card.append(answer);
    const criteria=el('details');criteria.append(el('summary','','채점 기준 보기'));
    const ul=el('ul');for(const t of lab.tests)ul.append(el('li','',t.name));criteria.append(ul);card.append(criteria);
    const status=el('p','lab-status','아직 실행하지 않았습니다.');status.setAttribute('role','status');
    const output=el('pre','lab-output','실행 결과가 여기에 표시됩니다.');output.setAttribute('aria-label',lab.title+' 실행 출력');output.tabIndex=0;
    const tests=el('ul','lab-tests'),plots=el('div','lab-plots');card.append(status,output,tests,plots);
    const r={lab,card,editor,input,run:runButton,reset,apply,stop,status,output,tests,plots,passed:!!saved[lab.id]?.passed};records.set(lab.id,r);
    if(r.passed)setStatus(r,'이전에 통과한 코드입니다. 다시 실행할 수 있습니다.','pass');
    const changed=()=>{r.passed=false;setStatus(r,'코드 또는 입력값이 바뀌었습니다. 다시 실행해 보세요.');persist();progress();};
    editor.addEventListener('input',changed);input?.addEventListener('input',changed);
    editor.addEventListener('keydown',event=>{if((event.ctrlKey||event.metaKey)&&event.key==='Enter'){event.preventDefault();run(r);}});
    runButton.addEventListener('click',()=>run(r));stop.addEventListener('click',()=>{if(active?.record===r)abort(active,'실행을 중지했습니다. 다시 실행하면 엔진을 새로 준비합니다.');});
    if(location.protocol==='file:')runButton.textContent='실습 페이지에서 실행';
    reset.addEventListener('click',()=>{editor.value=lab.starter;if(input)input.value=lab.stdin;changed();});
    apply.addEventListener('click',()=>{editor.value=lab.solution;changed();editor.focus();});
    const heading=document.getElementById('section-'+lab.section);let next=heading.nextElementSibling;
    while(next && next.tagName!=='H2')next=next.nextElementSibling;
    if(next)next.before(card);else heading.parentNode.append(card);
  }
  progress();persist();
  if(importedId) {
    const r=records.get(importedId);
    setStatus(r,'파일에서 가져온 코드입니다. 실행·채점을 눌러 확인하세요.');
    r.card.scrollIntoView();
  }
})();
