"""Study exercises. These are practice checks, not a secure examination system."""
LABS = []
def lab(id, section, lang, title, task, starter, solution, hint, checks, stdin=''):
    LABS.append(dict(id=id, section=section, lang=lang, title=title, task=task,
        starter=starter.strip()+'\n', solution=solution.strip()+'\n', hint=hint,
        tests=[dict(name=n, code=c) for n,c in checks], stdin=stdin))

lab('r-ops',2,'r','몫과 나머지',
    '13을 4로 나눈 나머지는 remainder, 정수 몫은 quotient에 저장하세요. 두 값을 출력하세요.',
    'remainder <- NA\nquotient <- NA\nprint(c(remainder, quotient))',
    'remainder <- 13 %% 4\nquotient <- 13 %/% 4\nprint(c(remainder, quotient))',
    '나머지는 %%, 몫은 %/%입니다.',
    [('나머지 = 1','stopifnot(identical(as.numeric(remainder), 1))'),('몫 = 3','stopifnot(identical(as.numeric(quotient), 3))')])

lab('r-vector',3,'r','벡터에서 값과 위치 고르기',
    'x에서 3보다 큰 값은 selected, 그 값들의 위치는 positions에 저장하세요.',
    'x <- c(1, 5, 2, 7, 3)\nselected <- NULL\npositions <- NULL\nprint(selected)\nprint(positions)',
    'x <- c(1, 5, 2, 7, 3)\nselected <- x[x > 3]\npositions <- which(x > 3)\nprint(selected)\nprint(positions)',
    'x[조건]은 값, which(조건)은 인덱스를 반환합니다.',
    [('선택한 값 5, 7','stopifnot(identical(as.numeric(selected), c(5,7)))'),('위치 2, 4','stopifnot(identical(as.numeric(positions), c(2,4)))')])

lab('r-matrix',3,'r','열부터 채우는 행렬',
    '1~12로 3행 4열 행렬 m을 만들고, 두 번째 행을 second_row에 저장하세요.',
    'm <- NULL\nsecond_row <- NULL\nprint(m)\nprint(second_row)',
    'm <- matrix(1:12, nrow=3, ncol=4)\nsecond_row <- m[2, ]\nprint(m)\nprint(second_row)',
    'matrix의 기본 채움은 열 방향입니다. 행 전체는 m[행, ]입니다.',
    [('행렬 크기 3×4','stopifnot(is.matrix(m), identical(dim(m), c(3L,4L)))'),('두 번째 행 2, 5, 8, 11','stopifnot(identical(as.numeric(second_row), c(2,5,8,11)))')])

lab('r-factor',3,'r','팩터에 새 범주 추가',
    'f의 수준에 C를 추가한 뒤 세 번째 값을 C로 바꾸세요. 결과에 NA가 없어야 합니다.',
    'f <- factor(c("A", "B", "A"))\n# 새 수준을 먼저 추가하세요\nprint(f)',
    'f <- factor(c("A", "B", "A"))\nlevels(f) <- c(levels(f), "C")\nf[3] <- "C"\nprint(f)',
    'levels(f)에 C를 추가한 후 f[3]에 대입하세요.',
    [('범주와 자료구조','stopifnot(is.factor(f), "C" %in% levels(f))'),('실제 값과 결측 여부','stopifnot(identical(as.character(f), c("A","B","C")), !anyNA(f))')])

lab('r-subset',3,'r','iris 조건 추출',
    'iris에서 Species가 setosa인 행을 chosen에 저장하고 행 수를 n에 저장하세요.',
    'chosen <- NULL\nn <- NA\nprint(n)',
    'chosen <- subset(iris, Species == "setosa")\nn <- nrow(chosen)\nprint(head(chosen))\nprint(n)',
    'subset(데이터, 조건)과 nrow()를 사용하세요.',
    [('50행의 데이터프레임','stopifnot(is.data.frame(chosen), nrow(chosen)==50, n==50)'),('setosa만 선택','stopifnot(all(chosen$Species == "setosa"), ncol(chosen)==5)')])

