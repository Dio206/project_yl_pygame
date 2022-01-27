import os
import pygame
pygame.init()
pygame.display.set_caption('pacman movement')
SIZE = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('black')
FPS = 60

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()



def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images




class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images):

        super(AnimatedSprite, self).__init__()

        size = (32, 32)

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

    def update_frame_dependent(self):

        if self.velocity.x > 0:
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left
        elif self.velocity.y > 0:
            self.images = self.images_up
        elif self.velocity.y < 0:
            self.images = self.images_down

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        self.update_time_dependent(dt)




def main():
    images = load_images(path='data')
    player = AnimatedSprite(position=(100, 100), images=images)
    all_sprites = pygame.sprite.Group(player)
    running = True
    while running:

        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity.x = 4
                elif event.key == pygame.K_LEFT:
                    player.velocity.x = -4
                elif event.key == pygame.K_DOWN:
                    player.velocity.y = 4
                elif event.key == pygame.K_UP:
                    player.velocity.y = -4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.velocity.x = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player.velocity.y = 0


        all_sprites.update(dt)

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()