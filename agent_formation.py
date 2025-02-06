import numpy as np
import random
import math
import matplotlib.pyplot as plt
import time
from agent import Agent
from environment import Environment
import matplotlib.pyplot as plt

size = 20
num_agents = 32
obv_radius = 5
num_leader = 2
train_loops = 100000

# random
target_pos = random.sample([[i, j] for i in range(0, size) for j in range(0, size)], num_agents)
# z-shape
target_pos = [[7, 0], [7, 2], [7, 6], [7, 10], [7, 12], [7, 14], [8, 1], [8, 5], [8, 7], [8, 9], [8, 13], [9, 1], [9, 4], [9, 8], [9, 13]]
# characters
target_pos = [[1, 11], [5, 11], [6, 11], [11, 11], [12, 11], [16, 11],
              [2, 10], [4, 10], [6, 10], [7, 10], [11, 10], [13, 10], [15, 10],
              [3, 9], [6, 9], [8, 9], [11, 9], [14, 9], 
              [3, 8], [6, 8], [9, 8], [11, 8], [14, 8], 
              [3, 7], [6, 7], [10, 7], [11, 7], [14, 7], 
              [3, 6], [6, 6], [11, 6], [14, 6]]
# car-shape
target_pos = [[9, 11], [10, 11], [11, 11], 
              [9, 10], [10, 10], [11, 10], [12, 10], 
              [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], 
              [4, 8], [13, 8], 
              [4, 7], [5, 7], [6, 7], [7, 7], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 7], 
              [6, 6], [11, 6]]
'''
# ship-shape
target_pos = [[11, 13], 
              [11, 12], 
              [9, 11], [10, 11], [11, 11], 
              [8, 10], [12, 10], 
              [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9], 
              [6, 8], [14, 8], 
              [7, 7], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 7]]
'''
num_agents = len(target_pos)
print("Target positions of agents:")
print(target_pos)
target_pos_set = {tuple(pos) for pos in target_pos}
env = Environment(size, num_agents, obv_radius, num_leader, target_pos)

'''
def loop_0():
    global train_loops
    while train_loops > 0 :
        env.send_self_pos_message()
        env.update_agents_pos_1()
        agents_pos_set = {tuple(pos) for pos in env.agents_pos }
        print("Current leaders:")
        print(env.leaders_id)
        print("Current positions of agents:")
        print(env.agents_pos)
        if len(set(tuple(pos) for pos in env.agents_pos)) != num_agents:
            print("Error: number of agents is not equal to the number of positions")
            break
        train_loops -= 1
        if agents_pos_set == target_pos_set:
            print("Congratulations! All agents reach their targets.")
            break
'''
def visualize():
    fig, ax = plt.subplots()
    ax.set_xlim(0, env.size)
    ax.set_ylim(0, env.size)

    # Draw grid
    for x in range(env.size + 1):
        ax.axhline(x, lw=0.5, color='gray')
        ax.axvline(x, lw=0.5, color='gray')

    # Plot target positions
    target_x, target_y = zip(*target_pos)
    target_positions = ax.scatter(target_x, target_y, c='red', marker='x', label='Target Positions')
    
    # Plot agent positions
    agents_positions = ax.scatter([], [], c='blue', marker='o', label='Agent Positions')

    plt.legend()
    plt.ion()  # Turn on interactive mode

    for _ in range(train_loops):
        env.send_self_pos_message()
        env.update_agents_pos_2()        
        agents_positions.set_offsets(env.agents_pos)
        plt.pause(0.1)
        plt.draw()

        agents_pos_set = {tuple(pos) for pos in env.agents_pos}
        print("Current leaders:")
        print(env.leaders_id)
        print("Current positions of agents:")
        print(env.agents_pos)
        print("Current pairs:")
        print(env.pairs)
        # activate obstacle avoidance function
        if len(set(tuple(pos) for pos in env.agents_pos)) != num_agents:
            print("activate obstacle avoidance function")
        if agents_pos_set == target_pos_set:
            print("Congratulations! All agents reach their targets.")
            print("number of agents:")
            print(num_agents)
            print("loops:")
            print(_)
            break
    plt.ioff()  # Turn off interactive mode
    plt.show()

'''            
def loop():
    global train_loops
    while train_loops > 0 :
        env.send_self_pos_message()
        env.update_agents_pos_2()
        agents_pos_set = {tuple(pos) for pos in env.agents_pos }
        print("Current leaders:")
        print(env.leaders_id)
        print("Current positions of agents:")
        print(env.agents_pos)
        print("Current pairs:")
        print(env.pairs)
        if len(set(tuple(pos) for pos in env.agents_pos)) != num_agents:
            print("Error: number of agents is not equal to the number of positions")
            break
        train_loops -= 1
        if agents_pos_set == target_pos_set:
            print("Congratulations! All agents reach their targets.")
            break
'''     
        
def run():
    env.initialize()
    env.transform_map()
    print("Initial positions of agents:")
    print(env.map)
    print(env.agents_pos)
    print(env.trans_map)
    #loop()
    print("Target positions of agents:")
    print(target_pos)
    print("Final pairs:")
    print(env.pairs)
    print("Final positions of agents:")
    print(env.trans_map)
    visualize()

run()




    




