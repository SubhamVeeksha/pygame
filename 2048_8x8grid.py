import pygame
import random
import time
import os
from collections import deque  

# Initialize Pygame
pygame.init()

# Game Constants
GRID_SIZE = 8  # Change to 4 for 4x4 mode
TILE_SIZE = 60  
MARGIN = 5  
WIDTH, HEIGHT = (GRID_SIZE * TILE_SIZE) + (MARGIN * (GRID_SIZE + 1)), (GRID_SIZE * TILE_SIZE) + (MARGIN * (GRID_SIZE + 1)) + 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 30)
TIMER_FONT = pygame.font.Font(None, 40)
SCORE_FONT = pygame.font.Font(None, 35)

# Tile Colors
TILE_COLORS = {
    0: (200, 200, 200),
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
    4096: (60, 58, 50),
    8192: (40, 40, 32),
    16384: (30, 30, 20)
}

# High Score File
HIGH_SCORE_FILE = "high_score.txt"

# Initialize Grid & Timer
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0
start_time = time.time()
undo_stack = deque(maxlen=5)
last_direction = None  

# Load high score from file
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(new_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_score))

high_score = load_high_score()

def get_highest_tile():
    """Returns the highest tile in the grid."""
    return max(max(row) for row in grid)

def get_new_tile_value():
    """Determines the new tile value based on the highest tile present."""
    highest_tile = get_highest_tile()
    
    if highest_tile >= 16384:
        return 4096
    elif highest_tile >= 8192:
        return 2048
    elif highest_tile >= 4096:
        return 1024
    elif highest_tile >= 2048:
        return 512
    elif highest_tile >= 1024:
        return 256
    elif highest_tile >= 512:
        return 128
    elif highest_tile >= 256:
        return 64
    elif highest_tile >= 128:
        return 32
    elif highest_tile >= 64:
        return 16
    elif highest_tile >= 32:
        return 8
    else:
        return 2 if random.random() < 0.9 else 4  # Default case

def add_new_tile():
    """Adds a new tile based on the highest tile in the grid."""
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = get_new_tile_value()

def draw_grid(screen):
    """Draws the grid, timer, and score."""
    screen.fill(WHITE)
    
    # Timer Display
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = TIMER_FONT.render(f"Time: {minutes:02}:{seconds:02}", True, BLACK)
    screen.blit(timer_text, (WIDTH // 2 - 100, 10))

    # Score Display
    score_text = SCORE_FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 10))

    # High Score Display
    high_score_text = SCORE_FONT.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (WIDTH - 200, 10))

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = grid[r][c]
            rect = pygame.Rect(c * (TILE_SIZE + MARGIN) + MARGIN, r * (TILE_SIZE + MARGIN) + MARGIN + 50, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, TILE_COLORS.get(value, (0, 0, 0)), rect, border_radius=10)
            if value:
                text = FONT.render(str(value), True, BLACK if value < 8 else WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    pygame.display.update()

def move_left():
    """Moves tiles left and merges if possible."""
    global grid, score, high_score
    moved = False
    new_grid = []
    
    for row in grid:
        new_row = [x for x in row if x != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                score += new_row[i]
                new_row[i + 1] = 0
        new_row = [x for x in new_row if x != 0]
        new_row.extend([0] * (GRID_SIZE - len(new_row)))
        new_grid.append(new_row)
    
    if new_grid != grid:
        undo_stack.append([row[:] for row in grid])
        grid = new_grid
        moved = True
    
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    
    return moved

def move_right():
    global grid
    grid = [row[::-1] for row in grid]
    moved = move_left()
    grid = [row[::-1] for row in grid]
    return moved

def move_up():
    global grid
    grid = list(map(list, zip(*grid)))  # Transpose
    moved = move_left()
    grid = list(map(list, zip(*grid)))  # Transpose back
    return moved

def move_down():
    global grid
    grid = list(map(list, zip(*grid)))  # Transpose
    grid = [row[::-1] for row in grid]
    moved = move_left()
    grid = [row[::-1] for row in grid]
    grid = list(map(list, zip(*grid)))  # Transpose back
    return moved

def handle_key(event):
    """Handles key presses for movement and undo."""
    global last_direction

    direction = None
    if event.key == pygame.K_LEFT:
        direction = "left"
        moved = move_left()
    elif event.key == pygame.K_RIGHT:
        direction = "right"
        moved = move_right()
    elif event.key == pygame.K_UP:
        direction = "up"
        moved = move_up()
    elif event.key == pygame.K_DOWN:
        direction = "down"
        moved = move_down()
    elif event.key == pygame.K_u and undo_stack:
        global grid
        grid = undo_stack.pop()  
        return  

    if moved and direction != last_direction:
        add_new_tile()  
        last_direction = direction  

def main():
    global start_time
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 - 8x8")

    add_new_tile()
    add_new_tile()
    start_time = time.time()

    running = True
    while running:
        draw_grid(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_key(event)

    pygame.quit()

if __name__ == "__main__":
    main()
