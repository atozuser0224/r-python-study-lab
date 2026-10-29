from pathlib import Path
import hashlib, json, shutil, zipfile

root=Path(__file__).resolve().parent.parent
version=json.loads((root/'package.json').read_text(encoding='utf-8'))['version']
dist=root/'dist'
dist.mkdir(exist_ok=True)
names=['index.html','README.md','CHANGELOG.md']
with zipfile.ZipFile(dist/f'r-python-study-lab-v{version}.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
    for name in names:
        info=zipfile.ZipInfo(name,date_time=(2026,10,30,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644 << 16
        archive.writestr(info,(root/name).read_bytes())
html=dist/f'r-python-study-lab-v{version}.html'
shutil.copyfile(root/'index.html',html)
assets=[dist/f'r-python-study-lab-v{version}.zip',html]
checksums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in assets)
(dist/'SHA256SUMS.txt').write_text(checksums,encoding='utf-8')
with zipfile.ZipFile(assets[0]) as archive:
    assert set(archive.namelist())==set(names)
    for name in names:
        assert archive.read(name)==(root/name).read_bytes()
notes=f'''R·Python 코드 실습 학습서 v{version}

- R 10개, Python 16개 연습과 테스트 68개
- 브라우저에서 실제 실행·채점, R 그래프, NumPy·pandas
- 힌트·예시 답안·코드 자동 저장·실행 중지
- HTML·ZIP·SHA-256 확인 파일 제공

웹 실행 주소: https://atozuser0224.github.io/r-python-study-lab/

다운로드한 HTML의 코드 실행 버튼은 작성 중인 코드를 웹 실습 페이지로 가져옵니다. 실행 엔진을 불러오는 인터넷 연결이 필요하며 완전한 오프라인 실행은 지원하지 않습니다.

Chromium에서 예시 답안 26개와 채점 항목 68개 통과, 오답·문법 오류·중지·자동 저장 확인. 원본 강의자료·시험지 파일과 개인정보는 포함하지 않습니다.
'''
(dist/'release-notes.md').write_text(notes,encoding='utf-8')
print(checksums,end='')
print('PASS: ZIP allowlist and per-file byte equality')
