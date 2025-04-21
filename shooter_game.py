#Создай собственный Шутер!
from pygame import *
from random import*

window = display.set_mode((700,500))
display.set_caption("Shooter")

background = transform.scale(image.load('lawn.jpg'),(700,500))
happy = transform.scale(image.load('happy.png'),(300,300))
sad = transform.scale(image.load('sad.png'),(300,300))

mixer.init()
mixer.music.load('song.ogg')
mixer.music.play()

throw = mixer.Sound('throw2.ogg')

font.init()
font1 = font.SysFont('Arial', 25)
font2 = font.SysFont('Arial', 70)

lost = font2.render("Вы проиграли...", 1, (245, 105, 66))
won = font2.render("Вы выиграли!", 1, (245, 105, 66))

class GameSprite(sprite.Sprite): # * класс спрайтов
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): # ! класс игрока
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('meteorite.png', self.rect.centerx, self.rect.top, 20, 20, 4)
        bullets.add(bullet)
    
loss = 0
score = 0
class Objects(GameSprite): # TODO: класс врагов
    def update(self):
        global loss
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.y -= 470
            self.rect.x = randint(100,650)
            self.speed = randint(1,3)
            loss += 1

class Bullet(GameSprite): # ? класс пуль
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
bunny = Player('amazed.png', 100,400,110,110, 7)

carrots = sprite.Group()
for i in range(5):
    carrot = Objects('angry.png', randint(100,650), 0, 90, 90, 2)
    carrots.add(carrot)

finish = False
run = True
num_fire = 0
rel_time = False
while run:

    keys_pressed = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5:
                    throw.play()
                    bunny.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = time.get_ticks()

    if not finish:
        window.blit(background,(0,0))
        carrots.draw(window)
        carrots.update()

        text_count = font1.render("Счёт: " + str(score), 1, (245, 105, 66))
        text_lose = font1.render("Пропущено: " + str(loss), 1, (245, 105, 66))
        window.blit(text_count, (10,25))
        window.blit(text_lose, (10,50))

        if rel_time:
            now = time.get_ticks()
            if now - start >= 3000:
                num_fire = 0
                rel_time = False
            else:
                text_time = font1.render("Подождите, идет перезарядка..." , 1, (245, 105, 66))
                window.blit(text_time, (230,350))

        carrots_list = sprite.groupcollide(carrots, bullets, True, True)
        for carrot in carrots_list:
            score += 1
            carrot = Objects('angry.png', randint(100,650), 0, 90, 90, 2)
            carrots.add(carrot)

        if score >= 10:
            finish = True
            window.blit(background, (0,0))
            window.blit(happy, (0,100))
            window.blit(won, (270,170))
            
        if sprite.spritecollide(bunny, carrots, False) or loss >= 3:
            finish = True
            window.blit(background, (0,0))
            window.blit(sad, (0,100))
            window.blit(lost, (270,170))
            

        bunny.reset()
        bunny.update()

        bullets.update()
        bullets.draw(window)
        
        display.update()

    time.delay(50) #0.05 sec




