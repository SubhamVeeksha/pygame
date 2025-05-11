import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Duplication & Bouncing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Paddle settings
paddle_width, paddle_height = 100, 10
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 30
paddle_speed = 8

# Ball settings
ball_radius = 10
initial_ball = {
    "x": random.randint(50, WIDTH - 50),
    "y": 0,
    "dx": random.choice([-4, 4]),
    "dy": 4
}
balls = [initial_ball]  # List to hold multiple balls

# Game settings
lives = 3
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # Event handling
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Ball movement and collision
    new_balls = []  # List to store new duplicated balls
    for ball in balls[:]:  # Iterate over a copy of the ball list
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]

        # Ball collision with walls
        if ball["x"] <= 0 or ball["x"] >= WIDTH - ball_radius:
            ball["dx"] *= -1  # Reverse direction

        # Ball collision with paddle
        if paddle_y <= ball["y"] + ball_radius <= paddle_y + paddle_height and paddle_x <= ball["x"] <= paddle_x + paddle_width:
            ball["dy"] *= -1  # Bounce upward
            ball["dx"] = random.choice([-4, 4])  # Randomize horizontal movement
            score += 10  # Increase score

            # Create a new duplicate ball
            new_ball = {
                "x": ball["x"],
                "y": ball["y"] - 10,  # Start slightly above the paddle
                "dx": random.choice([-4, 4]),
                "dy": -4
            }
            new_balls.append(new_ball)

        # Ball falls below the screen (lose a life)
        if ball["y"] > HEIGHT:
            balls.remove(ball)
            lives -= 1

    # Add new balls to the list
    balls.extend(new_balls)

    # If no balls remain, reset game
    if not balls and lives > 0:
        balls.append({
            "x": random.randint(50, WIDTH - 50),
            "y": 0,
            "dx": random.choice([-4, 4]),
            "dy": 4
        })

    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Draw balls
    for ball in balls:
        pygame.draw.circle(screen, RED, (ball["x"], ball["y"]), ball_radius)

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))

    lives_text = font.render(f"Lives: {lives}", True, YELLOW)
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Check for Game Over
    if lives <= 0:
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    lives = 3
                    score = 0
                    balls = [initial_ball]  # Reset to one ball
                    game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
