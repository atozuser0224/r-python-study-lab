# R·Python Study Lab

개념 설명 사이에서 코드를 직접 쓰고 실행·채점하는 한국어 학습서입니다.

**[웹에서 바로 실행](https://atozuser0224.github.io/r-python-study-lab/)** · **[릴리스 다운로드](https://github.com/atozuser0224/r-python-study-lab/releases/latest)**

## 사용 방법

1. 웹페이지를 열고 각 단원의 시작 코드를 완성합니다.
2. `실행·채점` 또는 `Ctrl+Enter`를 누릅니다.
3. 출력과 테스트 결과를 확인하고, 필요하면 힌트·예시 답안을 펼칩니다.

R 10개와 Python 16개 연습이 있습니다. 코드·입력값은 사용 중인 브라우저에 저장됩니다. 각 실행은 새 변수 환경을 사용합니다. 실행을 중지하거나 12초 제한에 걸리면 엔진을 다시 준비합니다.

Python·R 설치는 필요하지 않습니다. 처음에는 인터넷으로 실행 엔진과 필요한 패키지를 내려받습니다. 코드 실행은 브라우저에서 이루어집니다. 모바일에서는 큰 실행 엔진 때문에 브라우저 메모리 제한의 영향을 받을 수 있습니다.

릴리스의 `index.html`은 내려받아 읽을 수 있고, 실행 버튼은 작성 중인 코드를 웹 실습 페이지로 가져갑니다. 이때 실행은 다시 눌러야 하며, 링크만 열었다고 코드가 자동 실행되지는 않습니다. 완전한 오프라인 실행은 지원하지 않습니다.

## 구성과 검증

- R: 벡터·행렬·팩터·조건 추출·반복문·apply·결측값·회귀와 그래프.
- Python: 입력·자료구조·재귀·누적합·별·369·빈도표·콜라츠·암호·부분배열·행렬곱·원형합·RLE·클래스·NumPy·pandas.
- 연습 테스트 총 68개. Chromium에서 예시 답안, 오답 처리, 문법 오류, 중지, 자동 저장과 반응형 화면을 확인했습니다.
- 표시된 테스트는 학습용이며 모든 입력의 정답이나 실제 시험 출제 범위를 보장하지 않습니다.

강의자료·시험지 원본과 개인정보는 배포물에 포함하지 않습니다. 학습 본문과 코드 예제만 포함합니다.

## 개발

Python 3와 Node.js를 사용합니다. 추가 빌드 패키지는 필요하지 않습니다.

```sh
python src/build.py
node tests/verify.cjs
python -m http.server 8000 --bind 127.0.0.1
```

브라우저 실행 검증용 함수는 `tests/solutions.js`, `tests/python-solutions.js`, `tests/behavior.js`에 있습니다.

실행 환경: [webR 0.6.0](https://docs.r-wasm.org/webr/latest/), [Pyodide 314.0.7](https://pyodide.org/en/stable/usage/quickstart.html).
