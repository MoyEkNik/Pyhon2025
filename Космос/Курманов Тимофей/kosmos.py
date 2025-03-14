import pygame
import random
import sys
import time
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Галактикс")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Загрузка изображений
try:
    background = pygame.image.load("background.jpg")
    rocket = pygame.image.load("rocket.png")
    meteor = pygame.image.load("meteor.png")
    human = pygame.image.load("human.png")
    enemy_ship = pygame.image.load("enemy_ship.png")  # Вражеский корабль
    boss_ship = pygame.image.load("boss_ship.png")  # Главный вражеский корабль
    tutorial_image = pygame.image.load("tutorial.png")  # Картинка для обучения
    arrow_image = pygame.image.load("arrow.png")  # Стрелочка для продолжения
    victory_image = pygame.image.load("victory.png")  # Ваша картинка после победы над боссом
except FileNotFoundError:
    print("Ошибка: Не удалось загрузить изображения")
    sys.exit()

# Масштабирование изображений
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
rocket = pygame.transform.scale(rocket, (50, 100))
meteor = pygame.transform.scale(meteor, (50, 50))
human = pygame.transform.scale(human, (50, 50))
enemy_ship = pygame.transform.scale(enemy_ship, (50, 50))
boss_ship = pygame.transform.scale(boss_ship, (300, 300))  # Босс теперь больше
tutorial_image = pygame.transform.scale(tutorial_image, (WIDTH, HEIGHT))
arrow_image = pygame.transform.scale(arrow_image, (50, 50))
victory_image = pygame.transform.scale(victory_image, (WIDTH, HEIGHT))

# Шрифты
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 48)
title_font = pygame.font.SysFont("Arial", 64, bold=True)

# Состояния игры
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3
LEVEL_SELECT = 4
SETTINGS = 5
BOSS_FIGHT = 6
TUTORIAL = 7  # Новое состояние для обучения
PAUSED = 8  # Новое состояние для паузы
BOSS_VICTORY = 9  # Новое состояние для победы над боссом
game_state = MENU

# Игровые переменные
class GameState:
    def __init__(self):
        self.rocket_rect = rocket.get_rect()
        self.rocket_rect.x = WIDTH // 2 - self.rocket_rect.width // 2
        self.rocket_rect.y = HEIGHT - self.rocket_rect.height - 10
        self.rocket_hp = 100
        self.saved_humans = 0
        self.meteors = []
        self.humans = []
        self.enemies = []
        self.boss_bullets = []
        self.screen_shake = 0
        self.red_flash_alpha = 0
        self.current_level = 1
        self.max_levels = 5
        self.level_start_time = 0
        self.boss_hp = 1000  # У босса теперь 1000 HP
        self.boss_rect = boss_ship.get_rect()
        self.boss_rect.x = WIDTH // 2 - self.boss_rect.width // 2
        self.boss_rect.y = 50
        self.boss_speed = 3  # Скорость движения босса
        self.boss_direction = 1  # Направление движения босса (1 - вправо, -1 - влево)
        self.dodged_boss_bullets = 0  # Счетчик уклонений от пуль босса
        self.bullets = []  # Пули игрока
        self.enemy_hp = {}  # HP вражеских кораблей
        self.enemy_bullets = []  # Пули вражеских кораблей
        self.enemies_killed = 0  # Счетчик уничтоженных врагов на уровне 3

game = GameState()

