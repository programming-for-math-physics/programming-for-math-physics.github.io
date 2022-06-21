import visual
import math

def tetra():
    #  P(a,b,0)
    #     |   
    #     |   S    R(1,0,0)
    #     |
    #     |    
    #  Q(a,-b,0)
    a = math.cos(2 * math.pi / 3)
    b = math.sin(2 * math.pi / 3)
    c = math.sqrt(2)
    r = 0.2
    w = 0.02
    P = (a,b,0)
    Q = (a,-b,0)
    R = (1,0,0)
    S = (0,0,c)
    visual.display(background=visual.color.gray(0.9))
    P_ = visual.sphere(pos=P, radius=r, color=visual.color.white)
    Q_ = visual.sphere(pos=Q, radius=r, color=visual.color.red)
    R_ = visual.sphere(pos=R, radius=r, color=visual.color.yellow)
    S_ = visual.sphere(pos=S, radius=r, color=visual.color.green)
    PQ = visual.curve(pos=[P, Q], radius=w, color=visual.color.black)
    QR = visual.curve(pos=[Q, R], radius=w, color=visual.color.black)
    RP = visual.curve(pos=[R, P], radius=w, color=visual.color.black)
    PS = visual.curve(pos=[P, S], radius=w, color=visual.color.black)
    QS = visual.curve(pos=[Q, S], radius=w, color=visual.color.black)
    RS = visual.curve(pos=[R, S], radius=w, color=visual.color.black)

print "OK"
