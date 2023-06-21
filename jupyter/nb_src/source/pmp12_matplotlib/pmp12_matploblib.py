""" md

#* matplotlib

* matplotlib はグラフを描画するためのライブラリ
* 道具・スキルの学びとしてはこれが最終章(がんばって!)
* <a href="https://pmp.eidos.ic.i.u-tokyo.ac.jp/slides/pdf/visual_numpy_matplotlib.pdf" target="_blank">Visual Python, Numpy, Matplotlib スライド</a> 5 Matplotlib を参照

* 詳しい情報源: https://matplotlib.org/
* ギャラリー: 手っ取り早く, 「こんな絵を書きたいがどうすればいい?」 というときにはこれを見ると良い! https://matplotlib.org/gallery/index.html

"""

""" md

# matplotlibのimport (おまじない)

以下が多くの書籍や説明用サイトで使われているimportの仕方でこのゼミでもそれに従う

"""

""" code w """
import matplotlib.pyplot as plt
""" """

""" md

## 1次元(x軸とy軸)のプロット

* $y = x^2$のグラフとか, $y=\sin x$のグラフとか, 1変数関数のグラフを表示できる
* 基本
 - X = x座標だけを並べたリストまたは配列,
 - Y = y座標だけを並べたリストまたは配列, を用意する
 - plt.plot(X, Y)
 - plt.show() とすると実際に絵を表示

* 一番トリビアルな例

"""

""" code w """
import matplotlib.pyplot as plt
def plot_a_few():
    X = [ 1, 2, 3, 4 ]
    Y = [ 1, 4, 9, 16 ]
    plt.plot(X, Y)
    plt.show()

plot_a_few()
""" """

""" md

* 見ての通り点の数が少ないのでカクカクした絵になる
* 多数の点を表示するのにもちろん上のように点の座標をベタにプログラム中に書くことはせず, リスト自身をfor文やリスト内包表記を用いて作ったり, numpy の配列を作る
* 簡単な関数なら, numpyの配列を使うのが一番手っ取り早い

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def plot_square():
    X = np.linspace(0, 4*np.pi, 100) # 0から4*piまで99等分
    Y = np.sin(X)                  # universal関数で100点全てにsinを計算
    plt.plot(X, Y)
    plt.show()                  # 描画!

plot_square()
""" """

""" md

* この例では特にそうする必要はないが, あえてリストを使ってみる
* リストを徐々に(appendで)成長させる方式は要素数が最初からわかっていないときなどは便利

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def plot_square_by_for():
    X = []
    Y = []
    n = 100
    for i in range(n):
        x = 4 * np.pi * i / (n - 1)
        X.append(x)
        Y.append(np.sin(x))     # こちらは1点にたいするsin
    plt.plot(X, Y)
    plt.show()

plot_square_by_for()
""" """

""" md

* 同じリストでも, もう少しスマートにリスト内包表記で書いた例

"""

""" code w """
def plot_square_by_list_comprehension():
    n = 100
    X = [ 4 * np.pi * i / (n - 1) for i in range(n) ]
    Y = [ np.sin(x) for x in X ]
    plt.plot(X, Y)
    plt.show()

plot_square_by_list_comprehension()
""" """

""" md

## 少し違うフレーバーの描画

* plt.plot 関数は「与えられたx座標, y座標を線で結べ」という指令
* plt.なんとか という色々な関数があり, 異なる表示が可能

"""

""" md

#* scatter 

* バラバラの点として表示

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def scatter_square():
    X = np.linspace(0, 4*np.pi, 100) # 0から4*piまで99等分
    Y = np.sin(X)                  # universal関数で100点全てにsinを計算
    plt.scatter(X, Y)
    plt.show()                  # 描画!

scatter_square()
""" """

""" md

#* bar

* いわゆる棒グラフ

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def bar_square():
    X = np.linspace(0, 4*np.pi, 100) # 0から4*piまで99等分
    Y = np.sin(X)                  # universal関数で100点全てにsinを計算
    plt.bar(X, Y)
    plt.show()                  # 描画!

bar_square()
""" """

""" md

* 全部を覚えようなどと思わなくて良い
* ようするに, plt.xxxx の xxxx の部分を変えるだけで色々な表示が出来るということ
* どんなのがあるのか眺めてみたければギャラリーへ https://matplotlib.org/gallery/index.html

"""

""" md

# ややこしい計算結果の描画

* さて我々がこれからしばしばやりたくなるのは, シミュレーションなどでややこしい計算をした結果を表示することである
* 例えば質点の動きをシミュレートしたらその座標の時間変化を(例えば横軸をt, 縦軸を座標として)表示するとか, 2次元の軌跡(x(t), y(t))を表示するとか
* その場合も表示のやり方は変わらない. 計算の結果を適切にリストや配列に保存すればよい


"""

""" md

例えばいつぞややった(p08_de.py), バネに繋がれた質点

$$ m \ddot{x}(t) = -kx(t) $$

<img src="img/spring.svg" />

の動きをシミュレートする(最終時刻Tにおけるxとvを求める)関数は以下だった

"""

