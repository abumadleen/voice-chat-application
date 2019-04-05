from _thread import *

t = 0
def heron(a,th_no):
    """Calculates the square root of a"""
    global t
    t+=1
    print(th_no,'t=',t)
    eps = 0.0000001
    old = 1
    new = 1
    while True:
        old,new = new, (new + a/new) / 2.0
        # print(old,new,th_no,'t=',t)
        if abs(new - old) < eps:
            break
    t-=1
    return new

start_new_thread(heron,(99,1))
start_new_thread(heron,(999,2))
start_new_thread(heron,(1733,3))

c = input("Type something to quit.")
