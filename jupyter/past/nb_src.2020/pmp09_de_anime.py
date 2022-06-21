""" md

# 物理シミュレーション + アニメーション

いよいよ, 常微分方程式を解きながら, その結果をアニメーションで表示する.

先の単振動の例を引き続き用いる.

## 復習1: 

以下の状況

<img src="img/spring.svg" />

$$ {{\LARGE m \ddot{{x}}(t) = F }} $$

をシミュレートするコードが以下であった. 

__xが時々刻々変わる質点の位置を保持していた__ことを思い出しておく

"""

""" exec-code-box """
def mass_spring(x0, v0, T, m, k):
    x = x0
    v = v0
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    for i in range(n):
        a = -k * x / m
        x += v * dt
        v += a * dt
        t += dt
    return (x,v)

""" md

## 復習2: Visual Pythonでアニメーションをする

1. おまじない: 
```
from vpython import *
```
を唱えておく
1. sphere(), box(), helix()などの関数を呼び出すと対応するオブジェが表示される
1. sphere(pos=vector(1,2,3)) のようにposという属性を指定することで位置を指定できる
1. s = sphere(pos=vector(1,2,3)) としておいて, あとから s.pos += vector(0.1, 0.2, 0.3) のように pos属性を代入文で変更すれば, それだけで s の表示位置を変更, つまり sを動かせる
1. これを繰り返し行えばアニメーションができる. 
```
s = オブジェ(pos=vector(...))
for i in range(n):
  s.pos = ...
```
1. ただし, rate(更新レート) という関数を呼び出さないと画面は更新されない. 例えば毎秒30回の速度で更新するなら
```
s = オブジェ(pos=vector(...))
for i in range(n):
  s.pos = ...
  rate(30)
```
1. アニメーションの先頭で, 

```
c = canvas()
``` 

という呼び出しをしておくとよい. それにより新しい画面(キャンバス)に描画が行われる. これをやらないと以前に作られたキャンバスに上書きで描画されてしまう. つまり以下が最低限のテンプレート
```
c = canvas()
s = オブジェ(pos=vector(...))
for i in range(n):
  s.pos = ...
  rate(30)
```

"""



""" md 

以上, 復習1と復習2を合わせて, バネに繋がれて運動する質点

"""

""" exec-code-box """
from vpython import *

def mass_spring_anime(x0, v0, T, m, k):
    c = canvas()
    b0 = sphere()
    s = sphere(color=color.red, pos=vector(x0,0,0), vel=vector(v0,0,0))
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    t = 0
    for i in range(n):
        s.acc = -k * s.pos / m
        s.pos += s.vel * dt
        s.vel += s.acc * dt
        t += dt
        rate(1/dt)
    return (s.pos,s.vel)
        
""" exec-code-box """
# 以下で初期位置や速度, 質量, バネ定数などを変えて動きの違いを見てみよ
mass_spring_anime(10, 0, 50, 1, 1)


""" md 

# 問題 {C.inc_problem} 

上記を参考にして, 「空気抵抗のある状態」をシミュレートする関数,
mass_spring_drag_anime(x0, v0, T, m, k, mu) を書け.

空気抵抗は, 速度の逆向きに, 速度に比例して働くとせよ(その比例定数がmu).
空気抵抗の係数を変えて, 動きの違いを見てみよ.

"""

""" write-code-box """

""" answer-code-box """
from vpython import *

def mass_spring_drag_anime(x0, v0, T, m, k, mu):
    c = canvas()
    b0 = sphere()
    s = sphere(color=color.red, pos=vector(x0,0,0), vel=vector(v0,0,0))
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    t = 0
    for i in range(n):
        s.acc = (-k * s.pos - mu * s.vel) / m 
        s.pos += s.vel * dt
        s.vel += s.acc * dt
        t += dt
        rate(1/dt)
    return (s.pos,s.vel)

mass_spring_drag_anime(10, 0, 50, 1, 1, 0.1)


""" md 

# 問題 {C.inc_problem} 

アニメーションをそれらしくするために
バネや壁も表示してみよ.

"""

""" write-code-box """

""" answer-code-box """
from vpython import *

def mass_spring_drag_real_anime(x0, v0, T, m, k, mu):
    c = canvas()
    # b0 = sphere()
    s = sphere(color=color.red, pos=vector(x0,0,0), vel=vector(v0,0,0))
    h = helix(axis=s.pos, radius=0.5)
    floor = box(pos=vector(0,-1,0), height=0.2, width=2, length=20)
    dt = 0.01
    n = int(T / dt)
    dt = T / n
    t = 0
    for i in range(n):
        s.acc = (-k * s.pos - mu * s.vel) / m 
        s.pos += s.vel * dt
        s.vel += s.acc * dt
        h.axis = s.pos
        t += dt
        rate(1/dt)
    return (s.pos,s.vel)

mass_spring_drag_real_anime(10, 0, 50, 1, 1, 0.1)


""" md 

# 問題 {C.inc_problem} 

原点に太陽(動かない)があり, その周りを惑星が回っている状態をシミュレート(アニメーション)せよ.

地球が位置$x$にいる時に働く力は, 

$$ - G m M \frac{{x}}{{|x|^3}} $$

ただし$m$が惑星の質量, $M$は太陽の質量. 
ここでは地球と比べて非常に質量が大きいので動かないものとして良い.

* まずうまく初期値を設定し, 惑星が太陽を中心とした円運動をするようにしてみよ(物理の問題)

また初期値により,

* 惑星がどんどん遠ざかる
* ある軌道(太陽を一頂点とする楕円)を回り続ける

彗星のような, 太陽の周りをつぶれた楕円運動をする初期値を設定してみよ

"""

