# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 23:03:54 2019

@author: Karthick
"""

from contextualMAB.contextualMAB import contextualMAB
from contextualMAB.utilMAB import find_max
import numpy as np
import random

class Thompson(contextualMAB):
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.numbers_of_rewards_1 = [0] * n_arms
        self.numbers_of_rewards_0 = [0] * n_arms
        self.rewards = []
        self.chosen_arms = []
        self.max_random = 0
        self.chosen_arm = 0
        return
    
    def action(self):
        for i in range(0, self.n_arms):
            random_beta = random.betavariate(self.numbers_of_rewards_1[i] + 1, self.numbers_of_rewards_0[i] + 1)
            if random_beta >self.max_random:
                self.max_random = random_beta
                self.chosen_arm = i
        self.chosen_arms.append(self.chosen_arm)
        return self.chosen_arm
    
    def update(self, reward):
        reward = int(reward)
        self.rewards.append(reward)
        if reward == 1:
            self.numbers_of_rewards_1[self.chosen_arm] = self.numbers_of_rewards_1[self.chosen_arm] + 1
        else:
            self.numbers_of_rewards_0[self.chosen_arm] = self.numbers_of_rewards_0[self.chosen_arm] + 1
        