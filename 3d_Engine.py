from math import cos, sin
import pygame
from pygame import draw, display, event, key, time
from objects import *

# Initialize Pygame
pygame.init()

# Set up the window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

display.set_caption("3D")

SCALE = 1

# find the center of the screen
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2
P_CENTER = Point(center_x, center_y)

# Set up the player
player = Player('Player', Point(-50, -50), 0, 20, (255, 0, 0))


# Set up the clock
clock = time.Clock()
fps = 60

# set clipdepth
CLIPDEPTH = 0.1
WALLHEIGHT = 100

############## MAP STARTS HERE #####################
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
# build a room
for x in range(0, 900, 100):
    walls.append(Wall(Point(x, -800), Point(x, 0)))
    walls.append(Wall(Point(0, x-800), Point(800, x-800)))

for x in range(-900, 0, 100):
    walls.append(Wall(Point(x, 0), Point(x, 800), True))
    walls.append(Wall(Point(-900, x+900), Point(0, x+900), True))

# Define the center and radius of the pentagon
center = Point(-800, -800)
radius = 150

# Define the angles for the vertices of the pentagon
angles = [i * 2 * math.pi / 5 for i in range(5)]

# Create the vertices of the pentagon
vertices = [Point(center.x + radius * math.cos(angle),
                  center.y + radius * math.sin(angle)) for angle in angles]

# Create the walls of the pentagon
for i in range(5):
    start = vertices[i]
    end = vertices[(i + 1) % 5]  # Use modulo to loop back to the first vertex
    walls.append(Wall(start, end))

# Create the walls of the square
walls.append(Wall(Point(-100, -100), Point(-500, -100)))
walls.append(Wall(Point(-500, -600), Point(-500, -100)))


def appendSquare(x, y, size=100):
    walls.append(Wall(Point(x, y), Point(x, y+size)))
    walls.append(Wall(Point(x, y+size), Point(x+size, y+size)))
    walls.append(Wall(Point(x+size, y+size), Point(x+size, y)))
    walls.append(Wall(Point(x + size, y), Point(x, y)))

appendSquare(-500, 400,100)
appendSquare(-700, 100,100)

for y in range(-1000, -400, 50):
    appendSquare(-400, y, 20)
    appendSquare(-300, y, 20)


############## MAP ENDS HERE #####################

def rotate(point, angle):
    return Point(
        point.magnitude() * cos(point.angle() + angle),
        point.magnitude() * sin(point.angle() + angle)
    )


def transform(point):
    transformed = point - player.pos
    return rotate(transformed, player.rotation)


def toScreen(point):

    if point.y == 0:
        point.y = 0.0001

    depth = point.y

    depthScale = 1 / depth * SCREEN_HEIGHT

    transformed = Point(-point.x, WALLHEIGHT/2)
    transformed *= depthScale
    transformed += Point(center_x, 0)

    return transformed
# , (1 / depth * 1000)


def lerpWall(start, end, clipDepth, isFloor):

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

    return Wall(top, Point(clipX, -clipDepth), isFloor)


def findClipWalls(walls, clipDepth=CLIPDEPTH):
    clipWalls = []

    # set an offset for the clip depth

    # loop through walls
    for wall in walls:
        # rotate the lines according so that it in a state right before rendering.
        start = transform(wall.start)
        end = transform(wall.end)

        # Then, check if the lines are clipped or not.
        if start.y < clipDepth and end.y < clipDepth:
            # both are not clipped
            clipWalls.append(Wall(start, end, wall.floor))
        elif start.y > clipDepth and end.y > clipDepth:
            # both are clipped
            continue
        else:
            # one is clipped
            clipWalls.append(lerpWall(start, end, clipDepth, wall.floor))

    return clipWalls


# surface test(MINIMAP)
# Set up the surface

surface_scale = 5  # put the denominator here


def scaler(value):
    return value//surface_scale


def toSurface(point):
    transformed = point-player.pos
    transformed *= SCALE
    transformed += P_CENTER
    return transformed


surface = pygame.Surface(
    (SCREEN_WIDTH//surface_scale, SCREEN_HEIGHT//surface_scale))
surface_center = Point(SCREEN_WIDTH//(surface_scale*2),
                       SCREEN_HEIGHT//(surface_scale*2))


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
    draw.line(surface, (0, 255, 255), (surface_center.x-30*cos(-player.rotation), surface_center.y-30*sin(-player.rotation)),
              (surface_center.x+30*cos(-player.rotation), surface_center.y+30*sin(-player.rotation)), width=2)
    # draw line
    for wall in walls:
        scaledWall = Wall(toSurface(wall.start).divide(
            surface_scale), toSurface(wall.end).divide(surface_scale))
        draw.line(surface, (0, 0, 0),
                  (scaledWall.start.x, scaledWall.start.y), (scaledWall.end.x, scaledWall.end.y))
#####


def updateScreen():
    global player
    # Clear the window
    window.fill((0, 0, 0))

    # Draw horizon
    draw.line(window, (0, 255, 0), (0, center_y), (SCREEN_WIDTH, center_y))

    # draw cicle in the cetner of the screen
    # draw.circle(window, (255, 0, 0), (center_x, center_y), 20)

    # Find walls which clip
    clipWalls = findClipWalls(walls, CLIPDEPTH)

    # draw line
    for wall in clipWalls:
        topPoint = toScreen(wall.start)
        bottomPoint = toScreen(wall.end)
        w = Wall(topPoint, bottomPoint)

        # width = abs(int((w1+w2)/2))
        width = 1

        # draw.line(window, (255, 255, 255),
        #           (w.start.x, w.start.y), (w.end.x, w.end.y))

        # bottom Edge
        draw.line(window, (255, 255, 255),
                  (w.start.x, center_y-w.start.y), (w.end.x, center_y-w.end.y), width=width)
        if wall.floor:
            continue
        # top Edge
        draw.line(window, (255, 255, 255),
                  (w.start.x, center_y+w.start.y), (w.end.x, center_y+w.end.y), width)

        # Vertical Walls
        if w.start.y < CLIPDEPTH:
            draw.line(window, (255, 255, 255),
                      (w.start.x, center_y-w.start.y), (w.start.x, center_y+w.start.y), width)
        if w.end.y < CLIPDEPTH:
            draw.line(window, (255, 255, 255),
                      (w.end.x, center_y-w.end.y), (w.end.x, center_y+w.end.y), width)

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
