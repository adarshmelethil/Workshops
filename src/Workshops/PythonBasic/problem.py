
from .game import createMaze, printMaze, drawMaze, checkSolution
from .game import START, END, WALL, OPEN

def myAnswer(maze, pen=None):
  cur_pos = (1, 1)
  path = [cur_pos]
  
  # TODO: replace this array with your solution
  ans = [(1, 2), (1, 3), (2, 3)]

  return ans

if __name__ == "__main__":
  pen = None

  m = createMaze(10, 10)
  printMaze(m)

  # Comment out line to remove GUI
  pen = drawMaze(m)

  if checkSolution(m, myAnswer(m, pen=pen), pen=pen):
    print("Success!")
  else:
    print("Failed!")

  input("Press any key to continue...")
