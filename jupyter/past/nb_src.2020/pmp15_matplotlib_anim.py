""" md

# matplotlibでのアニメーション

"""

""" md

* グラフを書くにはmatplotlib, 3Dオブジェクトのアニメーションをするにはvpythonを使うのが基本だが, 2次元の場が時々刻々どのように変化するかを表示したいときなど, 「グラフのアニメーション」がしたくなることがある

* matplotlibにもアニメーション機能がある
* 実はあまりドキュメントがなくて不便なのでここにまとめておく

"""

""" md 

# {C.inc_section}. 1変数のグラフ(曲線)のアニメーション

## 復習: 

以下が $y = \sin x$のグラフを書くコード
(後でアニメーション化する都合で以前に書いたものよりも少し変更している)

"""

""" md
その前に, Jupyter notebook内でグラフを表示するには以下のおまじないを唱えておくと良いみたい
"""

""" exec-code-box """
%matplotlib notebook

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np

def draw_sin():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)
    plt.show()

draw_sin()

""" md 

## アニメ化したつもりで上手く行かない例

* たとえばこれを $y = \sin (x-k)$ の曲線を$k$を変えながら表示する(平行移動)アニメーションにしたいとしよう

* なんとなく以下のようなことをすればいいのではないかと思いたくなるが, 残念ながら以下は 色々な$k$に対する $y = \sin (x-k)$の曲線を一つの絵の中に重ねて書いて, それを最後に表示するだけのもので, アニメーションにはならない

"""

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np

def draw_many_sins():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = np.linspace(0, 10, 100)
    for k in range(20):
        y = np.sin(x-k)
        ax.plot(x, y)
    plt.show()

draw_many_sins()
    
""" md 

## アニメ化

* アニメーションにするには上記の繰り返しを

 1. 最初に一度だけ曲線を書き (plt.plot を呼び出し), 返り値(実は書かれた曲線を表すデータ)を変数に保存しておく
 1. それ以降は曲線を変更したい時に, 書かれた曲線の「データを変更する」関数(set_data)を呼び出す
 1. 「データを変更」したらおまじない(yield)を唱える

という風に変更する

* yieldはこれまで教えていないPython言語の要素なのだが話すと長くなるので今は, 実際に画面を更新する人に処理をうつす(で, 更新が終わったらまた戻ってくる)ための「おまじない」と思っていて下さい

"""

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anm

def generate_sins(fig):
    ax = fig.add_subplot(111)
    x = np.linspace(0, 10, 100)
    for k in range(100):
        y = np.sin(x-k/10)
        if k == 0:
            # 1周目は普通に plot などする
            # 返り値を保存しておく
            # 下記の代入文については以下の注を参照
            [ line ] = ax.plot(x, y)
        else:
            # 2週目以降は書いた曲線のデータを変更する
            # データを変更するための関数名はどうやって
            # 書いたか(plot, pcolor, etc.)により異なる
            line.set_data(x, y)
        # 更新してほしいところで, 更新してほしいオブジェクト
        # のリストを yield する(おまじない)
        yield [ line ]

""" md 

* その上で以下を呼び出すと実際の描画・アニメーションが始まる
* 以下で1行目 (fig, lambda x: x, repeat=0)はおまじないと思って良い
1. animate_sins が呼ばれる
1. animate_sins の中で yield するたびに yield した曲線が更新される
1. interval は ミリ秒 (1/1000秒)単位で更新間隔を指定する

"""

""" exec-code-box """
%matplotlib notebook
def animate_sins():
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=generate_sins(fig), 
                            interval=30)
    plt.show()
    return ani

animate_sins()

""" md

* 注: plt.plot は書かれた曲線のリストを返す
 * ここでは曲線を一つしか書いていないので1要素のリストが返る
 * 代入文 
```
[ line ] = plt.plot(x, y)
```
は右辺が1要素のリストである時にその唯一の要素をlineに代入するという構文(初出)
 * 想像通り右辺が2要素のリストなら, こんなことも書ける(以下は x=1, y=2 が代入される)
[ x,y ] = [ 1,2 ]

* 例えば以下は二つの曲線を同時にアニメーションする

"""

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anm

def generate_2_sins(fig):
    ax = fig.add_subplot(111)
    x = np.linspace(0, 10, 100)
    for k in range(100):
        y0 = np.sin(x - k/10)
        y1 = y0 + np.sin(x + k/10)
        if k == 0:
            # 1周目は普通に plot などする
            # 返り値を保存しておく
            # 下記の代入文については以下の注を参照
            [ line0,line1 ] = ax.plot(x, y0, x, y1)
        else:
            # 2週目以降は書いた曲線のデータを変更する
            # データを変更するための関数名はどうやって
            # 書いたか(plot, pcolor, etc.)により異なる
            line0.set_data(x, y0)
            line1.set_data(x, y1)
        # 更新してほしいところで, 更新してほしいオブジェクト
        # のリストを yield する(おまじない)
        yield [ line0,line1 ]

