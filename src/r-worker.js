let engine;
async function init() {
  if (engine) return engine;
  const { WebR, ChannelType } = await import('https://webr.r-wasm.org/v0.6.0/webr.mjs');
  engine = new WebR({ baseUrl: 'https://webr.r-wasm.org/v0.6.0/', channelType: ChannelType.PostMessage, interactive: false });
  await engine.init();
  return engine;
}
self.onmessage = async ({ data }) => {
  let shelter;
  try {
    const r = await init();
    shelter = await new r.Shelter();
    const env = await shelter.evalR('new.env(parent = globalenv())');
    self.postMessage({ type: 'running' });
    const capture = await shelter.captureR(data.code, { env, withAutoprint: true, captureGraphics: { width: 640, height: 420 } });
    let output = '';
    for (const item of capture.output) {
      if (item.type === 'stdout' || item.type === 'stderr') output += item.data + '\n';
      else if (item.type === 'warning' || item.type === 'message') output += '[' + item.type + '] ' + await item.data.toString() + '\n';
    }
    const tests = [];
    for (const test of data.tests) {
      try {
        await shelter.captureR(test.code, { env, captureGraphics: false });
        tests.push({ name: test.name, ok: true });
      } catch (error) { tests.push({ name: test.name, ok: false, detail: String(error) }); }
    }
    self.postMessage({ type: 'result', output: output.slice(0, 30000), tests, images: capture.images, error: '' }, capture.images);
  } catch (error) {
    self.postMessage({ type: 'result', error: String(error), output: '', tests: [] });
  } finally { if (shelter) await shelter.purge(); }
};
