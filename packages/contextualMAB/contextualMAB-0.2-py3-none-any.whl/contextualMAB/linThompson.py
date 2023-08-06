# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:34:29 2019

@author: Karthick
"""

from contextualMAB.contextualMAB import contextualMAB
from contextualMAB.utilMAB import find_max
import numpy as np

class linThompson(contextualMAB):
    def __init__(self, n_arms, n_vars, v_sq):
        """
        Thompson sampling with linear payoffs
        input : v_sq, number_of_arms, number_of_variables (numbers)
        output :  None
        """
        self.v_sq = v_sq
        self.n_arms = n_arms
        self.n_vars = n_vars
        self.rewards = []
        self.chosen_arms = []
        self.last_used_context = 0
        self.B_matrix = np.identity(self.n_vars)
        self.mu_vector = np.atleast_2d(np.zeros(self.n_vars)).T
        self.f_vector = np.atleast_2d(np.zeros(self.n_vars)).T
        return
    
    def action(self, context):
        """
        Implementation is based on the paper by agarwal et al;
        actions : sampling from a prior multi variate distribution, choosing an arm based on the argmax (context*mu)
        input : context (array /list)
        output : choosen arm (number)
        """
        context = np.atleast_2d(context).T
        self.last_used_context = context
        sampled = np.random.multivariate_normal(self.mu_vector.reshape(-1), self.v_sq*np.linalg.inv(self.B_matrix))
        sampled = sampled.reshape(sampled.shape[0],1)
        arm_prob = np.dot(context.T, sampled)
        chosen_arm = find_max(arm_prob)
        self.chosen_arms.append(chosen_arm)
        return chosen_arm
    
    def update(self, reward):
        """
        on observing the reward we need to update the A and B vectors corresponding for the arm which was chosen
        input : reward (number)
        output : None
        action : updating B matrix, mu vector and f vector
        """
        reward = int(reward)
        self.rewards.append(reward)
        # updaing B matrix
        self.B_matrix =  self.B_matrix + np.dot(self.last_used_context, self.last_used_context.T)
        # updating f_vector
        self.f_vector = self.f_vector + reward*self.last_used_context
        #updating mu vector
        self.mu_vector = np.dot(np.linalg.inv(self.B_matrix),self.f_vector)
        return "weights updated"
    
    