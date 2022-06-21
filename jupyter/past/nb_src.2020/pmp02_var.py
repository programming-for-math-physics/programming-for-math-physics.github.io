""" md

# {C.inc_section}. 変数: 「プログラミング」の第一歩

これまで, Pythonで色々な式が書けること --- 数は整数, 浮動小数点数はもちろん, 複素数が扱える, 整数は巨大でも良い, $\sin$, $\cos$はじめ色々な関数が使えるなど --- を学んだが, それらは一言で言って, 「高機能な電卓」という程度のことであり, プログラムというには遠い. あまりコンピュータに何かを「やらせている」感じはしない.

プログラムをプログラムたらしめる要素はいくつかあるがその一番目が「変数」である. 変数は, ある式を評価した結果に名前をつけて, 後でその名前でその値を参照できるようにする機能である.

まず以下で, $\sin 1$の結果を`x`という変数に覚えておく
"""

""" exec-code-box """
import math
x = math.sin(1)

""" md

このような記法を__代入文__と呼ぶ. つまり, 代入文はある式の結果(値)に名前をつける, あるいは同じことだが別の言い方として, 変数に式の結果(値)を格納する, という効果を持つ.

上記を実行したあと, 以下で`x`の値が表示できる.

"""

""" exec-code-box """
x

""" md

それだけでなく, `x`を使って色々な式を作ることができる. 要するに`x`も式の一種であって, 算術演算や関数の入力にしたりすることができる.

"""

""" exec-code-box """
x * x


""" md 

以下はおなじみの公式

$$ \cos^2 t + \sin^2 t = 1$$

を($t = 1$に対して)確かめてみたものである.
"""

""" exec-code-box """
t = 1
x = math.cos(t)
y = math.sin(t)
x * x + y * y

""" md 

この例は結局,

`math.cos(1) * math.cos(1) + math.sin(1) * math.sin(1)`

を計算しているに過ぎないのだが, 明らかに変数を使ったほうが短くわかりやすく, 意味も把握しやすい.

また, 同じ計算を, $t = 1$ではなく$t = 1.5$でやりたくなった時に, 変数を使っていれば書き換える場所は一箇所で済むのに対し, 後者の場合, 四箇所を書き換える羽目になる. プログラムが大きくなってくるとこのような変更を間違う可能性も大きくなる. 変数を使うことで, 「(やりたい計算が多少代わっても)こことここでは同じ値を使う」という制約を保つことができる.

実は変数には, 単に複雑な式を見やすく書けるという以上の, もっと本質的な意味がある(変数なしには決してできない計算がある)のだが, それはこのあとで関数や繰り返しを学ぶ時にわかる.
"""

""" md 

# 問題 {C.inc_problem}: 点と直線の距離の計算

直線$ax+by+c=0$と点$(x,y)$との距離の公式は

$$ \frac{{|ax+by+c|}}{{\sqrt{{a^2+b^2}}}} $$

であった. この公式を用いて,

直線$3x+4y+5 = 0$と点$(2,1)$の距離を, 変数を用いて見通しよく(あまり複雑な式を一行に書かずに)計算し, 結果を変数 l に格納せよ.

"""

""" write-code-box """

""" answer-code-box """
a = 3
b = 4
c = 5
x = 2
y = 1
si = abs(a * x + b * y + c)
bo = math.sqrt(a*a + b*b)
l = si/bo

""" md 
lを表示してみよう
"""

""" exec-code-box """
l

""" test-code-box """
assert(l == 3)

""" md 

# {C.section}-{C.inc_subsection}. 文や式の「順序」は重要

ところで

```
t = 1
x = math.cos(t)
y = math.sin(t)
x * x + y * y
```

の4行を, (後に述べる理由により変数名はx -> xx, y -> yy, t -> ttに変更しているがそれは今は重要ではない)以下のように入れ替えてみるとどうなるか?

"""

""" error-code-box """
xx * xx + yy * yy
xx = math.cos(tt)
yy = math.sin(tt)
tt = 1

