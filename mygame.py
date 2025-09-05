BOARD_WIDTH = 800
BOARD_HEIHGT = 800
BG_COLOR= (150,150,150)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
DEFAULT_COLOR = TILE_COLORS[0]

NUM_GRID = 4
GRID_SIZE = BOARD_WIDTH // NUM_GRID
TILE_MARGIN = 3



def draw_cell(screen,row,column,value):
    rect = pygame.Rect(column * GRID_SIZE + TILE_MARGIN,
                       row *GRID_SIZE + TILE_MARGIN,
                       GRID_SIZE - TILE_MARGIN * 2,
                       GRID_SIZE - TILE_MARGIN * 2)
    color = TILE_COLORS.get(value, DEFAULT_COLOR)
    pygame.draw.rect(screen,color,rect)

def render_board(screen):
    screen.fill(BG_COLOR)

def rotate(is_cw,board_map):
    pass

# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIHGT))
clock = pygame.time.Clock()
running = True
board_map = [[0 for _ in range(NUM_GRID)] for _ in range(NUM_GRID)]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        board_map[0][0] = 2
                    case pygame.K_RIGHT:
                        board_map[0][1] = 4
                    case pygame.K_UP:
                        board_map[0][2] = 8
                    case pygame.K_DOWN:
                        board_map[0][3] = 16
                    case _:
                        pass

                
    # fill the screen with a color to wipe away anything from last frame
    #screen.fill("purple")
    render_board(screen)
    for row in range(NUM_GRID):
        for column in range(NUM_GRID):
            draw_cell(screen,row,column,board_map[row][column])
    

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()