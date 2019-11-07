import pygame
import turtle


class Pen(turtle.Turtle):
  def __init__(self, window_width, window_height, draw_size, buffer_size):
    self.window_width, self.window_height = window_width, window_height
    self.draw_size, self.buffer_size = draw_size, buffer_size

    turtle.Turtle.__init__(self)
    self.shape("triangle")
    self.color("white")
    self.shapesize(0.5, 0.5, 0.5)
    self.speed(0)
    self.up()

    self.old_tracer = turtle.tracer()
    self.old_delay = turtle.delay()

  def noDelay(self):
    self.delay = False
    turtle.tracer(0, 0)

  def delay(self):
    turtle.tracer(self.old_tracer, self.old_delay)

  def setColor(self, color):
    return self.color(color)

  def setSize(self, size):
    return self.turtlesize(size)

  def draw(self, x, y, color="white"):
    old_pos = self.pos()
    self.setColor(color)
    screen_x, screen_y = self.mazeCoorToScreenCoor(x, y)
    self.goto(screen_x, screen_y)
    self.dot(size=self.draw_size)
    self.goto(old_pos)

  def moveTo(self, x, y):
    screen_x, screen_y = self.mazeCoorToScreenCoor(x, y)
    self.goto(screen_x, screen_y)

  def mazeCoorToScreenCoor(self, x, y):
    space = self.draw_size + self.buffer_size
    screen_x = -(self.window_width/2 - space) + (x * space)
    screen_y = -(self.window_height/2 - space) + (y * space) + self.buffer_size
    return screen_x, screen_y

  def goOffScreen(self):
    self.goto(*self.mazeCoorToScreenCoor(-1, -1))


def drawWorld(maze, start_pos, end_pos, obsticle_map, bgcolor="black"):
  wn = turtle.Screen()
  wn.bgcolor(bgcolor)
  wn.title("Maze")
  
  draw_size = 10
  buffer_size = 6
  window_width = (draw_size + buffer_size)  * (len(maze[0]) + 2)
  window_height = (draw_size + buffer_size) * (len(maze) + 2)
  # wn.setup(window_width+draw_size*2, window_height+draw_size*2)
  wn.setup(window_width, window_height)

  pen = Pen(window_width, window_height, draw_size=draw_size, buffer_size=buffer_size)

  old_tracer = turtle.tracer()
  old_delay = turtle.delay()
  turtle.tracer(0, 0)

  for x, row in enumerate(maze):
    for y, cell in enumerate(row):
      if cell in obsticle_map:
        pen.draw(x, y, color=obsticle_map[cell])
  
  turtle.update()
  turtle.tracer(old_tracer, old_delay)

  return pen
  