lab('r-loop',4,'r','3의 배수 합과 개수',
    'for 또는 while로 1~100 중 3의 배수 합 total과 개수 count를 구하세요.',
    'total <- 0\ncount <- 0\n# 반복문을 작성하세요\nprint(c(total, count))',
    'total <- 0\ncount <- 0\nfor (i in 1:100) {\n  if (i %% 3 == 0) {\n    total <- total + i\n    count <- count + 1\n  }\n}\nprint(c(total, count))',
    'i %% 3 == 0일 때 누적합과 개수를 각각 증가시키세요. 채점은 결과를 확인하므로 반복문 사용 여부도 직접 확인하세요.',
    [('합계 1683','stopifnot(total==1683)'),('개수 33','stopifnot(count==33)')])

lab('r-apply',4,'r','apply의 1과 2',
    'm의 행별 합은 row_total, 열별 평균은 col_average에 apply로 저장하세요.',
    'm <- matrix(1:6, nrow=2)\nrow_total <- NULL\ncol_average <- NULL\nprint(row_total)\nprint(col_average)',
    'm <- matrix(1:6, nrow=2)\nrow_total <- apply(m, 1, sum)\ncol_average <- apply(m, 2, mean)\nprint(row_total)\nprint(col_average)',
    'MARGIN=1은 행, 2는 열입니다. 이 연습의 채점은 결과를 검사합니다.',
    [('행별 합 9, 12','stopifnot(identical(as.numeric(row_total), c(9,12)))'),('열별 평균','stopifnot(identical(as.numeric(col_average), c(1.5,3.5,5.5)))')])

lab('r-air',5,'r','airquality와 NA',
    '5월 평균 Ozone을 may_mean, Ozone이 100을 넘는 관측 개수를 high_days에 저장하세요. 결측값은 제외하세요.',
    'may_mean <- NA\nhigh_days <- NA\nprint(c(may_mean, high_days))',
    'may_mean <- mean(airquality$Ozone[airquality$Month==5], na.rm=TRUE)\nhigh_days <- sum(airquality$Ozone > 100, na.rm=TRUE)\nprint(c(may_mean, high_days))',
    '부분 벡터를 먼저 추출하고 mean(..., na.rm=TRUE), sum(..., na.rm=TRUE)를 쓰세요.',
    [('5월 오존 평균','stopifnot(isTRUE(all.equal(may_mean, mean(airquality$Ozone[airquality$Month==5], na.rm=TRUE))))'),('100 초과 개수','stopifnot(high_days == sum(airquality$Ozone>100, na.rm=TRUE))')])

lab('r-na',5,'r','결측 행 제거',
    '열별 NA 개수는 missing_count, NA가 하나라도 있는 행의 개수는 bad_rows, NA 행을 제거한 데이터는 clean에 저장하세요.',
    'ds <- data.frame(a=c(1,NA,3), b=c(4,5,NA))\nmissing_count <- NULL\nbad_rows <- NA\nclean <- NULL\nprint(clean)',
    'ds <- data.frame(a=c(1,NA,3), b=c(4,5,NA))\nmissing_count <- colSums(is.na(ds))\nbad_rows <- sum(!complete.cases(ds))\nclean <- ds[complete.cases(ds), ]\nprint(missing_count)\nprint(clean)',
    'colSums(is.na(ds)), complete.cases(ds)를 조합하세요.',
    [('열별 결측 1개씩','stopifnot(identical(as.numeric(missing_count),c(1,1)))'),('결측 행 2개','stopifnot(bad_rows==2)'),('정상 행만 남음','stopifnot(is.data.frame(clean), nrow(clean)==1, clean$a==1, clean$b==4)')])

lab('r-regression',6,'r','회귀 예측과 그래프',
    'trees에서 Girth로 Volume을 예측하는 fit을 만들고 Girth 8.5, 9, 9.5의 예측값을 predictions에 저장하세요. plot(trees$Girth, trees$Volume)도 실행해 보세요.',
    'fit <- NULL\npredictions <- NULL\n# 회귀모델을 만들고 예측하세요\nprint(predictions)',
    'fit <- lm(Volume ~ Girth, data=trees)\npredictions <- predict(fit, newdata=data.frame(Girth=c(8.5,9,9.5)))\nprint(predictions)\nplot(trees$Girth, trees$Volume, xlab="Girth", ylab="Volume")\nabline(fit, col="blue")',
    'lm(목표 ~ 설명변수, data=...), predict(..., newdata=...)를 사용하세요.',
    [('올바른 회귀모델','stopifnot(inherits(fit,"lm"), identical(all.vars(formula(fit)), c("Volume","Girth")))'),('세 예측값','stopifnot(isTRUE(all.equal(as.numeric(predictions), as.numeric(predict(lm(Volume~Girth,data=trees),newdata=data.frame(Girth=c(8.5,9,9.5)))))))')])

