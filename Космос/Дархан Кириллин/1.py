import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alpha versions ")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

# Шрифты
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# Загрузка изображений
try:
    background = pygame.image.load("freepik__a-massive-ringed-planet-looms-large-as-a-sleek-sil__60918.jpeg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    player_img = pygame.image.load("png-transparent-pokemon-character-illustration-asteroids-outpost-defender-miner-cube-pro-sprite-video-game-space-craft-game-symmetry-fictional-character-thumbnail-Photoroom.png").convert_alpha()
    enemy_img = pygame.image.load("images (1)-Photoroom.png").convert_alpha()
    fast_enemy_img = pygame.image.load("foni-papik-pro-d9n7-p-kartinki-kosmicheskii-korabl-2d-na-prozrac-1-Photoroom-Photoroom (1).png").convert_alpha()  # Картинка быстрого врага
    strong_enemy_img = pygame.image.load("images (2)-Photoroom.png").convert_alpha()  # Картинка сильного врага
    bullet_img = pygame.image.load("png-transparent-gun-shot-effect-Photoroom.png").convert_alpha()
    star_img = pygame.image.load("images (2).jpg").convert_alpha()  # Картинка звезды
except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    sys.exit()

# Звуки
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("vyistrel-iz-kosmicheskogo-orujiya-23707.wav")
explosion_sound = pygame.mixer.Sound("vzryiv-s-ognennyim-plamenem.wav")
background_music = pygame.mixer.Sound("c26baac1db252bd (1).mp3")
background_music.play(-1)  # Зацикливаем фоновую музыку

# Класс кнопки
class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.hover_color = GREEN

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (70, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self, bullets, all_sprites):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


# Класс базового врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 5)


# Класс быстрого врага
class FastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(fast_enemy_img, (30, 30))
        self.speed = random.randint(8, 10)

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(8, 10)


# Класс сильного врага
class StrongEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(strong_enemy_img, (40, 40))
        self.speed = random.randint(2, 4)
        self.health = 2

    def reset(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4)
        self.health = 2


# Класс стреляющего врага
class ShootingEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.shoot_delay = random.randint(30, 60)
        self.shoot_timer = 0

    def update(self):
        super().update()
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True
        return False

    def shoot(self, enemy_bullets, all_sprites):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)


# Класс пули игрока
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -5  # Уменьшена скорость пуль игрока

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Класс пули врага
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 10  # Увеличена скорость пуль врага

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Класс звезды
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(star_img, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-HEIGHT, 0)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-HEIGHT, 0)
        self.speed = random.randint(1, 3)


