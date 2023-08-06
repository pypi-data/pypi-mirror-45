# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:15:56 2019

@author: Karthick
"""
from contextualMAB.contextualMAB import contextualMAB
from contextualMAB.utilMAB import find_max
import numpy as np


class eGreedy(contextualMAB):
    def __init__(self, n_arms, epsilon):
        """
        Implemented one of the famous and simple techniques of eGreedy for online learning
        Inputs : n_arms, epsilon (number(int),number(float))
        output: None
        Action: creates and initiates arms, number of times arms being used
        """
        self.n_arms =n_arms
        self.epsilon = epsilon # eploration probability
        self.counts = np.zeros(n_arms, dtype=int)
        self.values = np.zeros(n_arms, dtype=float)
        self.chosen_arms = []
        self.rewards = []
        return
    
    def action(self):
        """
        actions :Choosen the most observed arm from the past for probability 1-epsilon else choosen randomly
        input : None 
        output : choosen arm (number)
        """
        z = np.random.random()
        if z > self.epsilon:
            # Pick the best arm
            chosen_arm = find_max(self.values)
            self.chosen_arms.append(chosen_arm)
            return chosen_arm
        # Randomly pick any arm with prob 1 / len(self.counts)
        chosen_arm = np.random.randint(0, self.n_arms)
        self.chosen_arms.append(chosen_arm)
        return chosen_arm
    
    def update(self, reward):
        """
        input : reward (number)
        output : None 
        """
        reward = int(reward)
        self.rewards.append(reward)
        # Increment chosen arm's count by one
        self.counts[self.chosen_arms[-1]] += 1
        n = self.counts[self.chosen_arms[-1]]
        # Recompute the estimated value of chosen arm using new reward
        value = self.values[self.chosen_arms[-1]]
        new_value = value * ((n - 1) / n) + reward / n
        self.values[self.chosen_arms[-1]] = new_value