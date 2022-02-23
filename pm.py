import os
import random

import pygame

FPS = 60
WINDOW_SIZE = W_WIDTH, W_HEIGHT = 800, 600


def draw(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("Press 'z' to start game!", True, (100, 255, 100))
    text2 = font.render("Press 'q' to finish game", True, (100, 255, 100))
    text3 = font.render("Press 'i' to see rules", True, (100, 255, 100))
    text4 = font.render("Press 'j' to see the leaderboard", True, (100, 255, 100))
    screen.blit(text, (200, 106))
    screen.blit(text2, (200, 406))
    screen.blit(text3, (200, 206))
    screen.blit(text4, (200, 306))
    pygame.draw.rect(screen, (0, 255, 0), (190, 90, 391, 60), 1)
    pygame.draw.rect(screen, (0, 255, 0), (190, 390, 401, 60), 1)
    pygame.draw.rect(screen, (0, 255, 0), (190, 190, 351, 60), 1)
    pygame.draw.rect(screen, (0, 255, 0), (190, 290, 531, 60), 1)


def draw2(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("left up right down to move", True, (100, 255, 100))
    text2 = font.render("To win you need to collect all the food", True, (100, 255, 100))
    text3 = font.render("Ghosts can catch you", True, (100, 255, 100))
    text4 = font.render("Press 'z' to return", True, (100, 255, 100))
    screen.blit(text, (100, 106))
    screen.blit(text2, (100, 306))
    screen.blit(text3, (100, 206))
    screen.blit(text4, (100, 406))
    pygame.draw.rect(screen, (0, 255, 0), (90, 90, 451, 60), 1)
    pygame.draw.rect(screen, (0, 255, 0), (90, 290, 641, 60), 1)
    pygame.draw.rect(screen, (0, 255, 0), (90, 190, 381, 60), 1)
    pygame.draw.rect(screen, (0, 255, 0), (90, 390, 311, 60), 1)


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Border2(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([30, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 30, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 30])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 30)


class Ghost(pygame.sprite.Sprite):
    ghost = pygame.image.load('')
    ghost = pygame.transform.scale(ghost, (40, 40))

    def __init__(self, group, coord):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.x = 0
        self.y = 1
        self.image = Ghost.ghost
        self.rect = self.image.get_rect()
        self.rect.y = coord[0]
        self.rect.x = coord[1]
        print(self.rect.x, self.rect.y)

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect.y -= (5 * self.y)
            self.y = 0
            self.x = random.choice([1, -1])
        else:
            self.rect.x += (5 * self.x)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect.x -= (5 * self.x)
            self.x = 0
            self.y = random.choice([1, -1])
        else:
            self.rect.y += (5 * self.y)


def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images):
        self.x = 0
        self.y = 1

        super(AnimatedSprite, self).__init__()

        size = (30, 30)

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]
        self.images_up = [pygame.transform.rotate(image, 90) for image in images]
        self.images_down = [pygame.transform.rotate(image, -90) for image in images]

        self.index = 0
        self.image = images[self.index]

        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):

        if self.velocity.x > 0:
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left
        elif self.velocity.y < 0:
            self.images = self.images_up
        elif self.velocity.y > 0:
            self.images = self.images_down

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        self.update_time_dependent(dt)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.velocity.x = 0
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.velocity.y = 0




def main_menu():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    screen.fill((100, 100, 100))
    draw(screen)

    Border(5, 5, W_WIDTH - 5, 5)
    Border(5, W_HEIGHT - 5, W_WIDTH - 5, W_HEIGHT - 5)
    Border(5, 5, 5, W_HEIGHT - 5)
    Border(W_WIDTH - 5, 5, W_WIDTH - 5, W_HEIGHT - 5)
    Border2(50, 50, 500, 50)
    Border2(5, 125, 600, 125)
    Border2(725, 50, 725, 230)
    Border2(650, 5, 650, 230)
    Border2(50, 200, 650, 200)
    Border2(570, 50, 570, 155)
    Border2(725, 285, 795, 285)
    Border2(50, 285, 75, 285)
    Border2(385, 550, 385, 595)
    Border2(150, 285, 680, 285)
    Border2(385, 545, 725, 545)
    Border2(300, 385, 500, 385)
    Border2(385, 385, 385, 500)
    Border2(725, 300, 725, 575)
    Border2(650, 300, 650, 500)
    Border2(400, 470, 605, 470)
    Border2(575, 380, 575, 415)
    Border2(225, 385, 225, 500)
    Border2(235, 470, 325, 470)
    Border2(300, 470, 300, 545)
    Border2(225, 545, 225, 595)
    Border2(5, 545, 225, 545)
    Border2(50, 285, 50, 500)
    Border2(50, 470, 175, 470)
    Border2(145, 385, 145, 430)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game_menu()
                if event.key == pygame.K_i:
                    rules_menu()
                if event.key == pygame.K_j:
                    leader_menu()
                if event.key == pygame.K_q:
                    running = False

        pygame.display.flip()
    pygame.quit()


def game_menu():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    images = load_images(path='data')

    player = AnimatedSprite(position=(100, 100), images=images)
    all_sprites_pl = pygame.sprite.Group(player)

    for i in range(2):
        Ghost(all_sprites, [325, 380])

    screen.fill((100, 100, 100))

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(FPS) / 500
        screen.fill((100, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    main_menu()
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_RIGHT:
                    player.velocity.x = 5
                elif event.key == pygame.K_LEFT:
                    player.velocity.x = -5
                elif event.key == pygame.K_DOWN:
                    player.velocity.y = 5
                elif event.key == pygame.K_UP:
                    player.velocity.y = -5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.velocity.x = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player.velocity.y = 0

        all_sprites.draw(screen)
        all_sprites_pl.draw(screen)
        all_sprites.update()
        all_sprites_pl.update(dt)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


def rules_menu():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    screen.fill((100, 100, 100))
    draw2(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    main_menu()
                if event.key == pygame.K_q:
                    running = False

        pygame.display.flip()
    pygame.quit()


def leader_menu():
    # В разработке
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    screen.fill((100, 100, 100))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    main_menu()
                if event.key == pygame.K_q:
                    running = False

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main_menu()