def main_menu():
    buttons = [
        Button("Начать игру", WIDTH // 2 - 150, 250, 300, 50),
        Button("Смена уровня", WIDTH // 2 - 150, 320, 300, 50),
        Button("Выход", WIDTH // 2 - 150, 390, 300, 50)
    ]

    while True:
        screen.blit(background, (0, 0))

        # Отрисовка заголовка
        title_text = font.render("Meteorite Killer", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Начать игру":
                            return "start"
                        elif button.text == "Смена уровня":
                            return "level_select"
                        elif button.text == "Выход":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()


def level_select_menu():
    buttons = [
        Button("Уровень 1", WIDTH // 2 - 150, 200, 300, 50),
        Button("Уровень 2", WIDTH // 2 - 150, 270, 300, 50),
        Button("Уровень 3", WIDTH // 2 - 150, 340, 300, 50),
        Button("Назад", WIDTH // 2 - 150, 410, 300, 50)
    ]

    while True:
        screen.blit(background, (0, 0))

        # Отрисовка заголовка
        title_text = font.render("Выбор уровня", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Уровень 1":
                            return 1
                        elif button.text == "Уровень 2":
                            return 2
                        elif button.text == "Уровень 3":
                            return 3
                        elif button.text == "Назад":
                            return "back"

        pygame.display.flip()


def game_loop(initial_level=1):
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    stars = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Создание звезд
    for _ in range(50):
        star = Star()
        all_sprites.add(star)
        stars.add(star)

    # Настройка врагов в зависимости от уровня
    for _ in range(8):
        if initial_level == 1:
            enemy = Enemy()
        elif initial_level == 2:
            enemy = random.choice([Enemy(), FastEnemy()])
        elif initial_level == 3:
            enemy = random.choice([Enemy(), FastEnemy(), StrongEnemy()])
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    level = initial_level
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(bullets, all_sprites)

        all_sprites.update()

        # Проверка столкновений
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy in hits:
            if isinstance(enemy, StrongEnemy):
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
                    score += 15  # Больше очков за сильного врага
                    explosion_sound.play()
            else:
                enemy.kill()
                score += 10
                explosion_sound.play()

        # Добавление новых врагов
        if len(enemies) < 8 + level * 2:
            if initial_level == 1:
                enemy = Enemy()
            elif initial_level == 2:
                enemy = random.choice([Enemy(), FastEnemy()])
            elif initial_level == 3:
                enemy = random.choice([Enemy(), FastEnemy(), StrongEnemy()])
            all_sprites.add(enemy)
            enemies.add(enemy)

        if pygame.sprite.spritecollide(player, enemies, True):
            player.lives -= 1
            if player.lives <= 0:
                running = False

        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.lives -= 1
            if player.lives <= 0:
                running = False

        # Стрельба врагов
        for enemy in enemies:
            if isinstance(enemy, ShootingEnemy):
                if enemy.update():
                    enemy.shoot(enemy_bullets, all_sprites)

        # Отрисовка
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Отображение информации
        score_text = small_font.render(f"Счет: {score}", True, WHITE)
        lives_text = small_font.render(f"Жизни: {player.lives}", True, WHITE)
        level_text = small_font.render(f"Уровень: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(level_text, (10, 70))

        pygame.display.flip()

        # Увеличение уровня
        if score >= level * 100:
            level += 1
            for _ in range(2):
                if initial_level == 1:
                    enemy = ShootingEnemy()
                elif initial_level == 2:
                    enemy = random.choice([ShootingEnemy(), FastEnemy()])
                elif initial_level == 3:
                    enemy = random.choice([ShootingEnemy(), FastEnemy(), StrongEnemy()])
                all_sprites.add(enemy)
                enemies.add(enemy)

    return score


def game_over_screen(score):
    buttons = [
        Button("Играть снова", WIDTH//2-150, 300, 300, 50),
        Button("Главное меню", WIDTH//2-150, 370, 300, 50),
        Button("Выход", WIDTH//2-150, 440, 300, 50)
    ]

    while True:
        screen.blit(background, (0, 0))  # Всегда рисуем фон

        # Отрисовка текста
        title_text = font.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH//2, 150))
        screen.blit(title_text, title_rect)

        score_text = small_font.render(f"Счет: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, 220))
        screen.blit(score_text, score_rect)

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button.text == "Играть снова":
                            return "restart"
                        elif button.text == "Главное меню":
                            return "menu"
                        elif button.text == "Выход":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()
        #     if button.text == "Играть снова":
        #         return "restart"
        #     elif button.text == "Главное меню":
        #         return "menu"
        #     elif button.text == "Выход":
        #         return "menu"


if __name__ == "__main__":
    while True:
        action = main_menu()
        if action == "start":
            score = game_loop()  # Получаем счет после игры
            print(score)
            action = game_over_screen(score)  # Передаем счет в game_over_screen
        elif action == "level_select":
            selected_level = level_select_menu()
            if selected_level == "back":
                continue
            else:
                score = game_loop(selected_level)  # Получаем счет после игры
                action = game_over_screen(score)  # Передаем счет в game_over_screen
        else:
            break

        if action == "restart":
            continue
        elif action == "menu":
            pass
        else:
            break


