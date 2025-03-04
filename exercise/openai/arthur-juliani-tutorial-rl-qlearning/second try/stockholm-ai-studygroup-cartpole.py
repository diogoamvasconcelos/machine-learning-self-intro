import math
import gym
import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt

import rl_utils as rl

#import dynamon
#proximal policy gradient opmitization

def discretize_to_bins(val, low, high, num_bins=10):
    rel_val = np.clip((val-low)/(high - low), 0, 1)  #np.clip -> clamp
   
    if rel_val == 0:
        return 0
    else:
        return math.ceil(rel_val * num_bins) - 1
    
def convert_continuos_state_to_discrete(s, bins, bounds_low, bounds_high):
    discrete_s = 0
    prev_whole_space = 1
    for i in range(len(s)):#s.shape[0]):
        d_s = discretize_to_bins(s[i], bounds_low[i], bounds_high[i], bins[i])
        discrete_s += d_s * prev_whole_space
        prev_whole_space *= bins[i]

    return discrete_s


def cartpole_qlearning():
    #load environment
    env = gym.make("CartPole-v1")
    action_size = env.action_space.n

    num_state_bins = [1, 1, 6, 3]
    bins_bounds_low = [env.observation_space.low[0], -1.0, env.observation_space.low[2], -1]
    bins_bounds_high = [env.observation_space.high[0], 1.0, env.observation_space.high[2], 1]

    #print(convert_continuos_state_to_discrete([0,0,2,6], [1,1,2,6], [0,0,0,0], [1,1,2,6]))

    #initialize table (zeros)
    Q = np.zeros([np.prod(num_state_bins), action_size])
    q_table = rl.QTable(np.prod(num_state_bins), action_size)
    
    #setup hyperparameters
    num_episodes = 1000
    num_sim_steps = 500

    #list to store total rewards and steps per episode (debugging)
    j_list = []
    r_list = []

    for i in range(num_episodes):
        #reset env
        s = env.reset()
        s = convert_continuos_state_to_discrete(s, num_state_bins, bins_bounds_low, bins_bounds_high)

        r_all = 0
        done = False

        #Q-Table learning algorithm
        for j in range(num_sim_steps):
            
            if (i % 200 == 0):
                env.render()

            #Choose action by greedily (with noise) picking from QTable
            a = q_table.get_action(s, episode=i)
            
            #Get new state and reward
            s1, r, done, _ = env.step(a)

            #improve r
            r = (math.radians(13) - abs(s1[2])) / math.radians(13)

            s1 = convert_continuos_state_to_discrete(s1, num_state_bins, bins_bounds_low, bins_bounds_high)

            #Update Q-Table with new knowledge
            q_table.update_q(s=s, a=a, s1=s1, r=r)

            r_all += r
            s = s1

            if (done):
                break

        #register the rewards
        j_list.append(j)
        r_list.append(r_all)

        if i % 100 == 0:
            print(np.mean(j_list[-100:]))
        

    #print score
    print("Q-Table success rate: " +  str(sum(r_list)/num_episodes) + "%")

    #plot
    plt.figure(1)

    plt.subplot(211)
    plt.plot(r_list, linewidth=0.3)

    plt.subplot(212)
    plt.plot(j_list, linewidth=0.3)

    plt.show()


if __name__ == "__main__":
    cartpole_qlearning()