# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:16:05 2019

@author: Karthick
"""

from contextualMAB.contextualMAB import contextualMAB
from contextualMAB.utilMAB import find_max
import numpy as np

class linUCB(contextualMAB):
    def __init__(self, n_arms, n_vars, alpha):
        """
        Linear payoffs for upper confidence bound with disjoint linear models
        Implementation is based on the "A contextual bandit approach to personalsed news
        article recommendation, by Wei chu et al.,
        input : number of arms, number of variables, alpha (number)
        output : None (init cant return anything)
        """
        
        self.alpha = alpha
        self.n_arms = n_arms
        self.n_vars = n_vars
        self.A_matrix = [0]* n_arms
        self.b_vector = [0]* n_arms
        self.theta_vector = [0]* n_arms
        self.pta = [0]* n_arms
        self.last_used_context = 0
        self.rewards = []
        self.chosen_arms = []
        for arm in range(self.n_arms):
            self.A_matrix[arm] = np.identity(self.n_arms)
            self.b_vector[arm] = np.atleast_2d(np.zeros(self.n_vars)).T
            self.theta_vector[arm] = np.dot(np.linalg.inv(self.A_matrix[arm]),self.b_vector[arm])
        return
    
    def action(self, context):
        """
        Intializing a and b matrix with d dimnesional matrix and vector respectively
        updating them based on the formula from paper LinUCB
        input: context (array or list)
        output: chosen_arm(number)
        """
        context = np.atleast_2d(context).T
        self.last_used_context = context
        for arm in range(self.n_arms):
            self.theta_vector[arm] = np.dot(np.linalg.inv(self.A_matrix[arm]), self.b_vector[arm])
            self.pta[arm] = int(np.dot(self.theta_vector[arm].T, context))
            self.pta[arm] = self.pta[arm]+int(self.alpha * np.sqrt(np.dot(context.T, np.dot(np.linalg.inv(self.A_matrix[arm]), context))))
        chosen_arm = find_max(self.pta)
        self.chosen_arms.append(chosen_arm)
        return chosen_arm
    
    def update(self, reward):
        """
        on observing the reward we need to update the A and B vectors corresponding for the arm which was chosen
        input : reward (number)
        output : None
        """
        reward = int(reward)
        self.rewards.append(reward)
        self.A_matrix[self.chosen_arms[-1]] = self.A_matrix[self.chosen_arms[-1]] + np.dot(self.last_used_context, self.last_used_context.T)
        self.b_vector[self.chosen_arms[-1]] = self.b_vector[self.chosen_arms[-1]] + reward*self.last_used_context
        return "weights updated"