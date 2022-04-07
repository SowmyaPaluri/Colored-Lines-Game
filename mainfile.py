import pygame
import math
import copy
import time
import random
from pygame.time import Clock
from pygame.event import get as get_events
from pygame import QUIT, Color, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from pygame.draw import circle as draw_circle

pygame.init()

class ColoredLines:
    def __init__(self):
        self.height = 700
        self.width = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        self.create_window()
        self.ballmap = [[1 for i in range(9)] for j in range(9)]
        self.colormap = [[[] for i in range(9)] for j in range(9)]
        self.close = False
        self.clock = pygame.time.Clock()
        self.color = ['red', 'pink', 'purple', 'yellow', 'blue', 'orange']
        self.mouse_pos = [0, 0]
        self.mouse_cond = 0
        self.last_ball = [0, 0]
        self.score = 0
    
    def creating_window(self):
        pygame.display.set_caption("COLORED LINES GAME")
        self.draw_Grid()
        pygame.display.flip()

    def events(self):
        event_list = get_events()
        for event in event_list:
            self.single_Event(event)

    def single_Event(self, event):
        if event.type == QUIT:
            self.close = True
        elif event.type == MOUSEBUTTONUP:
            self.mouse_pos[0], self.mouse_pos[1] = event.pos


    def play_game(self):
        self.generate_Ball()
        pygame.display.flip()
        while not self.close:
            self.clock.tick(30)
            self.events()
            if self.end_Game():
                self.window.fill((0, 0, 0))
                self.message_Display("GAME OVER", self.width/2, self.height/2, 50)
                time.sleep(3)
                break

    def draw_Grid(self):
        height_h = self.height
        width_w = self.width
        grid_h = height_h / 11
        lines = [((grid_h, grid_h), (grid_h, height_h - grid_h)),
                 ((grid_h, grid_h), (height_h - grid_h, grid_h)),
                 ((grid_h, height_h - grid_h), (height_h - grid_h, height_h - grid_h)),
                 ((height_h - grid_h, grid_h), (height_h - grid_h, height_h - grid_h))]
        color = Color('gray')
        for i in lines:
            pygame.draw.line(self.window, color, i[0], i[1], 2)
        for i in range(8):
            pygame.draw.line(self.window, color,
                             (grid_h * (i + 2), grid_h), (grid_h * (i + 2), height_h - grid_h))
            pygame.draw.line(self.window, color,
                             (grid_h, grid_h * (i + 2)), (height_h - grid_h, grid_h * (i + 2)))


        def generate_Ball(self):
        array = [i for i in range(81)]
        for i in range(9):
            for j in range(9):
                if self.ballmap[i][j] == 0:
                    array.remove(i * 9 + j)
        random_ball = [0, 0, 0]
        for i in range(3):
            random_ball[i] = random.choice(array)
            array.remove(random_ball[i])
            self.ballmap[int(random_ball[i] / 9)][int(random_ball[i] % 9)] = 0
        for i in range(3):
            c = random.choice(self.color)
            self.colormap[int(random_ball[i] / 9)][int(random_ball[i] % 9)] = c
        self.draw_Ball()

    def draw_Ball(self):
        self.window.fill((0, 0, 0))
        self.draw_Grid()
        grid_h = self.height / 11
        for i in range(9):
            for j in range(9):
                if self.ballmap[i][j] == 0:
                    draw_circle(self.window, Color(self.colormap[i][j]),
                                (int((i + 1.5) * grid_h), int((j + 1.5) * grid_h)),
                                int(grid_h / 5 * 2))

        pygame.display.flip()


    def end_Game(self):
        s = 0
        for i in range(9):
            for j in range(9):
                if self.ballmap[i][j] == 1:
                    s += 1
        if s > 3:
            return False
        else:
            return True

def main():
    game = ColoredLine()
    game.play_game()
    pygame.display.quit()


main()
