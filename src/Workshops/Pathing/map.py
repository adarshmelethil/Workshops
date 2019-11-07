import sys
from math import pow, sqrt
import random

from drawer import drawWorld

WALL = "#"
OPEN = " "
CUR_POS = "*"
OBJ_POS = "@"

class World():
  def __init__(self, size=50, obsticles=1000, start_pos=(0,0), end_pos=(49,49)):
    self.size = size
    self.cur_pos, self.obj_pos = start_pos, end_pos

    self.regenerate(size=size, obsticles=obsticles, start_pos=start_pos, end_pos=end_pos)
    
    self.draw_color = {
      WALL: "white",
      OPEN: "black",
      CUR_POS: "purple",
      OBJ_POS: "green"
    }
    self.pen = drawWorld(self.world, start_pos, end_pos, self.draw_color)
    self.pen.draw(self.obj_pos[0], self.obj_pos[1], self.draw_color[OBJ_POS])

    self.pen.color(self.draw_color[CUR_POS])
    self.drawCurrentPos()

  def drawCurrentPos(self):
    self.pen.moveTo(self.cur_pos[0], self.cur_pos[1])

  def currentPos(self):
    return self.cur_pos[0], self.cur_pos[0]

  def objectivePos(self):
    return self.obj_pos[0], self.obj_pos[0]

  def regenerate(self, size, obsticles, start_pos, end_pos):
    self.world = [[OPEN]*size for _ in range(size)]
    
    possible_path = self.AStarFindPath()
    obsticle_count = 0
    while obsticle_count < obsticles:
      x = random.randint(0, size-1)
      y = random.randint(0, size-1)
      if self.world[x][y] != OPEN:
        continue

      if (x,y) in possible_path:
        self.world[x][y] = WALL
        possible_path = self.AStarFindPath()
        if possible_path is None:
          self.world[x][y] = OPEN
          possible_path = self.AStarFindPath()
          continue

      self.world[x][y] = WALL
      obsticle_count += 1

  # A*
  def safeUpdateHCost(self, path_values, path_trace, prev_pos, old_hcost, x, y, neighbours):
    if self.world[x][y] == OPEN:
      if path_values[x][y][0] > old_hcost + 1 or path_values[x][y][0] == -1:
        path_values[x][y][0] = old_hcost + 1
        path_trace[x][y] = prev_pos

      neighbours.append((x, y))

  def updatePosValues(self, path_values, path_trace, pos):
    size_x, size_y = len(self.world), len(self.world[0])

    x, y = pos
    h_cost, _ = path_values[x][y]
    neighbours = []
    if x + 1 < size_x:
      self.safeUpdateHCost(path_values, path_trace, pos, h_cost, x+1, y, neighbours)
    if y + 1 < size_y:
      self.safeUpdateHCost(path_values, path_trace, pos, h_cost, x, y+1, neighbours)
    if x - 1 >= 0:
      self.safeUpdateHCost(path_values, path_trace, pos, h_cost, x-1, y, neighbours)
    if y - 1 >= 0:
      self.safeUpdateHCost(path_values, path_trace, pos, h_cost, x, y-1, neighbours)
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

  def drawPath(self, path, color="orange"):
    for p in path:
      x, y = p
      if self.world[x][y] != OPEN:
        self.pen.draw(x, y, "red")
      else:
        self.pen.draw(x, y, color)


  def AStarFindPath(self):
    obj_x, obj_y = self.obj_pos
    path_values = [[[-1, sqrt(pow(x-obj_x, 2)+pow(y-obj_y, 2))] for x in range(len(self.world[0]))] for y in range(len(self.world))]
    path_trace = [[(-1, -1) for x,_ in enumerate(row)] for y, row in enumerate(self.world)]
    path_values[self.cur_pos[0]][self.cur_pos[1]] = (0, path_values[self.cur_pos[0]][self.cur_pos[1]][1])

    visted = [self.cur_pos]
    cur_pos = self.cur_pos
    next_options = []
    while cur_pos != self.obj_pos:
      neighbours = self.updatePosValues(path_values, path_trace, cur_pos)

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

if __name__ == "__main__":
  w = World()
  # print(w)
  path = w.AStarFindPath()
  w.drawPath(path)
  input()