""" md
やってみるとわかるが以下のようなエラーになる. 

```
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-1-d0a489cf3236> in <module>
----> 1 xx * xx + yy * yy
      2 xx = math.cos(tt)
      3 yy = math.sin(tt)
      4 tt = 1

NameError: name 'xx' is not defined
```

それは, xx という変数が「定義されていない」というエラーである
(プログラミングでは, 習得した後も間違いを犯すのが日常なので, 上記のようなエラーメッセージをきちんと読んでその意味を解読し, 自分の間違いを発見できるようになることも重要. それは後の話題).

数学では, ある式(例えば $x^2+y^2$)の中で文字(例えば $x$)を使っておいて, あとから("ここで $x = \cdots$である")などといって定義することはよくある. 

$$ x * x + y * y $$
ただしここで,
$$ x = \ldots t \ldots $$
$$ y = \ldots t \ldots $$
$$ t = \ldots $$

のように. 全体としてすべての文字にきちんと定義が与えられていれば良しとして, それらを書く順番はどうでもよい. もし実際の値を計算しなくてはならなくなったら, 読み手が適切な順番で(この例であれば, $t$, つぎに$x$と$y$, 最後に$ x * x + y * y $ という具合に)計算する約束になっている.

プログラミング言語(少なくともPython)はもっと杓子定規であり, 要するに, 「実際に計算可能な順番」に代入文と式を並べてあげないといけない. 

と, いうよりも, Pythonでこのように, 文と式を複数並べた場合に起きることは, 単純に, __「上から順に実行(計算)をしているだけである」__という風に考えるのが今後にとっても役に立つ. 以下にまとめておく.

"""

""" md 

# {C.section}-{C.inc_subsection}. 複数の文と式を並べたときの実行規則

```
t = 1
x = math.cos(t)
y = math.sin(t)
x * x + y * y
```

のように, 複数行にわたるプログラム片をセルに書いてそれを実行したときの規則は以下の通り

 1. 各行は「式」または「文」である(もっとも「文」は代入文しかまだ習っていない)
 1. 上から順に実行(式であれば評価(値を計算))していく
 1. 代入文を実行すると, 右辺の式が評価され, 左辺の変数名で記憶される(= その変数に値が格納される)
 1. 式を評価する際, 式の部分式として変数名が現れたら(例: x * x という式にはxという部分式が(2回)現れている),
  * その変数に値が格納されていたらその値がその部分式の値となる
  * その変数に値が格納されていなければエラーが発生する(※)
 1. 最後に実行した行が式であればその値が表示される(文の場合は何も表示されない)

(※)が, 以下のような順番で書いてもエラーになる理由で,

```
xx * xx + yy * yy
xx = math.cos(tt)
yy = math.sin(tt)
tt = 1
```

単純に, 

 1. 上から実行していく
 1. 最初の式で xx が使われている
 1. しかしその時, __まだ__ xx には値が代入(格納)されていない

からエラーになる, というだけのことである.

くどいかも知れないがもう一度.

複数行を並べたら, 上から順に実行していく(だけ)

"""



""" md 

# 問題 {C.inc_problem}: ヘロンの公式

ヘロンの公式は, 3辺の長さが$a, b, c$であるような三角形の面積が,

$$ S = \sqrt{{s(s-a)(s-b)(s-c)}} $$

というものである. ただし,

$$ s = \frac{{a+b+c}}{{2}} $$

である.

変数を使いつつ, 3辺の長さが, 7, 8, 9 であるような三角形の面積を求め, 結果を変数Hに格納せよ.

"""

""" write-code-box """

""" answer-code-box """
a = 7
b = 8
c = 9
s = (a + b + c) / 2
H = math.sqrt(s * (s-a) * (s-b) * (s-c))

""" md 
Hを表示してみよ
"""

""" exec-code-box """
H

""" test-code-box """
assert(H == 26.832815729997478), H

""" md 

# {C.section}-{C.inc_subsection}. 同じ変数に何度も代入することもできる

以下のプログラムを実行すると何が表示されるか?

"""

""" exec-code-box """
x = 3
x = 4
x * x

""" md

見ての通り`x`に2回代入されている. これを数学でいうところの

$$ x * x $$
ただし
$$ x = \cdots $$

のようなものだと思って読むと, いったい$x$は3, 4どっちやねん, ということになるのだが, こういう場合も「上から順に実行していく(だけ)」という規則さえ頭に入っていれば,

```
16
```

と表示される, というのは簡単にわかると思う. 要するにこの例では最初の`x = 3`は無意味だったということ. ではなぜこんな話をわざわざするのか, それはこの後を読んでくれればわかる.

以下のようなプログラムも全く合法である.

何が表示されるか予想(理解)した上で実行してみよ.
"""

