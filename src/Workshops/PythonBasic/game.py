import random

import pygame
import turtle

START = "a"
END = "b"
WALL = "#"
OPEN = "_"

window_width, window_height = 240, 240

def neighbours(maze, coor):
  x, y = coor
  if x < 0 or y < 0:
    raise ValueError("invalid coordinates")
  if y >= len(maze) or x >= len(maze[0]):
    raise ValueError("invalid coordinates")

  n = []
  if x + 1 < len(maze[0]):  # right
    n.append((1, 0))
  if x - 1 >= 0:            # left
    n.append((-1, 0))
  if y - 1 >= 0:            # up
    n.append((0, -1))
  if y + 1 < len(maze):     # down
    n.append((0, 1))

  return n

def createMaze(width, height):
  if width < 1 or height < 1:
    raise ValueError("Width and Height must be positive, recieved: {}x{}".format(width, height))
  if width < 2 and height < 2:
    raise ValueError("Area must be minimal 2 (1x2 or 2x1), recieved: {}x{}".format(width, height))

  maze_nodes = [[[] for i in range(width)] for i in range(height)]
  
  cur_cell = (0, 0)
  visted = []
  stack = []
  while len(visted) < width*height:
    not_visted = [n for n in neighbours(maze_nodes, cur_cell) if (cur_cell[0]+n[0], cur_cell[1]+n[1]) not in visted]
    if not_visted:
      next_cell = random.choice(not_visted)
      stack.append(cur_cell)
      
      maze_nodes[cur_cell[0]][cur_cell[1]].append(next_cell)
      # maze_nodes[next_cell[0]][next_cell[1]].append(cur_cell)

      cur_cell = (cur_cell[0]+next_cell[0], cur_cell[1]+next_cell[1])
      visted.append(cur_cell)
    else:
      cur_cell = stack.pop()

  maze = [[WALL if not(i%2) or not(j%2) or not i or not j else OPEN for i in range(2*width+1)] for j in range(2*height+1)]

  for x, row in enumerate(maze_nodes):
    for y, cell in enumerate(row):
      maze_x = 2*x+1
      maze_y = 2*y+1
      for conn in cell:
        maze[maze_x+conn[0]][maze_y+conn[1]] = OPEN

  maze[1][1] = START
  maze[2*(len(maze_nodes)-1)+1][2*(len(maze_nodes)-1)+1] = END
  return maze

def mazeCoorToScreenCoor(coor):
  x, y = coor
  # print("mazeCoorToScreenCoor", x, y)
  screen_x = (-(window_width/2) + (x * 24) ) + 6
  screen_y = (window_height/2 - (y * 24)) - 6
  return screen_x, screen_y

def stamp(pen, x, y, color="white", size=1):
  pen.setSize(size)
  pen.setColor(color)
  screen_x, screen_y = mazeCoorToScreenCoor((x, y))
  pen.goto(screen_x, screen_y)
  pen.stamp()

def drawMaze(maze):
  class Pen(turtle.Turtle):
    def __init__(self):
      turtle.Turtle.__init__(self)
      self.shape("square")
      self.color("white")
      self.penup()
      self.speed(0)

    def setColor(self, color):
      return self.color(color)

    def setSize(self, size):
      return self.turtlesize(size)

  pen = Pen()
  
  wn = turtle.Screen()
  wn.bgcolor("black")
  wn.title("Maze")
  global window_width, window_height
  window_width = 24 * len(maze[0])
  window_height = 24 * len(maze)

  wn.setup(window_width+6, window_height+6)

  for x, row in enumerate(maze):
    for y, cell in enumerate(row):
      if cell == WALL:
        stamp(pen, x, y, color="white", size=1)

  stamp(pen, 1, 1, color="blue", size=1)

  stamp(pen, len(maze)-2, len(maze[0])-2, color="green", size=1)

  return pen

def checkSolution(maze, path, pen=None):
  '''
    Takes a maze: 2d array and a 
    series of paths: 1d array of tuple of size 2 (x, y)
    and returns true if from starting at the START marker, and following the path you arrive at END
  '''
  cur_pos = (1, 1)

  old_pos = None
  for pos in path:
    if old_pos:
      if (abs(old_pos[0]-pos[0]) + abs(old_pos[1]-pos[1])) != 1:
        return False

    if pen is not None:
      stamp(pen, pos[0], pos[1], color="red", size=1)

    if maze[pos[0]][pos[1]] == WALL:
      return False

    if maze[pos[0]][pos[1]] == END:
      return True

    old_pos = pos

  return False

def printMaze(maze):
  for row in maze:
    for cell in row:
      print(cell, end="")
    print("")

def nextPaths(maze, pos, visted):
  x, y = pos
  possiblePath = []
  if x + 1 < len(maze[0]) and (maze[x+1][y] == OPEN or maze[x+1][y] == END):  # right
    possiblePath.append((x+1, y))
  if x - 1 >= 0 and (maze[x-1][y] == OPEN or maze[x-1][y] == END):            # left
    possiblePath.append((x-1, y))
  if y - 1 >= 0 and (maze[x][y-1] == OPEN or maze[x][y-1] == END):            # up
    possiblePath.append((x, y-1))
  if y + 1 < len(maze) and (maze[x][y+1] == OPEN or maze[x][y+1] == END):     # down
    possiblePath.append((x, y+1))
  
  return [position for position in possiblePath if position not in visted]

def recursiveDepthSearch(maze, cur_pos, path, pen=None):
  if maze[cur_pos[0]][cur_pos[1]] == END:
    return path
  nps = nextPaths(maze, cur_pos, path)
  for np in nps:
    if pen:
      stamp(pen, np[0], np[1], color="orange", size=0.8)
    ans = recursiveDepthSearch(maze, np, path+[np], pen=pen)
    if ans:
      return ans
    if pen:
      pen.clearstamps(-1)
  return None

def loopDepthSearch(maze, pos):
  path = [pos]
  toVist = []
  while maze[path[-1][0]][path[-1][1]] != END:
    nps = nextPaths(maze, path[-1], path)
    for np in nps:
      toVist.append(path + [np])
    path = toVist.pop()

  return path
  

def answer(maze, loop=False, pen=None):
  cur_pos = (1, 1)
  path = [cur_pos]
  
  # TODO:
  # - implement drawing for loop
  # - other algorithems
  if loop:
    ans = loopDepthSearch(maze, cur_pos)
  else:
    ans = recursiveDepthSearch(maze, cur_pos, path, pen=pen)

  if ans:
    return ans
  return []

if __name__ == "__main__":
  pen = None

  m = createMaze(10, 10)
  printMaze(m)

  # Comment out line to remove GUI
  pen = drawMaze(m)

  if checkSolution(m, answer(m, pen=pen), pen=pen):
    print("Success!")
  else:
    print("Failed!")

  input("Press any key to continue...")

