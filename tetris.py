import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки игры
WIDTH, HEIGHT = 300, 600
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]]
]

SHAPE_COLORS = [RED, GREEN, BLUE, CYAN, YELLOW, MAGENTA, ORANGE]

# Класс для фигур
class Shape:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def draw(self, surface):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.color,
                                     (self.x * CELL_SIZE + j * CELL_SIZE, self.y * CELL_SIZE + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        original_shape = self.shape
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if check_collision(self, grid):
            self.shape = original_shape  # Откат поворота при коллизии

# Функция проверки коллизии
def check_collision(shape, grid):
    for i, row in enumerate(shape.shape):
        for j, cell in enumerate(row):
            if cell:
                if (shape.y + i >= ROWS or
                        shape.x + j < 0 or
                        shape.x + j >= COLS or
                        grid[shape.y + i][shape.x + j]):
                    return True
    return False

# Функция удаления полных линий
def remove_full_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    new_grid = [[0] * COLS for _ in range(ROWS - len(new_grid))] + new_grid
    return new_grid

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    global grid
    grid = [[0] * COLS for _ in range(ROWS)]
    current_shape = Shape(random.choice(SHAPES), random.choice(SHAPE_COLORS))
    next_shape = Shape(random.choice(SHAPES), random.choice(SHAPE_COLORS))
    fall_time = 0
    fall_speed = 500  # Время падения в миллисекундах

    running = True
    while running:
        screen.fill(BLACK)
        delta_time = clock.tick()
        fall_time += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_shape.move(-1, 0)
                    if check_collision(current_shape, grid):
                        current_shape.move(1, 0)
                if event.key == pygame.K_RIGHT:
                    current_shape.move(1, 0)
                    if check_collision(current_shape, grid):
                        current_shape.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    current_shape.move(0, 1)
                    if check_collision(current_shape, grid):
                        current_shape.move(0, -1)
                if event.key == pygame.K_UP:
                    current_shape.rotate()
                    if check_collision(current_shape, grid):
                        current_shape.rotate()
                        current_shape.rotate()
                        current_shape.rotate()

        if fall_time > fall_speed:
            fall_time = 0
            current_shape.move(0, 1)
            if check_collision(current_shape, grid):
                current_shape.move(0, -1)
                for i, row in enumerate(current_shape.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            grid[current_shape.y + i][current_shape.x + j] = current_shape.color
                current_shape = next_shape
                next_shape = Shape(random.choice(SHAPES), random.choice(SHAPE_COLORS))
                if check_collision(current_shape, grid):
                    running = False  # Игра окончена

        grid = remove_full_lines(grid)

        # Отрисовка сетки и фигур
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        current_shape.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
