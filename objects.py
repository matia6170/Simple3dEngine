import math
from math import cos, sin, atan2
import pygame

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Unsupported operand type for +")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Unsupported operand type for -")
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Unsupported operand type for *")
        return Point(self.x * scalar, self.y * scalar)
    
    def set(self, x, y):
        self.x = x
        self.y = y
    def set(self, other):
        if not isinstance(other, Point):
            raise TypeError("Unsupported operand type for set")
        self.x = other.x
        self.y = other.y
            
    def multiply(self, scalar):
        self.x *= scalar
        self.y *= scalar
    def divide(self, scalar):
        self.x //= scalar
        self.y //= scalar
        return self
    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Unsupported operand type for dot product")
        return self.x * other.x + self.y * other.y
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def normalize(self):
        self.divide(self.magnitude())
    def angle(self):
        return atan2(self.y, self.x)

class Player:
    def __init__(self, name, pos, rotation=0, radius=20, color=(255, 0, 0)):
        if not isinstance(pos, Point):
            raise TypeError('pos must be an instance of Point')
        self.name = name
        self.pos = pos
        self.radius = radius
        self.color = color
        self.rotation = rotation
    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy
    def handleControls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            #self.move(-5, 0)
            self.rotation += 0.02
        if keys[pygame.K_RIGHT]:
            #self.move(5, 0)
            self.rotation -= 0.02
        if keys[pygame.K_a]:
            #move left
            self.move(-5*cos(self.rotation), 5*sin(self.rotation))
        if keys[pygame.K_d]:
            #move right
            self.move(5*cos(self.rotation), -5*sin(self.rotation))
        if keys[pygame.K_w]:
            #move up
            self.move(-5*sin(self.rotation), -5*cos(self.rotation))
        if keys[pygame.K_s]:
            #move down
            self.move(5*sin(self.rotation), 5*cos(self.rotation))


# class Point(Vector):
#     def __init__(self, x=0, y=0):
#         super().__init__(x, y)
#     def angle(self):
#         return atan2(self.y, self.x)
        

class Wall:
    def __init__(self, start, end, floor=False):
        if not isinstance(start, Point) or not isinstance(end, Point):
            raise TypeError('start and end must be instances of Point')
        self.start = start
        self.end = end
        self.floor = floor






    



