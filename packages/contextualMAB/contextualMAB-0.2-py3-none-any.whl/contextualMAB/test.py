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