""" write-code-box """

""" answer-code-box """
import math
from vpython import *

def sun_and_earth():
    cv = canvas()
    G = 6.67408e-11
    scale = 1e-10
    r = 149.6 * 1e9             # [m]
    x0 = vector(r, 0, 0)
    sun = sphere(color=color.yellow, radius=5, m=1.98892e30, x=vector(0,0,0))
    v0 = vector(0, math.sqrt(G * sun.m / r), 0)
    earth = sphere(color=color.blue, radius=1, m=5.9742e24,
                   x=x0, v=v0, pos=x0 * scale)
    # 1 step = 1 日
    dt = 86400
    # 365 step = 1 年
    for i in range(365 * 3):
        dx = sun.x - earth.x
        a = (G * sun.m / dx.dot(dx)) * dx.norm()
        earth.v += a * dt
        earth.x += earth.v * dt
        earth.pos = earth.x * scale
        # 30日に一度, 軌跡を残す
        if i % 30 == 0:
            sphere(pos=earth.pos, color=earth.color, radius=0.5*earth.radius)
        # 1 秒に30 step = 1ヶ月分
        rate(30)

sun_and_earth()

""" md 

# 問題 {C.inc_problem} 

前問で, もう一方の太陽も動かしてみよ. $M$と$m$をだいたい同じくらいにすれば両者が絡まり合って動く, 連星のような動きができる.

"""

""" write-code-box """

""" answer-code-box """
from vpython import *

def binary_star():
    cv = canvas()
    G = 6.67408e-11
    scale = 1e-8
    r = 149.6 * 1e7             # [m]
    x0 = vector(r, 0, 0)
    sun = sphere(color=color.yellow, radius=1, m=5.9742e24, x=vector(0,0,0))
    earth = sphere(color=color.blue, radius=1, m=5.9742e24, x=x0)
    v0 = vector(0, math.sqrt(2/3 * G * sun.m / r), 0)
    sun.v = -v0
    earth.v = v0
    sun.pos = sun.x * scale
    earth.pos = earth.x * scale

    # 1 step = 1 日
    dt = 86400
    # 365 step = 1 年
    for i in range(3650):
        dx = sun.x - earth.x
        earth.a = (G * sun.m / dx.dot(dx)) * dx.norm()
        earth.v += earth.a * dt
        earth.x += earth.v * dt
        sun.a = -(G * earth.m / dx.dot(dx)) * dx.norm()
        sun.v += sun.a * dt
        sun.x += sun.v * dt
        earth.pos = earth.x * scale
        sun.pos = sun.x * scale
        # 30日に一度, 軌跡を残す
        if i % 30 == 0:
            sphere(pos=earth.pos, color=earth.color, radius=0.5*earth.radius)
            sphere(pos=sun.pos,   color=sun.color,   radius=0.5*sun.radius)
        # 1 秒に30 step = 1ヶ月分
        rate(30)

binary_star()


""" md 

# 問題 {C.inc_problem} 

地上から速さ$v_0$, 角度$\theta$で斜めに打ち上げられた質点の動き(初期位置を原点とする)を時刻$T$までシミュレート(アニメーション)する関数 free_fall(v0, theta, T) を書いて実行せよ. ただし, 時刻$T$に至るまでに再び地上に衝突したら, バウンドさせよ, つまり, 速度の$y$成分を反転させよ.

"""

""" write-code-box """

""" answer-code-box """
import math
from vpython import *

def free_fall(v0, theta, T):
    cv = canvas()
    b = box(height=0.1, length=100, width=10)
    vel = v0 * vector(math.cos(theta), math.sin(theta), 0)
    c = cone(vel=vel)
    dt = 0.01
    t = 0.0
    n_steps = T / dt
    g = vector(0, -9.8, 0)
    n = 1000
    for i in range(n):
        c.vel += g * dt
        c.pos += c.vel * dt
        if c.pos.y < 0.0:
            c.vel.y = -c.vel.y
        rate(1/dt)

free_fall(10.0, 0.4*math.pi, 100)
    

""" md 

# 問題 {C.inc_problem} 

前問を修正して, バウンドする際の反発係数$e < 1$を設定できるようにした関数 free_fall2(v0, theta, e, T) を書いて実行せよ. 

"""

""" write-code-box """

""" answer-code-box """
import math
from vpython import *


def free_fall2(v0, theta, T, e):
    cv = canvas()
    b = box(height=0.1, length=100, width=10)
    vel = v0 * vector(math.cos(theta), math.sin(theta), 0)
    c = cone(vel=vel)
    dt = 0.01
    t = 0.0
    n_steps = T / dt
    g = vector(0, -9.8, 0)
    n = 1000
    for i in range(n):
        c.vel += g * dt
        c.pos += c.vel * dt
        if c.pos.y < 0.0 and c.vel.y < 0:
            c.vel.y = -e * c.vel.y
        rate(1/dt)

free_fall2(10.0, 0.4*math.pi, 100, 0.99)
    
