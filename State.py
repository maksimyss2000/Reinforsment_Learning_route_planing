from itertools import combinations


class State:
    def allPossibleState(self, wight, height, money):
        q_table = {}
        for x in range(wight):
            for y in range(height):
                for i in range(len(money) + 1):
                    for j in combinations(money, i):
                        q_table[x, y, j] = [0, 0, 0, 0]
        return q_table
    def __init__(self):
        self.x = 0
        self.y = 0
        self.money = []
