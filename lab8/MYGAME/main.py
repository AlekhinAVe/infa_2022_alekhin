import pygame
from pygame.draw import *
from random import randint

pygame.init()

WIDTH = 800
HEIGHT = 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 35

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


text_font = pygame.font.SysFont("Comic Sans", 24)

global scores
scores = 0

global data
data = []

def new_ball():
    '''
        Создает обычный мяч
        x, y - координаты центра мяча
        r - радиус мяча
        color - рандомный цвет из списка
        vx - скорость мяча по ox
        vy - скорость мяча по oy
    '''
    x = randint(100,700)
    y = randint(100,540)
    r = randint(50,60)
    color = GAME_COLORS[randint(0, 5)]
    vx = randint(-10, 10)
    vy = randint(-10, 10)
    circle(sc, color, (x, y), r)
    data.append([x, y, r, color, vx, vy, 0])

def new_circle():
    '''
        Создает малый быстрый мяч
        x, y - координаты центра мяча
        r - радиус мяча
        color - рандомный цвет из списка
        vx - скорость мяча по ox
        vy - скорость мяча по oy
    '''
    x = randint(100,700)
    y = randint(100,570)
    r = randint(20,30)
    color = GAME_COLORS[randint(0, 5)]
    vx = randint(-20, 20)
    vy = randint(-20, 20)
    circle(sc, color, (x, y), r)
    circle(sc, (255, 255, 255), (x, y), r, 5)
    data.append([x, y, r, color, vx, vy, 1])

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    '''
        Функция отображения счета
        surf - экран
        text - счет
        size - не очень большой размер
        x, y - координаты центра текста
    '''
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def click(event, data):
    '''
        Проверяет наличие клика на мяч и реализовывает счет
        Сначала - сравнивает координаты клика с множеством точек окружностей
        Потом засчитывает очки: 1 за обычный мяч, 5 за необычный
        '''
    global scores
    p = 0
    for i in range(len(data)):
        a = ((event[0] - data[i][0]) ** 2 + (event[1] - data[i][1]) ** 2) ** 0.5
        if a < data[i][2] and data[i][6] == 0:
            p += 1
        elif a < data[i][2] and data[i][6] == 1:
            p += 5
        else:
            continue
    if p > 4:
        scores += 5
        return True
    elif p != 0:
        scores += 1
        return True
    else:
        return False



pygame.display.update()
clock = pygame.time.Clock()
finished = False

#начальное состояние
qball = randint(3, 4)
for i in range(qball):
    new_ball()
for i in range(5 - qball):
    new_circle()


while not finished:
    clock.tick(FPS)
    sc.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (click(event.pos, data)):
                sc.fill(BLACK)
                data = [] #стирает данные для следующего этапа
                qball = randint(3, 4)
                for i in range(qball):
                    new_ball()
                for i in range(5-qball):
                    new_circle()



    for i in range(len(data)):
        data[i][0] += data[i][4] #изменение координат
        data[i][1] += data[i][5]

        # рассмотрен случай столкновения со стеной и случайное изменение скоростей всвязи с этим
        if data[i][6] == 0:
            if data[i][0] + data[i][2] >= WIDTH:
                data[i][4] = randint(-10, 1)
            elif data[i][0] - data[i][2] <= 0:
                data[i][4] = randint(1, 10)
            if data[i][1] + data[i][2] >= HEIGHT:
                data[i][5] = randint(-10, 1)
            elif data[i][1] - data[i][2] <= 0:
                data[i][5] = randint(1, 10)
            circle(sc, data[i][3], (data[i][0], data[i][1]), data[i][2])

        elif data[i][6] == 1:
            if data[i][0] + data[i][2] >= WIDTH:
                data[i][4] = randint(-20, 1)
            elif data[i][0] - data[i][2] <= 0:
                data[i][4] = randint(1, 20)
            if data[i][1] + data[i][2] >= HEIGHT:
                data[i][5] = randint(-20, 1)
            elif data[i][1] - data[i][2] <= 0:
                data[i][5] = randint(1, 20)
            circle(sc, data[i][3], (data[i][0], data[i][1]), data[i][2])
            circle(sc, (255, 255, 255), (data[i][0], data[i][1]), data[i][2], 5)

    draw_text(sc, 'Твой счет: ' + str(scores), 26, WIDTH / 2, 10)
    pygame.display.update()


pygame.quit()

