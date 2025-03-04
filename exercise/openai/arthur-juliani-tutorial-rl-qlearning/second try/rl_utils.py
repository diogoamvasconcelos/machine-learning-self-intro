import math

import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

import gym

# ---- Utils ----
def discretize_to_bins(val, low, high, num_bins=10):
    rel_val = np.clip((val-low)/(high - low), 0, 1)  #np.clip -> clamp
   
    if rel_val == 0:
        return 0
    else:
        return math.ceil(rel_val * num_bins) - 1
    
def hash_continuos_state_to_discrete(s, bins, bounds_low, bounds_high):
    discrete_s = 0
    prev_whole_space = 1
    for i in range(len(s)):
        d_s = discretize_to_bins(s[i], bounds_low[i], bounds_high[i], bins[i])
        discrete_s += d_s * prev_whole_space
        prev_whole_space *= bins[i]

    return discrete_s

# ---- Q-Table ----
class QTable():
    def __init__(self, state_space, action_space, learning_rate=0.8, gamma=0.95, epsilon=0.1):
        self.state_space = state_space
        self.action_space = action_space
        self.lr = learning_rate
        self.gamma=gamma
        self.epsilon = epsilon

        self._initialize_table()
        pass

    def _initialize_table(self):
        self.Q = np.zeros([self.state_space, self.action_space])

    def get_action(self, s, episode=0):
        '''
        e = self.epsilon ** (1 + episode/100) #reduce change as episodes go on
        #Choose action by greedily picking from QTable (with 'epsilon' change of random choice) 
        if np.random.rand(1) < e:
            a = np.random.randint(0, self.action_space)
        else:
            a = np.argmax(self.Q[s, :])
        return a
        '''
        return np.argmax(self.Q[s, :] + np.random.randn(1, self.action_space)  * (1./(1 + episode)))
        
    def update_q(self, s, a, s1, r):
        max_future_reward = np.max(self.Q[s1, :])
        new_estimate = r + self.gamma * max_future_reward
        self.Q[s, a] = (1 - self.lr) * self.Q[s, a] + self.lr * new_estimate