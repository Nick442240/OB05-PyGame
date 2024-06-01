import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Standoff 2 Like Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self, keys, controls):
        if keys[controls['left']] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[controls['right']] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[controls['up']] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[controls['down']] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


def main():
    running = True
    game_started = False

    player1 = Player(WIDTH // 4, HEIGHT // 2, RED)
    player2 = Player(3 * WIDTH // 4, HEIGHT // 2, BLUE)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)

    player1_controls = {
        'left': pygame.K_a,
        'right': pygame.K_d,
        'up': pygame.K_w,
        'down': pygame.K_s
    }

    player2_controls = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN
    }

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_started:
                    game_started = True

        if game_started:
            keys = pygame.key.get_pressed()
            player1.update(keys, player1_controls)
            player2.update(keys, player2_controls)

            # Drawing code
            screen.fill(BLACK)
            all_sprites.draw(screen)
        else:
            screen.fill(BLACK)
            font = pygame.font.Font(None, 74)
            text = font.render("Press SPACE to Start", True, WHITE)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
