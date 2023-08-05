# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:18:53 2019

@author: Karthick
"""

class contextualMAB(object):
    """
    Defining the most basics actions done by any of the algorithms:
        
    1. Choosing an action from available options ( with or without context )
    2. update the weight matrix on seeing the reward of the actiont taken
    
    """
    
    def action(self, context):
        pass
    
    def update(self, reward):
        pass
    
    