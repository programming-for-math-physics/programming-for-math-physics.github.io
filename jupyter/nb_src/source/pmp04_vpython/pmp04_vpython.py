""" md

#* VPython

 * VPythonは, 非常に簡単に3Dアニメーションを作成できるPythonのモジュール

"""

""" md

# 基本

 * mathモジュールを使う時同様, 最初にモジュールをimportする.
 * なぜか世の中の習わしで以下のスタイル(from xxx import *)でimportする

"""

""" code """
from vpython import *
""" """

""" md

 * 書きたいオブジェ毎に関数があり, それらを呼び出すことでオブジェが描画される.
 * 「球」を描く関数はsphere
 * 以下がうまく行けば上に球が表示される

もしいつまで立っても球が表示されなければ以下をやって下さい

 * メニューの "restart the kernel" ボタンを押してやり直す
 * それでもダメなら(左上のJupyterアイコンをクリックして)最初の画面に戻り, File -> Hub Control Panel -> Stop My Server -> Start My Server
 * それでもダメなら知らせて下さい. 恐らくシステム側の問題なので粘らず, 先のnotebook (pmp05) に進んだほうが良いです
"""

""" code """
sphere()
""" """

""" md
* `sphere`は`vpython`モジュール内の関数であり, 上記はこの関数を呼び出している
* `sphere`関数は, 呼び出されると, 半径1の球を原点に配置する
* これはこれまで見た, いわゆる入力から何かを計算して答えを返す, 数学でもよく出てくる関数とは少し異なるが, プログラミングではこのような, 「呼び出すと何かを起こす(表示する)関数」---計算結果というより, 計算させることで結果として起こる作用が大事な関数---がたくさん出てくる

"""

""" md

* 引数に色々な属性(位置, 色など)を指定できる. `pos=vector(a,b,c)`で位置を指定する.
* 以下を実行したら上(始めに急が現れた領域)をチェック
* うまく行けばそこに, 球が描き足される(わかりにくいので注意)

"""

""" code """
sphere(pos=vector(1,0,0))
""" """


""" md
なお`sphere()`は, `sphere(pos=vector(0,0,0))` と同じ意味になる.
つまり, `pos=vector(0,0,0)`を省略すると`vector(0,0,0)`を指定したのと同じ意味になる.

* Pythonの関数はこのように, 「渡しても省略してもよい良い引数(今の場合のpos)」を持つことができ, 省略した場合の値も(関数の定義の中で)決められる
* キーワード引数と呼ばれる
* 引数が多くて毎回全てを指定するのが面倒な場合によく使われ, `vpython`では多用される

"""

""" md

 * なお`vector(1,0,0)`もまた, 関数呼び出しであり, (1,0,0)というベクトルを作る関数である. ただの関数呼び出しだから変数に入れることももちろんできる

"""

""" code """
p = vector(0,1,0)
sphere(pos=p)
""" """

""" md

これらを実行した絵を見てもらえればわかるとおり, x軸が画面内の水平線, y軸が画面内の垂直線である. また, どうやら何も指定しないで作った最初の球は単位球(原点中心, 半径1)であろうということもわかる.

残るz軸が画面に垂直な直線で, 画面手前に伸びる向きがプラスの向き.

"""

""" code """
sphere(pos=vector(0,0,1))
""" """

""" md

描画されている画面上にマウスを持っていき

 * 右ボタンを押しながらドラッグすると, オブジェクトの向き(カメラの向き)を変えられる
 * マウスのダイアルをまわすとズーミング(カメラの位置)を変えられる

"""

""" md

# その他の属性の指定

`color=`で色を, `radius=`で半径を指定できる.
(s = canvas() については後で説明する)

"""

""" code """
s = canvas()
sphere(pos=vector(-1,0,0), color=color.red, radius=1.5)
""" """


""" md

# 作ったオブジェの属性をあとから変更する

一旦書いたオブジェの属性(位置, 色, 半径など)を__後から__変更することもできる. その場合, オブジェを作る関数呼び出しの結果を変数に入れておく.

"""

