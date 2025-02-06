import numpy as np
import random
class Agent:
    def __init__(self, id):
        # 定义了一个无人系统
        self.id = id
        self.action_space = ['up', 'down', 'left', 'right']
        self.pos = [0, 0]
        self.target = None

    def act(self):
        # 随机选择一个动作值
        move = {'up': [0, 1], 'down': [0, -1], 'left': [-1, 0], 'right': [1, 0]}
        action = random.choice(self.action_space)
        #print(action)
        return move[action]
        
    
    def update_pos(self, pos):
        self.pos = pos

    def update_target(self, target=None):
        self.target = target

        



    




    
    