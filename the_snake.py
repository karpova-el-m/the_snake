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

# Настройка игрового окна.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pg.display.set_caption('Змейка')

# Настройка времени.
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

    def draw(self, position):
        """Принимает координаты и цвет, рисует клетку"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # "Код же ниже идеален был для орисовки одной конкретной клетки.
        # То есть создаем еще один метод в базовом классе по отрисовке клетки.
        # По сути контрл ц контрл в сделать."
        # Тут не очень поняла - в случае яблока мы используем
        # этот метод 1 в 1 - рисуем одну клетку.
        # В случае змеи - тоже 1 клетку, сначала центральную позицию,
        # а потом каждый цикл новую голову. То есть мы не рисуем всю змею
        # целиком ни в одном из циклов. И отдельно в методе draw
        # в классе Snake мы прописываем как стирать хвост.


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

    def randomize_position(self):
        """Возвращаются случайные координаты клетки"""
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )
    # Не могу понять, как реализовать комментарий:
    # В конструктор класса передать объект змейки,
    # чтобы получить координаты змеи, и учесть попадание яблока на змею.


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
        self.last = None
        self.direction = RIGHT

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
        mod_width = head_position[0] % (SCREEN_WIDTH + GRID_SIZE)
        mod_height = head_position[1] % (SCREEN_HEIGHT + GRID_SIZE)
        head_1 = mod_width + self.direction[0] * GRID_SIZE
        head_2 = mod_height + self.direction[1] * GRID_SIZE
        self.positions.insert(0, (head_1, head_2))
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисует "голову", затирает "хвост"."""
        super().draw(self.get_head_position())
        last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [self.position]


def handle_keys(game_object):
    """Функция обработки действий пользователя при нажатии клавиш"""
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    if keys[pg.K_UP] and game_object.direction != DOWN:
        return Snake.update_direction(game_object, UP)
    elif keys[pg.K_DOWN] and game_object.direction != UP:
        return Snake.update_direction(game_object, DOWN)
    elif keys[pg.K_LEFT] and game_object.direction != RIGHT:
        return Snake.update_direction(game_object, LEFT)
    elif keys[pg.K_RIGHT] and game_object.direction != LEFT:
        return Snake.update_direction(game_object, RIGHT)


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
        apple.draw(apple.position)
        snake.move()
        snake.draw()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
        pg.display.update()


if __name__ == '__main__':
    main()
