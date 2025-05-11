import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
HEIGHT = WIDTH + 50
BACKGROUND_COLOR = (187, 173, 160)
FONT = pygame.font.Font(None, 40)

# Colors for tiles
COLORS = {
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
    2048: (237, 194, 46),
}

# Initialize game variables
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0

def draw_grid(screen):
    """Draw the 2048 grid."""
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, 
                             (MARGIN + col * (TILE_SIZE + MARGIN),
                              MARGIN + row * (TILE_SIZE + MARGIN),
                              TILE_SIZE, TILE_SIZE), border_radius=8)
            if value > 0:
                text = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(
                    MARGIN + col * (TILE_SIZE + MARGIN) + TILE_SIZE // 2,
                    MARGIN + row * (TILE_SIZE + MARGIN) + TILE_SIZE // 2
                ))
                screen.blit(text, text_rect)
    
    # Draw score
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, WIDTH))

def add_new_tile():
    """Add a new tile (2 or 4) to a random empty spot."""
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4

def compress(grid):
    """Slide all numbers to the left."""
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE):
        position = 0
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                new_grid[row][position] = grid[row][col]
                position += 1
    return new_grid

def merge(grid):
    """Merge tiles of the same value."""
    global score
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 1):
            if grid[row][col] == grid[row][col + 1] and grid[row][col] != 0:
                grid[row][col] *= 2
                score += grid[row][col]
                grid[row][col + 1] = 0
    return grid

def move_left():
    """Move all tiles to the left and merge."""
    global grid
    grid = compress(grid)
    grid = merge(grid)
    grid = compress(grid)

def move_right():
    """Move all tiles to the right and merge."""
    global grid
    grid = [row[::-1] for row in grid]
    move_left()
    grid = [row[::-1] for row in grid]

def move_up():
    """Move all tiles up and merge."""
    global grid
    grid = list(map(list, zip(*grid)))
    move_left()
    grid = list(map(list, zip(*grid)))

def move_down():
    """Move all tiles down and merge."""
    global grid
    grid = list(map(list, zip(*grid)))
    move_right()
    grid = list(map(list, zip(*grid)))

def check_game_over():
    """Check if there are no more moves left."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True

# Initialize game
add_new_tile()
add_new_tile()

# Pygame loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            previous_grid = [row[:] for row in grid]
            if event.key == pygame.K_LEFT:
                move_left()
            elif event.key == pygame.K_RIGHT:
                move_right()
            elif event.key == pygame.K_UP:
                move_up()
            elif event.key == pygame.K_DOWN:
                move_down()

            if grid != previous_grid:
                add_new_tile()

            if check_game_over():
                running = False

pygame.quit()
