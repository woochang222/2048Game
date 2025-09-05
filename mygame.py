import math


BOARD_WIDTH = 800
BOARD_HEIGHT = 800
BG_COLOR = [187, 173, 160]
NUM_GRID = 4
GRID_SIZE = BOARD_WIDTH // NUM_GRID
TILE_MARGIN = 3
TILE_COLORS = {
    1: (205, 193, 180),
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
    2048: (237, 194, 46),
}
DEFAULT_COLOR = TILE_COLORS[1]
SPAWN_NUMBERS = [2, 4] 
SPAWN_CHANCES = [0.9, 0.1]
HISTORIC_MAX = 0 

def render_board(screen, board_map):
    screen.fill(BG_COLOR)
    for row in range(NUM_GRID):
        for column in range(NUM_GRID):
            draw_cell(screen, row, column, board_map[row][column])


def draw_cell(screen, row, column, cell):
    rect = pygame.Rect(
        column * GRID_SIZE + TILE_MARGIN,
        row * GRID_SIZE + TILE_MARGIN,
        GRID_SIZE - TILE_MARGIN * 2,
        GRID_SIZE - TILE_MARGIN * 2
    )
    color = TILE_COLORS.get(cell, DEFAULT_COLOR)
    
    
    pygame.draw.rect(screen, color, rect)
    if cell != 0:
        font = pygame.font.Font(None, 72)
        text = font.render(str(cell), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    
    
def rotate(is_cw, board_map):
    new_map = None
    if is_cw:
        new_map = [list(row) for row in zip(*board_map[::-1])]
    else:
        new_map = [list(row) for row in zip(*board_map)][::-1]
    return new_map

def merge_row(row):
    new_row = []
    skip_merge = False
    for i in range(NUM_GRID):
        if skip_merge:
            skip_merge = False
            continue
        if row[i] == 0:
            continue
        if i+1 < len(row) and row[i] == row[i+1]:
            new_row.append(row[i]*2)
            skip_merge = True
        elif i < len(row) :
            new_row.append(row[i])
    while len(row) > len(new_row):
        new_row.append(0)
    return new_row

def push_and_merge(direction, board_map):
    if direction == pygame.K_LEFT:
        for r in range(NUM_GRID):
            board_map[r] = merge_row(board_map[r])
    elif direction == pygame.K_RIGHT:
        for r in range(NUM_GRID):
            board_map[r] = merge_row(board_map[r][::-1])[::-1]
    elif direction == pygame.K_DOWN:
        board_map = rotate(True, board_map)
        for r in range(NUM_GRID):
            board_map[r] = merge_row(board_map[r])
        board_map = rotate(False, board_map)
    elif direction == pygame.K_UP:
        board_map = rotate(False, board_map)
        for r in range(NUM_GRID):
            board_map[r] = merge_row(board_map[r])
        board_map = rotate(True, board_map)
    return board_map

def game_over(board_map):
    for r in range(NUM_GRID):
        for c in range(NUM_GRID):
            if board_map[r][c] == 0:
                return False
            if c + 1 < NUM_GRID and board_map[r][c] == board_map[r][c+1]:
                return False
            if r + 1 < NUM_GRID and board_map[r][c] == board_map[r+1][c]:
                return False
    return True

def create_new_tile(board_map):
    import random
    empty_cells = [(r, c) for r in range(NUM_GRID) for c in range(NUM_GRID) if board_map[r][c] == 0]
    if not empty_cells:
        return board_map
    r, c = random.choice(empty_cells)
    board_map[r][c] = random.choices(SPAWN_NUMBERS, SPAWN_CHANCES)[0]
    return board_map

def current_max_number(board_map):
    max_num = 0
    for r in range(NUM_GRID):
        for c in range(NUM_GRID):
            if board_map[r][c] > max_num:
                max_num = board_map[r][c]
    return max_num

def calculate_score(board_map):
    score = 0
    for r in range(NUM_GRID):
        for c in range(NUM_GRID):
            if board_map[r][c] >= 4:
                score += board_map[r][c]
    return score

def calculate_current_level(board_map):
    max_num = current_max_number(board_map)
    level = 0
    while max_num >= 2**(level + 1):
        level += 1
    return level

def reset():
    global HISTORIC_MAX
    if(calculate_score(board_map) > HISTORIC_MAX):
        HISTORIC_MAX = calculate_score(board_map)
    return [[0 for _ in range(NUM_GRID)] for _ in range(NUM_GRID)]

if __name__ == "__main__":
    # Example file showing a basic pygame "game loop"
    import pygame

    # pygame setup
    pygame.init()
    pygame.display.set_caption("2048 Game")
    screen = pygame.display.set_mode((1280, 960))
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
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    board_map = push_and_merge(event.key, board_map)
                    board_map = create_new_tile(board_map)
                    print(board_map)
                if game_over(board_map):
                    print("Game Over!")
                    board_map = reset()

        # fill the screen with a color to wipe away anything from last frame
        # screen.fill(BG_COLOR)
        render_board(screen, board_map)
        pygame.display.set_caption(f"2048 Game - Max: {current_max_number(board_map)} Score: {calculate_score(board_map)} Level: {calculate_current_level(board_map)}")
        pygame.draw.rect(screen, (255, 0, 0), (50, 850, 200, 50))
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        text = font.render("Reset Game", True, (255, 255, 255))
        screen.blit(text, (60, 860))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if 50 <= mouse_pos[0] <= 250 and 850 <= mouse_pos[1] <= 900:
            pygame.draw.rect(screen, (200, 0, 0), (50, 850, 200, 50))
            screen.blit(text, (60, 860))
            if mouse_click[0] == 1:
                board_map = reset()
        
        
        fonty = pygame.font.Font(None, 24)
        texty = fonty.render(f"Historic Max: {HISTORIC_MAX}", True, (0, 0, 0))
        screen.blit(texty, (300, 865))
        
        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()