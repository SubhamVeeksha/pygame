import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone (No Images)")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (135, 206, 250)
RED = (255, 0, 0)

# Game variables
bird_x, bird_y = 100, HEIGHT // 2
bird_radius = 20  # Bird is a circle
gravity = 0.5
velocity = 0
jump_strength = -8
pipes = []
pipe_width = 70
pipe_speed = 3
score = 0
game_over = False
clock = pygame.time.Clock()

# Pipe generator
def create_pipe():
    gap = 150
    top_height = random.randint(50, HEIGHT - gap - 50)
    bottom_y = top_height + gap
    return {"x": WIDTH, "top": top_height, "bottom": bottom_y}

# Add initial pipes
pipes.append(create_pipe())

# Game loop
running = True
while running:
    screen.fill(BLUE)  # Background color

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                velocity = jump_strength  # Jump effect

    if not game_over:
        # Bird movement
        velocity += gravity
        bird_y += velocity

        # Pipe movement
        for pipe in pipes:
            pipe["x"] -= pipe_speed

        # Remove off-screen pipes & add new pipes
        if pipes[0]["x"] < -pipe_width:
            pipes.pop(0)
            pipes.append(create_pipe())
            score += 1

        # Collision detection
        for pipe in pipes:
            if (bird_x < pipe["x"] + pipe_width and bird_x + bird_radius > pipe["x"] and
               (bird_y < pipe["top"] or bird_y + bird_radius > pipe["bottom"])):
                game_over = True

        if bird_y > HEIGHT or bird_y < 0:
            game_over = True  # Hit ground or top

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))  # Top pipe
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT - pipe["bottom"]))  # Bottom pipe

    # Draw bird
    pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

    # Display score
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game Over Screen
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 6, HEIGHT // 2))
        pygame.display.flip()

        # Restart option
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    restart = True
                    bird_y = HEIGHT // 2
                    velocity = 0
                    pipes.clear()
                    pipes.append(create_pipe())
                    score = 0
                    game_over = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