""" code w """
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
""" """
        
""" md

* 上記のfor文中で, 刻々とt, xが計算されている
* それらをリストに保存して, plt.plot に渡せば表示できる

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np
def mass_spring_plot(x0, v0, T, m, k):
    x = x0
    v = v0
    t = 0
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    T = []                      # 追加 (tの記録用)
    X = []                      # 追加 (xの記録用)
    for i in range(n):
        T.append(t)             # tを記録
        X.append(x)             # xを記録
        a = -k * x / m
        x += v * dt
        v += a * dt
        t += dt
    plt.plot(T, X)              # シミュレーション終了. plotを呼び出し
    plt.show()                  # 描画!

mass_spring_plot(1, 0, 10*np.pi, 1, 1)
""" """

""" md

* 可視化するまでは気づきにくいことだが, 見ての通り, 本来単振動するはずの運動が, 徐々に振幅が大きくなっていることがわかる(可視化の効能)
* いつかも述べたとおり上記で, vを先に更新してから(更新後のvを使って)xを更新したほうが誤差が少なくなる

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np
def mass_spring_plot_vx(x0, v0, T, m, k):
    x = x0
    v = v0
    t = 0
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    T = []                      # 追加 (tの記録用)
    X = []                      # 追加 (xの記録用)
    for i in range(n):
        T.append(t)             # tを記録
        X.append(x)             # xを記録
        a = -k * x / m
        v += a * dt             # vを先に更新
        x += v * dt             # xをあとに(更新後のvで)更新
        t += dt
    plt.plot(T, X)              # シミュレーション終了. plotを呼び出し
    plt.show()                  # 描画!

mass_spring_plot_vx(1, 0, 10*np.pi, 1, 1)
""" """

""" md

* もうひとつ, 今度は軌跡の表示をしてみよう
* 以下はいつぞや問題にした, 動かない重い質点(太陽)の周りを回る, 軽い質点(地球)のシミュレーション

"""

""" code w """
from vpython import *
import math
def sun_and_earth():
    G = 6.67408e-11             # 万有引力定数
    M = 1.98892e30              # 太陽の質量[kg]
    m = 5.9742e24               # 地球の質量[kg]
    r = 149.6 * 1e9             # 地球と太陽の距離 [m]
    x0 = vector(r, 0, 0)        # 初期位置
    v0 = vector(0, math.sqrt(G * M / r), 0) # 初速
    x = x0                                      # 地球の位置
    v = v0
    # 1 step = 1 日
    dt = 86400
    # 365 step = 1 年
    for i in range(365 * 3):
        dx = - x
        a = (G * M / dx.dot(dx)) * dx.norm()
        x += v * dt
        v += a * dt
    return (x,v)

sun_and_earth()
""" """

""" md 

#*P 軌跡の表示

上記(以下にもコピーした)のコードを修正し, 地球の軌跡を表示せよ

"""

""" code points=1 w """
# これを修正して地球の軌跡が出るようにせよ

from vpython import *
import math
def sun_and_earth_plot():
    G = 6.67408e-11             # 万有引力定数
    M = 1.98892e30              # 太陽の質量[kg]
    m = 5.9742e24               # 地球の質量[kg]
    r = 149.6 * 1e9             # 地球と太陽の距離 [m]
    x0 = vector(r, 0, 0)        # 初期位置
    v0 = vector(0, math.sqrt(G * M / r), 0) # 初速
    x = x0                                      # 地球の位置
    v = v0
    # 1 step = 1 日
    dt = 86400
    # 365 step = 1 年
    for i in range(365 * 3):
        dx = - x
        a = (G * M / dx.dot(dx)) * dx.norm()
        x += v * dt
        v += a * dt
    return (x,v)

sun_and_earth_plot()
""" """

""" code label=ans """
from vpython import *
import math
def sun_and_earth_plot():
    G = 6.67408e-11             # 万有引力定数
    M = 1.98892e30              # 太陽の質量[kg]
    m = 5.9742e24               # 地球の質量[kg]
    r = 149.6 * 1e9             # 地球と太陽の距離 [m]
    x0 = vector(r, 0, 0)        # 初期位置
    v0 = vector(0, math.sqrt(G * M / r), 0) # 初速
    x = x0                                      # 地球の位置
    v = v0
    X = []
    Y = []
    # 1 step = 1 日
    dt = 86400
    # 365 step = 1 年
    for i in range(365 * 3):
        dx = - x
        a = (G * M / dx.dot(dx)) * dx.norm()
        v += a * dt
        x += v * dt
        X.append(x.x)
        Y.append(x.y)
    plt.plot(X, Y)
    plt.show()

sun_and_earth_plot()
""" """

""" md

* ここでも見ての通り, 誤差の関係で地球がうまく周回軌道を回ってくれない
* vの更新とxの更新を入れ替えるとだいぶマシになる(上記を変更してやってみよ)

"""
