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

class ColoredLine:
    def __init__(self):
        self.height = 700
        self.width = 900
        self.window = pygame.display.set_mode((self.width, self.height))
        self.create_window()
        self.ballmap = [[1 for i in range(9)] for j in range(9)]
        self.colormap = [[[] for i in range(9)] for j in range(9)]
        self.close = False
        self.clock = pygame.time.Clock()
        self.color = ['red', 'white', 'purple', 'yellow', 'blue', 'orange']
        self.mouse_pos = [0, 0]
        self.mouse_cond = 0
        self.last_ball = [0, 0]
        self.score = 0
    
    def create_window(self):
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
            self.move_Ball()
            self.check_Ball()
