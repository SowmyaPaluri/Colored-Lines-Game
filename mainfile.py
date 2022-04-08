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

def check_valid(mg, x, y):
    if x >= 0 and x < len(mg) and y >= 0 and y < len(mg[0]) and mg[x][y] == 1:
        return True
    else:
        return False


def process(step):
    # Checking the next point that cannot reach.
    change_records = []
    for i in range(len(step) - 1):
        if (abs(step[i][0] - step[i + 1][0]) == 0 and
            abs(step[i][1] - step[i + 1][1]) == 1) or \
                        (abs(step[i][0] - step[i + 1][0]) == 1
                        and abs(step[i][1] - step[i + 1][1]) == 0):
            pass
        else:
            change_records.append(i + 1)
    # print(change_records)
    # According to these points to find the farthest retreat point.
    clip_nums = []
    for i in change_records:
        for j in range(i):
            if (abs(step[j][0] - step[i][0]) == 0 and
                abs(step[j][1] - step[i][1]) == 1) or \
                        (abs(step[j][0] - step[i][0]) == 1 and
                        abs(step[j][1] - step[i][1]) == 0):
                break
        clip_nums.append((j, i))
    # print(clip_nums)
    # Reverse processing to prevent the mark move to below.
    record = []
    for i in clip_nums[::-1]:
        if not (i[0] in record or i[1] in record):
            step = step[:i[0] + 1] + step[i[1]:]
        record += list(range(i[0], i[1]))


step = []

# movement of the ball
def walk(mp, x, y, a, b):
    global step
    if x == a and y == b:
        step.append((x, y))
        process(step)
        return 1
    if check_valid(mp, x, y):
        step.append((x, y))
        mp[x][y] = 2
        switch = walk(mp, x, y + 1, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x, y - 1, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x - 1, y, a, b)
        if switch == 1:
            return 1
        switch = walk(mp, x + 1, y, a, b)
        if switch == 1:
            return 1

# checking row validation for the movement of the ball
def rowcheck(matrix):
    newcolumnlist = []
    for row in range(9):
        column = 0
        rowcount = 0
        columncount = 0
        columnlist = []
        zu = (row, column)
        columnlist.append(zu)

        for i in range(8):

            if matrix[row][column] == matrix[row][column + 1]:
                rowcount += 1
                zu = (row, column + 1)
                columnlist.append(zu)

            if matrix[row][column] != matrix[row][column + 1] and rowcount < 4:
                rowcount = 0
                columnlist = []
                zu = (row, column + 1)
                columnlist.append(zu)
            if matrix[row][column] != matrix[row][column + 1] and rowcount >= 4:
                break
            column += 1
        if rowcount >= 4:
            for i in columnlist:
                newcolumnlist.append(i)
        row += 1
    return(newcolumnlist)

# checking row validation for the movement of the ball
def columncheck(matrix):
    newrowlist = []
    for column in range(9):
        row = 0
        column_count = 0
        row_list = []
        z = (row, column)
        row_list.append(z)
        for i in range(8):
            if matrix[row][column] == matrix[row + 1][column]:
                column_count += 1
                z = (row+1, column)
                row_list.append(z)
            elif matrix[row][column] != matrix[row + 1][column] and column_count < 4:
                column_count = 0
                row_list = []
                z = (row + 1, column)
                row_list.append(z)
            elif matrix[row][column] != matrix[row + 1][column] and column_count >= 4:
                break
            row += 1
        if column_count >= 4:
            for i in row_list:
                newrowlist.append(i)
        column += 1
    return(newrowlist)

