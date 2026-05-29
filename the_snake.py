from random import choice, randint

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(
        self,
        body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
    ):
        """Инициализирует базовый игровой объект"""
        self.position = (GRID_WIDTH // 2 * GRID_SIZE,
                         GRID_HEIGHT // 2 * GRID_SIZE)
        self.body_color = body_color

    def draw(self):
        """Заготовка для отрисовки фигур на игрвоом поле"""
        pass


class Apple(GameObject):
    """
    Класс для представления Яблока
    Наследует от GameObject
    """

    def __init__(self):
        """
        Инициализирует Яблоко ч заданным цветом
        и случайным расположением на игровом поле
        """
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайная позиция Яблока на игровом поле"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка Яблока на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления Змеи. Наследует от GameObject"""

    def __init__(self):
        """
        Инициализирует Змею с заданным цветом,
        начальным состоянием и направлением вправо
        """
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def reset(self):
        """Возвращение Змеи в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.next_direction = None
        self.last = None
        directions = [UP, DOWN, LEFT, RIGHT]
        self.direction = choice(directions)

    def get_head_position(self):
        """Возвращает голову Змеи"""
        return self.positions[0]

    def move(self):
        """Движение Змеи"""
        head = self.get_head_position()
        new_head = ((head[0] + self.direction[0]
                     * GRID_SIZE + SCREEN_WIDTH) % SCREEN_WIDTH,
                    (head[1] + self.direction[1]
                     * GRID_SIZE + SCREEN_HEIGHT) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка Змеи на игровом поле"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object: Snake):
    """Обработка действий пользователя"""
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


def main():
    """Инициализация PyGame"""
    pygame.init()
    # Cоздаются экземпляры классов
    apple = Apple()
    snake = Snake()

    #  Основная логика игры
    while True:
        clock.tick(SPEED)
        handle_keys(game_object=snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        snake.update_direction()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()
        snake.move()
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()
