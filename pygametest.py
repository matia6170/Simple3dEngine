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
    # Triangle
    Wall(Point(-100, -175), Point(-125, -225)),  # Top to bottom left
    Wall(Point(-125, -225), Point(-75, -225)),  # Bottom left to bottom right
    Wall(Point(-75, -225), Point(-100, -175)),  # Bottom right to top


    # # Outer walls
    # Wall(Point(0, 0), Point(0, 800)),
    # Wall(Point(0, 800), Point(800, 800)),
    # Wall(Point(800, 800), Point(800, 0)),
    # Wall(Point(800, 0), Point(0, 0)),
    # # Maze walls
    # Wall(Point(100, 0), Point(100, 300)),
    # Wall(Point(100, 500), Point(100, 800)),
    # Wall(Point(200, 0), Point(200, 200)),
    # Wall(Point(200, 400), Point(200, 800)),
    # Wall(Point(300, 0), Point(300, 300)),
    # Wall(Point(300, 500), Point(300, 800)),
    # Wall(Point(400, 0), Point(400, 200)),
    # Wall(Point(400, 400), Point(400, 800)),
    # Wall(Point(500, 0), Point(500, 300)),
    # Wall(Point(500, 500), Point(500, 800)),
    # Wall(Point(600, 0), Point(600, 200)),
    # Wall(Point(600, 400), Point(600, 800)),
    # Wall(Point(700, 0), Point(700, 300)),
    # Wall(Point(700, 500), Point(700, 800)),
    # Outer walls
    Wall(Point(0, 0), Point(0, 800)),
    Wall(Point(0, 800), Point(800, 800)),
    Wall(Point(800, 800), Point(800, 0)),
    Wall(Point(800, 0), Point(0, 0)),
    # Maze walls
    Wall(Point(100, 0), Point(100, 300)),
    Wall(Point(100, 400), Point(100, 800)),
    Wall(Point(200, 0), Point(200, 200)),
    Wall(Point(200, 300), Point(200, 500)),
    Wall(Point(200, 600), Point(200, 800)),
    Wall(Point(300, 100), Point(300, 400)),
    Wall(Point(300, 500), Point(300, 700)),
    Wall(Point(400, 0), Point(400, 300)),
    Wall(Point(400, 400), Point(400, 800)),
    Wall(Point(500, 100), Point(500, 500)),
    Wall(Point(500, 600), Point(500, 800)),
    Wall(Point(600, 0), Point(600, 400)),
    Wall(Point(600, 500), Point(600, 800)),
    Wall(Point(700, 200), Point(700, 600)),
    Wall(Point(700, 700), Point(700, 800)),
]


def rotate(point, angle):
    return Point(
        point.magnitude() * cos(point.angle() + angle),
        point.magnitude() * sin(point.angle() + angle)
    )


def transform(point):
    return point - player.pos


def toScreen(point, surface=False):
    transformed = transform(point)
    if not surface:
        transformed = rotate(transformed, player.rotation)
    transformed *= SCALE
    transformed += P_CENTER
    return transformed


def lerpWall(start, end, clipDepth):

    top, bottom = Point(), Point()

    # get top and bottom points
    if start.y < clipDepth:
        top = start
        bottom = end
    else:
        top = end
        bottom = start

    # get total height
    dy = bottom.y-top.y
  
    # get proportions
    proportion = (clipDepth - top.y) / dy

    # get clip point depending on if top is on the left or right
    if top.x > bottom.x:
        clipX = top.x - (top.x - bottom.x) * proportion
    else:
        clipX = top.x + (bottom.x - top.x) * proportion

    return Wall(top, Point(clipX, clipDepth))


def findClipWalls(walls, clipDepth=0.1):
    clipWalls = []

    # set an offset for the clip depth
    clipDepth = center_y - clipDepth

    # loop through walls
    for wall in walls:
        # rotate the lines according so that it in a state right before rendering.
        start = toScreen(wall.start)
        end = toScreen(wall.end)

        # Then, check if the lines are clipped or not.
        if start.y < clipDepth and end.y < clipDepth:
            # both are not clipped
            clipWalls.append(Wall(start, end))
        elif start.y > clipDepth and end.y > clipDepth:
            # both are clipped
            continue
        else:
            # one is clipped
            clipWalls.append(lerpWall(start, end, clipDepth))

    return clipWalls


# surface test(MINIMAP)
# Set up the surface

surface_scale = 5 # put the denominator here
def scaler(value):
    return value//surface_scale

surface = pygame.Surface((width//surface_scale, height//surface_scale))
surface_center = Point(width//(surface_scale*2), height//(surface_scale*2))


surface.fill((255, 255, 255))


def updateSurface():
    global player
    # Clear the window
    surface.fill((255, 255, 255))

    # Draw player
    scaledPlayer = Point(scaler(player.pos.x), scaler(player.pos.y))

    draw.circle(surface, player.color,
                (surface_center.x, surface_center.y), scaler(player.radius))
    draw.line(surface, (0, 0, 0),
              (surface_center.x, surface_center.y), (surface_center.x+10*cos(-player.rotation-math.pi/2), surface_center.y+10*sin(-player.rotation-math.pi/2)))

    # draw line
    for wall in walls:
        scaledWall = Wall(toScreen(wall.start, True).divide(surface_scale), toScreen(wall.end, True).divide(surface_scale))
        draw.line(surface, (0, 0, 0),
                  (scaledWall.start.x, scaledWall.start.y), (scaledWall.end.x, scaledWall.end.y))
#####


def updateScreen():
    global player
    # Clear the window
    window.fill((0, 0, 0))

    # draw cicle in the cetner of the screen
    draw.circle(window, (255, 0, 0), (center_x, center_y), 20)

    # Find walls which clip
    clipWalls = findClipWalls(walls)

    # draw line
    for wall in clipWalls:
        w = Wall((wall.start), (wall.end))
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