# checking left diagonal validation for the movement of the ball
def left_diagonal(matrix):
    column = 0
    newleftslop = []

    for column in range(5):
        row = 0
        count = 0
        leftslop = []
        a = 0
        z = ()
        if row == 0 and column == 0:
            a = 9
            z = (0, 0)
        elif row == 0 and column == 1:
            a = 8
            z = (0, 1)
        elif row == 0 and column == 2:
            a = 7
            z = (0, 2)
        elif row == 0 and column == 3:
            a = 6
            z = (0, 3)
        elif row == 0 and column == 4:
            a = 5
            z = (0, 4)
        leftslop.append(z)
        for i in range(a - 1):
                if matrix[row][column] == matrix[row + 1][column + 1]:
                    count += 1
                    z = (row+1, column+1)
                    leftslop.append(z)
                elif matrix[row][column] != matrix[row + 1][column + 1] and count < 4:
                    count = 0
                    leftslop = []
                    z = (row + 1, column + 1)
                    leftslop.append(z)
                elif matrix[row][column] != matrix[row + 1][column + 1] and count >= 4:
                    break
                row += 1
                column += 1
        if count >= 4:
            for i in leftslop:
                    newleftslop.append(i)
        column += 1
    column = 0
    row = 1
    a = 0
    leftslop = []
    for row in range(5):
        column = 0
        count = 0
        leftslop = []
        a = 0
        if row == 1 and column == 0:
            a = 8
            z = (1, 0)
        elif row == 2 and column == 0:
            a = 7
            z = (2, 0)
        elif row == 3 and column == 0:
            a = 6
            z = (3, 0)
        elif row == 4 and column == 0:
            a = 5
            z = (4, 0)
        leftslop.append(z)
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column + 1]:
                count += 1
                z = (row + 1, column + 1)
                leftslop.append(z)
            elif matrix[row][column] != matrix[row + 1][column + 1] and count < 4:
                count = 0
                leftslop = []
                z = (row + 1, column + 1)
                leftslop.append(z)
            elif matrix[row][column] != matrix[row + 1][column + 1] and count >= 4:
                break
            row += 1
            column += 1
        if count >= 4:
            for i in leftslop:
                newleftslop.append(i)
        row += 1
    return(newleftslop)

# checking right diagonal validation for the movement of the ball
def right_diagonal(matrix):
    column = 8
    newrightslop = []
    columnlist = [8, 7, 6, 5, 4]
    for g in columnlist:
        row = 0
        count = 0
        rightslop = []
        a = 0
        z = ()
        if row == 0 and g == 8:
            a = 9
            z = (0, 8)
        elif row == 0 and g == 7:
            a = 8
            z = (0, 7)
        elif row == 0 and g == 6:
            a = 7
            z = (0, 6)
        elif row == 0 and g == 5:
            a = 6
            z = (0, 5)
        elif row == 0 and g == 4:
            a = 5
            z = (0, 4)
        rightslop.append(z)
        column = g
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column - 1]:
                count += 1
                z = (row + 1, column - 1)
                rightslop.append(z)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count < 4:
                count = 0
                rightslop = []
                z = (row + 1, column - 1)
                rightslop.append(z)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count >= 4:
                break
            row += 1
            column -= 1
        if count >= 4:
            for i in rightslop:
                newrightslop.append(i)
        column -= 1
    column = 8
    row = 1
    a = 0
    rightslop = []
    for row in range(5):
        column = 8
        count = 0
        rightslop = []
        a = 0
        if row == 1 and column == 8:
            a = 8
            z = (1, 8)
        elif row == 2 and column == 8:
            a = 7
            z = (2, 8)
        elif row == 3 and column == 8:
            a = 6
            z = (3, 8)
        elif row == 4 and column == 8:
            a = 5
            z = (4, 8)
        rightslop.append(z)
        for i in range(a - 1):
            if matrix[row][column] == matrix[row + 1][column - 1]:
                count += 1
                z = (row+1, column-1)
                rightslop.append(z)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count < 4:
                count = 0
                rightslop = []
                z = (row + 1, column - 1)
                rightslop.append(z)
            elif matrix[row][column] != matrix[row + 1][column - 1] and count >= 4:
                break
            row += 1
            column -= 1
        if count >= 4:
            for i in rightslop:
                newrightslop.append(i)
        row += 1
    return(newrightslop)

# Creating a class named ColoredLine 
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
        self.color = ['red', 'pink', 'purple', 'yellow', 'blue', 'orange']
        self.mouse_pos = [0, 0]
        self.mouse_cond = 0
        self.last_ball = [0, 0]
        self.score = 0

# function for creating window 
    def create_window(self):
        pygame.display.set_caption("COLORED LINES GAME")
        self.draw_Grid()
        pygame.display.flip()
    
# function to playing the game whether it has ended or not
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
    
# function to create an event
    def events(self):
        event_list = get_events()
        for event in event_list:
            self.single_Event(event)
    
# decribing what the event happening
    def single_Event(self, event):
        if event.type == QUIT:
            self.close = True
        elif event.type == MOUSEBUTTONUP:
            self.mouse_pos[0], self.mouse_pos[1] = event.pos
            self.move_Ball()
            self.check_Ball()

