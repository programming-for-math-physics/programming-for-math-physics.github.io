""" md

# 場の方程式(偏微分方程式)

* 物理の色々な法則が偏微分方程式として表される
* 多次元配列を使って計算し, それを可視化まで持っていければ中級者

"""

""" md

# {C.inc_section}. 場の方程式

* __「場」__とは, つまりは「位置」ごとに付随する物理量のこと. 数学では位置の関数のことにほかならない
* 色々な物理量が, 「場」として表される
* 例えば部屋の温度, 電場, 磁場, 重力場, 重力によるポテンシャル(位置エネルギー), 媒体を伝わる音波(の振幅), 電子の存在確率, 流体における速度, 圧力, ... ありとあらゆるものが, 「位置」に依存する値, つまり場である
* 位置に依存する「値」が一つの数(スカラー)の場合もあれば, ベクトルの場合もある. 前者の場合を__スカラー場__と呼び, 後者を__ベクトル場__と呼ぶ. 例えば温度や圧力, ポテンシャルの場はスカラー場であるし, 電場, 速度の場などはベクトル場である.
* 多くの場は時間と共に変化する. つまり場は位置の関数でもあり, 時刻の関数でもある
 * 表記としては, 温度場を$T(t, x, y, z)$と書いたり, 電場を$E(t, x, y, z)$と書いたりする.
* さまざまな物理法則はある条件下でどのような「場」ができるかを記述する. それは「場」を時には位置で微分したり, 時刻で微分したりしたものの間の関係式として表される. 
* ある量が色々な変数の関数である時, 微分と言ってもどの変数に関する微分であるかを明示する記法が必要. ある関数$F$を変数$x$で微分したものを, $F$の$x$に関する__偏微分__と呼び
$$ \frac{{\partial F}}{{\partial x}} $$
と書く. $x$で2回偏微分したものは,
$$ \frac{{\partial^2 F}}{{\partial x^2}}, $$
$y$で偏微分したものを$x$で偏微分したものは
$$ \frac{{\partial^2 F}}{{\partial x\partial y}} $$
と書く.

* ある関数の偏微分に関する関係式を, 偏微分方程式という. 以下は偏微分方程式の例

* とりあえずこんなに色々あるのかということがわかればよく, 現時点で意味がわからなくても気にしなくて良い

* 一様な熱伝導率を持つ媒質内の温度場の方程式

$$ \frac{{\partial T}}{{\partial t}} 
= \frac{{\partial^2 T}}{{\partial x^2}} 
+ \frac{{\partial^2 T}}{{\partial y^2}} 
+ \frac{{\partial^2 T}}{{\partial z^2}}. $$

* よく使う記号

 * 物理の微分方程式には,

$$ \frac{{\partial^2 f}}{{\partial x^2}} 
 + \frac{{\partial^2 f}}{{\partial y^2}} 
 + \frac{{\partial^2 f}}{{\partial z^2}} $$

という項が非常によく現れるので, これを

$$ \Delta f $$

と表記する(ラプラシアン). これを使うと上記は,

$$ \frac{{\partial T}}{{\partial t}} = \Delta T $$

 * 1階微分の様々なバリエーションもよく現れる
 * fは実数(スカラー場)とする
$$ \nabla f \equiv
\left(
\frac{{\partial f}}{{\partial x}}, 
\frac{{\partial f}}{{\partial y}}, 
\frac{{\partial f}}{{\partial z}}
\right) $$

 * Fはベクトル$(F_x, F_y, F_z)$とする(ベクトル場)
$$ \nabla \cdot F \equiv
\frac{{\partial F_x}}{{\partial x}} + 
\frac{{\partial F_y}}{{\partial y}} +
\frac{{\partial F_z}}{{\partial z}}
$$

$$ \nabla \times F \equiv
\left(
\frac{{\partial F_z}}{{\partial y}} - \frac{{\partial F_y}}{{\partial z}},
\frac{{\partial F_x}}{{\partial z}} - \frac{{\partial F_z}}{{\partial x}},
\frac{{\partial F_y}}{{\partial x}} - \frac{{\partial F_x}}{{\partial y}},
\right)
$$

* 波動方程式

$$ \frac{{\partial^2 f}}{{\partial t^2}} = \Delta f $$

* マックスウェルの方程式

$$ \nabla \cdot B = 0 $$
$$ \nabla \cdot E = \frac{{\rho}}{{\epsilon}} $$
$$ \frac{{\partial B}}{{\partial t}} = - \nabla \times E $$
$$ \epsilon \mu \frac{{\partial E}}{{\partial t}} = \nabla \times B - \mu j $$

* シュレーディンガー方程式

$$ ih \frac{{d\phi}}{{dt}} = -\frac{{h^2}}{{2m}} \left(\Delta + V\right) \phi $$

* ナビエストークス方程式

$$ \frac{{\partial v}}{{\partial t}} + (v \cdot \nabla) v
= - \frac{{1}}{{\rho}} \nabla p + \nu \Delta v $$

"""

