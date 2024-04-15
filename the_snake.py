from random import randint

import pygame as pg

# Инициализация PyGame.
pg.init()

# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL_POINT = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения.
UP = 0, -1
DOWN = 0, 1
LEFT = -1, 0
RIGHT = 1, 0

# Цвет фона - светло-серый.
BOARD_BACKGROUND_COLOR = (150, 150, 150)

# Цвет по умолчанию - серый.
DEFAULT_COLOR = (100, 100, 100)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 20

# Настройка игрового окна.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна игрового поля.
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
        super().__init__(APPLE_COLOR, Apple.randomize_position(self))

    def randomize_position(self):
        """Возвращаются случайные координаты клетки"""
        return (randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE)
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
        self.length = 1
        self.positions = [self.position]
        self.last = self.positions[-1]
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты "головы" змеи"""
        return self.positions[0]
        # Функция бесплолезная, но тесты без нее не проходят

    def update_direction(self):
        """Метод обновляет направление движения"""
        self.direction = handle_keys(self)
        # Можно без функции, но тесты без нее не проходят

    def move(self):
        """
        Обновляет голову змейки.
        Добавляя новую голову в начало списка positions.
        Удаляет последний элемент, если длина змейки не увеличилась.
        """
        get_head_position = Snake.get_head_position(self)
        mod_width = get_head_position[0] % (SCREEN_WIDTH + GRID_SIZE)
        mod_height = get_head_position[1] % (SCREEN_HEIGHT + GRID_SIZE)
        head_1 = mod_width + self.direction[0] * GRID_SIZE
        head_2 = mod_height + self.direction[1] * GRID_SIZE
        self.positions.insert(0, (head_1, head_2))
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисует "голову", затирает "хвост"."""
        super().draw(Snake.get_head_position(self))
        last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions.clear()
        self.positions.append(self.position)
        # По тестам этот метод должен быть в классе Snake


def handle_keys(game_object):
    """Функция обработки действий пользователя при нажатии клавиш"""
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    if keys[pg.K_UP] and game_object.direction != DOWN:
        return UP
    elif keys[pg.K_DOWN] and game_object.direction != UP:
        return DOWN
    elif keys[pg.K_LEFT] and game_object.direction != RIGHT:
        return LEFT
    elif keys[pg.K_RIGHT] and game_object.direction != LEFT:
        return RIGHT
    else:
        return game_object.direction


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
    # Экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        apple.draw(apple.position)
        snake.move()
        snake.draw()
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
            apple.draw(apple.position)
        pg.display.update()


if __name__ == '__main__':
    main()
