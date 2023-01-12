import pygame
import math
import random

pygame.init()

sw = 800  # ширина экрана
sh = 800  # высота экрана

bg = pygame.image.load('starbg.png')         # фон
playerRocket = pygame.image.load('spaceRocket.png')   # корабль
star = pygame.image.load('star.png')     # взрыв
asteroid50 = pygame.image.load('asteroid50.png')   # астероиды
asteroid100 = pygame.image.load('asteroid100.png')
asteroid150 = pygame.image.load('asteroid150.png')


pygame.display.set_caption('Asteroids')  # изменим заголовок окна
win = pygame.display.set_mode((sw, sh))  # формируем игровое окно
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0


class Player:
    def __init__(self):
        self.img = playerRocket
        self.w = self.img.get_width()  # размеры корабля
        self.h = self.img.get_height()
        self.x = sw//2  # координаты центра поля
        self.y = sh//2
        self.angle = 0  # начальный угол
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)  # вращение корабля
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)  # располагаем корабль в центре поля
        self.cosine = math.cos(math.radians(self.angle + 90))  # косинус точки
        self.sine = math.sin(math.radians(self.angle + 90))   # синус точки
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)  # координаты передней части коробля

    def draw(self, win):
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

class Bullet:
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True


class Asteroid:
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Star:
    def __init__(self):
        self.img = star
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


def redrawGameWindow():
    '''перерисовка игрового окна'''
    win.blit(bg, (0,0))
    font = pygame.font.SysFont('arial',30)
    livesText = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255,255,255))
    scoreText = font.render('Score: ' + str(score), 1, (255,255,255))
    highScoreText = font.render('High Score: ' + str(highScore), 1, (255, 255, 255))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for s in stars:
        s.draw(win)
    for a in aliens:
        a.draw(win)
    for b in alienBullets:
        b.draw(win)

    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [sw//2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [sw//2 - 50, 20, 100 - 100*(count - rfStart)/500, 20])

    if gameover:
        win.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
    win.blit(scoreText, (sw- scoreText.get_width() - 25, 25))
    win.blit(livesText, (25, 25))
    win.blit(highScoreText, (sw - highScoreText.get_width() -25, 35 + scoreText.get_height()))
    pygame.display.update()



player = Player()
playerBullets = []
asteroids = []
count = 0
stars = []
aliens = []
alienBullets = []
run = True
while run:   # главный цикл обработки событий
    clock.tick(60)  # число кадров в секунду
    count += 1
    # если игра не завершена
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))
        if count % 1000 == 0:
            stars.append(Star())
        for i, a in enumerate(aliens):
            a.x += a.xv
            a.y += a.yv
            if a.x > sw + 150 or a.x + a.w < -100 or a.y > sh + 150 or a.y + a.h < -100:
                aliens.pop(i)


            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens.pop(i)

                        score += 50
                        break

        for i, b in enumerate(alienBullets):
            b.x += b.xv
            b.y += b.yv
            if (b.x >= player.x - player.w//2 and b.x <= player.x + player.w//2) or b.x + b.w >= player.x - player.w//2 and b.x + b.w <= player.x + player.w//2:
                if (b.y >= player.y-player.h//2 and b.y <= player.y + player.h//2) or b.y + b.h >= player.y - player.h//2 and b.y + b.h <= player.y + player.h//2:
                    lives -= 1
                    alienBullets.pop(i)
                    break

        player.updateLocation()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))


        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))

                    break

            # bullet collision
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in playerBullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                playerBullets.append(Bullet())


    for event in pygame.event.get():   # перебираем очередь событий
        if event.type == pygame.QUIT:  # если пользователь вышел из игры
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(Bullet())
            if event.key == pygame.K_TAB:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    aliens.clear()
                    alienBullets.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0

    redrawGameWindow()
pygame.quit()