""" md

# 常微分方程式

# {C.inc_section}. 記号的な求解の例

常微分方程式とは1つの入力($x$とする)の未知の関数($y(x)$, 以下$(x)$を省略して単に$y$と書く)に関する方程式で, 特に$y$の微分($y'$や$y''$)を含んだ方程式を言う. 

"""

""" md

普通最初に習う一番簡単な微分方程式はこういうものである.

$$ \begin{{array}}{{l}} y' = -\frac{{y}}{{2x}} \\ y(1) = 1 \end{{array}} \quad \cdots (\dagger) $$

解き方は上記を,

$$ \frac{{y'}}{{y}} = -\frac{{1}}{{2x}} $$

と($y$だけの式 $\times$ $y'$ $=$ $x$だけの式, という形に)変形する.

そして両辺を1から$x$まで積分する.

$$ \int_1^x \frac{{y'(t)}}{{y(t)}} dt = - \int_1^x \frac{{1}}{{2t}} dt $$


$$ \left[ \log y(t) \right]_1^x = -\frac{{1}}{{2}} \left[ \log t \right]_1^x $$

$$ \log y(x) - \log y(1) = -\frac{{1}}{{2}} \log x $$

よって 

$$ y = \frac{{1}}{{\sqrt{{x}}}} $$

もちろんこのやり方で解が見つかる方程式は極めて限定されている.
まず「$y$だけの式$\times y'$ $=$ $x$だけの式」という形に変形できるために,
右辺が「($y$だけの式) $\times$ ($x$だけの式)」という積の形(変数分離型) 
をしていなくてはならず, その上で左辺の$y$だけの式, $x$だけの式の部分の
原子関数を見つけられなくてはならない.

"""

""" md

# {C.inc_section}. 数値計算で微分方程式を解く基本アイデア

* 一方プログラム(数値計算)で解く方法はもっと簡単でかつ一般性のあるものである.

* まず, 「解く」と言っても, $y$を($-x^2+2x+1$のような)$x$の「式」として表すことが目標ではなく, __任意の$b$に対して$y(b)$の(近似)値を計算する関数を作ること__を目標とする.

つまり, 以下のような関数を書くことが目標になる.

> $(\dagger)$ を満たす$y(x)$の, $x=b$における値$y(b)$を求める関数 solve($b$) を書け.

* $b$が何でも良いのだから, これは数値計算としては満足の行く目標であると言える.

* これを数値計算でおこなう原理は実に簡単で, $x=1$ ($y(1)=1$) からスタートして, 少しずつ$x$を増やしたときの$y(x)$の値を次々と求めていく, というだけのものである.

* それをするための__鍵となる式変形は以下:__

$$ y'(x) = -\frac{{y}}{{2 x}} $$

を以下のように書き換える.

$h \approx 0$のとき
$$ \frac{{y(x+h)-y(x)}}{{h}} \approx -\frac{{y}}{{2 x}} \quad (\ast) $$

* ここで$\approx$は微分係数の定義式

$$ y'(x) = \lim_{{h\rightarrow 0}} \frac{{y(x+h)-y(x)}}{{h}} $$

を, $h \approx 0$のとき

$$ y'(x) \approx \frac{{y(x+h)-y(x)}}{{h}} $$

と読み替えた過ぎない. 

* 上記のような, 微分方程式の微分係数の部分を, $y(x+h)$, $y(x)$, $h$などの近似式で置き換える式変形を__離散化__という. 数値計算を使って微分方程式を解く際のキーとなるステップはこの, 離散化という操作である.

"""

""" md 

# {C.inc_section}. 離散化後の計算

* ($\ast$)から, $h\approx 0$のとき

$$ y(x+h) \approx y(x) -\frac{{y}}{{2 x}} \cdot h$$

* これは, __ある$x$に対する$y(x)$の値がわかっていれば, 右辺を計算することで, $y(x+h)$の近似値が得られる__ことを意味する.

* 例えば$h = 0.01$に対し,

$$y(1+h) \approx y(1) + y'(1) h = 1 - \frac{{1}}{{2}} h = 0.995 $$

とわかる. こうして, $y(1)$の値をもとに$y(1+h)$を得ることが出来た.

* 同じことを今度は$x = 1 + h$に適用すれば, $y(1+2h)$が求まる. すなわち,

$$ \begin{{array}}{{rcl}} y(1+2h) & \approx & y(1+h) + y'(1+h) h \\
           & = & y(1+h) -\frac{{y(1+h)}}{{2 (1+h)}} h \\
           & = & 0.995 - \frac{{0.995}}{{2 (1+0.01)}} 0.01 \\
           & = & 0.99097... \end{{array}} $$

* つまり以下の式

$$ y(x+h) \approx y(x) - \frac{{y(x)}}{{2x}} h $$

を繰り返し, $x = 1, 1+h, 1+2h, \ldots$に適用していけば, __次々と, $x = 1+h, 1+2h, 1+3h, \ldots$に対する$y(x)$の近似値が求まる__ ということである. これを, $x$がほしい$b$に達するまで繰り返せば良い.

* これをプログラムにするのも簡単で, 以下のようになる.

"""

