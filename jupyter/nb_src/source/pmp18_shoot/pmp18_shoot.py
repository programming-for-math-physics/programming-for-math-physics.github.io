""" md

# [おまけ] 

"""

""" md

* シミュレーションでしばしば現れ, かつ身につけると強力な手法を紹介する
* その強力な手法を一言で言えば,
  * 未知数を「いっぱい」導入する
  * それら未知数の連立一次方程式をたてて解く
ということ

"""


""" md

# {C.inc_section}. 例題: ホールインワン狙い.

時刻0で$(0,0)$にいる点をどんな初速度(大きさと角度)で打ち出したら, 時刻1で$(1,0)$に命中するか. ただし重力と空気抵抗を受けるとして考える. 

ゴルフでホールに命中させるにはどんな角度, 強さで打ち出せばいいかという問題だと思ってもよい(もっともゴルフの場合はボールの回転(バックスピン)が重要. 以下の式はそれを無視しているが, 適当化感じで良ければ簡単に入れられる)し, ミサイルを建物に命中させるという問題だと思っても良い. 式は変わるがロケットをどの角度で打ち上げれば無事火星に到着するかという問題も同じように解ける

運動方程式は

$$ ma = mg - kv $$

* m : 質量 (定数)
* g : 重力加速度 (定数)
* k : 空気抵抗の係数 (定数)

* v : 速度 (時刻の関数) 丁寧には $v(t)$と書くべきもの
* a : 加速度 (時刻の関数) 丁寧には $a(t)$と書くべきもの

すべてを位置 $x$ の方程式として書き直すと

$$ \ddot{{x}} = g - \frac{{k}}{{m}}\dot{{x}} $$

より丁寧に書けば

$$ \ddot{{x}}(t) = g - \frac{{k}}{{m}}\dot{{x}}(t) $$

もしここで問題が, 「初速度を与えられて以降の軌跡を求める」という問題であれば何も難しいことはなく, これまでやってきたとおり時刻を少しずつ進めながら$x$, $v$を更新していけば良い. 言い換えれば, $x(t)$は, 初期値$x(0)$から出発して $x(h), x(2h), \ldots$, と順々に求めて行ける

"""

""" md

この問題が違うのは初速度ではなく, **最終的な位置**が与えられて, その場合の初速度をいくつにすればよいか, という問題であるところ. そこで**軌跡全体を大量の未知数であらわしてそれらの間の関係を元に大きな連立方程式**を立てて解く. 

具体的には,

* 時間$[0,1]$を$n$等分し, $t_0, t_1, ..., t_n$ とする ($t_i = i/n$)
  * 以降, $h = 1/n$とする. つまり, $t_i = ih$
* 時刻$t_i$における位置を$(x_i, y_i)$と書き($x_1, \ldots , x_{{n-1}}, y_1, \ldots , y_{{n-1}}$は未知数), 運動方程式を元にこれらの間に成り立つ方程式を立てる.

"""

""" md

* ポイント: 運動方程式の**離散化**

$$ \ddot{{x}} = g - \frac{{k}}{{m}}\dot{{x}} $$

において, $\dot{{x}}(t)$, $\ddot{{x}}(t)$ を以下で近似

$$ \dot{{x}}(t) \approx \frac{{x(t+h) - x(t)}}{{h}} $$

$$ \ddot{{x}}(t) \approx \frac{{\dot{{x}}(t+h) - \dot{{x}}(t)}}{{h}} = \frac{{x(t+2h) - 2x(t+h) + x(t)}}{{h^2}}  $$



$$ \frac{{x_{{i+2}} - 2 x_{{i+1}} + x_i}}{{h^2}} =     - \frac{{k}}{{m}} \frac{{x_{{i+1}} - x_i}}{{h}} $$
$$ \frac{{y_{{i+2}} - 2 y_{{i+1}} + y_i}}{{h^2}} = - g - \frac{{k}}{{m}} \frac{{y_{{i+1}} - y_i}}{{h}} $$
$$ (i = 0, \ldots, n - 2) $$

方程式が$2(n-1)$本, 未知数が$2(n-1)$の連立一次方程式なので解けるはずということになる.

よく見ると$\{{ x_i \}}_{{i=1,\ldots,n-1}}$と$\{{ y_i \}}_{{i=1,\ldots,n-1}}$には関係がないので, 2つをバラバラに解けばよいということになる.

"""

""" md

* $x$の式を見やすく整理する

$$ \frac{{x_{{i+2}} - 2 x_{{i+1}} + x_i}}{{h^2}} =     - \frac{{k}}{{m}} \frac{{x_{{i+1}} - x_i}}{{h}} $$

全体に $\times h^2$

$$ x_{{i+2}} - 2 x_{{i+1}} + x_i =     - \frac{{kh}}{{m}} (x_{{i+1}} - x_i) $$

移項して整理

$$ \left(1 - \frac{{kh}}{{m}}\right) x_i + \left(- 2 + \frac{{kh}}{{m}}\right) x_{{i+1}} + x_{{i+2}} = 0 \quad (i = 0, 1, \ldots , n - 2) $$

確認: $x_0 = 0, x_n = 1$ は与えられており, 未知数は, $x_1, \ldots , x_{{n-1}}$ の$(n-1)$個. 方程式の数も$(n-1)$個.

"""

