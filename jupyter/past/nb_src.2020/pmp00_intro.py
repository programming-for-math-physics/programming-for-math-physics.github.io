""" md

# {C.inc_section}. Jupyter環境の基本

Jupyter環境は今まさに使っているもので, 様々なプログラミング言語をウェブブラウザを通して実行し, プログラム, その出力, このようなドキュメント, を一緒にして保存できる仕組み.

本初年次ゼミではJupyter環境を用いながら, Pythonというプログラミング言語を用いて, プログラミングを習得する.

Jupyterでは以下のような四角を __セル__ と呼ぶ.

セルには Pythonの__「式」__や__「文」__を, (いくつでも)書ける(「式」と「文」の違いは今は余り気にしなくて良い. 以下でわかる). 
"""

""" empty-code """

""" md
セルの上でマウスをクリックするとセルが「選択」され, 入力できる状態になる(その他にもキーボードの矢印キーで, 選択することもできる).

セルに`Shift + Enter` を入力する (`Shift`キーを押しながら`Enter`キーを押す)と, セルの中身が計算される (「計算する」=「式の値を規則に従って求める」ということなので, 「評価する」ということもある. また, 「実行する」ということもある)

"""

""" md

# {C.inc_section}. まずはやってみよう

以下のセルに何が書かれているかを確認し(雰囲気だけわかれば, 意味がわからなくても気にする必要はない), `Shift + Enter` を押して実行してみよ.

"""

""" exec-code-box """
1 + 2

""" md

# {C.inc_section}. matplotlibでグラフが書ける

"""

""" error-code-box """
%matplotlib inline

""" md """

# -------- 実行してみよ Execute this cell --------
import matplotlib.pyplot as plt
import math

X = range(0,100)
Y = [ math.sin(x) for x in X ]

plt.plot(X, Y)
plt.show()

""" md

# {C.inc_section}. numpyで行列計算(など色々)ができる

以下は

$$ A = \left( \begin{{array}} \\ 1 & 2 \\ 3 & 4 \end{{array}} \right) $$

$$ x = \left( \begin{{array}} \\ 5 \\ 6 \end{{array}} \right) $$

に対して

$$ y = Ax$$

を計算し, その後で(求まった$y$に対して方程式)

$$ Ax = y$$

を解いている(ので, 当然

$$ x = \left( \begin{{array}} \\ 5 \\ 6 \end{{array}} \right) $$

が解として求まる)

"""

""" exec-code-box """
import numpy as np
A = np.matrix([[1,2],[3,4]])
x = np.matrix([[5],[6]])
y = A * x
# Ax = y を解く
np.linalg.solve(A, y)

""" md

# {C.inc_section}. scipyでも色々な計算ができる

以下は 単位円に内接する三角形の面積$S$の最大値(正確には$-2S$の最小値)を求めている.

ご存知の(または容易に想像がつく)通り, 最大になるのは正三角形のときで, その面積は$\frac{{3\sqrt{{3}} }}{{4}}$なので, 以下では答えとして, $=-\frac{{3\sqrt{{3}} }}{{2}} \approx -2.5980762...$が求まるはず.

"""

""" exec-code-box """
import scipy.optimize
from math import pi,sin

def f(x):
    return - sin(x[0]) - sin(x[1]) - sin(2.0 * pi - x[0] - x[1])

print(scipy.optimize.minimize(f, (0.5, 0.5)))

""" md

# {C.inc_section}. VPython で3Dグラフィクス・アニメーションができる

"""

""" exec-code-box """
from vpython import *
sphere()
