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