lab('py-input',7,'python','입력과 형변환',
    '입력칸의 한 줄에서 정수 a, b를 읽고 합을 total, 몫을 quotient, 나머지를 remainder에 저장하세요. b는 양수입니다.',
    'a, b = map(int, input().split())\ntotal = None\nquotient = None\nremainder = None\nprint(total, quotient, remainder)',
    'a, b = map(int, input().split())\ntotal = a + b\nquotient = a // b\nremainder = a % b\nprint(total, quotient, remainder)',
    'input().split()으로 나눈 문자열을 int로 변환합니다.',
    [('입력 합계','assert total == a+b, "a+b를 확인하세요"'),('몫과 나머지','assert quotient == a//b and remainder == a%b, "//와 %를 확인하세요"')], '13 4')

lab('py-count',8,'python','딕셔너리 빈도 세기',
    '단어 리스트를 받아 단어별 등장 횟수를 딕셔너리로 반환하는 count_words(words)를 작성하세요.',
    'def count_words(words):\n    # 딕셔너리에 누적하세요\n    return {}\n\nprint(count_words(["R", "Python", "R"]))',
    'def count_words(words):\n    counts = {}\n    for word in words:\n        counts[word] = counts.get(word, 0) + 1\n    return counts\n\nprint(count_words(["R", "Python", "R"]))',
    '없는 키의 기본값은 counts.get(word, 0)으로 가져올 수 있습니다.',
    [('반복 단어','assert count_words(["R","Python","R"]) == {"R":2,"Python":1}'),('빈 입력','assert count_words([]) == {}'),('대소문자는 다른 키','assert count_words(["a","A","a"]) == {"a":2,"A":1}')])

lab('py-factorial',9,'python','재귀 팩토리얼',
    '0 이상의 정수 n에 대해 n!을 반환하는 factorial(n)을 재귀로 작성하세요.',
    'def factorial(n):\n    raise NotImplementedError("종료 조건과 재귀 호출을 작성하세요")\n\nprint(factorial(5))',
    'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n\nprint(factorial(5))',
    '0!=1이고 n!=n×(n−1)!입니다. 검사 입력은 0 이상의 정수입니다.',
    [('종료 조건','assert factorial(0)==1 and factorial(1)==1'),('5!','assert factorial(5)==120'),('10!','assert factorial(10)==3628800')])

lab('py-limit',10,'python','누적합을 넘지 않는 최대 n',
    '1+2+...+n이 limit 이하인 최대 정수 n을 반환하는 max_n(limit)을 작성하세요. limit은 0 이상의 정수입니다.',
    'def max_n(limit):\n    return 0\n\nprint(max_n(55))',
    'def max_n(limit):\n    total, n = 0, 0\n    while total + n + 1 <= limit:\n        n += 1\n        total += n\n    return n\n\nprint(max_n(55))',
    '다음 수를 더해도 한도를 넘지 않는지 먼저 검사하세요.',
    [('경계 0과 1','assert max_n(0)==0 and max_n(1)==1'),('55는 10','assert max_n(55)==10'),('경계 전후','assert max_n(54)==9 and max_n(56)==10')])

lab('py-stars',10,'python','모래시계 출력',
    'n이 1 이상일 때 모래시계 각 행을 문자열 리스트로 반환하는 hourglass(n)을 만드세요. n=2 → ["***", " *", "***"]. 뒤쪽 공백은 넣지 마세요.',
    'def hourglass(n):\n    return []\n\nprint("\\n".join(hourglass(5)))',
    'def hourglass(n):\n    top = [" "*i + "*"*(2*(n-i)-1) for i in range(n)]\n    return top + top[-2::-1]\n\nprint("\\n".join(hourglass(5)))',
    '윗부분의 공백은 i개, 별은 2*(n-i)-1개. 가운데를 뺀 윗부분을 뒤집어 붙이세요.',
    [('n=1','assert hourglass(1)==["*"]'),('n=2','assert hourglass(2)==["***"," *","***"]'),('n=5 대칭과 행 수','h=hourglass(5)\nassert len(h)==9 and h==h[::-1] and h[4]=="    *" and h[0]=="*********"')])

