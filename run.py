import pygame
from enum import Enum, auto

class CellType(Enum):
    WALL = auto()
    GRASS = auto()
    START = auto()
    END = auto()
    PIT = auto()
    DIAMOND = auto()
    ROBOT = auto()

GRID = [
    [CellType.GRASS ,CellType.GRASS , CellType.GRASS , CellType.END],
    [CellType.GRASS ,CellType.WALL , CellType.GRASS, CellType.DIAMOND],
    [CellType.START ,CellType.GRASS,CellType.GRASS , CellType.PIT]
]

CELL_IMAGE = {
    CellType.GRASS : "images/grass.png",
    CellType.WALL : "images/wall.png",
    CellType.START : "images/start.png",
    CellType.END : "images/end.png",
    CellType.PIT : "images/lava.png",
    CellType.DIAMOND : "images/diamond.png",
    CellType.ROBOT : "images/robot.png",
}

class Action(Enum):
    QUIT = "quit"
    UP = "up"
    RIGHT = "right"
    LEFT = "left"
    DOWN = "down"

ACTION_ANGLE = {
    Action.UP: 0,
    Action.LEFT: 90,
    Action.DOWN: 180,
    Action.RIGHT: -90,
}

ACTION_DELTA = {
    Action.UP:    (-1, 0),
    Action.DOWN:  (1, 0),
    Action.LEFT:  (0, -1),
    Action.RIGHT: (0, 1),
}

KEY_TO_ACTION = {
    pygame.K_ESCAPE : Action.QUIT,
    pygame.K_UP : Action.UP,
    pygame.K_DOWN : Action.DOWN,
    pygame.K_LEFT : Action.LEFT,
    pygame.K_RIGHT : Action.RIGHT,
}

CELL_SIZE = 200
CELL_W , CELL_H = 4, 3
SIDEBAR_H = 200
SCREEN_W = CELL_SIZE*CELL_W
SCREEN_H = CELL_SIZE*CELL_H+SIDEBAR_H
robot_pos = [2,0]
robot_direction = Action.UP
score = 0
steps = 0
game_over = False
game_status = "Playing..."

def run():
    running = True
    pygame.init()
    screen = display_create()
    images= load_images()
    font = load_font()


    clock = pygame.time.Clock()
    print(pygame.display.Info())
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_ACTION:
                    action = KEY_TO_ACTION[event.key]

                    if action == Action.QUIT:
                        running = False
                    else:
                        move_robot(robot_pos , action)
            
        screen.fill((0,0,0))
        map_create(screen , images)
        draw_robot(screen ,images , robot_pos , robot_direction)
        draw_sidebar(screen, font , score , steps, game_status)
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()


def display_create():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Grid world")
    return screen

def load_images():
    images = {}
    for cell_type, path in CELL_IMAGE.items():
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image , (CELL_SIZE , CELL_SIZE))
        images[cell_type] = image
    return images


def map_create(screen, images):
    for row_index , row in enumerate(GRID):
        for col_index , cell_type in enumerate(row):
            x =  col_index * CELL_SIZE
            y = row_index * CELL_SIZE
            screen.blit(images[cell_type] , (x,y))

def move_robot(robot_pos , action):
    global robot_direction, steps , game_over

    if game_over:
        return

    x , y = ACTION_DELTA[action]
    x = robot_pos[0] + x
    y = robot_pos[1] + y

    robot_direction = action

    if not(0<= x < CELL_H and 0 <= y < CELL_W):
        return
    if GRID[x][y] == CellType.WALL:
        return

    robot_pos[0] = x
    robot_pos[1] = y

    steps +=1
    check_collision(robot_pos)

def draw_robot(screen, images , robot_pos , robot_direction):
    row,col = robot_pos
    x1 = col* CELL_SIZE
    y1 = row*CELL_SIZE

    angle = ACTION_ANGLE[robot_direction]
    rotated_image = pygame.transform.rotate(images[CellType.ROBOT], angle)
    
    screen.blit(rotated_image , (x1,y1))

def load_font():
    return pygame.font.Font(None , 48)

def draw_sidebar(screen , font , score , steps, status):
    sidebar_y = CELL_SIZE * CELL_H
    pygame.draw.rect(screen, (30,30,30), (0 ,sidebar_y , SCREEN_W , SCREEN_H))

    steps_surface = font.render(f'Steps: {steps}' , True , (255,255,255))
    score_surface = font.render(f'Score: {score}' , True , (255,255,255))
    game_status = font.render(f'Status: {status}' , True , (255,255,255))

    screen.blit(steps_surface , (20, sidebar_y+20))
    screen.blit(score_surface , (20, sidebar_y+70))
    screen.blit(game_status , (20, sidebar_y+120))

def check_collision(robot_pos):
    global score , game_over, game_status
    row , col = robot_pos 
    cell = GRID[row][col]

    if cell == CellType.DIAMOND:
        score += 100
        GRID[row][col] = CellType.GRASS

    elif cell == CellType.PIT:
        score -=200
        game_over = True
        game_status = "YOU LOST!"
    
    elif cell == CellType.END:
        score += 50
        game_over = True
        game_status = "YOU WON!"

run()