""" code """
s = sphere(pos=vector(2,2,2),color=color.blue)
""" """

""" md

その後で, その変数を通じてオブジェの属性を, 代入文で変更する. たとえば, `pos`という属性を変更するとそれは位置の変更になる.

"""

""" md

以下で, 作った青玉を黄色に変更

"""

""" code """
s.color = color.yellow
""" """

""" md

以下で, 作った青玉を少し遠くへ移動

"""

""" code """
s.pos = vector(3,3,3)
""" """

""" md

さらに遠くへ移動

"""

""" code """
s.pos = vector(5,5,5)
""" """

""" md

# vectorとその演算

vectorはベクトルで, 描画とは関係なくおなじみの演算もできる.

足し算

"""

""" code """
u = vector(1, 2, 3)
v = vector(4, 5, 6)
u + v
""" """

""" md 

引き算

"""

""" code """
v - u
""" """

""" md 

スカラ倍

"""

""" code """
3 * u
""" """

""" md 

内積

"""

""" code """
u.dot(v)
""" """

""" md

ベクトル演算を使うとオブジェを「少し動かす」ことができる.
これはアニメーションをするときの考え方になる.

"""

""" code """
s = canvas()
sun = sphere(color=color.yellow, radius=2)
t = sphere(color=color.blue)
""" """

""" md
以下を「何度も」実行してみよ.
(なお, x += a は x = x + a の略記)

"""

""" code """
t.pos += vector(1.5,1.5,1.5)
""" """

""" md

それをプログラムに「やらせる」方法が以下(詳しくは後ほど説明).
これは, 「繰り返し」というプログラムの超重要機能.

"""

""" code """
for i in range(10):
    t.pos += vector(0.5, 0.5, 0.5)
    rate(5)
""" """

""" md

以下は, 「20回左に動いたら20回右に動く」

"""

""" code """
s = canvas()
sun = sphere(color=color.yellow)
earth = sphere(color=color.blue, pos=vector(5,0,0))
dx = vector(1,0,0)
for i in range(20):
    earth.pos += dx
    rate(5) # 5フレーム/秒 で更新
for i in range(20):
    earth.pos -= dx
    rate(5) # 5フレーム/秒 で更新
""" """

""" md
注: 上記の rate(5)には二つの効果がある
 * 画面を更新する (これを呼ばないと上記が終了するまで画面の更新が行われない)
 * 5フレーム/秒 でrateが画面が更新されるように時間を調節する (具体的には, 他の部分の計算にほとんど時間がかからなかったとして, 0.2秒弱, 休憩する)
 * いずれまた説明する

"""

""" md

最後に, 球以外のオブジェを表示してみよう

"""

""" code """
box(pos=vector(5,5,5), color=color.yellow)
""" """

""" md

# キャンバス

 * これまでの例からわかるとおり, `sphere`, `box`などオブジェを描画する関数を呼んでいくと, 同じ画面の中に重ねてオブジェが描画されていく.
 * 別の画面に表示したければ, `canvas`という関数を呼び出すことで以降の描画が新しい画面(キャンバス)に対して行われるようになる

"""

""" code """
s = canvas()
box()
""" """

""" md

マウスでカメラ角度を変えて実際箱になっていることを確かめよ

"""

""" md

# 色々なオブジェ

 * 色々なオブジェを書いてみる.
 * どんなオブジェがあるか, それらの属性の設定の仕方は, https://www.glowscript.org/docs/VPythonDocs/index.html にある. 
 * 必要に応じて上記ページを自分で読む習慣をつけること(コンピュータを学ぶ際は, 「必要に応じて自分で調べる」ということが大事. いや, 本当は何を学ぶ場合でもそうなのだろうがコンピュータの場合はインターネット上に「原典(オリジナルの文書など)」があることがほとんどであるしそれが容易に見つかる場合がほとんどなので)

"""

""" md

矢印 (太さや向きを変えてみよ)

"""

""" code """
s = canvas()
arrow()
""" """

""" md

箱 (各辺の大きさを変えてみよ)

"""

""" code """
s = canvas()
box()
""" """

