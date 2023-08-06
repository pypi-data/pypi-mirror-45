# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:31:29 2019

@author: Lenovo
"""
from linUCB import linUCB
algo = linUCB(5,5,0.1)
context = [1,2,3,4,5]

algo.action(context)
algo.update(0)

from utilMAB import get_regret


from eGreedy import eGreedy
from UCB import UCB
from Thompson import Thompson

algo = UCB(5)
for i in range(500):
    print("the chosen arm .. ",algo.action())
    algo.update(1)


algo = Thompson(5)
for i in range(500):
    print("the chosen arm .. ",algo.action())
    algo.update(random.choice([0,1]))
    
algo.action()
algo.update(0)