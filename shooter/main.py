from pygame import *
from random import *


score = 0

global lost
lost = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(player_image), (self.size_x, self.size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        x = randint(1,2)
        if x == 1:
            z = 'bullet.png'
            t = 45
            y = 50
        else:
            z = 'bullet2.png'
            t = 15
            y = 15
        bullet = Bullet(z, self.rect.centerx-10, self.rect.top, t, y, -15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 700:
            self.rect.y = 10
            self.rect.x = randint(50, 450)
            lost += 1
            self.speed = randint(1, 4)


# Настройки музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Настройки окна
win_width = 500
win_height = 700
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

font.init()
f1 = font.Font(None, 36)
f2 = font.Font(None, 50)
win = f1.render('Уничтоженно: ' + str(score), 1, (255, 255, 255))
lose = f1.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
game_over = f2.render('Хьюстен у нас проблемы', 1, (255, 0, 0))
game_win = f2.render('Вы их уничтожили', 1, (0, 200, 0))

window = display.set_mode((win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 5)
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

bullets = sprite.Group()

# Монстры
monsters = sprite.Group()
for i in range(7):
    c = randint(1,2)

    if c == 1:
        x = 'asteroid2.png'
        z = randint(70, 90)
    else:
        x = 'asteroid.png'
        z = randint(70, 90)

    monster = Enemy(x, randint(50, 450), 10, z, z, randint(1, 4))
    monsters.add(monster)

# Основные переменные для игрового цикла
finish = False

game = True
clock = time.Clock()
FPS = 60

# Пгровой цикл
while game:
    # Прохождение в цикле по всем событиям
    for e in event.get():
        if e.type == QUIT:
            game = False
            break

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    # Отображение фона и спрайтов
    if not finish:



        window.blit(background, (0, 0))

        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.update()
        ship.reset()



        if sprite.collide_rect(list(monsters)[0], ship) or sprite.collide_rect(list(monsters)[1],
                                                                               ship) or sprite.collide_rect(
            list(monsters)[2], ship) or sprite.collide_rect(list(monsters)[3], ship) or sprite.collide_rect(
            list(monsters)[4], ship) or sprite.collide_rect(
            list(monsters)[5], ship) or sprite.collide_rect(
            list(monsters)[6], ship):
            finish = True
            status = False

        for i in list(bullets):
            for j in list(monsters):
                if sprite.collide_rect(i, j):
                    i.kill()
                    j.rect.y = 0
                    j.rect.x = randint(50, 450)
                    score += 1

                    c = randint(1, 2)
                    if c == 1:
                        x = 'asteroid2.png'
                    else:
                        x = 'asteroid.png'
                    j.image = transform.scale(image.load(x), (j.size_x, j.size_y))

        lose = f1.render('Пропущенно: ' + str(lost), 1, (255, 255, 255))
        win = f1.render('Уничтоженно: ' + str(score), 1, (255, 255, 255))
        window.blit(lose, (5, 10))
        window.blit(win, (5, 30))


    if lost >= 5:
        finish = True
        status = False

    if score >= 100:
        finish = True
        status = True

    if finish == True and status == False:
        window.blit(game_over, (40, 180))

    if finish == True and status == True:
        window.blit(game_win, (100, 150))






    # Обновление экрана и FPS
    display.update()
    clock.tick(FPS)
