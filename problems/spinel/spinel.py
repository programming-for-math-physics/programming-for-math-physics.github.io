#!/usr/bin/python
# -*- coding: utf-8 -*-
import visual,random

epsilon = 1.0e-2

def force(p, q):
    # force p feels from q
    # <0 => attactive
    # >0 => repulsive
    dx = p.pos - q.pos
    r = dx.mag
    sigma = p.radius + q.radius
    x = sigma / r
    f = p.e * q.e / (r * r) + (epsilon/sigma) * (12*x**13 - 6*x**7) 
    return (f / r) * dx

def pot(p, q):
    r = (p.pos - q.pos).mag
    sigma = p.radius + q.radius
    x = sigma / r
    return p.e * q.e / r + epsilon * (x**12 - x**6)

def tot_uk(C):
    U = 0.0
    K = 0.0
    for i,p in enumerate(C):
        K += 0.5 * p.m * p.v.mag2
        for j,q in enumerate(C):
            if i < j:
                U += pot(p, q)
    return U,K

def all_acc(C):
    for i,p in enumerate(C):
        p.a = visual.vector(0,0,0)
        for j,q in enumerate(C):
            if i != j:
                p.a += force(p, q)
        p.a /= p.m

def move(C, dt):
    for p in C:
        p.v   += p.a * dt
        p.pos += p.v * dt

def evolve(C, dt):
    for i in range(100):
        visual.rate(30)
        U,K = tot_uk(C)
        print "%3d : U + K = %f = %f + %f" % (i, U + K, U, K)
        all_acc(C)
        move(C, dt)

def init_conf(n, ion_types, colors):
    rg = random.Random(729)
    C = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                m,e,r = random.choice(ion_types)
                col = colors[m,e,r]
                x = visual.vector(2 * n * rg.random(),
                                  2 * n * rg.random(),
                                  2 * n * rg.random())
                v = visual.vector(0,0,0)
                C.append(visual.sphere(radius=r, pos=x, color=col, 
                                       m=m, e=e, v=v))
    return C

def normalize_ion_types(ion_types):
    m_min = min([ m for m,_,_ in ion_types ])
    r_max = max([ r for _,_,r in ion_types ])
    return [ (m / m_min, e, r / (2.0 * r_max)) 
             for m,e,r in ion_types ]

def nacl_ion_types():
    m0,e0,r0 = 22.99,  1.0, 102.0
    m1,e1,r1 = 35.45, -1.0, 181.0
    return [(m0,e0,r0),(m1,e1,r1)]

def mk_color_map(ion_types):
    cm = {}
    colors = [ visual.color.yellow, visual.color.red ]
    for m,e,r in ion_types:
        assert ((m,e,r) not in colors), (m,e,r,colors)
        cm[m,e,r] = colors[len(cm)]
    return cm

def main():
    n = 8                       # 4**3 particles
    dt = 1.0e-2
    ion_types = normalize_ion_types(nacl_ion_types())
    cm = mk_color_map(ion_types)
    C = init_conf(n, ion_types, cm)
    evolve(C, dt)

main()
#print "OK"
            
# NaCl(食塩)
# Na+: 102nm, 22.99g/mol,+1e
# Cl-: 181nm, 35.45g/mol,-1e
#
# CsCl(塩化セシウム)
# Cs+: 174nm, 132.9g/mol,+1e
# Cl-: 181nm, 35.45g/mol,-1e
#
# ZnS(硫化亜鉛)
# Zn2+: 88nm, 65.39g/mol, +2e
# S2-: 170nm, 32.07g/mol, -2e
#
# どれも、wikipediaで調べると、
# 結晶構造が出てくるはずです。確か、
# NaClを基準として、
# ・CsCl：イオン半径が同じくらい
# ・ZnS：陰イオンの半径が大きい
