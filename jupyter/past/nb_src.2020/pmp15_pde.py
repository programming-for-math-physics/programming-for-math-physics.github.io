""" md

# 偏微分方程式

"""

""" md

# 例題

未知の関数$u$は$x$ (場所)と$t$ (時刻)の関数(丁寧に書けば$u(x,t)$)で,

$0 < x < 1$で
$$ \frac{{\partial u}}{{\partial t}} = 3\frac{{\partial u}}{{\partial x}}, $$
および
$$ u(0,t) = u(1,t) = 0 $$
を満たす. 

場所は$x$座標ひとつなので1次元の問題.

ある時刻$t$における$u(x,t)$がわかっていれば右辺が計算でき, それによって
$$ \frac{{\partial u}}{{\partial t}} $$ 
が与えられるわけだから, 少し時間が経過した後の$u$, つまり, $u(x, t+\Delta t)$がわかる. 

ので, 理屈はこれまで質点の運動方程式をといてきたときと変わらない.

```
for in range(n_steps):
  u = u + 右辺 * dt
```

違いは, ある時刻における状態が, これまではたかだか質点1つの位置(と速度)だったのに対して, すべて(多数)の$x$における値になることだけ. もちろん文字通りすべての(無限の)場所における$u$を保持することは無理なので, 値を保持する$x$の場所を適当な間隔で設定してそれらにおける値だけを追跡することにする. そのために配列が役に立つ.

"""

""" md

* $0 = x_0 < x_1 < \cdots x_n = 1$ と [0,1] 上に$n$個の点を等間隔に取る
* つまり, $x_i$ = $i / (n-1)$
* 隣り合う点の間隔を$\Delta x$ と書くことにする ($\Delta x = 1/n$)

$$ \frac{{\partial u}}{{\partial x}} \approx \frac{{u(x+\Delta x,t) - u(x,t)}}{{\Delta x}} $$

* 配列の言葉で書けば,

```
(u[i+1] - u[i]) / dx
```

"""


""" exec-code-box """
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anm

# 0---x1---x2---x3--- ... ---1
#u[0]u[1] u[2] u[3]   ...  u[n-1]

def simple_pde(fig, dx, dt, end_t):
    # ax = fig.add_subplot(111)
    k = 1.0
    n = int(1/dx)
    x = np.linspace(0,1,n)
    u = np.sin(2 * np.pi * x)   # 端で0を満たすならなんでもよい
    n_steps = int(end_t / dt)
    for s in range(n_steps):
        if 1:
            if s == 0:
                [ line ] = plt.plot(x, u)
            else:
                line.set_data(x, u)
        u[1:n-1] += (k * dt / dx) * (u[2:n] - u[1:n-1])
        yield [ line ]

def animate_simple_pde(dx, dt, end_t):
    fig = plt.figure()
    ani = anm.FuncAnimation(fig, lambda x: x, repeat=0,
                            frames=simple_pde(fig, dx, dt, end_t), 
                            interval=30)
    plt.show()
    return ani

animate_simple_pde(1.0e-2, 1.0e-3, 1.0)