# drawing of grid
    def draw_Grid(self):
        height_h = self.height
        width_w = self.width
        grid_h = height_h/11
        lines = [((grid_h, grid_h), (grid_h, height_h-grid_h)),
                 ((grid_h, grid_h), (height_h-grid_h, grid_h)),
                 ((grid_h, height_h-grid_h), (height_h-grid_h, height_h-grid_h)),
                 ((height_h-grid_h, grid_h), (height_h-grid_h, height_h-grid_h))]
        color = Color('gray')
        for i in lines:
            pygame.draw.line(self.window, color, i[0], i[1], 2)
        for i in range(8):
            pygame.draw.line(self.window, color,
                (grid_h*(i+2), grid_h), (grid_h*(i+2), height_h-grid_h))
            pygame.draw.line(self.window, color,
                (grid_h, grid_h*(i+2)), (height_h-grid_h, grid_h*(i+2)))

# Generationg the ball in the cell of the grid
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

# creating the ball structure in the cell
    def draw_Ball(self):
        self.window.fill((0, 0, 0))
        self.draw_Grid()
        grid_h = self.height/11
        for i in range(9):
            for j in range(9):
                if self.ballmap[i][j] == 0:
                    draw_circle(self.window, Color(self.colormap[i][j]),
                                    (int((i+1.5) * grid_h), int((j+1.5) * grid_h)),
                                    int(grid_h/5 * 2))
        string = "SCORE: "+str(self.score)
        width = self.height + (self.width - self.height) / 3
        self.message_Display(string, width, grid_h, 25)
        pygame.display.flip()

# Movement of ball in the cells
    def move_Ball(self):

        grid_h = self.height / 11
        x_pos = self.mouse_pos[0] - grid_h
        y_pos = self.mouse_pos[1] - grid_h
        mou_pos = [int(x_pos / grid_h), int(y_pos / grid_h)]
        if mou_pos[0] > 8 or mou_pos[1] > 8:
            return
        if self.ballmap[mou_pos[0]][mou_pos[1]] == 0:
            self.mouse_cond = 1
            self.last_ball = mou_pos
        elif self.ballmap[mou_pos[0]][mou_pos[1]] == 1:
            if self.mouse_cond == 1:
                m = copy.deepcopy(self.ballmap)
                m[self.last_ball[0]][self.last_ball[1]] = 1
                s = walk(m, self.last_ball[0], self.last_ball[1],
                    mou_pos[0], mou_pos[1])
                if(s != 1):
                    return
                self.ballmap[mou_pos[0]][mou_pos[1]] = 0
                self.ballmap[self.last_ball[0]][self.last_ball[1]] = 1
                self.colormap[mou_pos[0]][mou_pos[1]] = self.colormap[self.last_ball[0]][self.last_ball[1]]
                self.colormap[self.last_ball[0]][self.last_ball[1]] = []
                self.mouse_cond = 0
                self.draw_Ball()
                time.sleep(0.2)
                if self.check_Ball():
                    time.sleep(0.2)
                    self.generate_Ball()
            else:
                pass

# Checking the position of ball which is valid or not
    def check_Ball(self):
        s = 0
        c = columncheck(self.colormap)
        for i in c:
            if(self.ballmap[i[0]][i[1]] == 0):
                s = 1
                self.score += 2
            self.ballmap[i[0]][i[1]] = 1
        c = rowcheck(self.colormap)
        for i in c:
            if(self.ballmap[i[0]][i[1]] == 0):
                s = 1
                self.score += 2
            self.ballmap[i[0]][i[1]] = 1
        c = left_diagonal(self.colormap)
        for i in c:
            if(self.ballmap[i[0]][i[1]] == 0):
                s = 1
                self.score += 2
            self.ballmap[i[0]][i[1]] = 1
        c = right_diagonal(self.colormap)
        for i in c:
            if(self.ballmap[i[0]][i[1]] == 0):
                s = 1
                self.score += 2
            self.ballmap[i[0]][i[1]] = 1
        self.draw_Ball()
        if s == 0:
            return True

# function to end the game
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

    def text_Objects(self, text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def message_Display(self, text, width, height, size):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_Objects(text, largeText)
        TextRect.center = ((width), (height))
        self.window.blit(TextSurf, TextRect)
        pygame.display.update()

def main():
    game = ColoredLine()
    game.play_game()
    pygame.display.quit()
    
main()


