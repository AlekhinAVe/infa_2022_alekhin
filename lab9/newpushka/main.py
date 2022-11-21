import math
import itertools
import random
from random import choice
from random import randint
import pygame
import time

pygame.init()

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Ball:
    """ Конструктор класса ball
    Args:
    x - начальное положение мяча по горизонтали
    y - начальное положение мяча по вертикали
    """
    def __init__(self, screen):
        """ Конструктор класса ball
        Args:
        x - положение снаряда в танке по горизонтали
        y - положение снаряда в танке по вертикали
        type - тип снаряда: 1 - тяжелый, 0 - легкий
        """
        self.screen = screen
        self.x = tank.x
        self.y = tank.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def hit(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
        obj: Обьект, с которым проверяется столкновение.
        Returns:
        Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2) <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Heavyball(Ball):
    def move(self):
        self.vy += 2
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx // 2
            if self.vx < 1:
                self.x = WIDTH - self.r
        if self.y + self.r >= HEIGHT - 50:
            self.vy = -self.vy // 2
            self.vx = self.vx // 2
            if abs(self.vy) < 0.1:
                self.y = HEIGHT - 50 - self.r
                self.vx = 0
                self.vy = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
            )
        pygame.draw.ellipse(self.screen, BLACK,
                            (self.x - (self.r - 7), self.y - self.r, 2 * (self.r - 7), 2 * self.r))


class Lightball(Ball):
    def move(self):
        self.vy += 1
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx // 2
            if self.vx < 1:
                self.x = WIDTH - self.r
        if self.y + self.r >= HEIGHT - 50:
            self.vy = -self.vy // 2
            self.vx = self.vx // 2
            if abs(self.vy) < 0.1:
                self.y = HEIGHT - 50 - self.r
                self.vx = 0
                self.vy = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.ellipse(self.screen, BLACK,
                            (self.x - self.r, self.y - (self.r - 7), 2 * self.r, 2 * (self.r - 7)))