lab('py-369',10,'python','숫자에 3·6·9가 포함되면 X',
    '1부터 n까지 문자열 목록을 반환하는 game369(n)을 작성하세요. 숫자에 3,6,9 중 하나가 있으면 X 하나를 반환하세요.',
    'def game369(n):\n    return []\n\nprint(" ".join(game369(29)))',
    'def game369(n):\n    result = []\n    for i in range(1,n+1):\n        result.append("X" if any(c in str(i) for c in "369") else str(i))\n    return result\n\nprint(" ".join(game369(29)))',
    '3의 배수인지와 숫자에 3·6·9가 포함됐는지는 다른 조건입니다.',
    [('1~9','assert game369(9)==["1","2","X","4","5","X","7","8","X"]'),('문자 포함 판정','assert game369(29)[11]=="12" and game369(29)[12]=="X" and game369(29)[25]=="X"'),('빈 범위','assert game369(0)==[]')])

lab('py-attendance',10,'python','출석번호 빈도표',
    '번호 1~23이 담긴 numbers를 받아 각 번호의 등장 횟수 23개를 반환하는 attendance(numbers)를 작성하세요.',
    'def attendance(numbers):\n    return [0] * 23\n\nprint(attendance([1,3,2,2,5]))',
    'def attendance(numbers):\n    counts = [0]*23\n    for number in numbers:\n        counts[number-1] += 1\n    return counts\n\nprint(attendance([1,3,2,2,5]))',
    '번호 1은 인덱스 0에 대응합니다.',
    [('중복 번호','assert attendance([1,3,2,2,5])[:5]==[1,2,1,0,1]'),('마지막 번호','assert attendance([23,23])==[0]*22+[2]'),('빈 입력','assert attendance([])==[0]*23')])

lab('py-collatz',10,'python','콜라츠 수열',
    'n부터 1까지의 콜라츠 수열을 리스트로 반환하는 collatz(n)을 재귀로 작성하세요. 이 문제의 n은 작은 양의 정수입니다.',
    'def collatz(n):\n    return []\n\nprint(collatz(5))',
    'def collatz(n):\n    if n == 1:\n        return [1]\n    next_n = 3*n+1 if n%2 else n//2\n    return [n] + collatz(next_n)\n\nprint(collatz(5))',
    '종료 조건은 [1]. 그 외에는 [n]에 다음 수열을 붙이세요.',
    [('n=1','assert collatz(1)==[1]'),('n=5','assert collatz(5)==[5,16,8,4,2,1]'),('짝수 시작','assert collatz(8)==[8,4,2,1]')])

lab('py-caesar',10,'python','시저 암호 복호화',
    '소문자는 3칸 앞으로 되돌리고 공백·기호는 유지하는 decrypt(text)를 작성하세요. a는 x로 돌아갑니다.',
    'def decrypt(text):\n    return text\n\nprint(decrypt("qhyhu wuxvw euxwxv"))',
    'def decrypt(text):\n    result = ""\n    for ch in text:\n        if "a" <= ch <= "z":\n            result += chr((ord(ch)-ord("a")-3)%26+ord("a"))\n        else:\n            result += ch\n    return result\n\nprint(decrypt("qhyhu wuxvw euxwxv"))',
    'a 기준으로 0~25를 만들고 −3을 한 뒤 %26으로 순환시키세요.',
    [('예시 문장','assert decrypt("qhyhu wuxvw euxwxv")=="never trust brutus"'),('알파벳 순환과 기호','assert decrypt("abc!")=="xyz!"'),('빈 입력','assert decrypt("")==""')])

