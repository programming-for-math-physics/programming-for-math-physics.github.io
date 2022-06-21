"""md

#* for文とif文の組み合わせ

# for文とif文の組み合わせ

 * for文, if文を組み合わせてさらにできる計算が抱負になる
 * 特に, for文で繰り返し計算をしながら途中で答えが見つかったらその答えを返す(returnする)ような計算がよく現れる

"""

""" md

例えば以下は, $n$以上の整数で, 「100でわって1あまり, 101で割って2あまる数」(のうち最小の数)を求める関数 find_100_1_101_2(n).

ただし, 

 * 「(100 * 101)個の連続した数の中に少なくとも1つそのような数がある」という事実を証明なしに用いている. 
 * 本来あってはならないことだが, 見つからなかった場合はNoneを返している

"""

""" code """
def find_100_1_101_2(n):
    for i in range(n, n+100*101):
        if i % 100 == 1 and i % 101 == 2:
            return i
    return None # 見つからなかった(実際はありえない)
""" """

""" code """
find_100_1_101_2(1000)
""" """

""" code """
find_100_1_101_2(100000)
""" """

""" md 

 * なお「式1 and 式2」という記法は(恐らく想像通り), 式1と式2が両方真であれば真になる式である.
 * 上と同じプログラムを and を使わずに以下のように書くことも可能 (else節が存在しないif文. i % 100 == 1が成り立たなければ「何もしない(のですぐに次のnに進む)」. i % 101 == 2 が成り立たない場合も同様.

"""

""" code """
def find_100_1_101_2(n):
    for i in range(n, n+100*101):
        if i % 100 == 1:
            if i % 101 == 2:
                return i
    return None # 見つからなかった(実際はありえない)
""" """

""" code """
find_100_1_101_2(1000)
""" """

""" code """
find_100_1_101_2(100000)
""" """

""" md 

# continue文

for文を実行しながら, 「現在の繰り返しを終了して直ちに次の繰り返しに進む」continue文というものがある.

複雑な条件式を and や or で繋げる代わりに, continueを使うときれいに書けることがある.

"""

""" code """
def find_100_1_101_2(n):
    for i in range(n, n+100*101):
        if i % 100 != 1:        # このiは違う
            continue
        if i % 101 != 2:        # このiは違う
            continue
        return i
    return None # 見つからなかった(実際はありえない)
""" """

""" code """
find_100_1_101_2(1000)
""" """

""" code """
find_100_1_101_2(100000)
""" """

""" md

 * 同じ関数を書くのにどの書き方がいいかは場合, 好みにもよるが, 一般的に
  * あまり長い式は見にくくなるので避けたほうが良い
  * ifやforが深く入れ子になるのは見にくくなるので避けたほうが良い
 ということで, continueなどを使いこなして, 短い文が縦に並ぶ, という書き方がわかりやすいことが多い

"""

""" md label=prob,ans

#*P 素数の判定

2以上の整数n が与えられ, それが素数であるか否かを判定する(素数であればTrue, 素数でなければFalseを返す)関数を書け

ヒント: nが素数か否かを判定するには, i = 2, 3, 4, 5, ... で, nを順に割っていき, 約数 (nを割って余りが0になる数)を見つける. $i < n$である約数が見つかれば素数ではない. $i = n$まで約数が見つからなければ, $n$未満の約数がないということだから素数である. なお, 実際には$n = a b$と分解できたとすると, $a, b$のどちらかは$\leq \sqrt{n}$だから, $i^2 \leq n$の範囲で約数が見つからなければ, ただしに素数であると断定できる (1000001が素数かどうかを判定するには 1000まで割り算をすればよい).

"""

""" code points=1 w """
""" """

""" code label=ans """
def is_prime(n):
    for i in range(2, n):
        if i * i > n:
            return True
        elif n % i == 0:
            return False
    return True
""" """

""" code points=1 label=prob,ans """
# test
assert(is_prime(2))
assert(is_prime(3))
assert(not is_prime(4))
assert(is_prime(5))
assert(is_prime(99991))
assert(not is_prime(99991 * 99991))
print("OK")
""" """

""" md label=prob,ans

#*P 方程式の解

関数$f$と実数$a, b$ ($a < b$)が与えられ, 
区間$[a,b]$の中で$f(x) = 0$の解(のうち最小のもの)
を求める関数 find_root(f, a, b) を書け.
解がなければ, Noneを返せ.

ヒント: ここでやりたいのは人間が紙で計算するときのように, $f(x)$の形を見て記号的に解くということではなく, $f(x) \approx 0$となるような$x$ (の近似値)を, 「コンピュータらしい」単純なやり方で求めるということ. 

それは単に, $x$を$a$から$b$までくまなく動かしてその中で$f(x)\approx 0$となる値が現れたらそれを答えとする, というだけである. $f(x) \approx 0$というのがあまりにも曖昧であるのと, できるだけ真の解に近いものを求めるため, 以下のようにする.

それをプログラムにする上でのヒント:

 * $\Delta x = (b-a)/10000$とする
 * $x$を$a$から$b$まで, $\Delta x$ずつ動かしていく
 * それぞれに対し, $f(x)$と$f(x+\Delta x)$を計算
 * どちらかが0になるか, 両者の符号が入れ変わったところで$x$を答えとする

なお, 運が悪いとこのやり方で解を見逃すこともある. どのような場合か考えてみよ(そのような場合にどうしたらいいかというのは実際かなり難しい問題なのでとりあえず深入りはしない).

"""

