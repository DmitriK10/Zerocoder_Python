import pygame
import sys
import random
from abc import ABC, abstractmethod

class GameObject(ABC):
    """
    Абстрактный базовый класс для всех игровых объектов.
    """
    def __init__(self, x, y, width, height, color):
        # Прямоугольник для позиционирования и обнаружения столкновений
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  # Цвет объекта

    @abstractmethod
    def update(self):
        """Абстрактный метод для обновления состояния объекта"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Абстрактный метод для отрисовки объекта"""
        pass

    def get_rect(self):
        """Возвращает прямоугольник объекта для обработки коллизий"""
        return self.rect

class Paddle(GameObject):
    """
    Класс ракетки.
    """

    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color)
        self.speed = speed                              # Скорость движения ракетки
        self.score = 0                                  # Счет игрока

    def update(self):
        """Обновление состояния ракетки. Ограничивает движение в пределах экрана."""
        if self.rect.top < 0:
            self.rect.top = 0                           # Не даем ракетке выйти за верхнюю границу
        if self.rect.bottom > 600:
            self.rect.bottom = 600                      # Не даем ракетке выйти за нижнюю границу

    def draw(self, screen):
        """Отрисовка ракетки на экране"""
        pygame.draw.rect(screen, self.color, self.rect)

class Ball(GameObject):
    """
    Класс мяча, отвечает за движение мяча, обработку столкновений с границами и ракетками.
    """

    def __init__(self, x, y, radius, color, speed):
        super().__init__(x, y, radius * 2, radius * 2, color)
        self.radius = radius                            # Радиус мяча
        self.speed = speed                              # Скорость мяча
        # Начальное направление движения (случайное)
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        """Обновление позиции мяча и обработка отскоков от границ"""
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        # Отскок от верхней и нижней границ
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction[1] = abs(self.direction[1])   # Двигаем вниз
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.direction[1] = -abs(self.direction[1])  # Двигаем вверх

    def draw(self, screen):
        """Отрисовка мяча на экране"""
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def reset(self):
        """Сброс мяча в центр поля со случайным направлением"""
        self.rect.center = (400, 300)
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

class GameSettings(ABC):
    """
    Абстрактный класс для управления настройками игры.
    """

    @abstractmethod
    def get_background_color(self):
        pass

    @abstractmethod
    def get_paddle_color(self):
        pass

    @abstractmethod
    def get_ball_color(self):
        pass

    @abstractmethod
    def get_text_color(self):
        pass

    @abstractmethod
    def get_line_color(self):
        pass

    @abstractmethod
    def get_ball_speed(self):
        pass

    @abstractmethod
    def get_paddle_speed(self):
        pass

    @abstractmethod
    def get_max_score(self):
        pass

class DefaultGameSettings(GameSettings):
    """
    Реализация настроек игры
    """
    def __init__(self):
        # Цвета игровых элементов
        self.background_color = (0, 0, 0)               # Черный фон
        self.paddle_color = (255, 255, 255)             # Белые ракетки
        self.ball_color = (255, 0, 0)                   # Красный мяч
        self.text_color = (255, 255, 255)               # Белый текст
        self.line_color = (128, 128, 128)               # Серая центральная линия

        # Скорости игровых элементов
        self.ball_speed = 3
        self.paddle_speed = 6

        # Настройки игры
        self.max_score = 5                              # Игра до 5 очков

    def get_background_color(self):
        return self.background_color

    def get_paddle_color(self):
        return self.paddle_color

    def get_ball_color(self):
        return self.ball_color

    def get_text_color(self):
        return self.text_color

    def get_line_color(self):
        return self.line_color

    def get_ball_speed(self):
        return self.ball_speed

    def get_paddle_speed(self):
        return self.paddle_speed

    def get_max_score(self):
        return self.max_score

