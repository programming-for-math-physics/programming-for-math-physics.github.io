""" md

#* matplotlib で2変数関数を表示する

* 1入力(x), 1出力(y)の関数を表示するには, xを横軸, yを縦軸にとり, plot, scatter, barなどで表示すれば良い

* 2入力(x, y), 1出力(z)の関数を表示するにはどうしたらよいか?
* 1つの方法はzを色で表示する(pcolor)方法
* もう1つの方法はz = f(x,y)のグラフを曲面(3D)で表示する方法

"""

""" md

# 色で表示する

* import matplotlib.pyplot as plt としておいて plt.pcolor という関数を呼び出すのが基本
* データの渡し方:
* pcolorに渡すのは, 2次元の格子点の, xの値だけを並べた2次元配列(またはリスト), yの値だけを並べた2次元配列(またはリスト), zの値だけを並べた2次元配列(またはリスト).
* shading='auto' はpcolorを使うときのおまじないだと思ってください(理解したい人は https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolor.html?highlight=pcolor#matplotlib.pyplot.pcolor )
* 下記を実行して納得して下さい

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_a_few_2d():
    print("pcolor_a_few_2d")
    X = np.array([ [ 0,1,2,3 ], [ 0,1,2,3 ], [ 0,1,2,3 ], [ 0,1,2,3 ] ])
    Y = np.array([ [ 4,4,4,4 ], [ 5,5,5,5 ], [ 6,6,6,6 ], [ 7,7,7,7 ] ])
    Z = X * X - Y * Y
    plt.pcolor(X, Y, Z, shading='auto')
    plt.show()

pcolor_a_few_2d()
""" """

""" md

* 上の点の与え方はいかにもまだるっこしい
* できれば, X = [ 0, 1, 2, 3 ], Y = [ 4, 5, 6, 7 ] と書くだけで済ませたい
* それをやるのが np.meshgrid という関数

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_a_few_with_meshgrid():
    print("pcolor_a_few_with_meshgrid")
    X = np.array([ 0,1,2,3 ])
    Y = np.array([ 4,5,6,7 ])
    X,Y = np.meshgrid(X, Y)
    Z = X * X - Y * Y
    plt.pcolor(X, Y, Z, shading='auto')
    plt.show()

pcolor_a_few_with_meshgrid()
""" """

""" md

* もちろん座標をベタに書くことはほとんどしない

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_with_meshgrid():
    print("pcolor_with_meshgrid")
    X = np.linspace(0,3,101)
    Y = np.linspace(4,7,101)
    X,Y = np.meshgrid(X, Y)
    Z = X * X - Y * Y
    plt.pcolor(X, Y, Z, shading='auto')
    plt.show()

pcolor_with_meshgrid()
""" """

""" md

# 曲面(3D)で表示する

* 若干おまじないと手順が増える
* おまじない: `from mpl_toolkits.mplot3d import Axes3D`
* 手順として, 最終的に plot_surface という関数を呼べば良いのだが, 
```
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
```
という手順を踏んだ上で, axに対してplot_surfaceを呼び出す

"""

""" code w """
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot3d():
    print("plot3d")
    X = np.linspace(-1,1,101)
    Y = np.linspace(-1,1,101)
    X,Y = np.meshgrid(X, Y)
    Z = 2 - X * X - Y * Y
    fig = plt.figure()
    axis = fig.add_subplot(111, projection="3d")
    axis.plot_surface(X, Y, Z)
    plt.show()

plot3d()
""" """

""" md

# 参考 fig, axisについて

 * 上記で登場した
```
    fig = plt.figure()
    axis = fig.add_subplot(111, projection="3d")
```
は, 3D表示のためだけにあるわけではなく, 一般にグラフの表示をカスタマイズしたり, 複数のグラフを表示したりするのに使える

 * まず説明のために, 先に説明した pcolor を(あえて), fig, ax を経由して表示することが出来る

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_with_fig_axis():
    print("pcolor_with_fig_axis")
    X = np.linspace(0,3,101)
    Y = np.linspace(4,7,101)
    X,Y = np.meshgrid(X, Y)
    Z = X * X - Y * Y
    fig = plt.figure()
    axis = fig.add_subplot(111)
    axis.pcolor(X, Y, Z, shading='auto')
    plt.show()

pcolor_with_fig_axis()
""" """

""" md

 * このようにしておくと, 
  1. 別のグラフを同じ窓に配置する
  1. グラフのラベルや範囲などをカスタマイズすることが出来る

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_2x3_axes():
    print("pcolor_2x3_axes")
    X = np.linspace(0,3,101)
    Y = np.linspace(0,3,101)
    X,Y = np.meshgrid(X, Y)
    fig = plt.figure()
    axis1 = fig.add_subplot(231)
    axis2 = fig.add_subplot(232)
    axis3 = fig.add_subplot(233)
    axis4 = fig.add_subplot(234)
    axis5 = fig.add_subplot(235)
    axis6 = fig.add_subplot(236)
    axis1.pcolor(X, Y, Y - 1 * X, shading='auto')
    axis2.pcolor(X, Y, Y - 2 * X, shading='auto')
    axis3.pcolor(X, Y, Y - 3 * X, shading='auto')
    axis4.pcolor(X, Y, Y - 4 * X, shading='auto')
    axis5.pcolor(X, Y, Y - 5 * X, shading='auto')
    axis6.pcolor(X, Y, Y - 6 * X, shading='auto')
    plt.show()

pcolor_2x3_axes()
""" """

""" md

* 上記 fig.add_subplot(23$x$) は 2 x 3 のタイルを準備し, その中の$x$番目の位置にグラフを追加するコマンド
* 返された値 (axisと呼ばれる)がひとつの「グラフ」を表すと思えば良い
* なおもちろん上のように6つも文を並べる代わりにもう少しスマートな書き方は以下
"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_2x3_axes_loop():
    print("pcolor_2x3_axes_loop")
    X = np.linspace(0,3,101)
    Y = np.linspace(0,3,101)
    X,Y = np.meshgrid(X, Y)
    fig = plt.figure()
    for k in range(1,7):
        axis = fig.add_subplot(230 + k)
        axis.pcolor(X, Y, Y - k * X, shading='auto')
    plt.show()

pcolor_2x3_axes_loop()
""" """

""" md

* axisに対しては色々な属性を設定してグラフをカスタマイズできる
* たとえばx軸, y軸につけるラベル, x, yの範囲など
* 詳しくは, https://matplotlib.org/3.1.0/api/axes_api.html

"""

""" code w """
import matplotlib.pyplot as plt
import numpy as np

def pcolor_with_label():
    print("pcolor_with_label")
    X = np.linspace(0,3,101)
    Y = np.linspace(0,3,101)
    X,Y = np.meshgrid(X, Y)
    fig = plt.figure()
    axis = fig.add_subplot(111)
    axis.set_xlabel("X")
    axis.set_ylabel("Y")
    axis.set_xlim((-1,4))
    axis.set_ylim((-1,4))
    axis.pcolor(X, Y, Y - X, shading='auto')
    plt.show()

pcolor_with_label()
""" """

