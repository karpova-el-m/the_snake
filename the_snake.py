from random import randint

import pygame

""" Инициализация PyGame."""
pygame.init()

"""Константы для размеров поля и сетки."""
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL_POINT = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

"""Направления движения."""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""Цвет фона - черный."""
BOARD_BACKGROUND_COLOR = (0, 0, 0)

"""Цвет по умолчанию - серый."""
DEFAULT_COLOR = (100, 100, 100)

"""Цвет границы ячейки."""
BORDER_COLOR = (93, 216, 228)

"""Цвет яблока."""
APPLE_COLOR = (255, 0, 0)

"""Цвет змейки."""
SNAKE_COLOR = (0, 255, 0)

"""Скорость движения змейки."""
SPEED = 20

"""Настройка игрового окна."""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

"""Заголовок окна игрового поля."""
pygame.display.set_caption('Змейка')

"""Настройка времени."""
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов.
    Этот же класс содержит и заготовку метода
    ля отрисовки объекта на игровом поле.
    """

    def __init__(self):
        self.body_color = DEFAULT_COLOR
        self.position = CENTRAL_POINT

    def draw(self):
        """Абстрактный метод, который предназначен для переопределения
        в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко,
    его позицию (должно отображаться в случайных клетках игрового поля)
    и отрисовку.
    """

    def __init__(self):
        """Атрибуты яблока - цвет и позиция"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Определение позиции случайным образом"""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)
        return self.position

    def draw(self):
        """Отрисовка яблока в случайной клетке"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    Обрабатывает действия при достижении границ экрана,
    а также при столкновении с собой.
    """

    def __init__(self):
        """Артибуты змеи - длина, скорость, цвет, начальная позиция,
        направление движения
        """
        self.length = 1
        self.snake_speed = SPEED
        self.body_color = SNAKE_COLOR
        self.position = CENTRAL_POINT
        self.positions = []
        self.positions.append(self.position)
        self.last = None
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Метод возвращает координаты "головы" змеи"""
        get_head_position = self.positions[0]
        return get_head_position

    def update_direction(self):
        """Метод обновляет направление движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент, если длина змейки не увеличилась.
        Применяется обработка краёв экрана
        и проверка на столкновение с собой.
        """
        get_head_position = Snake.get_head_position(self)
        head_1 = get_head_position[0] + self.direction[0] * GRID_SIZE
        head_2 = get_head_position[1] + self.direction[1] * GRID_SIZE
        if head_1 > SCREEN_WIDTH:
            head_1 = 0
        elif head_1 < 0:
            head_1 = SCREEN_WIDTH
        elif head_2 < 0:
            head_2 = SCREEN_HEIGHT
        elif head_2 > SCREEN_HEIGHT:
            head_2 = 0
        self.positions.insert(0, (head_1, head_2))
        Snake.draw(self)
        if self.positions[0] in self.positions[1:]:
            self.reset()
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)

    def draw(self):
        """Закомментированный код - был в прекоде,
        но на самом деле не нужен.
        """
        # for position in self.positions[:-1]:
        #     rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
        #     pygame.draw.rect(screen, self.body_color, rect)
        #     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = self.positions[-1]

    def reset(self):
        """Метод отвечает за сброс змейки в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions.clear()
        self.positions.append(self.position)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя при нажатии клавиш"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and game_object.direction != DOWN:
        game_object.next_direction = UP
    if keys[pygame.K_DOWN] and game_object.direction != UP:
        game_object.next_direction = DOWN
    if keys[pygame.K_LEFT] and game_object.direction != RIGHT:
        game_object.next_direction = LEFT
    if keys[pygame.K_RIGHT] and game_object.direction != LEFT:
        game_object.next_direction = RIGHT


def main():
    """Экземпляры классов."""
    apple = Apple()
    snake = Snake()
    """Переменная для бесконечного цикла while."""
    running = True

    while running:
        """Основная логика игры.
        Переменной running присваивается значение False при выходе из игры,
        в этом случае цикл while завершается.
        Вызывается функция обработки действий пользователя.
        Методы обновления направления движения змейки,
        отрисовки яблока и движения змейки.
        Проверка на "съедание" яблока.
        Обновление экрана после каждого цикла."""
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()
