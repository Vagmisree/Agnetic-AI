import numpy as np
import time
from collections import deque

class Shelf:
    def __init__(self, shelf_id, x, y, stock, max_stock, low_threshold):
        self.id = shelf_id
        self.x = x
        self.y = y
        self.stock = stock
        self.max_stock = max_stock
        self.low_threshold = low_threshold

    def replenish(self, qty):
        self.stock = min(self.stock + qty, self.max_stock)

    def is_low(self):
        return self.stock <= self.low_threshold


class Robot:
    def __init__(self, robot_id, x=0, y=0):
        self.id = robot_id
        self.x = x
        self.y = y
        self.busy = False
        self.path = []
        self.task = None
        self.history = [(x, y)]

    def assign_task(self, task, shelves):
        target = shelves[task % len(shelves)]
        self.task = target
        self.busy = True
        self.path = SimulationManager.bfs((self.x, self.y), (target.x, target.y), [])
        return target


class SimulationManager:
    @staticmethod
    def bfs(start, end, occupied):
        q = deque([(start, [])])
        seen = set()
        while q:
            (x, y), path = q.popleft()
            if (x, y) == end:
                return path + [(x, y)]
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if (nx, ny) not in seen and (nx, ny) not in occupied and 0 <= nx < 10 and 0 <= ny < 10:
                    seen.add((nx, ny))
                    q.append(((nx, ny), path + [(x, y)]))
        return []

    @staticmethod
    def create_simulation(num_shelves=10, num_robots=2):
        shelves = [Shelf(f"S{i}", np.random.randint(0, 10), np.random.randint(0, 10),
                         np.random.randint(1, 15), 20, 5) for i in range(num_shelves)]
        robots = [Robot(f"R{i}", np.random.randint(0, 10), np.random.randint(0, 10))
                  for i in range(num_robots)]
        return shelves, robots
