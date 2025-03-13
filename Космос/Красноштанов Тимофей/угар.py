import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звёздные войны")

# Класс для космического корабля
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("тай файтер.png").convert_alpha(), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.health = 3  # Здоровье игрока

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

# Класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('5d5b5c1ee279f3ac7324df518ab76d76.png').convert_alpha(), (40, 40))  # Замените на ваше изображение врага
        # self.image.fill(RED)
        self.rect = self.image    .get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 50)
            self.rect.y = random.randint(-100, -40)

# Класс для пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Замените на ваше изображение пули
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Создание врагов
for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Главный игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Обновление спрайтов
    all_sprites.update()

    # Проверка на столкновения между пулями и врагами
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Проверка на столкновения между игроком и врагами
    if pygame.sprite.spritecollide(player, enemies, False):
        player.health -= 1  # Уменьшаем здоровье игрока
        if player.health <= 0:
            running = False  # Если здоровье ≤ 0, завершаем игру

    # Отрисовка объектов
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Отображение здоровья игрока
    font = pygame.font.Font(None, 36)
    health_text = font.render(f'Health: {player.health}', True, WHITE)
    screen.blit(health_text, (10, 10))

    pygame.display.flip()

    # Ограничение кадров в секунду
    clock.tick(40  )

# Завершение игры
pygame.quit()