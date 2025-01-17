from random import randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL_POINT = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = 0, -1
DOWN = 0, 1
LEFT = -1, 0
RIGHT = 1, 0

BOARD_BACKGROUND_COLOR = (150, 150, 150)
DEFAULT_COLOR = (100, 100, 100)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс.
    ...
    Атрибуты
    --------
    body_color : tuple
        цвет объекта
    position : tuple
        позиция на экране
    Методы
    ------
    __init__
    draw
    """

    def __init__(self, body_color=DEFAULT_COLOR, position=CENTRAL_POINT):
        """Конструктор класса - присваивает цвет и позицию"""
        self.body_color = body_color
        self.position = position

    def draw(self):
        """
        Метод, который предназначен для переопределения
        в наследуемых классах
        """
        raise NotImplementedError(
            f'Необходимо определить метод в классе {self.__class__.__name__}.')

    def draw_square(self):
        """Принимает координаты и цвет, рисует клетку"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """
    Наследуемый класс.
    ...
    Атрибуты
    --------
    body_color : tuple
        цвет объекта
    position : tuple
        позиция на экране
    Методы
    ------
    __init__
    randomize_position
    """

    def __init__(self):
        """Доступ к родительскому функционалу конструктора"""
        super().__init__(APPLE_COLOR, self.randomize_position())

    def draw(self):
        """Принимает координаты и цвет, рисует яблоко"""
        super().draw_square()

    def randomize_position(self):
        """Возвращаются случайные координаты клетки"""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """
    Наследуемый класс.
    ...
    Атрибуты
    --------
    body_color : tuple
        цвет объекта
    position : tuple
        позиция на экране
    length : int
        длина змейки
    positions : list of tuples
        позиции всех элементов змейки
    last : tuple
        последний элемент змейки
    direction : tuple
        направление движения
    Методы
    ------
    __init__
    get_head_position
    update_direction
    move
    draw
    reset
    """

    def __init__(self):
        """
        Доступ к родительскому функционалу конструктора
        и присвоение собственных атрибутов.
        """
        super().__init__(SNAKE_COLOR, CENTRAL_POINT)
        self.reset()

    def get_head_position(self):
        """Возвращает координаты "головы" змеи"""
        return self.positions[0]

    def update_direction(self, direction):
        """Метод обновляет направление движения"""
        self.direction = direction

    def move(self):
        """
        Обновляет голову змейки.
        Добавляя новую голову в начало списка positions.
        Удаляет последний элемент, если длина змейки не увеличилась.
        """
        head_position = self.get_head_position()
        new_head = (
            head_position[0] % (SCREEN_WIDTH + GRID_SIZE)
            + self.direction[0] * GRID_SIZE,
            head_position[1] % (SCREEN_HEIGHT + GRID_SIZE)
            + self.direction[1] * GRID_SIZE
        )
        self.positions.insert(0, (new_head))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Рисует "голову", затирает "хвост"."""
        self.position = self.get_head_position()
        super().draw_square()
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT


def handle_keys(game_object):
    """Функция обработки действий пользователя при нажатии клавиш"""
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    if keys[pg.K_UP] and game_object.direction != DOWN:
        return game_object.update_direction(UP)
    elif keys[pg.K_DOWN] and game_object.direction != UP:
        return game_object.update_direction(DOWN)
    elif keys[pg.K_LEFT] and game_object.direction != RIGHT:
        return game_object.update_direction(LEFT)
    elif keys[pg.K_RIGHT] and game_object.direction != LEFT:
        return game_object.update_direction(RIGHT)


def main():
    """
    Основная логика игры.
    Вызывается функция обработки действий пользователя.
    Вызывается функция обновления направления движения змейки,
    Отрисовки яблока и движения змейки.
    Проверка на "съедание" яблока.
    Проверка на столкновение змейки с собой.
    Обновление экрана после каждого цикла.
    """
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.positions[0] == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