class ScoreManager(ABC):
    """
    Абстрактный класс для управления счетом игры.
    """

    @abstractmethod
    def update(self, player):
        pass

    @abstractmethod
    def is_game_over(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class DefaultScoreManager(ScoreManager):
    """
    Реализация управления счетом.
    """

    def __init__(self, text_color, max_score):
        self.font = pygame.font.Font(None, 36)      # Шрифт для отображения счета
        self.scores = [0, 0]                                   # Счет игроков [левый игрок, правый игрок]
        self.text_color = text_color
        self.max_score = max_score

    def update(self, player):
        """Увеличение счета указанного игрока"""
        self.scores[player] += 1

    def is_game_over(self):
        """Проверка, достиг ли какой-либо игрок максимального счета"""
        return self.scores[0] >= self.max_score or self.scores[1] >= self.max_score

    def get_winner(self):
        """Определение победителя игры"""
        if self.scores[0] >= self.max_score:
            return 0                                            # Левый игрок победил
        elif self.scores[1] >= self.max_score:
            return 1                                            # Правый игрок победил
        return -1                                               # Игра еще не окончена

    def draw(self, screen):
        """Отрисовка счета на экране"""
        score_text = f"{self.scores[0]} : {self.scores[1]}"
        score_render = self.font.render(score_text, True, self.text_color)
        screen.blit(score_render, (400 - score_render.get_width() // 2, 20))

        goal_text = f"Игра до {self.max_score} очков"
        goal_render = self.font.render(goal_text, True, self.text_color)
        screen.blit(goal_render, (400 - goal_render.get_width() // 2, 60))

class InputHandler(ABC):
    """
    Абстрактный класс для обработки ввода данных.
    """

    @abstractmethod
    def handle_input(self, paddle):
        pass

class KeyboardInputHandler(InputHandler):
    """
    Реализация обработки ввода с клавиатуры.
    """

    def __init__(self, up_key, down_key):
        self.up_key = up_key                                    # Клавиша для движения вверх
        self.down_key = down_key                                # Клавиша для движения вниз

    def handle_input(self, paddle):
        """Обработка нажатий клавиш и движение ракетки"""
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            paddle.rect.y -= paddle.speed
        if keys[self.down_key]:
            paddle.rect.y += paddle.speed

class GameObjectFactory(ABC):
    """
    Абстрактный класс для фабрики игровых объектов.
    """

    @abstractmethod
    def create_paddle(self, x, y, width, height, speed, color):
        pass

    @abstractmethod
    def create_ball(self, x, y, radius, speed, color):
        pass

class DefaultGameObjectFactory(GameObjectFactory):
    """
    Реализация фабрики игровых объектов.
    """

    def create_paddle(self, x, y, width, height, speed, color):
        return Paddle(x, y, width, height, color, speed)

    def create_ball(self, x, y, radius, speed, color):
        return Ball(x, y, radius, color, speed)

class PongGame:
    """
    Основной класс игры, координирующий работу всех компонентов.
    """

    def __init__(self):
        # Инициализация pygame
        pygame.init()

        # Создание окна игры
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Пинг-Понг")
        self.clock = pygame.time.Clock()  # Для контроля FPS

        # Использование абстракций для настроек и фабрики
        self.settings = DefaultGameSettings()
        self.factory = DefaultGameObjectFactory()

        # Создание игровых объектов через фабрику
        self.player1 = self.factory.create_paddle(
            50, 250, 20, 100,
            self.settings.get_paddle_speed(),
            self.settings.get_paddle_color()
        )
        self.player2 = self.factory.create_paddle(
            730, 250, 20, 100,
            self.settings.get_paddle_speed(),
            self.settings.get_paddle_color()
        )
        self.ball = self.factory.create_ball(
            400, 300, 10,
            self.settings.get_ball_speed(),
            self.settings.get_ball_color()
        )

        # Использование абстракции для управления счетом
        self.score_manager = DefaultScoreManager(
            self.settings.get_text_color(),
            self.settings.get_max_score()
        )

        # Использование абстракции для обработки ввода
        self.input_handler1 = KeyboardInputHandler(pygame.K_w, pygame.K_s)
        self.input_handler2 = KeyboardInputHandler(pygame.K_UP, pygame.K_DOWN)

        # Состояние игры
        self.running = True                                 # Флаг продолжения игрового цикла
        self.game_over = False                              # Флаг окончания игры

    def run(self):
        """Запуск основного игрового цикла"""
        while self.running:
            self.handle_events()                            # Обработка событий

            if not self.game_over:
                self.handle_input()                         # Обработка ввода
                self.update()                               # Обновление состояния игры
                self.check_collisions()                     # Проверка столкновений
                self.check_game_over()                      # Проверка окончания игры

            self.render()                                   # Отрисовка игры
            self.clock.tick(60)                             # Ограничение до 60 FPS

        # Завершение работы
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Обработка событий pygame (закрытие окна, нажатия клавиш)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False                        # Завершаем игру при закрытии окна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()                     # Перезапуск игры по нажатию R

    def handle_input(self):
        """Обработка ввода для обоих игроков"""
        self.input_handler1.handle_input(self.player1)
        self.input_handler2.handle_input(self.player2)

    def update(self):
        """Обновление состояния всех игровых объектов"""
        self.player1.update()
        self.player2.update()
        self.ball.update()

    def check_collisions(self):
        """Проверка столкновений мяча с ракетками и границами поля"""
        # Проверка столкновения с левой ракеткой (player1)
        if self.ball.get_rect().colliderect(self.player1.get_rect()):
            # Корректируем позицию мяча, чтобы он не был внутри ракетки
            self.ball.rect.left = self.player1.rect.right
            self.ball.direction[0] = abs(self.ball.direction[0])  # Двигаем вправо
            # Немного изменяем угол отскока в зависимости от точки попадания
            hit_position = (self.ball.rect.centery - self.player1.rect.centery) / (self.player1.rect.height / 2)
            self.ball.direction[1] = hit_position * 0.7

        # Проверка столкновения с правой ракеткой (player2)
        if self.ball.get_rect().colliderect(self.player2.get_rect()):
            # Корректируем позицию мяча, чтобы он не был внутри ракетки
            self.ball.rect.right = self.player2.rect.left
            self.ball.direction[0] = -abs(self.ball.direction[0])  # Двигаем влево
            # Немного изменяем угол отскока в зависимости от точки попадания
            hit_position = (self.ball.rect.centery - self.player2.rect.centery) / (self.player2.rect.height / 2)
            self.ball.direction[1] = hit_position * 0.7

        # Проверка выхода мяча за границы (гол)
        if self.ball.rect.left <= 0:
            self.score_manager.update(1)                            # Очко правому игроку
            self.ball.reset()                                       # Сброс мяча
        elif self.ball.rect.right >= 800:
            self.score_manager.update(0)                            # Очко левому игроку
            self.ball.reset()                                       # Сброс мяча

    def check_game_over(self):
        """Проверка условий окончания игры"""
        if self.score_manager.is_game_over():
            self.game_over = True

    def restart_game(self):
        """Перезапуск игры после окончания"""
        # Сброс позиций объектов
        self.player1.rect.y = 250
        self.player2.rect.y = 250
        self.ball.reset()

        # Сброс счета
        self.score_manager.scores = [0, 0]

        # Сброс состояния игры
        self.game_over = False

    def render(self):
        """Отрисовка всех элементов игры на экране"""
        # Отрисовка фона
        self.screen.fill(self.settings.get_background_color())

        # Отрисовка центральной линии
        pygame.draw.aaline(self.screen, self.settings.get_line_color(), (400, 0), (400, 600))

        # Отрисовка игровых объектов
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen)

        # Отрисовка счета
        self.score_manager.draw(self.screen)

        # Отображение сообщения о конце игры
        if self.game_over:
            winner = self.score_manager.get_winner()
            message_font = pygame.font.Font(None, 72)

            winner_text = f"Игрок {winner + 1} победил!"
            text_render = message_font.render(winner_text, True, self.settings.get_text_color())
            self.screen.blit(text_render, (400 - text_render.get_width() // 2, 250))

            restart_text = "Нажмите R для рестарта"
            restart_render = message_font.render(restart_text, True, self.settings.get_text_color())
            self.screen.blit(restart_render, (400 - restart_render.get_width() // 2, 320))

        # Обновление экрана
        pygame.display.flip()

if __name__ == "__main__":
    """
    Создает экземпляр игры и запускает её.
    """
    game = PongGame()
    game.run()