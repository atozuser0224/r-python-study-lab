let engine;
async function init() {
  if (engine) return engine;
  const base = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/';
  self.postMessage({ type: 'phase', text: 'Python 로더를 다운로드하고 있습니다.' });
  const { loadPyodide } = await import(base + 'pyodide.mjs');
  self.postMessage({ type: 'phase', text: 'Python 엔진을 다운로드하고 초기화하고 있습니다.' });
  engine = await loadPyodide({ indexURL: base });
  return engine;
}
self.onmessage = async ({ data }) => {
  try {
    const py = await init();
    self.postMessage({ type: 'phase', text: '필요한 패키지를 확인하고 있습니다.' });
    await py.loadPackagesFromImports(data.code);
    self.postMessage({ type: 'running' });
    py.globals.set('__request_json', JSON.stringify(data));
    const json = await py.runPythonAsync(`
import json as _json, io as _io, sys as _sys, traceback as _traceback
from contextlib import redirect_stdout as _stdout, redirect_stderr as _stderr
_req = _json.loads(__request_json)
_out, _err = _io.StringIO(), _io.StringIO()
_scope = {'__name__': '__main__', '__source__': _req['code']}
_result = {'output': '', 'error': '', 'tests': []}
_old_stdin = _sys.stdin
try:
    _sys.stdin = _io.StringIO(_req.get('stdin', ''))
    with _stdout(_out), _stderr(_err):
        try:
            exec(compile(_req['code'], '<연습 코드>', 'exec'), _scope)
        except BaseException:
            _result['error'] = _traceback.format_exc()
        if not _result['error']:
            for _test in _req['tests']:
                try:
                    exec(compile(_test['code'], '<채점>', 'exec'), _scope)
                    _result['tests'].append({'name': _test['name'], 'ok': True})
                except BaseException as _exc:
                    _result['tests'].append({'name': _test['name'], 'ok': False, 'detail': str(_exc) or type(_exc).__name__})
finally:
    _sys.stdin = _old_stdin
_result['output'] = (_out.getvalue() + _err.getvalue())[:30000]
_json.dumps(_result, ensure_ascii=False)
`);
    self.postMessage({ type: 'result', ...JSON.parse(json) });
  } catch (error) {
    self.postMessage({ type: 'result', error: String(error), tests: [], output: '' });
  }
};
