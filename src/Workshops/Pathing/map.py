import sys
from math import pow, sqrt
import random

from .drawer import drawWorld

WALL = "#"
OPEN = " "
CUR_POS = "*"
OBJ_POS = "@"

class World():
  def __init__(self, size=50, obsticles=500, start_pos=(0,0), end_pos=(49,49), var=None):
    self.size = size
    self.cur_pos, self.obj_pos = start_pos, end_pos

    self.regenerate(size=size, obsticles=obsticles, start_pos=start_pos, end_pos=end_pos, var=var)
    
    self.draw_color = {
      WALL: "white",
      OPEN: "black",
      CUR_POS: "purple",
      OBJ_POS: "green"
    }
    self.pen = drawWorld(self.world, start_pos, end_pos, self.draw_color)
    self.pen.draw(self.obj_pos[0], self.obj_pos[1], self.draw_color[OBJ_POS])

    self.pen.color(self.draw_color[CUR_POS])
    self._drawCurrentPos()

  def _drawCurrentPos(self):
    self.pen.moveTo(self.cur_pos[0], self.cur_pos[1])

  def objectivePos(self):
    return self.obj_pos
  def isObjective(self, x, y):
    return self.obj_pos == (x, y)

  def clampVal(self, val, mi, ma):
    return max(mi, min(ma, val))

  def getRandomPoint(self, size, var=None):
    if var:
      return self.clampVal(int(random.normalvariate(size/2, size*var)), 0, size-1), self.clampVal(int(random.normalvariate(size/2, size*var)), 0, size-1)
    else:
      return random.randint(0, size-1), random.randint(0, size-1)

  def regenerate(self, size, obsticles, start_pos, end_pos, var):
    self.world = [[OPEN]*size for _ in range(size)]
    
    possible_path = self._AStarFindPath()
    obsticle_count = 0
    while obsticle_count < obsticles:
      x, y = self.getRandomPoint(size, var=var)
      
      if self.world[x][y] != OPEN:
        continue

      if (x,y) in possible_path:
        self.world[x][y] = WALL
        possible_path = self._AStarFindPath()
        if possible_path is None:
          self.world[x][y] = OPEN
          possible_path = self._AStarFindPath()
          continue

      self.world[x][y] = WALL
      obsticle_count += 1

  def getNeighbours(self, x, y):
    size_x, size_y = len(self.world), len(self.world[0])
    neighbours = []
    if x+1 < size_x and self.world[x+1][y] == OPEN:
      neighbours.append((x+1, y))
    if y+1 < size_y and self.world[x][y+1] == OPEN:
      neighbours.append((x, y+1))
    if x-1 >= 0 and self.world[x-1][y] == OPEN:
      neighbours.append((x-1, y))
    if y-1 >= 0 and self.world[x][y-1] == OPEN:
      neighbours.append((x, y-1))
    return neighbours

  def NoDelay(self):
    self.pen.removeDelay()
    self.delayed = False

  def YesDelay(self):
    self.pen.addDelay()
    self.delayed = True
  def UpdateScreen(self):
    self.pen.updateScreen()

  # A*
  def updateHCost(self, path_values, path_trace, prev_pos, old_hcost, x, y):
    if path_values[x][y][0] > old_hcost + 1 or path_values[x][y][0] == -1:
      path_values[x][y][0] = old_hcost + 1
      path_trace[x][y] = prev_pos

  def updatePosValues(self, path_values, path_trace, pos):
    x, y = pos
    h_cost, _ = path_values[x][y]
    neighbours = self.getNeighbours(*pos)
    # update the H costs
    for neighbour in neighbours:
      self.updateHCost(path_values, path_trace, pos, h_cost, *neighbour)
    return neighbours

  def pickNextPos(self, path_values, options):
    picked = 0
    for i, opt in enumerate(options):
      if sum(path_values[options[picked][0]][options[picked][1]]) \
        > sum(path_values[opt[0]][opt[1]]):
        picked = i
    picked_pos = options[picked]
    del options[picked]
    return picked_pos

  def _AStarFindPath(self):
    obj_x, obj_y = self.obj_pos
    path_values = [[[-1, sqrt(pow(x-obj_x, 2)+pow(y-obj_y, 2))] for x in range(len(self.world[0]))] for y in range(len(self.world))]
    path_trace = [[(-1, -1) for x,_ in enumerate(row)] for y, row in enumerate(self.world)]
    path_values[self.cur_pos[0]][self.cur_pos[1]] = (0, path_values[self.cur_pos[0]][self.cur_pos[1]][1])

    visted = [self.cur_pos]
    cur_pos = self.cur_pos
    next_options = []
    while cur_pos != self.obj_pos:
      neighbours = self.updatePosValues(path_values, path_trace, cur_pos)
      # if there is a neighbour that has not been visted
      next_options.extend([n for n in neighbours if n not in visted and n not in next_options])
      if next_options == []:
        return None

      cur_pos = self.pickNextPos(path_values, next_options)
      visted.append(cur_pos)

    path = [cur_pos]
    while cur_pos != self.cur_pos:
      cur_pos = path_trace[cur_pos[0]][cur_pos[1]]
      path.insert(0, cur_pos)
    return path

  def __str__(self):
    return f'\n{"-"*self.size*2}\n'.join([f"|{'|'.join(row)}|" for row in self.world])

  def currentPosition(self):
    return self.cur_pos

  def check(self, x, y, open_color="orange", blocked_color=None):
    if (x, y) == self.cur_pos:
      return True
    if self.world[x][y] == OPEN:
      if open_color is not None:
        self.pen.draw(x, y, open_color)
      return True
    else:
      if blocked_color is not None:
        self.pen.draw(x, y, blocked_color)
      return False

  def __len__(self):
    return len(self.world) * len(self.world[0])

  def width(self):
    return len(self.world)

  def height(self):
    return len(self.world[0])

  def __getitem__(self, x):
    return self.world[x]

  def getGrid(self):
    return self.world

  def _boardingCells(self, first_cell, second_cell):
    return sum([abs(first_cell[0]-second_cell[0]), abs(first_cell[1]-second_cell[1])]) <= 1 # 0 if paths repeat
  def drawPath(self, path, color="green"):
    # remove previous path drawing
    # self.pen.undoStampTil()
    cpos = self.cur_pos
    for p in path:
      if not self._boardingCells(cpos, p):
        return False

      if self.check(*p, open_color=None): # open
        if color is not None:
          self.pen.stampAtPos(*p, color=color)
      else: # hit a wall
        return False
      if self.world[p[0]][p[1]] == OBJ_POS:
        return True

      cpos = p
    return False

  # def moveTo(self, path=[]):
  #   for p in path:
  #     self.pen.moveTo(self.cur_pos[0], self.cur_pos[1])
  #     self.pen.stamp(*p)

if __name__ == "__main__":
  w = World()
  # print(w)
  path = w._AStarFindPath()
  w.drawPath(path)
  input()


