""" md

#* リスト, タプル, 辞書, (numpy)配列, その他, 複数のデータを束ねたデータ

* 複数の数値, 複数の(Visual Python)のオブジェ, など, 複数のデータを扱うのに最もストレートな方法は, その数だけの変数を用意することである
* しかしこの方法には明らかに限界がある. 例えば100個の粒子の運動を追跡していくのに, 各粒子の位置, 速度, それぞれのx,y,z成分をひとつずつの変数にしたら, 変数が600個必要になる
* 仮に根性でやったとしても, $n$を与えられて「$n$個」の粒子の運動を追跡せよと言われたら, 変数を何個用意していいかわからない
* ある文を100回, または(与えられた)$n$回実行するのに for 文が決定的に重要であった
* それと同じように, 一つのデータ, したがってひとつの変数に代入できるデータ, でありながら, 内部に多数, 100個でも, $n$個でも, のデータを持つことが出来る機能が決定的に重要
* そのために
 * Pythonにもともと備わったいくつかのデータ構造(リスト, タプル, 辞書など)
 * 多数の数値を扱うのに特化したnumpyというライブラリ(モジュール)の, 配列
がある
* 本ゼミにおいてはnumpy配列が特に重要なため, リスト, タプル, 辞書は最小限の説明に留める

"""

""" md

# リスト

* 以下の最小限の説明に加えて以下を時間のある時に読んでおくと良い
* https://docs.python.org/ja/3/tutorial/introduction.html#lists
* https://docs.python.org/ja/3/tutorial/datastructures.html#more-on-lists

## リスト式

* __文法:__ 以下のような記法(リスト式)でリストを作ることが出来る

```
[ 式 , 式 , ... , 式 ]
```
"""

""" md

* 一番簡単な例

"""

""" code w """
[ 1.0, 1.2, 1.4, 1.6, 1.8, 2.0 ]
""" """

""" md

* リストは絵で書けば以下のようなものだと思えば良い
* 値を入れる「箱」が一列に並んでいる

<img src="img/list.svg" />

* Jupyter環境のバグで, 上の絵が上手く表示されていないと思われる
* 絵を正しく表示するにはこのnotebookをJupyterLab環境で表示する. それにはページ左上隅の Jupyterアイコンで初期ページに行き, 左のフォルダから pmp11_list -&gt pmp11_list.py.ipynb を選び表示する (以下でも同様)

"""

""" md

* 要素数は任意で, 特に0個でもよい

"""

""" code w """
[]
""" """

""" md 

* 各要素の式は計算を伴う__任意の式__であって良い
* 当然変数を含んだりしていてもよい
* リストは式そのものを覚えているのではなくあくまで計算した結果を保持している

"""

""" code w """
x = 7 ** 8

[ 1+2, 3*4, 5/6, x ]
""" """

""" md 

* 重要なことはこれ(リストの式)自身が「式」の一種であって, 他の式が許される任意の場所で許されること
* 例えば当然, 代入文の右辺に書ける

"""

""" code w """
l = [ 1+2, 3**4, 5/6, x ]

l
""" """

""" md 

* 当然, 関数の返り値として返すことも出来る

"""

""" code w """
def mk_list():
    return [ 1+2, 3**4, 5/6, x ]

mk_list()
""" """

""" md

## リストに対する操作

__要点:__

* len関数 : `len(リスト)` でリストの長さ
* appendメソッド : `リスト.append(要素)` でリスト末尾に要素を追加
* 添字式 : `リスト[i]` でリストのi番目の要素
* 代入 : `リスト[i] = x` でリストのi番目の要素を変更
* リストの連結 : `リスト + リスト` で二つのリストを連結
* リストの繰り返し : `リスト * 整数` で同じリストを繰り返す(多数回連結)

"""

""" md

### len関数

"""

""" code w """
l = [ 1.0, 1.2, 1.4, 1.6, 1.8, 2.0 ]

len(l)
""" """

""" md

### appendメソッド

appendはリストの末尾に要素を追加する

<img src="img/append.svg" />

"""

""" code w """
l.append(3.0)

l
""" """

""" md

### 添字式

* 添字は0から始まる

"""

""" code w """
l[0]
""" """

""" md

* 0から始まる帰結として, $n$要素のリストの最後の添字は$n-1$
* 範囲外の添字でアクセスするとエラーになるので注意

"""

""" code w """
l[6]
""" """

""" code w """
# error
l[7]
""" """

""" md

### 要素の更新

"""

""" code w """
l[3] = 30

l
""" """

""" md

### 連結

"""

