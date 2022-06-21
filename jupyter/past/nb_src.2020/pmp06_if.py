""" md

# {C.inc_section}. if文

 * 関数定義, for文, に加え, もう一つの重要な文が if文
 * 条件によってことなる計算をさせたい時に使う

"""

""" md

一番簡単な例 (絶対値を計算する関数). 

"""

""" exec-code-box """
def absolute_value(x):
    if x < 0:
        return -x
    else:
        return x

""" exec-code-box """
absolute_value(3)

""" exec-code-box """
absolute_value(-2.1)
    
""" md

次に簡単な例 xの符号(xが正ならば1, 0ならば0, 負ならば-1を返す関数). 

"""

""" exec-code-box """
def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

""" exec-code-box """
sign(3.1)

""" exec-code-box """
sign(0)

""" exec-code-box """
sign(-1)
    

""" md

if文の文法:

 1.
```
if 式 :
    文
    ...
    文
```
 2.
```
if 式 :
    文
    ...
    文
else :
    文
    ...
    文
```
 3.
```
if 式 :
    文
    ...
    文
elif 式 :
    文
    ...
    文
else :
    文
    ...
    文
```

 * if 式の直後に並べる文を__then節__, else 以降に並べる文を__else節__と呼ぶ. 
 * else節は省略できる
 * 3つ以上の選択肢(節)を作りたい場合は「elif 式 : 」という節(あまり一般的な用語ではないが, __elif節__と呼ぶことにする)を好きなだけならべることができる
 * 関数呼び出しやfor文と同じ文法上の注意
  - then節, elif 節, else節に並べる文には字下げが必要
  - 複数の文を節内に並べる場合は同じだけ字下げする

意味(動作)は

 * 「式」を計算する
 * 結果が真 (True)の場合はthen節が実行される
 * 偽 (False)の場合はそれ以降の節(次のelif節ないしelse節)が実行される

"""    

""" md

# 問題 {C.inc_problem} : 

2数$a, b$を与えられ, そのうちの大きくない方を返す関数 `min2(a, b)`を書け

注: この関数は普通 min と呼ぶべきものであろうが, Pythonには組み込み関数としてminが備わっているため, それと名前が衝突しないよう, min2と名付けている

"""

""" write-code-box """

""" answer-code-box """
def min2(a, b):
    if a < b:
        return a
    else:
        return b

""" test-code-box """
assert(min2(3, 5) == 3), min2(3, 5)
assert(min2(4, 2) == 2), min2(4, 2)
assert(min2(1, 1) == 1), min2(1, 1)

""" md

# 問題 {C.inc_problem} 

3数 a, b, c (すべて正の実数であることを仮定して良い)を与えられ, 3辺をa, b, cとする三角形が存在するか否かを計算する(それに応じてTrueまたはFalse)を返す関数make_triangle(a, b, c)を書け.

"""

""" write-code-box """

""" answer-code-box """
def make_triangle(a, b, c):
    if a + b <= c:
        return False
    if b + c <= a:
        return False
    if c + a <= b:
        return False
    return True


""" test-code-box """
assert(make_triangle(1,1,1)), (1,1,1)
assert(not make_triangle(1,2,3)), (1,2,3)
assert(not make_triangle(1,3,2)), (1,3,2)
assert(not make_triangle(2,1,3)), (2,1,3)
assert(not make_triangle(2,3,1)), (2,3,1)
assert(not make_triangle(3,1,2)), (3,1,2)
assert(not make_triangle(3,2,1)), (3,2,1)
assert(make_triangle(7,8,9)), (7,8,9)
assert(make_triangle(7,9,8)), (7,9,8)
assert(make_triangle(8,7,9)), (8,7,9)
assert(make_triangle(8,9,7)), (8,9,7)
assert(make_triangle(9,7,8)), (9,7,8)
assert(make_triangle(9,8,7)), (9,8,7)

""" md

# 問題 {C.inc_problem} 

3数 a, b, c を与えられ, 方程式

$$ ax^2 + bx + c = 0 $$

の実数解の個数を計算する関数 count_roots(a, b,c) を書け. 
ただし無限にある場合は, Noneを返すようにせよ.

注: $a = 0$ などの「退化したケース」も正しく処理するようにせよ
(if文がたくさん並ぶ)

"""

""" write-code-box """

""" answer-code-box """
def count_roots(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                return None
            else:
                return 0
        else:
            return 1
    else:
        D = b * b - 4 * a * c
        if D > 0:
            return 2
        elif D == 0:
            return 1
        else:
            return 0


""" test-code-box """
assert(count_roots(2, 3, 2) == 0), (2,3,2)
assert(count_roots(2, 4, 2) == 1), (2,4,2)
assert(count_roots(2, 5, 2) == 2), (2,5,2)
assert(count_roots(0, 3, 2) == 1), (0,3,2)
assert(count_roots(0, 0, 2) == 0), (0,0,2)
assert(count_roots(0, 0, 0) == None), (0,0,0)

    