lab('py-subarray',11,'python','음수가 있는 연속 부분배열',
    '합이 target인 연속 구간의 (시작, 끝) 인덱스를 반환하는 find_subarray(a, target)을 작성하세요. 양 끝 포함이고, 없으면 None. 여러 답 중 하나면 됩니다.',
    'def find_subarray(a, target):\n    return None\n\nprint(find_subarray([3,4,-1,2], 7))',
    'def find_subarray(a, target):\n    seen = {0:-1}\n    prefix = 0\n    for i, value in enumerate(a):\n        prefix += value\n        if prefix-target in seen:\n            return (seen[prefix-target]+1, i)\n        if prefix not in seen:\n            seen[prefix] = i\n    return None\n\nprint(find_subarray([3,4,-1,2], 7))',
    '누적합 prefix에서 이전 누적합 prefix-target을 찾으세요. 초기 누적합 0의 인덱스는 −1입니다.',
    [('기본 예시','a=[3,4,-1,2]\nr=find_subarray(a,7)\nassert r is not None and 0<=r[0]<=r[1]<len(a) and sum(a[r[0]:r[1]+1])==7'),('음수 구간','a=[5,-7,3,1]\nr=find_subarray(a,-4)\nassert r is not None and 0<=r[0]<=r[1]<len(a) and sum(a[r[0]:r[1]+1])==-4'),('없음/빈 배열','assert find_subarray([1,2],10) is None and find_subarray([],0) is None')])

lab('py-matmul',11,'python','2차원 리스트 행렬곱',
    'NumPy 없이 matmul(A,B)를 작성하세요. A의 열 수와 B의 행 수가 다르면 False를 반환하세요. 입력은 비어 있지 않은 직사각형 행렬입니다.',
    'def matmul(A, B):\n    return False\n\nprint(matmul([[1,2,3]], [[1],[2],[3]]))',
    'def matmul(A, B):\n    if len(A[0]) != len(B):\n        return False\n    C = [[0]*len(B[0]) for _ in A]\n    for i in range(len(A)):\n        for j in range(len(B[0])):\n            for k in range(len(B)):\n                C[i][j] += A[i][k]*B[k][j]\n    return C\n\nprint(matmul([[1,2,3]], [[1],[2],[3]]))',
    '결과의 크기는 A의 행×B의 열입니다. 세 겹 반복문에서 i,j,k의 역할을 구분하세요.',
    [('1×3과 3×1','assert matmul([[1,2,3]],[[1],[2],[3]])==[[14]]'),('2×3과 3×2','assert matmul([[1,2,3],[4,5,6]],[[1,4],[2,5],[3,6]])==[[14,32],[32,77]]'),('크기 불일치','assert matmul([[1,2]],[[1,2]]) is False')])

lab('py-circle',11,'python','원형 접시의 합',
    '비어 있지 않은 리스트 a와 정수 k≥0을 받아 각 시작점에서 k개 접시를 먹은 합 목록을 반환하는 circular_sums(a,k)를 만드세요. k가 len(a)보다 클 수도 있습니다.',
    'def circular_sums(a, k):\n    return []\n\nprint(circular_sums([2,1,4,3,5], 3))',
    'def circular_sums(a, k):\n    n = len(a)\n    q, r = divmod(k, n)\n    base = q*sum(a)\n    return [base+sum(a[(i+j)%n] for j in range(r)) for i in range(n)]\n\nprint(circular_sums([2,1,4,3,5], 3))',
    '인덱스를 %n으로 감쌀 수 있습니다. 여러 바퀴는 q,r=divmod(k,n)으로 줄일 수 있습니다.',
    [('k=3','assert circular_sums([2,1,4,3,5],3)==[7,8,12,10,8]'),('여러 바퀴 k=8','assert circular_sums([2,1,4,3,5],8)==[22,23,27,25,23]'),('음수와 k=0','assert circular_sums([-1,2],3)==[0,3] and circular_sums([1,2],0)==[0,0]')])