class Tank:
    def __init__(self, screen):
        self.screen = screen
        self.color = GREEN
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.an1 = 1
        self.x = 40
        self.y = 460
        self.vx = 10

    def move_right(self):
        """
        Движение танка вправо
        """
        if self.x > WIDTH - 40:
            self.x += 0
        else:
            self.x += self.vx

    def move_left(self):
        """
        Движение танка влево
        """
        if self.x < 40:
            self.x += 0
        else:
            self.x += -self.vx

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_balls = [Heavyball(screen), Lightball(screen)]
        new_ball = random.choice(new_balls)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        try:
            self.an1 = math.atan2((event.pos[1]-self.y), (event.pos[0] - self.x))
        except BaseException:
            self.an1 = 0
        if event:
            try:
                self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            except BaseException:
                self.an = 0
        if self.f2_on:
            self.color = GREEN
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.ellipse(
            self.screen,
            BLACK,
            (self.x - 48, self.y - 23, 98, 46))

        pygame.draw.ellipse(
            self.screen,
            GREEN,
            (self.x - 45, self.y - 20, 90, 40))

        pygame.draw.circle(
            self.screen,
            GREEN,
            (self.x + 30, self.y+35),
            15
        )

        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x + 30, self.y + 35),
            15, 3
        )

        pygame.draw.circle(
            self.screen,
            GREEN,
            (self.x, self.y + 35),
            15
        )

        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y + 35),
            15, 3
        )

        pygame.draw.circle(
            self.screen,
            GREEN,
            (self.x - 30, self.y + 35),
            15
        )

        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x - 30, self.y + 35),
            15, 3
        )

        pygame.draw.polygon(screen, self.color,
                            [[self.x, self.y],
                             [self.x + 2 * self.f2_power * math.cos(self.an1), self.y + 2 * self.f2_power * math.sin(self.an1)],
                             [self.x + 2* self.f2_power * math.cos(self.an1) + 3 * math.sin(self.an1),
                              self.y + 2 * self.f2_power * math.sin(self.an1) - 3 * math.cos(self.an1)],
                             [self.x + 3 * math.sin(self.an1), self.y - 3 * math.cos(self.an1)]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """ Конструктор класса Target
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели.
        type - тип цели: 0, 1 - цели в переменном нравитационном поле, 2 - цель, не взаимодействующая с гр. полем
        """
        x = self.x = randint(600, 700)
        y = self.y = randint(100, 300)
        r = self.r = randint(20, 40)
        color = self.color = RED
        vx = self.vx = randint(5, 10)
        vy = self.vy = randint(5, 10)


class Usualtarget(Target):
    def draw(self):
        pygame.draw.circle(screen,
        RED,
        (self.x, self.y),
        self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= 800 or self.x - self.r <= 200:
            self.vx = -self.vx
        if self.y + self.r >= 400:
            self.vy = -self.vy
        elif self.y - self.r <= 50:
            self.vy = -self.vy


class Updowntarget(Target):
    def draw(self):
        pygame.draw.circle(screen,
                           0xFFD700,
                           (self.x, self.y),
                           self.r)

    def move(self):
        if self.y < 215:
            self.vy += 1
        else:
            self.vy += -1
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= 800 or self.x - self.r <= 200:
            self.vx = -self.vx
        if self.y + self.r >= 400:
            self.vy = -self.vy
        elif self.y - self.r <= 50:
            self.vy = -self.vy


class Rightlefttarget(Target):
    def draw(self):
        pygame.draw.circle(screen,
                           0xFFD700,
                           (self.x, self.y),
                           self.r)

    def move(self):
        if self.x < 500:
            self.vx += 1
        else:
            self.vx += -1
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= 800 or self.x - self.r <= 200:
            self.vx = -self.vx
        if self.y + self.r >= 400:
            self.vy = -self.vy
        elif self.y - self.r <= 50:
            self.vy = -self.vy


class Bomb:
    def __init__(self, screen):
        self.screen = screen
        self.color = 0xFF6103
        self.x = randint(40, 780)
        self.y = 0
        self.r = randint(10, 15)
        self.vy = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy += 1
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(screen,
            BLACK,
            (self.x, self.y),
            self.r, 2
        )

    def hit(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
        obj: Обьект, с которым проверяется столкновение.
        Returns:
        Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x)**2 + (self.y - obj.y - 35)**2) <= (self.r + 15) ** 2:
            return True
        elif ((self.x - obj.x - 30) ** 2 + (self.y - obj.y - 35) ** 2) <= (self.r + 15) ** 2:
            return True
        elif ((self.x - obj.x + 30) ** 2 + (self.y - obj.y - 35) ** 2) <= (self.r + 15) ** 2:
            return True

        else:
            return False


font_name = pygame.font.match_font('arial')


def delete_bomb(obj, points):
    """
    взрыв бомбы и снятие очка в случае попадания бомбы в танк
    """
    if obj.y > HEIGHT:
        bombs.remove(obj)
        bombs.append(Bomb(screen))
        return points
    if obj.hit(tank) and points > 0:
        bombs.remove(obj)
        bombs.append(Bomb(screen))
        points -= 1
        return points
    else:
        return points


def draw_text(surf, text, size, x, y):
    '''
        Функция отображения счета
        surf - экран
        text - счет
        size - не очень большой размер
        x, y - координаты центра текста
    '''
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def write_inf(bullet):
    draw_text(screen, 'Вы уничтожили цель за ' + str(bullet) + ' выстрелов', 26, WIDTH / 2, HEIGHT / 2 - 25)
    pygame.display.update()
    time.sleep(1)
    bullet = 0
    return bullet


def scoring(type, points):
    """
    Начисление очков: за 0, 1 тип - 2 очка, за 2 - 1 очко
    """
    hit_on = 1
    if type == 'Usualtarget':
        points += 1
    else:
        points += 2
    targets.remove(t)
    balls.remove(b)
    new_targets = [Usualtarget(), Updowntarget(), Rightlefttarget()]
    new_target = random.choice(new_targets)
    targets.append(new_target)
    t.live = 1
    return hit_on, points

bullet = 0
balls = []
bombs = []
targets = []
points = 0

clock = pygame.time.Clock()
tank = Tank(screen)
t1 = Usualtarget()
t2 = Usualtarget()
targets.append(t1)
targets.append(t2)
bomb = Bomb(screen)
bombs.append(bomb)
finished = False
hit_on = 0

while not finished:
    screen.fill(WHITE)
    draw_text(screen, str(points), 26, 15, 10)
    tank.draw()

    for bm in bombs:
        bm.draw()

    for t in targets:
        t.draw()

    if hit_on == 1:
        write_inf(bullet)
        hit_on = 0
        bullet = 0

    for b in balls:
        b.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            tank.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank.move_left()
    if keys[pygame.K_RIGHT]:
        tank.move_right()

    for bm in bombs:
        bm.move()
        points = delete_bomb(bm, points)

    for t in targets:
        t.move()

    for b in balls:
        for t in targets:
            if b.hit(t) and t.live:
                hit_on, points = scoring(type(t).__name__, points)
        if b.vy == 0 and hit_on == 0:
            balls.remove(b)
        b.move()
    tank.power_up()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()