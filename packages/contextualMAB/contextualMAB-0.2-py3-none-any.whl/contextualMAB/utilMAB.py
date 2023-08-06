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

def get_regret(best_strategy, actual_rewards):
    """
    Calculates regret at each step and returns an array equal to number of users
    input : rewards from best strategy, rewards from the system (list, array)
    output: array of regret values (array)
    action: returns regret for each user
    """
    regret =[]
    for i in range(1,len(best_strategy)+1):
        regret.append(best_strategy[:i].cumsum().iloc[-1]-actual_rewards[:i].cumsum().iloc[-1])
    return np.array(regret)