""" code w """
ll = l + l

ll
""" """

""" md

### 繰り返し

"""

""" code w """
lx = l * 5

lx
""" """

""" md

## for文によるリストの作成

* 柔軟にリストを作るために必要なのはappendという操作で, 一回実行する度に1個要素が増えるので, appendを$n$回繰り返せば$n$要素のリストが出来る
* appendを$n$回繰り返すのに当然ことながら for 文が使える

* 例えば長さnが与えられたら, 球(VPythonのsphere)を$n$個等間隔に表示し, それらを入れたリストを返す関数

"""

""" code w """
#
# なぜか絵が出なかったら, メニューから Kernel -> Restart & Clear Outputしてみてね
#

from vpython import *

def many_spheres(n):
    cv = canvas()
    S = []
    for i in range(n):
        x = vector(i, 0, 0)
        S.append(sphere(pos=x, radius=0.1))
    return cv,S

cv,S = many_spheres(10)
""" """

""" md

## for文によるリストの走査

* これまでfor文は
```
for i in range(a, b):
    ...
    ...
```
で i = a, a+1, a+2, ..., b-1 として文(...)を実行するものとして理解していた
* 実はfor文は, 「リストの要素を順に処理する」ために使える

```
for x in リスト:
    ...
    ...
```
で, リストの各要素xに対して ... を実行する

"""

""" code w """
l = [ 2, 3, 5, 7, 9 ]

for x in l:
    print(x)
""" """

""" md

例えば以下は与えられたリストに含まれるの全要素の和を計算する関数

"""

""" code w """
def sum_list(l):
    s = 0
    for x in l:
        s = s + x
    return x

sum_list([1,3,6])
""" """

""" md

* 例えばその後それらの球を乱数でブルブルと動かすにはこんなことをすれば良い
* rgは乱数生成器で, 使い方は下で説明する

"""

""" code w """
from vpython import *
import random

def move_random_all(S, rg):
    for s in S:
        # S中の各s (sphere)に対して, posを少し, 変更
        v = vector(rg.random() - 0.5, rg.random() - 0.5, rg.random() - 0.5)
        s.pos = s.pos + 0.2 * v

def vibrating_balls():
    cv,S = many_spheres(10)        # 10個のsphereを生成
    rg = random.Random()
    for t in range(1000):       # 1000回, ブルブル動かす
        move_random_all(S, rg)
        rate(30)
    return cv,S

cv,S = vibrating_balls()
""" """

""" md

#* 参考: 乱数生成器の使い方

* モジュールrandomをimport
* rg = random.Random() で乱数生成器を作成(して変数へ代入)
* rg.random() で実数の乱数
* rg.randint() で整数の乱数

* 詳しくは https://docs.python.org/ja/3/library/random.html

"""

""" code w """
import random
rg = random.Random()  # 乱数生成器を作る
print(rg.random())           # [0,1]の実数をひとつ生成する
print(rg.randint(50, 100))   # [50,100]の整数をひとつ生成する
for i in range(10):          # 当然こうして多数の乱数を生成できる
    print(rg.random())
""" """


""" md 

#*P $n$個の惑星のシミュレーション

* この問題はチームで協力してひとつのプログラムを作るようにすること
* 以前にやった, 太陽と1つの惑星のシミュレーションを, 太陽と$n$個の惑星のシミュレーションに拡張したもの. その問題の答えを参考にすると良い

以下の設定で $(n+1)$ 個の球の動きをVPythonで可視化せよ

* 原点に太陽がいて, 動かない
* 太陽以外に$n$個の惑星がいて, 太陽(のみ)から力を受ける(惑星間の力は無視)
* $i$番目の惑星は, 時刻$t=0$において位置が$(i+2,0,0)$, 速度が$(0,1/\sqrt{n},0)$
* 位置$x$にいる惑星は, 太陽から力を受けて以下の加速度を持つ

$$ a = - \frac{x}{|x|^3} $$

* 時間の刻み(dtの値)は0.005付近から適当に試行錯誤してみよ
* 大きくしすぎると惑星がすっ飛んでいったりとおかしな挙動になってしまう
* なお, ここでは理由は説明しないが, 加速度を計算した後,
```
 位置 += 速度 * dt
 速度 += 加速度 * dt
```
とする代わりに
```
 速度 += 加速度 * dt
 位置 += 速度 * dt
```
とする(つまり速度を先に更新する = 位置を更新するのに, 更新後の速度を使う)と, 誤差が小さくなる.

"""

""" code points=1 w """
""" """

""" code label=ans """
from vpython import *
import math