""" exec-code-box """
def solve(b):
    x = 1
    y = 1
    h = 0.01
    n = int((b - 1) / h)
    for i in range(n):
        yp = - y / (2 * x)
        y = y + yp * h
        x = x + h
    return y

""" md

なお, int($\cdot$) は, 入力の端数を切り捨てて整数にする関数である. rangeが受け付けるのは整数に限られるためこのようにする.

"""

""" exec-code-box """
int(2.1)

""" exec-code-box """
int(1.2345 / 0.01)

""" md

上記の for 文がやっていることがポイントで,  ($\ast$)に従って,

$$ y(x+h) \approx y(x) - \frac{{y(x)}}{{2 * x}} h $$

に従って, $x$から少し進んだ場所$x+h$における$y$を求めている, それだけである.

"""

""" md

__いくつか細かい問題:__

* $x$を1からhずつ動かしていることから明らかなように, $b$が 1+ h $\times$ 整数という場合でないと, 正確に x=b における値を求めていることにはならない. 
* for文の繰り返し回数を, (b-1)//h で計算しており, これは商の端数を切り捨てる(答えを整数とする)割り算であるから, 実際に求めているのは 

$$x = 1 + \left\lfloor \frac{{b-1}}{{h}} \right\rfloor h$$

における$y$の値ということになる($(b-1)/h$が充分大きければあまり神経質になることはなかろう). 

* 別の問題として, 繰り返し回数を(b-1)/hとしていることから, $b < 1$の場合におかしなことになる. 

* 以上の2点に気を配って直したものが以下である.
* 一度繰り返し回数を決めたあとで, 改めてhを計算し直している. $b < 1$のときはひとりでに$h < 0$になり, $x$は1から小さい方へ向かって進む.

"""

