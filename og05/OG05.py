import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы для настроек игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_WIDTH = 80
TARGET_HEIGHT = 80

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Тир")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Случайный цвет фона
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Позиция цели
target_x = random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
target_y = random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)

# Счет
score = 0
font = pygame.font.SysFont(None, 36)

# Игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Проверка попадания по цели
            if (target_x < mouse_x < target_x + TARGET_WIDTH and
                    target_y < mouse_y < target_y + TARGET_HEIGHT):
                # Увеличение счета
                score += 1

                # Перемещение цели в случайное место
                target_x = random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
                target_y = random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)

                # Смена цвета фона
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Отрисовка
    # Заливка фона
    screen.fill(color)

    # Отрисовка цели (круг с мишенью)
    pygame.draw.circle(screen, RED, (target_x + TARGET_WIDTH // 2, target_y + TARGET_HEIGHT // 2), TARGET_WIDTH // 2)
    pygame.draw.circle(screen, WHITE, (target_x + TARGET_WIDTH // 2, target_y + TARGET_HEIGHT // 2), TARGET_WIDTH // 3)
    pygame.draw.circle(screen, RED, (target_x + TARGET_WIDTH // 2, target_y + TARGET_HEIGHT // 2), TARGET_WIDTH // 6)

    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.update()

    # Ограничение FPS
    clock.tick(60)

# Завершение работы
pygame.quit()