""" exec-code-box """
x = 0
x = x + 1
x = x + 2
x = x + 3
x = x + 4
x

""" md

このプログラムでは`x`に複数回(5回も)代入されているというのみならず, `x`に代入している右辺にまた`x`が現れるという, 代入文を, 数学に出てくる等式だと思って理解すると意味不明な式になっている. 数学で`x`を定義するのに,

$$ x = x + 1 $$

などとかいたら普通は意味不明. 人によってはもう少し考えて, あ, これは

$$ x = x + 1 $$

を満たす$x$を定義しているのだな(方程式による定義)と思い直して, 「解なし」と言って満足するかも知れない.

プログラムとしての上記の意味はそれらとは全く違うもので, ここでも純粋に「上から順に」実行していく(だけ)という原則を守って理解する. そうすれば,

```
x = 0
```

でまず`x`に0が格納され,

```
x = x + 1
```

では, まず右辺が計算される. その際, __この時点では__ `x`に0が格納されているために右辺の値は, $0 + 1$, つまり1になる. したがってこの代入文の実行により`x`には1が格納される. 以下,

```
x = x + 2
```

で `x`に 3 $(1 + 2)$が,

```
x = x + 3
```

で 6 $(3 + 3)$が,

```
x = x + 4
```

で 10 $(6 + 4)$が代入される.

したがって最後の

```
x
```

で10が表示される.

つまり振り返ってみるとこのプログラムは, $0 + 1 + 2 + 3 + 4$を計算するための, 一方法だったことになる. もちろんそれが計算したいのであればわざわざこんな回りくどいことをしなくても素直に, $0 + 1 + 2 + 3 + 4$と書けばよかったのだが, あえて上記のように計算することの意義は後に(繰り返し(for)文を学ぶところで)わかる. ここでは深入りしない.

ここでのポイントは, しつこいようだが, プログラムが何を計算しているかを理解するには, 数式からの類推は有用だがあるところで諦めて, プログラムの実行規則:

文や式を並べたら上から実行していく

を(いわば機械的に)当てはめてそれに忠実に従うことが重要, ということである.

```
x = x + 1
```

のような, 数式としてみると謎(または単なる「偽」としか読めない)式も, プログラムにとっては, 「x(の今の値)」に1を足してxに入れる(以降のxとする), という意味があり, 実際プログラミングでは, そんなことを使って色々な計算をしていく.

"""


""" md 

# {C.section}-{C.inc_subsection}. 変数名の規則

変数は`x`, `y`のように1文字でなくてもよい.
むしろプログラミングでは, その変数に格納している値が「何」であるのかがわかるような, 意味のある名前をつけることが推奨されている.

だが, 変数の名前として任意の文字が許されているわけではない. 
実際, `x+y` などという (`+`を含んだ)変数の名前を許してしまうと, これが
$x + y$のことなのか, 一つの変数名のことなのかがわからなく(曖昧に)なってしまう.

そこで, 変数に使って良い文字は以下のような制限がある.

 * 使える文字は, アルファベット(A-Z, a-z), 下線(_), 数字(0-9), に限られる
 * ただし先頭には数字は使えない(「先頭に数字」を許してしまうとどのような不都合(曖昧性)があるか, 考えてみよ)

読みやすい変数名を選ぶことの重要性は, 徐々に複雑なプログラムを書くようになって初めてわかるもので, 現時点で無理に例を作ってもよあまり実感できない. が, あえてひとつ例を作ると, 以下は, 元金100万円, 年利15% のローンを35年

"""

""" md

以下を, エラーになるものとならないものを予想しながら実行せよ.
また, その際どのようなエラーメッセージが出てくるのかも一度見ておくこと

"""

""" exec-code-box """
x = 10

""" exec-code-box """
x0 = 10

""" exec-code-box """
x_0 = 10

""" error-code-box """
my name = 10


""" error-code-box """

""" md 

# {C.section}-{C.inc_subsection}. 代入されていない変数の参照

変数のタイプミスをして間違えて存在しない(代入されていない)変数を使ってしまうことがある. そのような場合のエラーも一度見ておくこと

"""

""" exec-code-box """
very_long_variable_name = 10

""" exec-code-box """
very_long_variable_name

""" error-code-box """
very_long_variable_neme