""" md

みやすさのために上記を

$$ P x_i + Q x_{{i+1}} + x_{{i+2}} = 0 \quad (i = 0, 1, \ldots , n - 2) $$

と書くことにする. すると全体は以下のように行列を使って書ける

$$
\left(
\begin{{array}}{{ccccccc}}
P & Q & 1 \\
  & P & Q & 1     \\
  &   & P & Q      & 1 \\
  &   &   & \ddots & \ddots & \ddots     \\
  &   &   &        & P      & Q      & 1 \\
\end{{array}}
\right)
\left(
\begin{{array}}{{c}}
0   \\
x_1 \\
\vdots \\
x_{{n-1}} \\
1
\end{{array}}
\right)
= 0
$$

ここで行列は$(n-1)\times(n+1)$行列.

未知数だけを取り出して$Ax = b$の形に書き換えると以下

$$
\left(
\begin{{array}}{{ccccc}}
Q & 1 \\
P & Q & 1     \\
  & P & Q      & 1 \\
  &   & \ddots & \ddots & \ddots \\
  &   &        & P      & Q      \\
\end{{array}}
\right)
\left(
\begin{{array}}{{c}}
x_1 \\
x_2 \\
\vdots \\
x_{{n-2}} \\
x_{{n-1}} \\
\end{{array}}
\right)
= 
\left(
\begin{{array}}{{c}}
0 \\
0  \\
\vdots \\
0  \\
-1 \\
\end{{array}}
\right)
$$

なお$y$の方は右辺が少し違うだけになる. これは各自やってみよ.

$$
\left(
\begin{{array}}{{ccccccc}}
P & Q & 1 \\
  & P & Q & 1     \\
  &   & P & Q      & 1 \\
  &   &   & \ddots & \ddots & \ddots     \\
  &   &   &        & P      & Q      & 1 \\
\end{{array}}
\right)
\left(
\begin{{array}}{{c}}
0   \\
y_1 \\
\vdots \\
y_{{n-1}} \\
0
\end{{array}}
\right)
= 0
$$

$$
\left(
\begin{{array}}{{ccccc}}
Q & 1 \\
P & Q & 1     \\
  & P & Q      & 1 \\
  &   & \ddots & \ddots & \ddots \\
  &   &        & P      & Q      \\
\end{{array}}
\right)
\left(
\begin{{array}}{{c}}
y_1 \\
y_2 \\
\vdots \\
y_{{n-2}} \\
y_{{n-1}} \\
\end{{array}}
\right)
= 
- gh^2
\left(
\begin{{array}}{{c}}
1 \\
1  \\
\vdots \\
1  \\
1 \\
\end{{array}}
\right)
$$

"""

""" md

Pythonコード化

上記を実際にPython (numpy)で解くのに必要なことは,

* 左辺の行列を作る
* 右辺のベクトルを作る
* np.linalg.solve を呼び出す

そこで

# 問題{C.inc_problem} 

* 数値$P, Q, n$を与えられ, 上記の左辺の行列

$$
\left(
\begin{{array}}{{ccccc}}
Q & 1 \\
P & Q & 1     \\
  & P & Q      & 1 \\
  &   & \ddots & \ddots & \ddots \\
  &   &        & P      & Q      \\
\end{{array}}
\right)
$$

を作って返すPython関数 `mk_matrix(P, Q, n)` を書け

"""

""" write-code-box """

""" md
# 問題{C.inc_problem} 

* 数値$P, Q, n$を与えられ, 上記の右辺のベクトル$x$用と$y$用を作る関数(それぞれ`mk_vect_x(P, Q, n)`, `mk_vect_y(P, Q, n)`)を書け
"""

""" write-code-box """

""" md

# 問題{C.inc_problem} 

* 上記を使い, $m, k, g, n$が与えられたら, 上記方程式をといた結果$X$, $Y$ (それぞれ$(n - 1)$要素の配列を求める関数 mk_trajectory(m, k, g, n)を書け.
* 2つの配列を返したければ, $2 \times (n -1)$の配列(1つ)を返してもよいし, 以下のようにしても良い

```
def mk_trajectory(m, k, g, n):
    ...
    return X,Y
```

受け取る方は

```
X,Y = mk_trajectory(m, k, g, n)
```
"""
                                                                          
""" md

# 問題{C.inc_problem} 

* mk_trajectory(m, k, g, n) を使って得た結果を matplotlib (plot関数) で可視化してみよ
* 空気抵抗(k)を変えるとどのように軌道が変わるか

"""

""" write-code-box """

