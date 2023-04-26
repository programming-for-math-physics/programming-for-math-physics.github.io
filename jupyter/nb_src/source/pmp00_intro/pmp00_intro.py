""" md

#* Jupyter環境の基本

* Jupyter環境は, 今まさに使っているもので, 様々なプログラミング言語をウェブブラウザを通して実行し, プログラム, その出力, このようなドキュメント, を一緒にして保存できる仕組み.

* 本初年次ゼミではJupyter環境を用いながら, Pythonというプログラミング言語を用いて, プログラミングを習得する.

* Jupyterでは以下のような四角を __セル__ と呼ぶ.

* セルには Pythonの__「式」__や__「文」__を, (いくつでも)書ける(「式」と「文」の違いは今は余り気にしなくて良い. 以下でわかる). 
"""

""" code w """
""" """

""" md

* セルの上でマウスをクリックするとセルが「選択」される
* そこで`Shift + Enter` を入力する (`Shift`キーを押しながら`Enter`キーを押す)と, セルの中身が計算される (「計算する」=「式の値を規則に従って求める」ということなので, 「評価する」ということもある. また, 「実行する」ということもある)

* 一部のセルは自分で修正したり, 一からコードを書くようになっており, 選択すると入力できる状態になる(その他にもキーボードの矢印キーで, 選択することもできる)
* 自分では入力できないセルもある(単に書かれたものを実行して結果を見ることを想定している場合)

"""

""" md

# まずはやってみよう

* 以下のセルに何が書かれているかを確認し(雰囲気だけわかれば, 意味がわからなくても気にする必要はない), `Shift + Enter` を押して実行してみよ.

"""

""" code """
1 + 2
""" """

""" md

# matplotlibでグラフが書ける

"""

""" code """
%matplotlib inline
""" """

""" code """
import matplotlib.pyplot as plt
import math

X = range(0,100)
Y = [ math.sin(0.2 * x) for x in X ]

plt.plot(X, Y)
plt.show()
""" """

""" md

# numpyで行列計算(など色々)ができる

以下は

$$ A = \left(\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}\right) $$

に対して

$$ y = Ax$$

を計算し, その後で(求まった$y$に対して方程式)

$$ Ax = y$$

を解いている(ので, 当然

$$ x = \left( \begin{array}{cc} 5 \\ 6 \end{array} \right) $$

が解として求まる

"""

""" code """
import numpy as np
A = np.matrix([[1,2],[3,4]])
x = np.matrix([[5],[6]])
y = A * x
# Ax = y を解く
print(np.linalg.solve(A, y))
""" """

""" md

# scipyでも色々な計算ができる

以下は 単位円に内接する三角形の面積$S$の最大値(正確には$-2S$の最小値)を求めている.

ご存知の(または容易に想像がつく)通り, 最大になるのは正三角形のときで, その面積は$\frac{{3\sqrt{{3}} }}{{4}}$なので, 以下では答えとして, $=-\frac{{3\sqrt{{3}} }}{{2}} \approx -2.5980762...$が求まるはず.

"""

""" code """
import scipy.optimize
from math import pi,sin

def f(x):
    return - sin(x[0]) - sin(x[1]) - sin(2.0 * pi - x[0] - x[1])

print(scipy.optimize.minimize(f, (0.5, 0.5)))
""" """

""" md

# VPython で3Dグラフィクス・アニメーションができる

* 以下を実行して, 黒い空間に大きな白い球が現れたら成功
* だが, 未だ解明できていない原因により, 何も表示されない, 黒い空間だけが表示されることがあるなど, <font color="red">動作がとても怪しい</font>
* うまく表示されなかったら以下をやってみてください ([詳細](https://pmp.eidos.ic.i.u-tokyo.ac.jp/html/jupyter.html#when_something_went_wrong))
  * メニューの Kernel -&gt; Restart Kernel
  * メニューの File Kernel -&gt; Hub Control Panel -&gt; Restart Kernel -&gt; Stop My Server -&gt; Start My Server
* ただしそれでもうまく行くとは限らない. その場合は今日のところは放っておいてください

* 以下でsphere() の変わりに helix() とすると, バネのようなもの画表示される
* 球はダメでなぜかバネなら表示されるなんてこともある
* どんなものが表示できるかは [このページ](https://www.glowscript.org/docs/VPythonDocs/index.html) の, 左のメニュー (Choose a 3D object) にあるので試してみてください

"""

""" code w """
from vpython import *
sphere()
""" """

""" md

* 与えられたセルを実行するだけでなく, 自分で新しいセルを作って自由に書くこともできるので適当に遊んでみてください
* メニューの + またはキーボードで 'b' でセルを追加
* 'x' でセルを削除
など

"""
