import numpy as np
from agent import Agent
import math
import random
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def distance(A, B):
    return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)


class Environment:
    def __init__(self, size, num_agents, obv_radius, num_leader, target_pos):
        self.size = size
        self.num_agents = num_agents
        self.agents = [Agent(i) for i in range(num_agents)]
        self.leaders_id = [i for i in range(num_leader)]
        self.agents_pos = []
        self.map = np.zeros((size, size))
        self.obv_radius = obv_radius
        self.num_leader = num_leader
        self.trans_map = np.zeros((size, size))
        self.target_pos = target_pos
        self.pairs = {}

    def initialize(self):
        possible_pairs = [[i, j] for i in range(0, self.size) for j in range(0, self.size)]
        self.agents_pos = random.sample(possible_pairs, self.num_agents)
        for i in range(self.num_agents):
            self.map[self.agents_pos[i][0]][self.agents_pos[i][1]] = i
        for id in self.leaders_id:
            self.agents[id].update_pos(self.agents_pos[id])

    def update_map(self):
        for i in range(self.num_agents):
            self.map[self.agents_pos[i][0]][self.agents_pos[i][1]] = i

    def update_agents(self):
        # update leader's position; others:[0, 0]
        for id in self.leaders_id:
            self.agents[id].update_pos(self.agents_pos[id])

    def update_agents_pos_1(self, i):
        # 随机移动
        could_move = True
        x, y = self.agents_pos[i][0], self.agents_pos[i][1]
        #print(x, y)
        dx, dy = self.agents[i].act()
        #print(dx, dy)
        x1, y1 = x + dx, y + dy
        #print(x1, y1)
        self.update_agents()
        self.update_map()
        self.transform_map()
        if x1 < 0 or x1 > self.size - 1 or y1 < 0 or y1 > self.size - 1 or i in self.pairs.keys():
            could_move = False
        if could_move:
            self.agents_pos[i] = [x1, y1]
        self.update_agents()
        self.update_map()
        self.transform_map()
                
    def update_agents_pos_2(self):
        # leader's action
        for id in self.leaders_id:
            if not self.reach_target(id):
                self.update_leader_target(id)
                self.decide_action(id)
                self.update_agents()
                self.update_map()
                self.transform_map()
                self.send_self_pos_message()
        # others' action
        if len(self.pairs) != self.num_agents:
            for i in range(self.num_agents):
                if i not in self.leaders_id:
                    if not self.reach_target(i):
                        self.update_agents_pos_1(i)
                        self.update_agents()
                        self.update_map()
                        self.transform_map()
                        self.send_self_pos_message()     

    def transform_map(self):
        self.trans_map = np.zeros((self.size, self.size))
        for i in range(self.num_agents):
            self.trans_map[self.agents_pos[i][0]][self.agents_pos[i][1]] = 1

    def send_self_pos_message(self):
        # leader向其他agent发送位置信息
        #print("send message")
        for id in self.leaders_id:
            for i in range(self.num_agents):
                #print("check distance")
                if distance(self.agents_pos[i], self.agents[id].pos) <= self.obv_radius and i not in self.leaders_id:
                    #print("send message to agent", i)
                    self.agents[i].update_pos(self.agents_pos[i])
                    self.leaders_id.append(i)

    def reach_target(self, id):
        # 如果agent到达目标点，则向self.pairs中添加该agent与target_pos的对应关系
        if (id not in self.leaders_id and self.agents_pos[id] in self.target_pos and self.agents_pos[id] not in self.pairs.values()) or (id in self.leaders_id and self.agents[id].target == self.agents_pos[id]):
            print("agent", id, "reach target", self.agents_pos[id])
            self.pairs[id] = self.agents_pos[id]
            return True
        else:
            return False
        
    def find_nearest_target(self, leader_id):
        # 寻找尚未被占领的最近的目标点
        min_dist = float('inf')
        nearest_target = None
        for target in self.target_pos:
            if target not in self.pairs.values():
                dist = distance(self.agents_pos[leader_id], target)
                if dist < min_dist:
                    min_dist = dist
                    nearest_target = target
        return nearest_target
    
    def update_leader_target(self, id):
        if id not in self.pairs.keys():
            self.agents[id].update_target(self.find_nearest_target(id))
            for other_id in self.leaders_id :
                # 如果遇到也未到达目标点的leader,则根据优先级更新目标点
                # 优先级：id较小的先行
                if other_id not in self.pairs.keys() and distance(self.agents_pos[id], self.agents_pos[other_id]) <= self.obv_radius and id > other_id:
                    self.agents[id].update_target(None)
            if self.agents[id].target in self.pairs.values():
                self.agents[id].update_target(None)
        

    def decide_action(self, id):
        # 未到达目标点的agent根据目标点的位置决定动作
        if id not in self.pairs.keys():
            target = self.agents[id].target
            if target != None:
                dx, dy = target[0] - self.agents_pos[id][0], target[1] - self.agents_pos[id][1]
                if dx > 0:
                    if self.could_move(id, "right"):
                        self.act_right(id)
                elif dx < 0:
                    if self.could_move(id, "left"):
                        self.act_left(id)
                else:
                    if dy > 0:
                        if self.could_move(id, "up"):
                            self.act_up(id)
                    elif dy < 0:
                        if self.could_move(id, "down"):
                            self.act_down(id)
                self.update_agents()
                self.update_map()
                self.transform_map()
                self.send_self_pos_message()   
            
            else:
                self.update_agents_pos_1(id)
                self.update_agents()
                self.update_map()
                self.transform_map()
                self.send_self_pos_message()


    def act_right(self, id):
        self.agents_pos[id][0] += 1

    def act_left(self, id):
        self.agents_pos[id][0] -= 1

    def act_up(self, id):
        self.agents_pos[id][1] += 1

    def act_down(self, id):
        self.agents_pos[id][1] -= 1

    def could_move(self, id, direction):
        # 判断是否可以移动
        dict_direction = {"right": [1, 0], "left": [-1, 0], "up": [0, 1], "down": [0, -1]}
        x, y = self.agents_pos[id][0], self.agents_pos[id][1]
        dx, dy = dict_direction[direction]
        x1, y1 = x + dx, y + dy

        if x1 < 0 or x1 > self.size - 1 or y1 < 0 or y1 > self.size - 1 :
            return False
        else:
            return True
    
        
        


        
        
       
    






    
                    
                    





    
                    


            
            





            
        