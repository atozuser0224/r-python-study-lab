from pathlib import Path
import json
from exercises import LABS

root=Path(__file__).parent
source=(root/'source-static.html').read_text(encoding='utf-8')
def inline(text):
    return text.replace('</script','<\\/script')
scripts='<script id="lab-data" type="application/json">'+inline(json.dumps(LABS,ensure_ascii=False))+'</script>'
for ident,name in [('python-worker','python-worker.js'),('r-worker','r-worker.js')]:
    scripts+='<script id="'+ident+'" type="text/plain">'+inline((root/name).read_text(encoding='utf-8'))+'</script>'
scripts+='<script>'+inline((root/'app.js').read_text(encoding='utf-8'))+'</script>'
head='<meta name="application-version" content="1.0.0"><style>'+(root/'lab.css').read_text(encoding='utf-8')+'</style>'
output=source.replace('</head>',head+'</head>').replace('</body>',scripts+'</body>')
(root.parent/'index.html').write_text(output,encoding='utf-8')
print(f'Built {len(LABS)} exercises and {sum(len(l["tests"]) for l in LABS)} checks')