def animate_2_sins():
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            # これで肝心の処理が始まる
                            frames=generate_2_sins(fig),
                            interval=30)
    plt.show()
    return ani

animate_2_sins()

""" md 

# {C.inc_section}. 2変数の色表示(pcolor)のアニメーション

## 復習 通常の2変数の色表示(pcolor)

"""

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
import numpy as np

# [0,1]x[0,1]の領域を1辺hの正方形に区切り, 
# dtずつ時刻を進めて, 時刻Tまでシミュレートする
# 最終結果(だけ)を最後に表示する

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
        T[1:n-1,1:n-1] = (T[1:n-1,1:n-1] +
                          (k * dt / (h*h)) *
                          (T[2:n,  1:n-1] +
                           T[0:n-2,1:n-1] +
                           T[1:n-1,2:n] +
                           T[1:n-1,0:n-2] -
                           4 * T[1:n-1,1:n-1]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pc = ax.pcolor(X, Y, T)
    plt.show()

heat2d(2.0e-2, 1.0e-3, 1.0)

""" md 

# アニメ化: 

* 概念的な仕組みは曲線(plt.plot)の場合と同じ
* 違いは,
1. plt.pcolor で返されるのは書かれた2次元色表示を表すオブジェクト1つ. つまりリストではない(なので [ ... ] = ... みたいな変な代入文は不必要)
1. データの変更には set_data ではなく set_array という関数を用いる
1. しかもややこしいことにset_arrayに渡すデータは2次元配列ではなく, 2次元の点の色データを1次元に無理やり変えた(reshape)したもので, しかもその2次元の点のデータは, X, Yよりも1行, 1列ずつ小さいものにしておく必要がある. つまり元々が100x100の2次元データを pcolor に渡したのであれば, その後のset_arrayに渡すデータは 99*99=9801 要素の1次元配列. (余談: 1つずつ縮めなくてはいけない理由はよく考えるとわかります. xやyは格子点のデータであるのに対して, 色のデータはセルに対するものなので, 植木算の理屈で縦横1ずつ小さくなる. 最初にpcolorに渡したときも実は最後の1行, 1列は無視されている)

"""
    
""" exec-code-box """
%matplotlib notebook
def shrink(z):
    # z : 2次元配列 を縦横1ずつ縮めて, かつ無理やり1次元の配列に直す
    m,n = z.shape
    return z[:m-1,:n-1].reshape((m - 1) * (n - 1))
    
def generate_heat2d(fig, h, dt, end_t):
    ax = fig.add_subplot(111)
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
        print("step %d" % s)
        T[1:n-1,1:n-1] = (T[1:n-1,1:n-1]
                          + (k * dt / (h*h))
                          * (T[2:n,  1:n-1] +
                             T[0:n-2,1:n-1] +
                             T[1:n-1,2:n]   +
                             T[1:n-1,0:n-2] -
                             4 * T[1:n-1,1:n-1]))
        if s == 0:
            pc = ax.pcolor(X, Y, T)
        else:
            pc.set_array(shrink(T))
            yield [pc]

def animate_heat2d():
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=generate_heat2d(fig, 2.0e-2, 1.0e-3, 1.0),
                            interval=1)
    plt.show()
    return ani

animate_heat2d()

""" md 

# {C.inc_section}. 2変数の3次元表示(plot_surface)のアニメーション

## 復習 通常の3次元表示

"""

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot3d():
    X = np.linspace(0,1,101)
    Y = np.linspace(0,1,101)
    X,Y = np.meshgrid(X, Y)
    Z = 2 - X * X - Y * Y
    fig = plt.figure()
    axis = fig.add_subplot(111, projection="3d")
    sfc = axis.plot_surface(X, Y, Z)
    plt.show()

plot3d()

""" md 

## アニメ化

* 3D表示のアニメ化はこれまでの方法では何故か上手く行かない
* 代わりに1 stepごとに前に書いたsurfaceを消去して(axis.clear()), また書き直すということをしている
* データに合わせてmatplotlibが軸の範囲を調整してしまうとアニメーションにならなくなってしまうので以下では z の範囲を強制的に 0 .. 4 までにしている


"""

""" exec-code-box """
%matplotlib notebook
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anm
import numpy as np

def generate_plot3d(fig):
    X = np.linspace(-1,1,101)
    Y = np.linspace(-1,1,101)
    X,Y = np.meshgrid(X, Y)
    axis = fig.add_subplot(111, projection="3d")
    for k in np.linspace(0,2 * np.pi,101):
        print("step %f" % k)
        Z = 2 - np.cos(k) * (X * X + Y * Y)
        axis.clear()
        sfc = axis.plot_surface(X, Y, Z)
        axis.set_zlim(0,4)
        yield


def animate_plot3d():
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x,  repeat=0,
                            frames=generate_plot3d(fig),
                            interval=1)
    plt.show()
    return ani

animate_plot3d()