""" md

# {C.inc_section}. 微分方程式の...

* ある場の方程式がなぜ成り立つのかの理由は様々で, それが根本的な物理法則の場合もある(シュレディンガー方程式やマックスウェルの方程式)し, ある特別な状況に対して, 根本的な法則を当てはめて導出される場合もある

* ここでは後者の一例として温度場の偏微分方程式を導いてみる
* なお, 「偏微分方程式を導ける」ことは, 与えられた方程式を計算機で解けるかどうかとは一応, 関係がない. 前者が出来なくても後者を実行することは出来る
* しかし, 偏微分方程式を導くことでその式に対する物理的な直感を得ることが出来るので, 「意味を理解する」一環として, それを導くことは有用である.

* 温度を支配する根本的な法則は, 「フーリエの法則」と呼ばれるもので, 早い話が, 熱は, 温度が高い方から低い方に流れ, その速さが, 温度差(正確には温度の「勾配」)に比例するというもの. 正確には, 「熱流速密度」$=$単位面積を単位時間に通る熱の量が, その場所における温度勾配に比例するというもの.

* 図を書きやすくするため, 2次元で考える.
* 以下のような位置$(x,y)$にある微小な(一辺$h$の)正方形の要素を考え, その場所の時刻$t$における温度を$T(t,x,y)$と書く
* その正方形の上下左右隣の温度は, それぞれ$T(t,x, y+h)$, $T(t, x, y-h)$, $T(t, x+h, y)$, $T(t, x, y-h)$ということになる
* よって, 上下左右隣の要素の間の温度勾配はそれぞれ, 
$$ \frac{{T(t, x, y+h) - T(t, x,y)}}{{h}}, $$
$$ \frac{{T(t, x, y-h) - T(t, x,y)}}{{h}}, $$
$$ \frac{{T(t, x+h, y) - T(t, x,y)}}{{h}}, $$
$$ \frac{{T(t, x-h, y) - T(t, x,y)}}{{h}}. $$

* よって, それぞれの辺における熱流速密度(2次元なので単位長さ単位時間あたりの通過熱量)がそれぞれ, 
$$ \frac{{T(t, x, y+h) - T(t, x,y)}}{{h}}, $$
$$ \frac{{T(t, x, y-h) - T(t, x,y)}}{{h}}, $$
$$ \frac{{T(t, x+h, y) - T(t, x,y)}}{{h}}, $$
$$ \frac{{T(t, x-h, y) - T(t, x,y)}}{{h}} $$
である.

* よってある微小時間$\Delta t$経過するまでの間に$(x,y)$のセルに流れ込む流量は,

$$ \left(T(t,x, y+h) - T(t,x,y) - T(t,x, y) + T(t,x,y-h)
+  T(t,x+h, y) - T(t,x,y) - T(t,x, y) + T(t,x-h,y)\right) 
\Delta t 
=
\left(T(t,x, y+h) + T(t,x,y-h) + T(t,x+h, y) - T(t,x-h,y) - 4T(t,x,y)\right) 
\Delta t 
$$

に比例する. 単位面積あたりに流れ込む熱量に比例した温度の上昇がもたらされるわけだから,

$$ T(t+\Delta t,x,y) - T(t,x,y) \approx
k 
\frac{{T(t,x, y+h) + T(t,x,y-h) + T(t,x+h, y) - T(t,x-h,y) - 4T(t,x,y)}}{{h^2}}
\Delta t 
\quad \cdots (\ast)
$$

両辺を$\Delta t$で割って$\Delta \rightarrow 0$, 
$h \rightarrow 0$の極限を取ったものが,

$$ \frac{{\partial T}}{{\partial t}} 
= k \left(\frac{{\partial^2 T}}{{\partial x^2}}
+ \frac{{\partial^2 T}}{{\partial y^2}}\right)
$$

ということ

"""


