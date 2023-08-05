# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:55:27 2019

@author: karthick
"""

import random
import numpy as np

def find_max(pta):
    """
    function to find the amx pta : tie breaking using random
    input: pta(list) probability of each arm
    output : chosen_arm (number)
    action: chosing the best arm with random tie breaking 
    """
    winner = np.argwhere(pta==np.amax(pta)).reshape(-1)
    winner = int(random.choice(winner))
    return winner