# Класс кнопки
class Button:
    def __init__(self, text, x, y, w, h, color, h_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.h_color = h_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.h_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# Функции игры
def reset_game():
    game.rocket_rect.x = WIDTH // 2 - game.rocket_rect.width // 2
    game.rocket_rect.y = HEIGHT - game.rocket_rect.height - 10
    game.rocket_hp = 100
    game.saved_humans = 0
    game.meteors.clear()
    game.humans.clear()
    game.enemies.clear()
    game.boss_bullets.clear()
    game.screen_shake = 0
    game.red_flash_alpha = 0
    game.level_start_time = time.time()
    game.dodged_boss_bullets = 0
    game.bullets.clear()
    game.enemy_hp.clear()
    game.enemy_bullets.clear()
    game.enemies_killed = 0
    game.boss_rect.x = WIDTH // 2 - game.boss_rect.width // 2
    game.boss_rect.y = 50
    game.boss_hp = 1000

def create_meteor():
    meteor_rect = meteor.get_rect()
    meteor_rect.x = random.randint(0, WIDTH - meteor_rect.width)
    meteor_rect.y = -meteor_rect.height
    game.meteors.append(meteor_rect)

def create_human():
    human_rect = human.get_rect()
    human_rect.x = random.randint(0, WIDTH - human_rect.width)
    human_rect.y = -human_rect.height
    game.humans.append(human_rect)

def create_enemy():
    enemy_rect = enemy_ship.get_rect()
    enemy_rect.x = random.randint(0, WIDTH - enemy_rect.width)
    enemy_rect.y = -enemy_rect.height
    game.enemies.append(enemy_rect)
    game.enemy_hp[id(enemy_rect)] = 80  # У вражеских кораблей 80 HP

def create_boss_bullet():
    bullet_rect = pygame.Rect(0, 0, 10, 20)
    bullet_rect.x = game.boss_rect.x + game.boss_rect.width // 2 - 5
    bullet_rect.y = game.boss_rect.y + game.boss_rect.height
    game.boss_bullets.append(bullet_rect)

def create_bullet():
    bullet_rect = pygame.Rect(0, 0, 5, 10)
    bullet_rect.x = game.rocket_rect.x + game.rocket_rect.width // 2 - 2
    bullet_rect.y = game.rocket_rect.y
    game.bullets.append(bullet_rect)

def create_enemy_bullet(enemy_rect):
    bullet_rect = pygame.Rect(0, 0, 5, 10)
    bullet_rect.x = enemy_rect.x + enemy_rect.width // 2 - 2
    bullet_rect.y = enemy_rect.y + enemy_rect.height
    game.enemy_bullets.append(bullet_rect)

# Эффекты
def screen_shake_effect():
    if game.screen_shake > 0:
        game.screen_shake -= 1
        return random.randint(-5, 5), random.randint(-5, 5)
    return 0, 0

def red_flash_effect():
    if game.rocket_hp <= 15:
        game.red_flash_alpha = int((math.sin(pygame.time.get_ticks() / 200) + 1) * 50)
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.fill(RED)
        flash.set_alpha(game.red_flash_alpha)
        return flash
    return None

# Отрисовка интерфейсов
def draw_menu():
    screen.blit(background, (0, 0))
    title = title_font.render("Галактикс", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    start_btn.draw(screen)
    settings_btn.draw(screen)
    exit_btn.draw(screen)

def draw_settings():
    screen.blit(background, (0, 0))
    title = large_font.render("Настройки", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)

    reset_progress_btn.draw(screen)
    back_btn.draw(screen)

def draw_level_select():
    screen.blit(background, (0, 0))
    title = large_font.render("Выберите уровень", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)

    for btn in level_buttons:
        btn.draw(screen)
    back_btn.draw(screen)  # Кнопка выхода из выбора уровней

def draw_game():
    # Применение эффекта дрожания
    dx, dy = screen_shake_effect()

    # Отрисовка фона и объектов со смещением
    screen.blit(background, (dx, dy))
    screen.blit(rocket, (game.rocket_rect.x + dx, game.rocket_rect.y + dy))

    for m in game.meteors:
        screen.blit(meteor, (m.x + dx, m.y + dy))

    for h in game.humans:
        screen.blit(human, (h.x + dx, h.y + dy))

    for e in game.enemies:
        screen.blit(enemy_ship, (e.x + dx, e.y + dy))

    for bullet in game.bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    for bullet in game.enemy_bullets:
        pygame.draw.rect(screen, RED, bullet)

    # Эффект красного мигания
    flash = red_flash_effect()
    if flash:
        screen.blit(flash, (0, 0))

    # HUD
    hp_text = font.render(f"HP: {game.rocket_hp}", True, GREEN)
    saved_text = font.render(f"Спасено: {game.saved_humans}/10", True, YELLOW)
    level_text = font.render(f"Уровень: {game.current_level}", True, WHITE)
    screen.blit(hp_text, (10 + dx, 10 + dy))
    screen.blit(saved_text, (10 + dx, 40 + dy))
    screen.blit(level_text, (10 + dx, 70 + dy))

def draw_boss_fight():
    # Отрисовка фона
    screen.blit(background, (0, 0))

    # Отрисовка босса
    screen.blit(boss_ship, game.boss_rect)

    # Отрисовка ракеты
    screen.blit(rocket, game.rocket_rect)

    # Отрисовка пуль босса
    for bullet in game.boss_bullets:
        pygame.draw.rect(screen, RED, bullet)

    # HUD
    hp_text = font.render(f"HP: {game.rocket_hp}", True, GREEN)
    boss_hp_text = font.render(f"Босс HP: {game.boss_hp}", True, RED)
    dodged_text = font.render(f"Уклонений: {game.dodged_boss_bullets}", True, YELLOW)
    screen.blit(hp_text, (10, 10))
    screen.blit(boss_hp_text, (10, 40))
    screen.blit(dodged_text, (10, 70))

def draw_tutorial():
    screen.blit(tutorial_image, (0, 0))
    screen.blit(arrow_image, (WIDTH // 2 - 25, HEIGHT - 100))
    text = font.render("Нажмите любую клавишу, чтобы начать уровень", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text, text_rect)

def draw_pause_menu():
    screen.fill(BLACK)
    title = large_font.render("Пауза", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    restart_btn.draw(screen)
    menu_btn.draw(screen)

def draw_boss_victory():
    screen.blit(victory_image, (0, 0))
    screen.blit(arrow_image, (WIDTH // 2 - 25, HEIGHT - 100))
    text = font.render("Нажмите любую клавишу, чтобы вернуться в меню", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text, text_rect)

# Кнопки
start_btn = Button("Начать игру", WIDTH // 2 - 100, 300, 200, 50, BLUE, LIGHT_BLUE, lambda: set_game_state(LEVEL_SELECT))
settings_btn = Button("Настройки", WIDTH // 2 - 100, 370, 200, 50, BLUE, LIGHT_BLUE, lambda: set_game_state(SETTINGS))
exit_btn = Button("Выйти", WIDTH // 2 - 100, 440, 200, 50, RED, LIGHT_BLUE, sys.exit)
menu_btn = Button("В меню", WIDTH // 2 - 100, 400, 200, 50, BLUE, LIGHT_BLUE, lambda: set_game_state(MENU))
restart_btn = Button("Рестарт", WIDTH // 2 - 100, 300, 200, 50, BLUE, LIGHT_BLUE, lambda: start_level(game.current_level))
back_btn = Button("Назад", WIDTH // 2 - 100, 500, 200, 50, BLUE, LIGHT_BLUE, lambda: set_game_state(MENU))
reset_progress_btn = Button("Сбросить прогресс", WIDTH // 2 - 100, 200, 200, 50, RED, LIGHT_BLUE, lambda: None)

# Кнопки для выбора уровня
level_buttons = []
for i in range(1, 6):
    level_buttons.append(Button(
        f"Уровень {i}",
        100 + (i - 1) % 5 * 120,
        150 + (i - 1) // 5 * 60,
        100, 50, BLUE, LIGHT_BLUE,
        lambda i=i: start_level(i)
    ))

# Функция для изменения состояния игры
def set_game_state(state):
    global game_state
    game_state = state

# Функция для начала уровня
def start_level(level):
    game.current_level = level
    reset_game()
    if level == 1:
        set_game_state(TUTORIAL)
    elif level == 5:
        set_game_state(BOSS_FIGHT)
    else:
        set_game_state(PLAYING)

# Главный цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if game_state == MENU:
                start_btn.check_click(pos)
                settings_btn.check_click(pos)
                exit_btn.check_click(pos)
            elif game_state == LEVEL_SELECT:
                for btn in level_buttons:
                    btn.check_click(pos)
                back_btn.check_click(pos)
            elif game_state == SETTINGS:
                reset_progress_btn.check_click(pos)
                back_btn.check_click(pos)
            elif game_state == GAME_OVER or game_state == VICTORY:
                menu_btn.check_click(pos)
            elif game_state == PAUSED:
                restart_btn.check_click(pos)
                menu_btn.check_click(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and (game_state == PLAYING or game_state == BOSS_FIGHT):
                set_game_state(PAUSED)
            if game_state == TUTORIAL:
                set_game_state(PLAYING)
            if game_state == BOSS_VICTORY:
                set_game_state(MENU)
            if game_state == PLAYING and event.key == pygame.K_SPACE:  # Стрельба на уровне 3
                create_bullet()

    if game_state == MENU:
        draw_menu()

    elif game_state == LEVEL_SELECT:
        draw_level_select()

    elif game_state == SETTINGS:
        draw_settings()

    elif game_state == TUTORIAL:
        draw_tutorial()

    elif game_state == PLAYING:
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and game.rocket_rect.x > 0:
            game.rocket_rect.x -= 5
        if keys[pygame.K_d] and game.rocket_rect.x < WIDTH - game.rocket_rect.width:
            game.rocket_rect.x += 5

        # Генерация объектов
        if game.current_level == 1 and random.random() < 0.05:  # Больше метеоритов на уровне 1
            create_meteor()
        if game.current_level == 2 and random.random() < 0.01:  # Люди на уровне 2
            create_human()
        if game.current_level == 3:
            if len(game.enemies) == 0:  # Если все враги уничтожены
                if not hasattr(game, 'next_wave_time'):  # Если время следующей волны не установлено
                    game.next_wave_time = time.time() + 3  # Устанавливаем задержку в 3 секунды
                elif time.time() >= game.next_wave_time:  # Если задержка прошла
                    for _ in range(4):  # Создаем 4 новых врага
                        create_enemy()
                    del game.next_wave_time  # Удаляем временную переменную
        if game.current_level == 4 and random.random() < 0.05:  # Больше метеоритов на уровне 4
            create_meteor()

        # Движение объектов
        for m in game.meteors[:]:
            m.y += 5
            if m.y > HEIGHT:
                game.meteors.remove(m)
            if m.colliderect(game.rocket_rect):
                game.rocket_hp -= 10
                game.meteors.remove(m)
                game.screen_shake = 10  # Тряска экрана
                if game.rocket_hp <= 0:
                    set_game_state(GAME_OVER)

        for h in game.humans[:]:
            h.y += 3
            if h.colliderect(game.rocket_rect):
                game.saved_humans += 1
                game.humans.remove(h)
                if game.saved_humans >= 10 and game.current_level == 2:
                    set_game_state(VICTORY)

        for e in game.enemies[:]:
            e.y += 3
            if e.colliderect(game.rocket_rect):
                game.rocket_hp -= 10
                game.enemies.remove(e)
                if game.rocket_hp <= 0:
                    set_game_state(GAME_OVER)

            # Вражеские корабли стреляют
            if random.random() < 0.01:
                create_enemy_bullet(e)

        # Движение пуль игрока
        for bullet in game.bullets[:]:
            bullet.y -= 5
            if bullet.y < 0:
                if bullet in game.bullets:  # Проверка перед удалением
                    game.bullets.remove(bullet)
            for e in game.enemies[:]:
                if bullet.colliderect(e):
                    if bullet in game.bullets:  # Проверка перед удалением
                        game.bullets.remove(bullet)
                    game.enemy_hp[id(e)] -= 10  # Уменьшаем HP врага
                    if game.enemy_hp[id(e)] <= 0:
                        game.enemies.remove(e)
                        del game.enemy_hp[id(e)]
                        game.enemies_killed += 1

        # Движение пуль врагов
        for bullet in game.enemy_bullets[:]:
            bullet.y += 5
            if bullet.y > HEIGHT:
                if bullet in game.enemy_bullets:  # Проверка перед удалением
                    game.enemy_bullets.remove(bullet)
            if bullet.colliderect(game.rocket_rect):
                if bullet in game.enemy_bullets:  # Проверка перед удалением
                    game.enemy_bullets.remove(bullet)
                game.rocket_hp -= 10
                game.screen_shake = 10  # Тряска экрана
                if game.rocket_hp <= 0:
                    set_game_state(GAME_OVER)

        # Проверка завершения уровня
        if game.current_level == 1 and time.time() - game.level_start_time >= 20:  # Уровень 1 завершается через 20 секунд
            set_game_state(VICTORY)
        elif game.current_level == 2 and game.saved_humans >= 10:  # Уровень 2 завершается после спасения 10 людей
            set_game_state(VICTORY)
        elif game.current_level == 3 and game.enemies_killed >= 12:  # Уровень 3 завершается после уничтожения 12 врагов
            set_game_state(VICTORY)
        elif game.current_level == 4 and time.time() - game.level_start_time >= 30:  # Уровень 4 завершается через 30 секунд
            set_game_state(VICTORY)

        draw_game()

    elif game_state == BOSS_FIGHT:
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and game.rocket_rect.x > 0:
            game.rocket_rect.x -= 5
        if keys[pygame.K_d] and game.rocket_rect.x < WIDTH - game.rocket_rect.width:
            game.rocket_rect.x += 5

        # Движение босса
        game.boss_rect.x += game.boss_speed * game.boss_direction
        if game.boss_rect.x <= 0 or game.boss_rect.x >= WIDTH - game.boss_rect.width:
            game.boss_direction *= -1  # Меняем направление движения

        # Генерация пуль босса
        if random.random() < 0.02:
            create_boss_bullet()

        # Движение пуль босса
        for bullet in game.boss_bullets[:]:
            bullet.y += 5
            if bullet.y > HEIGHT:  # Пуля ушла за экран
                if bullet in game.boss_bullets:  # Проверка перед удалением
                    game.boss_bullets.remove(bullet)
                game.dodged_boss_bullets += 1  # Уклонение засчитывается
                game.boss_hp -= 30  # Босс теряет 30 HP
                if game.boss_hp <= 0:
                    game.boss_hp = 0
            if bullet.colliderect(game.rocket_rect):  # Пуля попала в игрока
                if bullet in game.boss_bullets:  # Проверка перед удалением
                    game.boss_bullets.remove(bullet)
                game.rocket_hp -= 50  # Игрок теряет 50 HP
                game.screen_shake = 10  # Тряска экрана
                if game.rocket_hp <= 0:
                    set_game_state(GAME_OVER)

        # Проверка победы
        if game.boss_hp <= 0:  # Уровень 5 завершается, если у босса закончилось HP
            set_game_state(BOSS_VICTORY)

        draw_boss_fight()

    elif game_state == GAME_OVER:
        screen.fill(BLACK)
        text = large_font.render("ИГРА ОКОНЧЕНА!", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        menu_btn.draw(screen)

    elif game_state == VICTORY:
        screen.fill(BLACK)
        if game.current_level == 5:
            text = large_font.render("ПОБЕДА! ВЫ ПОБЕДИЛИ БОССА!", True, GREEN)
        else:
            text = large_font.render("ПОБЕДА! УРОВЕНЬ ПРОЙДЕН!", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        menu_btn.draw(screen)

    elif game_state == PAUSED:
        draw_pause_menu()

    elif game_state == BOSS_VICTORY:
        draw_boss_victory()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()