""" md

# {C.inc_section}. 偏微分方程式の数値計算

* 偏微分方程式をコンピュータで数値的に解く方法は様々で, それ自体が一大分野と言って良い
* ここでは概念的に簡単な方法(差分法)を紹介する. それは, 常微分方程式のときにそうしたように, 微分の項をその差分近似でおきかえるというものである
* 例えば常微分方程式

$$ \begin{{array}}{{l}} y' = -\frac{{y}}{{2x}} \\ y(1) = 1 \end{{array}}$$

を解く際に, 上式の $\frac{{dy}}{{dx}}$を

$$ \frac{{y(x+h) - y(x)}}{{h}}$$

で近似して置き換えたことを思い出そう. この式変形を「離散化」と呼ぶ.

すると,

$$ y(x+h) \approx  y(x) -\frac{{y}}{{2x}} h$$

つまり離散化をすると, ある時刻における値から次の(僅かな時間経過後の)時刻における値を具体的に求めることが出来たのだった.

偏微分方程式でも基本的な考え方は同じ. 例えば

$$ \frac{{\partial T}}{{\partial t}} 
= k \left(\frac{{\partial^2 T}}{{\partial x^2}}
+ \frac{{\partial^2 T}}{{\partial y^2}}\right)
$$

が与えられたら,

$$\frac{{\partial T}}{{\partial t}} \approx \frac{{T(t+\Delta t,x,y,z)-T(t,x,y,z)}}{{\Delta t}}$$
$$\frac{{\partial T}}{{\partial x}} \approx \frac{{T(t,x+h,y,z)-T(t,x,y,z)}}{{h}}$$
$$\frac{{\partial T}}{{\partial y}} \approx \frac{{T(t,x,y+h,z)-T(t,x,y,z)}}{{h}}$$
$$\frac{{\partial T}}{{\partial z}} \approx \frac{{T(t,x,y,z+h)-T(t,x,y,z)}}{{h}}$$

などで適宜置き換える. 2階微分も同様で,

$$\frac{{\partial^2 T}}{{\partial x^2}} 
\approx 
\frac{{\frac{{T(t,x+h,y,z)-T(t,x,y,z)}}{{h}} - \frac{{T(t,x,y,z)-T(t,x-h,y,z)}}{{h}}}}{{h}}
= 
\frac{{T(t,x+h,y,z)-2T(t,x,y,z)+T(t,x-h,y,z)}}{{h^2}}$$

のようになる. 上式では3次元空間をシミュレートすることを想定して,
$T$を$t, x, y, z$の関数としたが, シミュレーションを行う空間が
2次元だったり1次元だったりする場合は適宜$T(t,x,y)$, $T(t,x)$
のように変数を減らせば良い.

以下では式を簡単にするため2次元で考える.

上記を適用して

$$ \frac{{\partial T}}{{\partial t}} 
= k \left(\frac{{\partial^2 T}}{{\partial x^2}}
+ \frac{{\partial^2 T}}{{\partial y^2}}\right)
$$

を離散化すると結局,

$$ \frac{{T(t+\Delta t, x,y)-T(t,x,y)}}{{\Delta t}} 
\approx k \frac{{T(t, x+h,y)+T(t,x-h,y)+T(t,x,y+h)+T(t,x,y-h)-4T(t,x,y)}}{{h^2}}
$$

となる. つまり,

$$ T(t+\Delta t, x,y)\approx
T(t,x,y) + 
k (T(t, x+h,y)+T(t,x-h,y)+T(t,x,y+h)+T(t,x,y-h)-4T(t,x,y))
\frac{{\Delta t}}{{h^2}}
\quad \cdots (\dagger)
$$

が, 「次の時刻」における値を今の時刻における値から計算する式となる.

余談だが, この式は偏微分方程式を導く途中で得た式
$(\ast)$にほかならない. 偏微分方程式を解くというと仰々しいが,
要するに$(\dagger)$は,
「温度が高い方から低い方へ, 温度差に比例した速度で流れ込む」
「熱が流れ込んだらそれに比例して温度が上がる」
ということを表現しているに過ぎない.

右辺を見たらわかるとおり, 
ある点$(x,y)$における次の時刻($t+\Delta t$)における値は, 
今の時刻における, 自分自身の値$T(t,x,y)$
だけでなく, 周辺の値($T(t,x+h,y), T(t,x-h,y), T(t,x,y+h), T(t,x,y-h)$
から決まる. したがって空間内の,
多数の点における値を並行して計算していくことが必要になる.

そのために配列を使う.

* シミュレートしたい領域を, 一辺が$h$の微小正方形に分割する
* その格子点における値を格納する配列を作る
* ($\dagger$)を使って微笑時間経過した後の値を繰り返し計算していく

具体的にやってみる.

"""

""" exec-code-box """
import matplotlib.pyplot as plt
import numpy as np

# [0,1]x[0,1]の領域を1辺hの正方形に区切り, 
# dtずつ時刻を進めて, 時刻Tまでシミュレートする

def heat2d(h, dt, end_t):
    k = 0.1
    n = int(1/h)
    X = np.linspace(0,1,n)
    Y = np.linspace(0,1,n)
    X,Y = np.meshgrid(X,Y)
    T = np.zeros((n,n))
    T[:,0] = 1
    T[0,:] = 1
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        T[1:n-1,1:n-1] = T[1:n-1,1:n-1] + (k * dt / (h*h)) * (T[2:n,1:n-1] + T[0:n-2,1:n-1] + T[1:n-1,2:n] + T[1:n-1,0:n-2] - 4*T[1:n-1,1:n-1])
    plt.pcolor(X, Y, T)
    plt.show()

heat2d(1.0e-2, 1.0e-4, 1.0)