lab('py-rle',11,'python','RLE 인코딩·디코딩',
    'encode(s), decode(t)를 만드세요. 반복 2개 이상은 길이+영문자, 1개는 문자만. 여러 자리 길이와 빈 입력을 처리하고 잘못된 토큰은 ValueError를 발생시키세요. 슬라이싱을 사용하세요.',
    'def encode(s):\n    return s\n\ndef decode(t):\n    return t\n\nprint(encode("aaabccccdd"))',
    '''def encode(s):
    result, i = [], 0
    while i < len(s):
        j = i+1
        while j < len(s) and s[j] == s[i]:
            j += 1
        run = s[i:j]
        result.append((str(len(run)) if len(run)>1 else "") + run[0])
        i = j
    return "".join(result)

def decode(t):
    result, i = [], 0
    while i < len(t):
        j = i
        while i < len(t) and "0" <= t[i] <= "9":
            i += 1
        count = int(t[j:i]) if i>j else 1
        if i == len(t) or not ("a"<=t[i]<= "z" or "A"<=t[i]<= "Z"):
            raise ValueError("invalid")
        result.append(t[i]*count)
        i += 1
    return "".join(result)

print(encode("aaabccccdd"))
print(decode("3ab4c2d"))''',
    '현재 위치 i와 구간 끝 j를 두세요. 숫자는 한 글자가 아니라 연속한 묶음으로 읽습니다.',
    [('인코딩과 빈 문자열','assert encode("aaabccccdd")=="3ab4c2d" and encode("")==""'),('여러 자리 길이와 복원','assert decode("12aB")=="a"*12+"B" and decode("")=="" and decode(encode("aaZZb"))=="aaZZb"'),('잘못된 토큰','for bad in ["12", "!", "2?", "a3"]:\n    try:\n        decode(bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError("ValueError 필요: "+bad)'),('슬라이싱 사용','import ast\nassert any(isinstance(n,ast.Slice) for n in ast.walk(ast.parse(__source__))), "슬라이싱을 사용하세요"')])

lab('py-class',12,'python','객체마다 다른 상태',
    'Book(title)에 title과 available=True를 저장하세요. borrow()는 대출 가능하면 False로 바꾸고 True를, 이미 대출 중이면 False를 반환하세요.',
    'class Book:\n    def __init__(self, title):\n        pass\n\n    def borrow(self):\n        return False\n\n# 객체를 만들어 실행해 보세요',
    'class Book:\n    def __init__(self, title):\n        self.title = title\n        self.available = True\n\n    def borrow(self):\n        if not self.available:\n            return False\n        self.available = False\n        return True\n\nb = Book("파이썬")\nprint(b.title, b.borrow(), b.available)',
    '인스턴스 변수는 self.title, self.available에 저장하세요.',
    [('초기 상태','b=Book("R")\nassert b.title=="R" and b.available is True'),('대출 상태 전환','b=Book("R")\nassert b.borrow() is True and b.available is False and b.borrow() is False'),('객체 간 상태 독립','a,b=Book("A"),Book("B")\na.borrow()\nassert b.available is True')])

lab('py-numpy',12,'python','NumPy 축과 브로드캐스팅',
    'A의 각 행에 B를 더한 C, C의 열별 합 col_sum, 행별 평균 row_mean을 만드세요. 처음에는 NumPy 패키지를 추가로 불러옵니다.',
    'import numpy as np\nA = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])\nB = np.array([10,20,30,40])\nC = None\ncol_sum = None\nrow_mean = None\nprint(C)',
    'import numpy as np\nA = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])\nB = np.array([10,20,30,40])\nC = A + B\ncol_sum = C.sum(axis=0)\nrow_mean = C.mean(axis=1)\nprint(C)\nprint(col_sum, row_mean)',
    '열별 합은 axis=0, 행별 평균은 axis=1입니다.',
    [('브로드캐스팅','assert np.array_equal(C,A+B)'),('열별 합','assert np.array_equal(col_sum,[45,78,111,144])'),('행별 평균','assert np.allclose(row_mean,[27.5,31.5,35.5])')])

lab('py-pandas',12,'python','pandas 정렬과 위치 선택',
    'df를 price 내림차순으로 정렬한 sorted_df와 원래 df의 인덱스 1~2행/첫 2열인 picked를 만드세요. 처음에는 pandas 패키지를 추가로 불러옵니다.',
    'import pandas as pd\ndf = pd.DataFrame({"name":["A","B","C"], "price":[30,10,20], "qty":[1,2,3]})\nsorted_df = None\npicked = None\nprint(picked)',
    'import pandas as pd\ndf = pd.DataFrame({"name":["A","B","C"], "price":[30,10,20], "qty":[1,2,3]})\nsorted_df = df.sort_values("price", ascending=False)\npicked = df.iloc[1:3, 0:2]\nprint(sorted_df)\nprint(picked)',
    'sort_values는 정렬된 새 객체를 반환합니다. iloc 슬라이스는 끝 인덱스를 제외합니다.',
    [('가격 내림차순','assert sorted_df["price"].tolist()==[30,20,10]'),('행과 열 선택','assert picked.shape==(2,2) and picked["name"].tolist()==["B","C"] and picked.columns.tolist()==["name","price"]')])
