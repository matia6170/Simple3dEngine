from math import cos, sin
import pygame
from pygame import draw, display, event, key, time
from objects import *

# Initialize Pygame
pygame.init()

# Set up the window
width = 800
height = 600
window = display.set_mode((width, height))
display.set_caption("3D")

SCALE = 1

# find the center of the screen
center_x = width // 2
center_y = height // 2
P_CENTER = Point(center_x, center_y)

# Set up the player
player = Player('Player', Point(0, 0), 0, 20, (255, 0, 0))


# Set up the clock
clock = time.Clock()
fps = 60


# set up the walls

walls = [
    # Wall(Point(0, 0), Point(0, 100)),
    # Wall(Point(0, 100), Point(100, 100)),
    # Wall(Point(100, 100), Point(100, 0)),
    # Wall(Point(100, 0), Point(0, 0)),
    # # Triangle
    # Wall(Point(-100, -175), Point(-125, -225)),  # Top to bottom left
    # Wall(Point(-125, -225), Point(-75, -225)),  # Bottom left to bottom right
    # Wall(Point(-75, -225), Point(-100, -175))  # Bottom right to top


    # # Outer walls
    # Wall(Point(0, 0), Point(0, 600)),
    # Wall(Point(0, 600), Point(800, 600)),
    # Wall(Point(800, 600), Point(800, 0)),
    # Wall(Point(800, 0), Point(0, 0)),
    # # Maze walls
    # Wall(Point(100, 0), Point(100, 500)),
    # Wall(Point(200, 100), Point(200, 600)),
    # Wall(Point(300, 0), Point(300, 500)),
    # Wall(Point(400, 100), Point(400, 600)),
    # Wall(Point(500, 0), Point(500, 500)),
    # Wall(Point(600, 100), Point(600, 600)),
    # Wall(Point(700, 0), Point(700, 500)),
    # Outer walls
    Wall(Point(0, 0), Point(0, 800)),
    Wall(Point(0, 800), Point(800, 800)),
    Wall(Point(800, 800), Point(800, 0)),
    Wall(Point(800, 0), Point(0, 0)),
    # Maze walls
    Wall(Point(100, 0), Point(100, 300)),
    Wall(Point(100, 500), Point(100, 800)),
    Wall(Point(200, 0), Point(200, 200)),
    Wall(Point(200, 400), Point(200, 800)),
    Wall(Point(300, 0), Point(300, 300)),
    Wall(Point(300, 500), Point(300, 800)),
    Wall(Point(400, 0), Point(400, 200)),
    Wall(Point(400, 400), Point(400, 800)),
    Wall(Point(500, 0), Point(500, 300)),
    Wall(Point(500, 500), Point(500, 800)),
    Wall(Point(600, 0), Point(600, 200)),
    Wall(Point(600, 400), Point(600, 800)),
    Wall(Point(700, 0), Point(700, 300)),
    Wall(Point(700, 500), Point(700, 800)),

]


def rotate(point, angle):
    return Point(
        point.magnitude() * cos(point.angle() + angle),
        point.magnitude() * sin(point.angle() + angle)
    )


def transform(point):
    return point - player.pos


def toScreen(point):
    transformed = transform(point)
    transformed = rotate(transformed, player.rotation)
    transformed *= SCALE
    transformed += P_CENTER
    return transformed




##### surface test

# Set up the surface
surface = pygame.Surface((width//5, height//5))
surface_scale = 0.2

surface.fill((255,255, 255))



def updateSurface():
    global player
    # Clear the window
    surface.fill((255, 255, 255))

    # Draw player

    draw.circle(surface, player.color,
                (player.pos.x//5, player.pos.y//5), player.radius//5)
    draw.line(surface, (0, 0, 0),
              (player.pos.x//5, player.pos.y//5), (player.pos.x//5+10*cos(-player.rotation-math.pi/2), player.pos.y//5+10*sin(-player.rotation-math.pi/2)))

    # draw line
    for wall in walls:
       
        draw.line(surface, (0, 0, 0),
                  (wall.start.x//5, wall.start.y//5), (wall.end.x//5, wall.end.y//5))

    



#####

def updateScreen():
    global player
    # Clear the window
    window.fill((0, 0, 0))

    # Draw player
    playerPos = toScreen(player.pos)
    draw.circle(window, player.color,
                (playerPos.x, playerPos.y), player.radius)
    draw.line(window, (255, 255, 255),
              (playerPos.x, playerPos.y), (playerPos.x, playerPos.y-20))

    # draw line
    for wall in walls:
        w = Wall(toScreen(wall.start), toScreen(wall.end))
        draw.line(window, (255, 255, 255),
                  (w.start.x, w.start.y), (w.end.x, w.end.y))
    
    updateSurface()
    window.blit(surface, (0, 0))
    # Update the window
    display.flip()


# Game loop
running = True
while running:
    # Handle events
    for e in event.get():
        if e.type == pygame.QUIT:
            running = False

    # Handle controls
    # handleControls(player)
    player.handleControls()

    # Update the screen
    updateScreen()

    # Limit the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
