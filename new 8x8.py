import pygame
import random

# Initialize pygame
pygame.init()

# Game settings
GRID_SIZE = 8
TILE_SIZE = 80
MARGIN = 5
WIDTH, HEIGHT = GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN, GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200),
    6: (242, 177, 121), 8: (245, 149, 99), 16: (246, 124, 95),
    32: (246, 94, 59), 64: (237, 207, 114), 128: (237, 204, 97),
    256: (237, 200, 80), 512: (237, 197, 63), 1024: (237, 194, 46),
    2048: (237, 190, 29)
}
FONT = pygame.font.Font(None, 40)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - 8x8 Grid")

# Game board
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def draw_board():
    """Draws the game board."""
    screen.fill(BACKGROUND_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = board[row][col]
            color = TILE_COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, (col * (TILE_SIZE + MARGIN) + MARGIN,
                                             row * (TILE_SIZE + MARGIN) + MARGIN,
                                             TILE_SIZE, TILE_SIZE))
            if value > 0:
                text_surface = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(col * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2,
                                                           row * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

def add_new_tile():
    """Adds 2-3 new tiles in random empty positions."""
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if empty_tiles:
        for _ in range(random.randint(2, 3)):  # Spawn 2 or 3 tiles per move
            if empty_tiles:
                row, col = random.choice(empty_tiles)
                board[row][col] = random.choice([2, 4])
                empty_tiles.remove((row, col))

def compress_and_merge(row):
    """Compress row (left move logic) and merge more than two tiles at once."""
    new_row = [num for num in row if num != 0]  # Remove zeroes
    merged = []
    i = 0
    while i < len(new_row):
        if i < len(new_row) - 2 and new_row[i] == new_row[i+1] == new_row[i+2]:  
            merged.append(new_row[i] + new_row[i+1] + new_row[i+2])  # Merge three tiles
            i += 3
        elif i < len(new_row) - 1 and new_row[i] == new_row[i+1]:  
            merged.append(new_row[i] + new_row[i+1])  # Merge two tiles
            i += 2
        else:
            merged.append(new_row[i])
            i += 1
    return merged + [0] * (GRID_SIZE - len(merged))  # Fill remaining spaces with zeroes

def move_left():
    """Moves and merges the tiles to the left."""
    global board
    new_board = [compress_and_merge(row) for row in board]
    if new_board != board:
        board = new_board
        add_new_tile()

def move_right():
    """Moves and merges the tiles to the right."""
    global board
    new_board = [compress_and_merge(row[::-1])[::-1] for row in board]
    if new_board != board:
        board = new_board
        add_new_tile()

def move_up():
    """Moves and merges the tiles upwards."""
    global board
    transposed = list(map(list, zip(*board)))  # Transpose the board
    new_board = [compress_and_merge(row) for row in transposed]
    new_board = list(map(list, zip(*new_board)))  # Transpose back
    if new_board != board:
        board = new_board
        add_new_tile()

def move_down():
    """Moves and merges the tiles downwards."""
    global board
    transposed = list(map(list, zip(*board)))  # Transpose the board
    new_board = [compress_and_merge(row[::-1])[::-1] for row in transposed]
    new_board = list(map(list, zip(*new_board)))  # Transpose back
    if new_board != board:
        board = new_board
        add_new_tile()

def check_game_over():
    """Checks if the game is over (no possible moves left)."""
    for row in board:
        for i in range(GRID_SIZE - 1):
            if row[i] == 0 or row[i] == row[i+1]:
                return False
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 1):
            if board[row][col] == 0 or board[row][col] == board[row+1][col]:
                return False
    return True

def main():
    """Main game loop."""
    add_new_tile()
    running = True
    while running:
        draw_board()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left()
                elif event.key == pygame.K_RIGHT:
                    move_right()
                elif event.key == pygame.K_UP:
                    move_up()
                elif event.key == pygame.K_DOWN:
                    move_down()
                elif event.key == pygame.K_ESCAPE:
                    running = False

                if check_game_over():
                    print("Game Over!")
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()