""" exec-code-box """
def solve(b):
    x = 1
    y = 1
    h = 0.01
    n = int((b - 1) // h) + 1
    h = (b - 1) / n
    for i in range(n):
        yp = - y / (2 * x)
        y = y + yp * h
        x = x + h
    return y


""" md

いくつかの$b$の値に対して, solve($b$)と, $1/\sqrt{{b}}$の値を比べてみよう.

"""

""" exec-code-box """
import math

solve(4)

""" exec-code-box """
solve(9)

""" exec-code-box """
solve(4) - 1/math.sqrt(4)

""" exec-code-box """
solve(9) - 1/math.sqrt(9)

""" exec-code-box """
solve(16) - 1/math.sqrt(16)

""" exec-code-box """
solve(0.25) - 1/math.sqrt(0.25)

""" exec-code-box """
solve(0.01) - 1/math.sqrt(0.01)

""" md

* なお, $h$をいくらにするかは重要な問題で, 本来あまり気楽に決めてはいけないが, 上記では気楽に $h = 0.01$としている.
* 大きな$h$を使うと繰り返し回数が少ない, つまり少ない計算の量で答えが求まる一方で, 誤差が大きくなる.
* 逆に小さな$h$を使えば誤差が少なくなることが期待される一方, 繰り返しの回数が大きくなり, より多くの計算が必要になる.

上記のsolveの中のhを変更して, 誤差や計算時間がどう変わるかを確かめてみよ.

* なおこの問題では, 計算時間はhを相当小さくしても「一瞬」と感じられることだろう.
* 実際にhの選択が重要になるのは, 同じようなことを場の方程式(電場, 磁場, 流体の速度場のような, 空間の各点に未知数が割り当てられる問題)に対して行うときで, 計算量は, 空間に設定した点の数 $\times$ 時間方向の繰り返し数となり, 特に2次元, 3次元の問題ではたちまち膨大な量になる.

"""

""" md

# {C.inc_section}. より一般的な「求解関数」

solveを改めて眺めると, ここで用いた解法は, 右辺の形がなんであってもほとんど変更なく使えるということが直ちにわかると思う.

つまり,

$$y'(x) = f(x, y)$$
$$y(a) = c$$

という形の方程式であれば常に適用可能で, $f(x,y)$が変数分離できる必要もなければ, 偶然にも変数分離出来た場合でも, 原子関数が簡単に見つかるような式である必要もない.

擬似コードで書けば以下のようなことである.

```
    x = a
    y = c
    h = 十分小さな値
    for x が b に達するまで:
        yp = f(x, y)
        y = y + yp * h
        x = x + h
```

実際それを, a, b, c, f を引数として受け取る, 非常に一般性のあるPython関数として書くことができる. fは, x, yから微分方程式の右辺を計算する関数.

"""

""" exec-code-box """
def de_solve(a, b, c, f):
    x = a
    y = c
    h = 0.01
    n = int((b - 1) // h) + 1
    h = (b - 1) / n
    for i in range(n):
        yp = f(x, y)
        y = y + yp * h
        x = x + h
    return y

""" md

これを用いて改めて

$$ \begin{{array}}{{l}} y' = -\frac{{y}}{{2x}} \\ y(1) = 1 \end{{array}} \quad \cdots (\dagger) $$

を解くには,

"""

""" exec-code-box """
def rhs(x, y):
    return y/(2*x)

de_solve(1, 4, 1, rhs)

""" md

とすればよい. rhsの代わりに別の関数を渡すだけで, 別の微分方程式を解くことができる.
"""

""" md

# {C.inc_section}. 物理でよく現れるケース: $x$が時刻の場合で改めて説明

上で述べた解法は, $x$が時刻である場合にとりわけ理解しやすい.

* 時刻であることがわかりやすいように$x$を$t$と書き換える.
* $y(t)$を時刻$t$における位置だと思うことにする.
* 関数$y(t)$を「時刻で」微分したものを物理ではしばしば, $\dot{{y}}(t)$と書く.

その場合微分方程式

$$ \dot{{y}}(t) = f(y, t) $$
$$ y(0) = c $$

は, $\dot{{y}}(t)$が速度であって, この微分方程式の右辺$f(y,t)$を計算すれば, そのときの速度がわかる, という意味になる.

そして以下の解法

```
    t = a
    y = c
    dt = 十分小さな値
    for t が b に達するまで:
        yp = f(y, t)
        y = y + yp * dt
        t = t + dt

```

でやっていることは, $f(y, t)$を計算すれば速度がわかるので, それを用いて

```
        y = y + yp * dt
```

によって現在位置を更新している. それは,

```
微笑時間(dt)経過後の位置 = 現在の位置 $+$ 速度 $\times$ dt
```

という, かなり見慣れた式である.

要するに, 「速度 $\times$ 微小時間」を積み重ねて, 位置を更新し続けているに過ぎない.

""" 

""" md

# {C.inc_section}. ニュートンの運動方程式

力学でしばしばでてくるのが__ニュートンの運動方程式__で, 一番簡単なのは質量$m$の質点(大きさを無視できる物体)が運動するとき,

$${{\LARGE m a = F}} $$

に従うというもの. ここで$a$が加速度, つまり$x$を$t$で二度微分したものである. それを強調して書けば,

$$ {{\LARGE m \ddot{{x}}(t) = F }} $$

与えられた状況に応じて$F$ (質点が受ける力)が異なる. 例として, 下記のようにバネにつながれた質点の運動を考えよう.

"""

""" md

<img src="img/spring.svg" />

"""

""" md

バネ定数を$k$とし, (時刻と共に変わる)質点の位置を$x(t)$と書く. ただしバネが自然長の位置を$x=0$とする. すると, 質点が$x$にいるときに受ける力が$-kx(t)$だから, 運動方程式は

$$ m \ddot{{x}}(t) = -kx(t) $$

となる. 

もし右辺の$\ddot{{x}}(t)$が$\dot{{x}}(t)$だったら, この方程式の解き方は先とほぼ同じである. 今回は$x$の2階微分が含まれるところが異なるが, 考え方はあまり変わらない.

つまりは

```
  速度がわかれば微小時間(dt)経過後の位置 = 現在位置 + 速度 * dt
加速度がわかれば微小時間(dt)経過後の速度 = 現在速度 + 加速度 * dt
```

ということである時刻での位置と速度から, 微笑時間経過後の位置と速度がわかる.

プログラムにしたものは以下.

mass_spring(x0, v0, T, m, k) は, 時刻0に位置x0, 速度v0の状態にいた質量$m$の質点が, 時刻$T$のときにいる位置と速度を計算する. $k$はバネ定数. 

なお以下の

```
return (x,v)
```

は二つの値(xとv)を結果として返すときのやり方.

"""

""" exec-code-box """
def mass_spring(x0, v0, T, m, k):
    x = x0
    v = v0
    t = 0
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    for i in range(n):
        a = -k * x / m
        x += v * dt
        v += a * dt
        t += dt
    return (x,v)
        
""" md

* 注: tを更新する代入文は, このプログラムにおいては不要
* 一般には, a (加速度, つまり力)を計算するところで, t (時刻)に依存した外力などが加わる場合など, 必要な場合があるのでつけておく

"""


""" md

なおやってなくてわからない人はあまり気にしなくてよいが, この質点は,

$$ x(t) = A \sin \left(\sqrt{{\frac{{k}}{{m}}}} t\right) + B \sin \left(\sqrt{{\frac{{k}}{{m}}}} t\right) $$

という形の正弦波に沿って移動する. いわゆる単振動をする. その周期は明らかに

$$ 2\pi \sqrt{{\frac{{m}}{{k}}}} $$

である.

特に$x0=0$のときは$B=0$になり, $v0=0$のときは$A=0$になる.

検算のために以下を実行してみる.
* $m = k = 1$とする. 周期は$2\pi$になる
* $x_0 = 1$, $v_0 = 1$とする. 解は
$$ x(t) = \sin t $$
そのものになる.
* $T = \pi/2$のときに原点付近に戻っている, また速度は約$-1$
* $T = \pi$のとき逆の振幅が最大になっている. すなわち$x_0 \approx -1$で, $v_0 \approx 0$

"""

""" exec-code-box """
import math

""" exec-code-box """
mass_spring(1, 0, math.pi/2, 1, 1)

""" exec-code-box """
mass_spring(1, 0, math.pi, 1, 1)