def make_planets(n):
    cv = canvas()
    X = sphere(pos=vector(0,0,0), color=color.yellow, radius=0.3)
    S = []
    for i in range(n):
        x = vector(2 + i, 0, 0) # 1, ..., 1+0.5*(n-1)
        v = vector(0, 1.0/math.sqrt(n), 0)
        S.append(sphere(pos=x, vel=v, radius=0.2))
    return cv,S

def step(S, dt):
    for s in S:
        dx = - s.pos
        r2 = dx.dot(dx)
        alpha = dx / (r2 * math.sqrt(r2))
        s.vel += alpha * dt
        s.pos += s.vel * dt
        
def sim_planets(n):
    cv,S = make_planets(n)
    dt = 0.005
    for i in range(100000):
        step(S, dt)
        rate(1/dt)
    return cv,S
    
cv,S = sim_planets(10)
""" """

""" md

## (参考) リストの内包表記

* これまでリストを作るのにいくつかのやり方を学んだ
 * リスト式 `[ 式, 式, ... , 式 ]`
 * リストにappendを繰り返して成長させる
前者は一定個数の要素の, 短いリストにしか使えない. 後者は長いリストでも$n$要素のリストでも作れるが, そのために一々for文を書くのが面倒なこともある
* よりお手軽に長いリストを簡単に作れる(ときもある)のがリスト内包表記
* より詳しくは https://docs.python.org/ja/3/tutorial/datastructures.html#list-comprehensions

__文法:__

```
[ 式 for 変数名 in 式' ]
```

ここで式' のところには for 文と同様, range(...) 式やリストになる式が来る.

例を見たほうが早いので例を見せる

"""

""" code w """
[ i * i for i in range(10) ]
""" """

""" code w """
import math
[ math.sin(math.pi * i / 100) for i in range(100) ]
""" """

""" md

見ての通り文法的にはfor 文に似ている. for文の文法は

```
for x in R:
  文
```

であり, 「R中の各要素xに対し, 文を実行」ということである.

リスト内包表記は

```
[ 式 for x in R ]
```

であり,「R中の各要素xに対し, 式を評価」し, その結果をリストにするということである. 

"""

""" code w """
[ i * i for i in range(10) ]
""" """

""" md

を, あえてリスト内包表記を使わないで書くならば以下と同じことである.

"""

""" code w """
L = []

for i in range(10):
    L.append(i * i)

L
""" """

""" md

例として, 以前にやった積分を行う関数を取り上げる

"""

""" code w """
def integral(f, a, b, n):
    s = 0
    dx = (b - a) / n
    for i in range(n):
        x = a + i * dx
        s += f(x) * dx
    return s
""" """

""" code w """
import math
integral(math.sin, 0, math.pi/2, 100)
""" """

""" md

* これをリスト内包表記を使って書いて見る

"""

""" code w """
def integral2(f, a, b, n):
    dx = (b - a) / n
    return sum([ f(a + i * dx) * dx for i in range(n) ])
""" """

""" code w """
import math
integral2(math.sin, 0, math.pi/2, 100)
""" """

""" md

* または以下のようにしたほうが見やすいかも知れない

"""

""" code w """
def integral3(f, a, b, n):
    dx = (b - a) / n
    X = [ a + i * dx for i in range(n) ] # 分割点のx座標だけを並べたもの
    return sum([ f(x) * dx for x in X ])
""" """

""" code w """
import math
integral3(math.sin, 0, math.pi/2, 100)
""" """

""" md

* リスト内包表記は見やすく, 美しいプログラムを書くのに貢献する
* リスト内包表記に限らずプログラムの「見た目の良さ」「美しさ」を大切にしたほうが良い
* 「美しさ」は主観的で, 確かな基準を示すのが難しいが, 数学の計算をしているなら, 「見慣れた数式に見た目が近い」というのはひとつの基準である
* 「見慣れた数式に見た目が近い」$\approx$「読みやすい・理解しやすい」$\approx$「間違いを起こしにくい・間違いに気づきやすい」ということにつながる

"""


""" md

# タプル

* タプルについては説明を省略する. 以下を読んでおくと良い
* リストと似たものであり, この授業ではなくても十分生きていける
* https://docs.python.org/ja/3/tutorial/datastructures.html#tuples-and-sequences

"""

""" md

# 辞書

* 辞書についても説明を省略する. 
* 本当はPythonが強力な言語であるための重要な機能だが, この授業ではなくても十分生きていける
* https://docs.python.org/ja/3/tutorial/datastructures.html#dictionaries

"""