""" code points=1 w """
""" """

""" code label=ans """
def find_root(f, a, b):
    n = 10000
    dx = (b - a) / n
    for i in range(n):
        x = a + i * dx
        if f(x) * f(x+dx) <= 0:
            return x
    return None
""" """

""" code points=1 label=prob,ans """
# test
import math
def check_root(f, a, b, x_true):
    x = find_root(f, a, b)
    assert(math.isclose(x, x_true, abs_tol=(b - a) / 10000)), (x, x_true)
    print("OK")
    
check_root(math.cos, 0, 10, math.pi/2.0)

def f0(x):
    return (x - 1) * (x - 1.1) * (x - 1.2)

check_root(f0, -2, 2, 1)
""" """

""" md label=prob,ans

#*P 関数の最小値

* 関数 $f$ と, 2つの実数$a, b$ ($a < b$)が与えられ, $f$の, 区間$[a,b]$における最小値を与える$x$ (の近似値)を求める関数 find_min(f, a, b) を書け.

* ヒント: もちろんここでも考えているのは, $f(x)$ を(記号的に)微分して, $f'(x) = 0$をといて, ...みたいな紙の上でやったような記号的な計算をコンピュータにやらせようということではない.

* 「コンピュータらしい」単純なやり方をする. それは単に$x$を$a$から$b$までくまなく動かしてその中で出現する$f(x)$の最小値を拾い上げるというだけのやりかたである.

* それをプログラムにする上でのヒント:

 * $\Delta x = (b-a)/10000$とする
 * $x$を$a$から$b$まで, $\Delta x$ずつ動かしていく
 * それぞれに対し$f(x)$を計算
 * 「これまでの最小を記録した$x$」を別の変数に覚えておき, 記録が更新されたらその変数を更新する

"""

""" code points=1 w """
""" """

""" code label=ans """
def find_min(f, a, b):
    dx = (b - a) / 10000
    xm = a
    for i in range(10000):
        x = a + (i + 1) * dx
        if f(x) < f(xm):
            xm = x
    return xm
""" """

""" code points=1 label=prob,ans """
# test
import random
def check_min(f, a, b):
    rg = random.Random()
    x_min = find_min(f, a, b)
    for i in range(1000):
        x = a + (b - a) * rg.random()
        assert(f(x_min) <= f(x)), (x, x_min, f(x), f(x_min))
    print("OK")

def f1(x):
    return x * x - 2 * x + 3

check_min(f1, -5, 5)

def f2(x):
    return x ** 3 - 4 * x

check_min(f2, -2, 2)
""" """

""" md

# for文の中のfor文 (多重ループ, ループの入れ子)

* for文の文法は,
```
for 変数名 in range(式, 式):
    文
    ...
    文
```
で, for文自体, 「文」の一種なので, for文の中にまたfor文を書くことができる
* for文の中に代入文, if文, 関数呼び出し, などを書けるのと全く同じことで, 何も特別なものではない

* 例えば以下を実行すると何が起きるか予想してから実行してみよ
* 注: print(i, j) は iの値とjの値を1行に表示する (_i j_ のように)
"""

""" code """
for i in range(0, 3):
    for j in range(0, 3):
        print(i, j)
""" """

""" md label=prob,ans

#*P 関数の最小値(2変数)

 半径1の円に内接する三角形の面積の最大値を求める関数 find_max_triangle() を書け

 (数学の)ヒント: 円の中心をO, 三角形の三頂点ABC, ∠AOB $= x$ ∠BOC $= y$ とすると, 三角形の面積$S$は

$$ S = \frac{1}{2} (\sin x + \sin y + \sin(2\pi - x - y)) $$

あとは$x$と$y$を, $0 < x < \pi$, $0 < y < \pi$, $x + y < \pi$
の範囲で動かせばよいだけである.

 (プログラム上のヒント): 前問の, 最小値を求める考え方は変数が二つになってもほとんど同じで通用する. 違いは, for文を二重にしなくてはならないことだけ

```
xを0 < x < piまで動かすためのfor文:
  yを0 < y < pi - xまで動かすためのfor文:
    ... 記録更新していれば ...   
```

という具合.

* なお, $x$や$y$を動かす際, 区間$[0,\pi]$を何分割くらいにすればいいかは試行錯誤してみてほしいのだが, $1000$分割とでもすると, 合計で$1000 \times 1000$回, 面積の計算をすることになる. このくらいになると計算に体感できるほどの時間がかかることがわかる. ためしに5000分割すると相当またなくてはならない.

* コンピュータがいくら計算が速いと行っても, 2次元, 3次元, 多次元の問題になってくるとたちまち計算量が増えていき, 何らかの工夫をしなくてはならないことが感じられるだろう. ここでは時間がないので扱わずに先へ進む

"""

""" code points=1 w """
""" """

""" code label=ans """
def find_max_triangle():
    n = 2000
    S_max = 0
    for i in range(n):
        for j in range(n):
            x = i * math.pi / n
            y = j * math.pi / n
            z = 2 * math.pi - x - y
            if z > 0:
                S = 0.5 * (math.sin(x) + math.sin(y) + math.sin(z))
                if S > S_max:
                    S_max = S
    return S_max
""" """

""" code points=1 label=prob,ans """
# test
assert(math.isclose(find_max_triangle(), 3 * math.sqrt(3) / 4, rel_tol=1.0e-3)), find_max_triangle()
print("OK")
""" """
