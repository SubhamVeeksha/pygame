import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catching the Egg Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Load images
try:
    basket_img = pygame.image.load("basket.png")
    egg_img = pygame.image.load("egg.png")
    hen_img = pygame.image.load("hen.png")

    # Resize images
    basket_img = pygame.transform.scale(basket_img, (80, 50))
    egg_img = pygame.transform.scale(egg_img, (30, 40))
    hen_img = pygame.transform.scale(hen_img, (60, 60))
except pygame.error as e:
    print(f"Error loading images: {e}")
    exit()

# Basket class
class Basket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 8

    def move(self, direction):
        if direction == "LEFT" and self.x > 0:
            self.x -= self.speed
        if direction == "RIGHT" and self.x < WIDTH - 80:
            self.x += self.speed

    def draw(self):
        screen.blit(basket_img, (self.x, self.y))

# Egg class
class Egg:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = 70
        self.speed = random.randint(3, 6)

    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(egg_img, (self.x, self.y))

# Game variables
basket = Basket()
eggs = []
hens = [(50, 20), (250, 20), (450, 20)]  # Hen positions
score = 0
lives = 3
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw hens
    for hx, hy in hens:
        screen.blit(hen_img, (hx, hy))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move basket with keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket.move("LEFT")
    if keys[pygame.K_RIGHT]:
        basket.move("RIGHT")

    # Spawn eggs randomly
    if random.randint(1, 100) > 98:
        eggs.append(Egg())

    # Move and draw eggs
    for egg in eggs[:]:
        egg.fall()
        egg.draw()

        # Check if egg is caught
        if basket.x < egg.x < basket.x + 80 and basket.y < egg.y < basket.y + 40:
            eggs.remove(egg)
            score += 1

        # Check if egg is missed
        elif egg.y > HEIGHT:
            eggs.remove(egg)
            lives -= 1

    # Draw basket
    basket.draw()

    # Display score & lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    # Game over condition
    if lives <= 0:
        screen.fill(WHITE)
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()

        # Wait for restart
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    restart = True
                    score = 0
                    lives = 3
                    eggs.clear()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
