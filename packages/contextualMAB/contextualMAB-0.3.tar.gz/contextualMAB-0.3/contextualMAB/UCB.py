# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 21:31:00 2019

@author: Lenovo
"""
from contextualMAB.contextualMAB import contextualMAB
from contextualMAB.utilMAB import find_max
import numpy as np
import math

class UCB(contextualMAB):
    def __init__(self, n_arms):
        self.n_arms =n_arms
        self.numbers_of_selections = [0] * n_arms
        self.sums_of_rewards = [0] * n_arms
        self.chosen_arms = []
        self.rewards = []
        self.max_upper_bound = 0
        self.upper_bound = [0] * n_arms
        self.average_reward = [0] * n_arms
        self.chosen_arm = 0
        self.n_users = 0
        return
    
    def action(self):
        self.n_users = self.n_users + 1
        for i in range(self.n_arms):
            if (self.numbers_of_selections[i] > 0):
                self.average_reward[i] = self.sums_of_rewards[i] / self.numbers_of_selections[i]
                delta_i = math.sqrt(3/2 * math.log(self.n_users + 1) / self.numbers_of_selections[i])
                self.upper_bound[i] = self.average_reward[i] + delta_i
            else:
                self.upper_bound[i] = 1e400
            if self.upper_bound[i] > self.max_upper_bound:
                self.max_upper_bound = self.upper_bound[i]
                self.chosen_arm =  i
            
        self.chosen_arms.append(self.chosen_arm)
        return self.chosen_arm
        
    def update(self,reward):
        reward = int(reward)
        self.rewards.append(reward)
        self.numbers_of_selections[self.chosen_arm] = self.numbers_of_selections[self.chosen_arm] + 1
        self.sums_of_rewards[self.chosen_arm] = self.sums_of_rewards[self.chosen_arm] + reward

