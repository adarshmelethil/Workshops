# Python Basics

## Note 
Comment out the following line to remove the drawing, it will run a lot faster.
```python 
pen = drawMaze(m)
```

## Final Challenge
The final challenge is to solve a maze.
Most of the code has been already been writen except for the solution.
All you have to do is fill in the following `ans` function in problem.
```python
def answer(maze, pen=None):
  cur_pos = (1, 1)
  path = [cur_pos]
  
  # TODO: replace this array with your solution
  ans = [(1, 2), (1, 3), (2, 3)]

  if ans:
    return ans
  return []

```

I have defined the characters we will use the represent the maze.
```python
from .maze import START, END, WALL, OPEN
```

So to check wether a location is open you could do the following.
```python
.
.
.
# Check if the location at (5, 5) is open
if maze[5][5] == OPEN:
  print("it is open")
else:
  print("its not open")

  if maze[5][5] == END:
    print("FOUND END!")
```

### Solution
The solution is in `game.py`.
