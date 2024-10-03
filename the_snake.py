from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()
# поле 32х24 клетки


def handle_keys(game_object):
    """Function for choosing direction."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.
class GameObject:
    """Base class for defining other classes."""

    def __init__(self,
                 position: tuple[int, int] = (0, 0),
                 body_color: tuple[int, int, int] = APPLE_COLOR) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    """Apple class."""

    def __init__(self,
                 body_color: tuple[int, int, int] = APPLE_COLOR) -> None:
        """Initialize the apple."""
        self.randomize_position()
        super().__init__(self.position, body_color)

    def randomize_position(self) -> None:
        """Set random position of apple on the screen."""
        self.position = (randint(0, 31) * 20, randint(0, 23) * 20)

    def draw(self) -> None:
        """Vizualise an apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_pos(self) -> tuple:
        """Get the current position of apple"""
        return self.position


class Snake(GameObject):
    """Class for manipulate snake."""

    def __init__(self,
                 position: tuple[int, int] = (300, 220),
                 body_color: tuple[int, int, int] = SNAKE_COLOR) -> None:
        """Initialize the snake."""
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.speed = GRID_SIZE

    def update_direction(self) -> None:
        """Function, that setting direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> tuple:
        """Move the snake."""
        x = self.positions[0][0] + self.direction[0] * self.speed
        y = self.positions[0][1] + self.direction[1] * self.speed
        if x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        elif x > SCREEN_WIDTH:
            x = 0
        if y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        elif y > SCREEN_HEIGHT:
            y = 0
        self.positions.insert(0, (x, y))
        return self.positions.pop(-1)

    def draw(self) -> None:
        """Vizualise the snake."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self) -> tuple:
        """Getting the position of the head."""
        return self.positions[0]

    def reset(self) -> None:
        """Setting the snake to default/start condition."""
        if len(set(self.positions)) != len(self.positions):
            self.positions = [self.position]


def main():
    """
    Main function of the game.
    Contains game algorithm.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        last_part = snake.move()
        snake.reset()
        if snake.get_head_position() == apple.get_pos():
            apple.randomize_position()
            snake.positions.append(last_part)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
