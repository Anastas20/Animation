import pygame, math

screen = pygame.display.set_mode((600, 600))
a = b = 490
i = 0

clock = pygame.time.Clock()
FPS = 30

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill('black')
    pygame.draw.circle(screen, (247, 255, 0), (300, 300), 200)
    pygame.draw.circle(screen, 'blue', (a, b), 6)
    pygame.display.flip()

    if i <= 360:  # здесь мы ставим ограничения
        angle = i * (3.14 / 180)  # перевод из градусов в радианы
        a = 250 * math.cos(angle) + 300
        b = 250 * math.sin(angle) + 300
        i += 3  # увеличиваем угол перемещения.

    else:
        i = 0  # обнуляем i потому - что, углов > 360 градусов нет, а кружок прошел свой путь