""" md

板 (といっても極端に薄い箱にすぎない)

"""

""" code """
s = canvas()
box(height=0.1)
""" """

""" md

円柱

"""

""" code """
s = canvas()
cylinder()
""" """

""" md

バネ

"""

""" code """
s = canvas()
helix()
""" """

""" md

複数のオブジェを組み合わせて新しいオブジェを作る

バトン

"""

""" code """
s = canvas()
a = sphere(pos=vector(-10,0,0))
b = sphere(pos=vector(10,0,0))
c = cylinder(pos=vector(-10,0,0), axis=vector(20,0,0), radius=0.5)
""" """

""" md

上記のような絵を書くには, 位置をすべて手動で指定する代わりに, 変数や演算を上手く使って, 書くのがよい

"""

""" code """
s = canvas()
a_pos = vector(-10,0,0)
b_pos = vector(10,0,0)
a = sphere(pos=a_pos)
b = sphere(pos=b_pos)
c = cylinder(pos=a_pos, axis=b_pos-a_pos, radius=0.5)
""" """

""" md

さらにこういう一連の操作は「関数」としてまとめて, 関数に渡す引数を変えるだけで自在に調整できるようにするのが良い.

"""

""" code """
def baton(a_pos, b_pos):
    a = sphere(pos=a_pos)
    b = sphere(pos=b_pos)
    c = cylinder(pos=a_pos, axis=b_pos-a_pos, radius=0.5)
""" """

""" code """
s = canvas()
baton(vector(0,-20,0), vector(0,20,0))
""" """

""" md label=prob,ans

#*P 天井からバネで吊るされるおもり

物理でよくある, 「天井」から「バネ」が生えていてその先に「おもり」がついている, という絵を描く関数 mass_spring() を書け

大きさ, 長さなど, それらしい絵になるように調節してみよ. テクスチャを使って天井をリアルにするのも良い.

"""

""" code points=1 w """
""" """

""" code label=ans """
def mass_spring():
    pos = vector(0,-3,0)
    ceil = box(height=0.1)
    spring = helix(axis=pos, radius=0.5)
    weight = sphere(pos=pos)

s = canvas()
mass_spring()
""" """

""" md label=prob,ans

#*P 正三角形

長さ$l$が与えられたら, 一辺の長さ$l$の正三角形を作図する関数`regular_triangle(l)`を書け(正三角形でありさえすれば座標は自由に決めて良い). そして, 長さ1, 2の正三角形を書け. 正三角形は, 上記のバトンのように, 各頂点に球があり, その間が円柱で結ばれているという絵で書く.

"""

""" code points=1 w """
""" """

""" code label=ans """
import math
def regular_triangle(l):
    u = l / math.sqrt(2)
    a = vector(u, u, 0)
    b = vector(u, 0, u)
    c = vector(0, u, u)
    sphere(pos=a)
    sphere(pos=b)
    sphere(pos=c)
    cylinder(pos=a, axis=b-a, radius=0.1)
    cylinder(pos=b, axis=c-b, radius=0.1)
    cylinder(pos=c, axis=a-c, radius=0.1)

s = canvas()
regular_triangle(1.0)
regular_triangle(2.0)
""" """

""" md label=prob,ans

#*P メタン分子

メタン分子 $\mbox{CH}_4$みたいなものを描く関数 mathane() を書け
"""

""" code points=1 w """
""" """

""" code label=ans """
import math
def methane():
    u = 5
    H0 = vector(u, u, 0)
    H1 = vector(u, 0, u)
    H2 = vector(0, u, u)
    H3 = vector(0, 0, 0)
    C = vector(0.5, 0.5, 0.5)
    sphere(pos=H0)
    sphere(pos=H1)
    sphere(pos=H2)
    sphere(pos=H3)
    sphere(pos=C)
    cylinder(pos=C, axis=H0-C, radius=0.1)
    cylinder(pos=C, axis=H1-C, radius=0.1)
    cylinder(pos=C, axis=H2-C, radius=0.1)
    cylinder(pos=C, axis=H3-C, radius=0.1)

s = canvas()
methane()
""" """

