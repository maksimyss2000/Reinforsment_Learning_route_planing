import copy
import random
import time
from itertools import combinations

import pygame
import pygame as pg
from pygame.locals import *
from statistics import mean
pg.font.init()
from itertools import combinations
from Cell import Cell

my_map = [
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], ]

type_of_cell = {
    'E': 'empty',
    'W': 'wall',
    'G': 'goal',
}
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
colors = [
   # (0, 0, 0),
   # (127, 127, 127),
    (255, 255, 255),
    (255, 50, 45),
    (0, 255, 0),
    #(0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

color_of_cell = {
    'empty': BLUE,
    'wall': BLACK,
    'goal': YELLOW,
}


def allPossibleState(wight, height, money):
    q_table = {}
    for x in range(wight):
        for y in range(height):
            for i in range(len(money) + 1):
                for j in combinations(money, i):
                    q_table[x, y, j] = [0, 0, 0, 0]
    return q_table

class Field:
    def __init__(self):
        self.iteration = 0
        self.agent = None
        self.point_start = None
        self.point_exit = None
        self.wight = None
        self.height = None
        self.map = []
        self.sc = pg.display.set_mode((1500, 1000))
        self.money = None
        self.money_start = None

    # Voln is a very, very bad implementation at first. It is essential to change it first of all
    def test(self, lab, point_exit):
        lab = self.voln(self.point_start[0], self.point_start[1], 1, self.height, self.wight, lab)
        if lab[point_exit[0]][point_exit[1]] > 0:
            return True
        else:
            return False

    def voln(self, x, y, cur, n, m, lab):
        lab[x][y] = cur
        if y + 1 < n:
            if lab[x][y + 1] == 0 or (lab[x][y + 1] != -1 and lab[x][y + 1] > cur):
                self.voln(x, y + 1, cur + 1, n, m, lab)
        if x + 1 < m:
            if lab[x + 1][y] == 0 or (lab[x + 1][y] != -1 and lab[x + 1][y] > cur):
                self.voln(x + 1, y, cur + 1, n, m, lab)
        if x - 1 >= 0:
            if lab[x - 1][y] == 0 or (lab[x - 1][y] != -1 and lab[x - 1][y] > cur):
                self.voln(x - 1, y, cur + 1, n, m, lab)
        if y - 1 >= 0:
            if lab[x][y - 1] == 0 or (lab[x][y - 1] != -1 and lab[x][y - 1] > cur):
                self.voln(x, y - 1, cur + 1, n, m, lab)
        return lab

    def createRandomPoint(self, min_x, max_x, min_y, max_y):
        return (random.randint(min_x, max_x), random.randint(min_y, max_y))
        # Return a number between min and max (both included):

    def randomInit(self):
        for x in range(self.wight):
            self.map.append([])
            for y in range(self.height):
                self.map[x].append(Cell('empty'))
        self.point_start = self.createRandomPoint(0, 0, 0, self.height - 1)
        self.point_exit = self.createRandomPoint(self.wight - 1, self.wight - 1, 0, self.height - 1)

        self.point_start = (0, 4)
        self.point_exit = (12, 4)

        arr = [[0 for y in range(self.height)] for x in range(self.wight)]
        potential_points_for_wall = []
        for x in range(self.wight):
            for y in range(self.height):
                potential_points_for_wall.append((x, y))

        potential_points_for_wall.remove(self.point_start)
        potential_points_for_wall.remove(self.point_exit)
        count_wall = 20
        count_money = 3
        count_iterate = 0
        while count_wall != 0:
            count_iterate += 1
            if count_iterate == 10000:
                print("randomInit  error")
            wall = potential_points_for_wall[random.randint(0, len(potential_points_for_wall) - 1)]
            arr[wall[0]][wall[1]] = -1
            clone = copy.deepcopy(arr)
            if self.test(clone, self.point_exit):
                count_wall -= 1
            else:
                arr[wall[0]][wall[1]] = 0
            potential_points_for_wall.remove(wall)

        self.map[self.point_exit[0]][self.point_exit[1]].type = 'goal'
        for x in range(self.wight):
            for y in range(self.height):
                if arr[x][y] == -1:
                    self.map[x][y].type = 'wall'
        self.money_start = []
        while len(self.money_start) != count_money:
            money = potential_points_for_wall[random.randint(0, len(potential_points_for_wall) - 1)]
            potential_points_for_wall.remove(money)
            if 1 < money[0] < self.wight - 1:
                self.money_start.append(money)
        self.money = self.money_start.copy()

    def start(self):

        self.wight = 13
        self.height = 10
        self.randomInit()
        #for x in range(height):
        # self.height = len(my_map)
        # self.wight = len(my_map[0])
        # for y in range(self.height):
        #    self.map.append([])
        #    for x in range(self.wight):
        #        self.map[y].append(Cell(type_of_cell[my_map[y][x]]))

    def drawPatch(self, part_path):
        #print(part_path)
        number = 0
        number_part = 0
        for patch in part_path:
            number_part += 1
            # print(patch)
            # print(len(patch))
            if len(patch) < 2:
                return
            for index in range(len(patch) - 1):
                number += 1
                self.drawConnectionLine(patch[index], patch[index + 1], number, number_part)

    def drawConnectionLine(self, first, second, number, number_part):
        pg.draw.line(self.sc, colors[number_part % len(colors)],  # GREEN,
                     # [5 + first[0] * 100 + 50, 5 + first[1] * 100 + 50],
                     # [5 + second[0] * 100 + 50, 5 + second[1] * 100 + 50], 10)
                     [25 + first[0] * 80 + 10 * number_part, 25 + first[1] * 80 + 10 * number_part],
                     [25 + second[0] * 80 + 10 * number_part, 25 + second[1] * 80 + 10 * number_part], 10)

        f1 = pg.font.Font(None, 40)
        text1 = f1.render(str(number), True,
                          colors[(number_part+1) % len(colors)])
        self.sc.blit(text1, ((5 + first[0] * 80 + 50 + 5 + second[0] * 80 + 50) / 2 - 50 + 25 * number_part - 35,
                             (5 + first[1] * 80 + 50 + 5 + second[1] * 80 + 50) / 2 - 50 + 25 * number_part - 35))

    def drawCell(self, x, y, q_table):
        direction = q_table[(x, y, tuple(self.money))]
        current = self.map[x][y]
        rect = Rect(5 + x * 80, 5 + y * 80, 75, 75)
        pg.draw.rect(self.sc, color_of_cell[current.type], rect)
        '''

        f1 = pg.font.Font(None, 20)
        text1 = f1.render('L:' + str(round(direction[0], 4)), True,
                          (180, 0, 0))
        self.sc.blit(text1, (5 + x * 100, 5 + y * 100))
        text1 = f1.render('R:' + str(round(direction[1], 4)), True,
                          (180, 0, 0))
        self.sc.blit(text1, (5 + x * 100, 25 + y * 100))
        text1 = f1.render('U:' + str(round(direction[2], 4)), True,
                          (180, 0, 0))
        self.sc.blit(text1, (5 + x * 100, 45 + y * 100))
        text1 = f1.render('D:' + str(round(direction[3], 4)), True,
                          (180, 0, 0))
        self.sc.blit(text1, (5 + x * 100, 65 + y * 100))
        '''
        for elem in self.money:
            if elem == (x, y):
                pg.draw.circle(self.sc, GREEN,
                               (x * 80 + 40, y * 80 + 40), 25)

    def drawAgent(self):
        pg.draw.circle(self.sc, YELLOW,
                       (self.agent[0] * 80 + 40, self.agent[1] * 80 + 40), 25)

    def isEqual(self, x):
        return len(set(x)) <= 1

    def find_current_path(self, q_table):
        # self.iteration += 1
        # if self.iteration > 100:
        #    print(self.iteration)
        # q_table[(cur_x, cur_y, tuple(self.money))][action]
        part_path = []
        path_cell = []
        current_cell = list(self.point_start)
        current_money = self.money_start.copy()
        max_value = max(q_table[(current_cell[0], current_cell[1], tuple(current_money))])
        while self.isEqual(q_table[(
                current_cell[0], current_cell[1],
                tuple(current_money))]) != True and max_value != 0 and current_cell not in path_cell:
            path_cell.append(current_cell.copy())
            max_index = q_table[(current_cell[0], current_cell[1], tuple(current_money))].index(max_value)
            if max_index == 0 and current_cell[0] > 0:
                current_cell[0] -= 1
            if max_index == 1 and current_cell[0] < self.wight - 1:
                current_cell[0] += 1
            if max_index == 2 and current_cell[1] > 0:
                current_cell[1] -= 1
            if max_index == 3 and current_cell[1] < self.height - 1:
                current_cell[1] += 1
            if tuple(current_cell) in current_money:
                current_money.remove(tuple(current_cell))
                path_cell.append(current_cell.copy())
                part_path.append(path_cell.copy())
                path_cell = []
            max_value = max(q_table[(current_cell[0], current_cell[1], tuple(current_money))])

        part_path.append(path_cell.copy())
        return part_path

    def show_legend(self):
        f1 = pg.font.Font(None, 50)
        text1 = f1.render('Legend:', True,
                          (0, 0, 0))
        self.sc.blit(text1, (32 + 13 * 80, 10 + 0 * 100))
        text2 = f1.render(' - empty', True,
                          (0, 0, 0))
        text3 = f1.render(' - wall', True,
                          (0, 0, 0))
        text4 = f1.render(' - goal', True,
                          (0, 0, 0))
        text5 = f1.render(' - agent', True,
                          (0, 0, 0))
        text6 = f1.render(' - additional reward', True,
                          (0, 0, 0))
        rect = Rect(32 + 13 * 80,  60, 75, 75)
        pg.draw.rect(self.sc, color_of_cell['empty'], rect)
        self.sc.blit(text2, (105 + 13 * 80, 80))
        rect = Rect(32 + 13 * 80,  145, 75, 75)
        pg.draw.rect(self.sc, color_of_cell['wall'], rect)
        rect = Rect(32 + 13 * 80,  230 , 75, 75)
        self.sc.blit(text3, (105 + 13 * 80, 160))
        pg.draw.rect(self.sc, color_of_cell['goal'], rect)
        self.sc.blit(text4, (105 + 13 * 80, 240))

        pg.draw.circle(self.sc, YELLOW,
                       (13 * 80 + 70, 345), 25)
        self.sc.blit(text5, (105 + 13 * 80, 320))

        pg.draw.circle(self.sc, GREEN,
                   (13 * 80 + 70, 410), 25)
        self.sc.blit(text6, (105 + 13 * 80, 395))


    def visualisation(self, q_table):
        current_path = self.find_current_path(q_table)
        #print(current_path)
        time_pause = 0.025
        for event in pg.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
                pressed = pg.mouse.get_pressed()
                pos = pg.mouse.get_pos()
                find_x = int(pos[0]/80)
                find_y = int(pos[1]/80)
                print(find_x, find_y)
                if pressed[0]: #left
                    if self.map[find_x][find_y].type == "wall":
                        self.map[find_x][find_y].type = "empty"
                    else:
                        self.map[find_x][find_y].type = "wall"

            #print(event)
        self.sc.fill(GRAY)
        for x in range(self.wight):
            for y in range(self.height):
                self.drawCell(x, y, q_table)
        self.drawPatch(current_path)
        self.drawAgent()
        self.show_legend()
        pg.display.update()
        time.sleep(time_pause)



    def new_egreedy_policy(self, q_table, epsilon=0.1):
        # Get a random number from a uniform distribution between 0 and 1,
        # if the number is lower than epsilon choose a random action
        if random.random() < epsilon:
            return random.choice([i for i in range(4)])
        # Else choose the action with the highest value
        else:
            # return np.argmax(q_values[state])
            state = (self.agent[0], self.agent[1], tuple(self.money))
            max_value = max(q_table[state])
            return q_table[state].index(max_value)


    def step(self, action):
        reward = -1
        done = False
        if action == 0 and self.agent[0] > 0:
            if self.map[self.agent[0] - 1][self.agent[1]].type == "wall":
                return [reward, done]
            self.agent[0] -= 1
        if action == 1 and self.agent[0] < self.wight - 1:
            if self.map[self.agent[0] + 1][self.agent[1]].type == "wall":
                return [reward, done]
            self.agent[0] += 1
        if action == 2 and self.agent[1] > 0:
            if self.map[self.agent[0]][self.agent[1] - 1].type == "wall":
                return [reward, done]
            self.agent[1] -= 1
        if action == 3 and self.agent[1] < self.height - 1:
            if self.map[self.agent[0]][self.agent[1] + 1].type == "wall":
                return [reward, done]
            self.agent[1] += 1

        if self.map[self.agent[0]][self.agent[1]].type == "empty":
            reward = -1
            done = False
       # if self.map[self.agent[0]][self.agent[1]].type == "wall":
       #     reward = -50
       #     done = True
        if self.map[self.agent[0]][self.agent[1]].type == "goal":
            reward = 100
            done = True
        if (self.agent[0], self.agent[1]) in list(self.money):
            reward = 500

        if (self.agent[0], self.agent[1]) in list(self.money):
            m = list(self.money)
            m.remove((self.agent[0], self.agent[1]))
            self.money = tuple(m)


        return [reward, done]


    def get_cur_state(self):
        return ( self.agent[0], self.agent[1], tuple(self.money))



    def set_start_state(self):
        self.agent = list(self.point_start)
        self.money = self.money_start.copy()

    def expected_Sarsa(self):
        file = open("sarsa_expectedv3.txt", "w")
        self.set_start_state()
        q_table = allPossibleState(self.wight, self.height, self.money)
        alpha = 1  # Скорость обучения
        gamma = 0.8  # Коэффициент дисконтирования
        count = 0
        for i in range(10000):
            done = False
            all_reward = 0
            self.set_start_state()
            action = self.new_egreedy_policy(q_table, 0.1)
            while not done:
                state = self.get_cur_state()
                reward, done = self.step(action)
                new_state = self.get_cur_state()
                next_action = self.new_egreedy_policy(q_table, 0.1)
                max_value_new_state = mean(q_table[new_state])
                td_target = reward + gamma * max_value_new_state
                td_error = td_target - q_table[state][action]
                learning_rate = 0.5
                q_table[state][action] += td_error * learning_rate
                all_reward += reward
                action = next_action
                self.visualisation(q_table)
            file.write(str(all_reward) + ' ')
            count += 1
            print(count)
            if count == 300:
                file.close()
                break

    def Sarsa(self):
        file = open("sarsav3.txt", "w")
        self.set_start_state()
        q_table = allPossibleState(self.wight, self.height, self.money)
        alpha = 1  # Скорость обучения
        gamma = 0.8  # Коэффициент дисконтирования
        count = 0
        for i in range(10000):
            done = False
            all_reward = 0
            self.set_start_state()
            action = self.new_egreedy_policy(q_table, 0.1)
            count += 1
            while not done:
                state = self.get_cur_state()
                reward, done = self.step(action)
                new_state = self.get_cur_state()
                next_action = self.new_egreedy_policy(q_table, 0.1)
                max_value_new_state = q_table[new_state][next_action]
                td_target = reward + gamma * max_value_new_state
                td_error = td_target - q_table[state][action]
                learning_rate = 0.5
                q_table[state][action] += td_error * learning_rate
                all_reward += reward
                action = next_action
                self.visualisation(q_table)
            file.write(str(all_reward) + ' ')
            print(count)
            if count == 300:
                file.close()
                print("lol")
                break


    def Q_learning(self):
        file = open("q_learningv3.txt", "w")
        self.set_start_state()
        q_table = allPossibleState(self.wight, self.height, self.money)
        alpha = 1  # Скорость обучения
        gamma = 0.8  # Коэффициент дисконтирования
        count = 0
        for i in range(10000):
            done = False
            all_reward = 0
            self.set_start_state()
            count += 1
            while not done:
                state = self.get_cur_state()
               # action = self.new_egreedy_policy(q_table, 0.1)
               # reward, done = self.step(action)
                new_state = self.get_cur_state()
                max_value_new_state = max(q_table[new_state])
               # td_target = reward + gamma * max_value_new_state
                #td_error = td_target - q_table[state][action]
                learning_rate = 0.5
               # q_table[state][action] += td_error * learning_rate
               # all_reward += reward
                self.visualisation(q_table)

            #file.write(str(all_reward) + ' ')
            #print(count)
            #if count == 300:
            #    file.close()
            #    print("lol")
                
            #    break

    def Update(self,q_table_first, q_table_second):
        alpha = 1  # Скорость обучения
        gamma = 0.8  # Коэффициент дисконтирования
        state = self.get_cur_state()
        action = self.new_egreedy_policy(q_table_first, 0.1)
        reward, done = self.step(action)
        new_state = self.get_cur_state()
        max_value_new_state = max(q_table_second[new_state])
        td_target = reward + gamma * max_value_new_state
        td_error = td_target - q_table_first[state][action]
        learning_rate = 0.5
        if state[0] == new_state[0] and state[1] == new_state[1]:
            q_table_first[state][action] += -1
        else:
            q_table_first[state][action] += td_error * learning_rate
        return [done, reward]

    def QQ_learning(self):
        file = open("qq_learningv3.txt", "w")
        self.set_start_state()
        q_table_first = allPossibleState(self.wight, self.height, self.money)
        q_table_second = allPossibleState(self.wight, self.height, self.money)
        alpha = 1  # Скорость обучения
        gamma = 0.8  # Коэффициент дисконтирования
        count = 0
        for i in range(10000):
            done = False
            all_reward = 0
            self.set_start_state()
            while not done:
                if random.random() < 0.5:
                    done, reward = self.Update(q_table_first, q_table_second)
                else:
                    done, reward = self.Update(q_table_second, q_table_first)
                all_reward += reward
                self.visualisation(q_table_first)
            #ile.write(str(all_reward) + ' ')
           # count += 1
            #if count == 300:
            #    file.close()
            #   print("lol")
             #   break

