import pygame

# Инициализируем pygame
pygame.init()

# Создаем экран
screen = pygame.display.set_mode((500, 300))

pacman = pygame.image.load('pm.png')

pmX = 0
pmY = 200
speed = 10

to_left = False
to_right = False
to_up = False
to_down = False

# Пока игровое поле открыто
while True:
    # Заливаем экран серо-синим цветом
    screen.fill(("black"))
    # Определяем время задержки
    pygame.time.delay(30)

    # цикл для обработки событий
    for event in pygame.event.get():
        # если произошло событие - нажатие клавиши
        if event.type == pygame.KEYDOWN:
            # если была нажата стрелка влево
            if event.key == pygame.K_LEFT:
                to_left = True
            # если была нажата стрелка вправо
            if event.key == pygame.K_RIGHT:
                to_right = True
            # если была нажата стрелка вниз
            if event.key == pygame.K_DOWN:
                to_down = True
            # если была нажата стрелка вверх
            if event.key == pygame.K_UP:
                to_up = True

        # если пользователь перестал нажимать клавишу
        if event.type == pygame.KEYUP:
            # если это была стрелка влево
            if event.key == pygame.K_LEFT:
                to_left = False
            # если это была стрелка вправо
            if event.key == pygame.K_RIGHT:
                to_right = False
            # если это была стрелка вниз
            if event.key == pygame.K_DOWN:
                to_down = False
            # если это была стрелка вверх
            if event.key == pygame.K_UP:
                to_up = False

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # В зависимости от значений переменных направления
    # меняем значения координат
    if to_right:
        pmX += speed
    if to_left:
        pmX -= speed
    if to_down:
        pmY += speed
    if to_up:
        pmY -= speed

    # выводим мяч на экран и обновляем дисплей
    screen.blit(pacman, (pmX, pmY))
    pygame.display.update()