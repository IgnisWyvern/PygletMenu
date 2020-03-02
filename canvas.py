import pyglet
from enum import Enum


class Shape(Enum):
    rect = 1
    circle = 2
    quad = 3

class Canvas:
    def __init__(self, x: int, y: int, height: int, width: int, reso_x: int,
                 reso_y: int):
        self.x: int = x
        self.y: int = y
        self.height: int = height
        self.width: int = width
        self.reso_x: int = reso_x
        self.reso_y: int = reso_y

        self.batch = pyglet.graphics.Batch()
        self.user_fore = pyglet.graphics.OrderedGroup(3)
        self.fore = pyglet.graphics.OrderedGroup(2)
        self.mid = pyglet.graphics.OrderedGroup(1)
        self.back = pyglet.graphics.OrderedGroup(0)

    def draw(self):
        self.batch.draw()

    def addShape(self, Shape.rect, x1, y1, x2, y2):
        pass

    def addShape(self, Shape.circle, x, y, radi):
        pass
