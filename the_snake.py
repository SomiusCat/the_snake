from random import choice, randint

import pygame as pg

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
allowed_directions = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


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
        """Заготовка для отрисовки фигур на игровом поле"""
        raise NotImplementedError(
            f'Метод не переопределен в классе {self.__class__.__name__}')

    def draw_rect(self, position: tuple[int, int]):
        """Отрисовка квадрата на указанной поверхности"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Класс для представления Яблока
    Наследует от GameObject
    """

    def __init__(
        self,
        body_color: tuple[int, int, int] = APPLE_COLOR,
        occupied_positions: list[tuple[int, int]] | None = None,
    ):
        """
        Инициализирует Яблоко c заданным цветом
        и случайным расположением на игровом поле
        """
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(
        self,
        occupied_positions: list[tuple[int, int]] | None
    ):
        """Случайная позиция Яблока на игровом поле"""
        if occupied_positions is None:
            occupied_positions = []
        while self.position in occupied_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка Яблока на игровом поле"""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс для представления Змеи. Наследует от GameObject"""

    def __init__(
        self,
        body_color: tuple[int, int, int] = SNAKE_COLOR,
    ):
        """
        Инициализирует Змею c заданным цветом,
        начальным состоянием и направлением вправо
        """
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def reset(self):
        """Возвращение Змеи в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.last = None
        directions = [UP, DOWN, LEFT, RIGHT]
        self.direction = choice(directions)

    def get_head_position(self):
        """Возвращает голову Змеи"""
        return self.positions[0]

    def move(self):
        """Движение Змеи"""
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + self.direction[0]
                     * GRID_SIZE + SCREEN_WIDTH) % SCREEN_WIDTH,
                    (head_y + self.direction[1]
                     * GRID_SIZE + SCREEN_HEIGHT) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def draw(self):
        """Отрисовка Змеи на игровом поле"""
        for position in self.positions:
            if self.last is None or self.last != position:
                self.draw_rect(position)

    def update_direction(self, next_direction: tuple[int, int]):
        """Метод обновления направления после нажатия на кнопку"""
        self.direction = next_direction


def handle_keys(game_object: Snake):
    """Обработка действий пользователя"""
    next_direction: tuple[int, int] = game_object.direction
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            direction_key = (event.key, game_object.direction)
            if direction_key in allowed_directions:
                next_direction = allowed_directions[direction_key]
    game_object.update_direction(next_direction)


def main():
    """Инициализация PyGame"""
    pg.init()
    # Cоздаются экземпляры классов
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    #  Основная логика игры
    while True:
        handle_keys(game_object=snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.move()
        apple.draw()
        snake.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
