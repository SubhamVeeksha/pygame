import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 10, 10  # Grid size
CELL_SIZE = WIDTH // COLS  # Cell dimensions

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Player
GREEN = (0, 255, 0)  # Goal
RED = (255, 0, 0)  # Mines
LIGHT_RED = (255, 102, 102)  # High danger
ORANGE = (255, 165, 0)  # Medium danger
YELLOW = (255, 255, 0)  # Low danger
GRAY = (200, 200, 200)  # Grid

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minefield Game with Prediction")

# Generate random mine positions
num_mines = 15
def generate_mines():
    mines = set()
    while len(mines) < num_mines:
        mine = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if mine != (0, 0) and mine != (ROWS - 1, COLS - 1):  # Avoid start & goal
            mines.add(mine)
    return mines

mines = generate_mines()

# Player starting position
player_x, player_y = 0, 0

# Goal position
goal_x, goal_y = ROWS - 1, COLS - 1

# Game state
game_over = False

# Font setup
font = pygame.font.Font(None, 36)

# Function to count nearby mines
def count_nearby_mines(x, y):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx, dy) != (0, 0):  # Exclude the player's tile
                if (x + dx, y + dy) in mines:
                    count += 1
    return count

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            if event.key == pygame.K_RIGHT and player_x < COLS - 1:
                player_x += 1
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            if event.key == pygame.K_DOWN and player_y < ROWS - 1:
                player_y += 1

            # Check for mine
            if (player_x, player_y) in mines:
                game_over = True

            # Check for goal
            if (player_x, player_y) == (goal_x, goal_y):
                game_over = "win"

        # Restart game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player_x, player_y = 0, 0
            game_over = False
            mines = generate_mines()

    # Draw grid with mine predictions
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Set danger level based on nearby mines
            nearby_mines = count_nearby_mines(col, row)
            if nearby_mines >= 3:
                pygame.draw.rect(screen, LIGHT_RED, rect)  # High danger
            elif nearby_mines == 2:
                pygame.draw.rect(screen, ORANGE, rect)  # Medium danger
            elif nearby_mines == 1:
                pygame.draw.rect(screen, YELLOW, rect)  # Low danger
            else:
                pygame.draw.rect(screen, WHITE, rect)  # No nearby mines

            pygame.draw.rect(screen, GRAY, rect, 1)  # Draw grid border

            # Draw mines if game over
            if game_over and (col, row) in mines:
                pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Draw goal
    pygame.draw.rect(screen, GREEN, (goal_x * CELL_SIZE, goal_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Display Game Over message
    if game_over == True:
        text = font.render("💣 BOOM! You hit a mine!", True, RED)
        screen.blit(text, (WIDTH // 6, HEIGHT // 2))
        restart_text = font.render("Press 'R' to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 4, HEIGHT // 2 + 40))
    elif game_over == "win":
        text = font.render("🎉 You Win! 🎉", True, GREEN)
        screen.blit(text, (WIDTH // 3, HEIGHT // 2))
        restart_text = font.render("Press 'R' to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 4, HEIGHT // 2 + 40))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
