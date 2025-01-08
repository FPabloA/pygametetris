import pygame
import random

import pygame.docs

#tetris code being adapted from https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('arial', 25)

# SHAPE FORMATS
S = [['.....',  #rotation 0
      '......',
      '..00..',
      '.00...',
      '.....'],

     ['.....',  #rotation 1
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',  #rotation 0
      '.....',
      '.00..',
      '..00.',
      '.....'],

     ['.....',  #rotation 1
      '..0..',
      '.00..',
      '.0...',
      '.....']]


I = [['..0..',  #rotation 0
      '..0..',
      '..0..',
      '..0..',
      '.....'],

     ['.....',  #rotation 1
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',  #rotation 0
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....', #rotation 0
      '.0...',
      '.000.',
      '.....',
      '.....'],

     ['.....', #rotation 1
      '..00.',
      '..0..',
      '..0..',
      '.....'],

     ['.....', #rotation 2
      '.....',
      '.000.',
      '...0.',
      '.....'],

     ['.....', #rotation 3
      '..0..',
      '..0..',
      '.00..',
      '.....']]


L = [['.....', #rotation 0
      '...0.',
      '.000.',
      '.....',
      '.....'],

     ['.....', #rotation 1
      '..0..',
      '..0..',
      '..00.',
      '.....'],

     ['.....', #rotation 2
      '.....',
      '.000.',
      '.0...',
      '.....'],

     ['.....', #rotation 3
      '.00..',
      '..0..',
      '..0..',
      '.....']]


T = [['.....', #rotation 0
      '..0..',
      '.000.',
      '.....',
      '.....'],

     ['.....', #rotation 1
      '..0..',
      '..00.',
      '..0..',
      '.....'],

     ['.....', #rotation 2
      '.....',
      '.000.',
      '..0..',
      '.....'],

     ['.....', #rotation 3
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece():
        def __init__(self, col, row, shape):
            self.x = col
            self.y = row
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]
            self.rotation = 0

class TetrisGame():

    def __init__(self, window_w=800, window_h=700, play_w=300, play_h = 600):
        self.w = play_w     #30 width per block
        self.h = play_h     #20 heigth per block
        self.top_left_x = (window_w - self.w) // 2
        self.top_left_y = (window_h - self.h)

        self.grid = [[]]

        self.score = 0

        self.display = pygame.display.set_mode((window_w, window_h))
        pygame.display.set_caption('Tetris')

        self.clock = pygame.time.Clock()
    
    def createGrid(self, locked_positions={}):
        #grid is initially filled with white spaces as no pieces have been placed
        grid=[[(0,0,0) for _ in range(10)] for _ in range(20)] 

        #fill in colors for pieces that are already placed (from dictionary of positions?)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_positions:
                    c = locked_positions[(j,i)]
                    grid[i][j] = c
        return grid

    def getPiece(self):
        return Piece(5, 0, random.choice(shapes))

    def checkLost(self, positions):
        for pos in positions:
            x,y = pos
            if y < 1:
                return True
        return False
    
    def drawGrid(self):
        sx = self.top_left_x
        sy = self.top_left_y

        for i in range(len(self.grid)):
            pygame.draw.line(self.display, (128,128,128), (sx, sy + i * 30), (sx + self.w, sy + i * 30))
            
            for j in range(len(self.grid[i])):
                pygame.draw.line(self.display, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + self.h))

    
    def playStep(self):
        locked_positions = {}   #(x,y):(255,0,0)
        self.grid = self.createGrid(locked_positions)

        changePiece = False
        run = True
        currPiece = self.getPiece()
        nextPiece = self.getPiece()

        fall_time = 0
        fall_speed = 0.27
        level_time = 0


        while run:

            self.grid = self.createGrid(locked_positions)
            level_time += self.clock.get_rawtime()
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            if level_time/1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005

            #piece falling
            if fall_time/1000 >= fall_speed:
                fall_time = 0
                currPiece.y += 1
                if not(self.validSpace(currPiece)) and currPiece.y > 0:
                    currPiece.y -= 1
                    changePiece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        currPiece.x -= 1
                        if not self.validSpace(currPiece):
                            currPiece.x += 1
                    
                    elif event.key == pygame.K_RIGHT:
                        currPiece.x += 1
                        if not self.validSpace(currPiece):
                            currPiece.x -= 1

                    elif event.key == pygame.K_UP:
                        #rotate shape
                        currPiece.rotation = currPiece.rotation + 1 % len(currPiece.shape)
                        if not self.validSpace(currPiece):
                            currPiece.rotation = currPiece.rotation - 1 % len(currPiece.shape)
                    
                    elif event.key == pygame.K_DOWN:
                        currPiece.y += 1
                        if not self.validSpace(currPiece):
                            currPiece.y -= 1

            shapePos = self.convShape(currPiece)

            for i in range(len(shapePos)):
                x, y = shapePos[i]
                if y > -1:
                    self.grid[y][x] = currPiece.color
            
            if changePiece:
                for pos in shapePos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = currPiece.color
                currPiece = nextPiece
                nextPiece = self.getPiece()
                changePiece = False
            
                self.score += self.clearRows(locked_positions) * 10

        
            self.drawWindow(self.display)
            self.drawNextShape(nextPiece)
            pygame.display.update()

            if self.checkLost(locked_positions):
                run = False
        
        return (True, self.score)


    def drawWindow(self, surface):
        surface.fill((0,0,0))

        #Title
        font= pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255,255,255))

        surface.blit(label, (self.top_left_x + self.w / 2 - (label.get_width() / 2), 30))

        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(self.score), 1, (255,255,255))

        sx = self.top_left_x +self.w + 50
        sy = self.top_left_y + self.h/2 - 100
        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(surface, self.grid[i][j], (self.top_left_x + j*30, self.top_left_y + i*30, 30, 30), 0)
        
        #draw grid and border
        self.drawGrid()
        pygame.draw.rect(surface, (255, 0, 0), (self.top_left_x, self.top_left_y, self.w, self.h), 5)
        pygame.display.update()


    def validSpace(self, shape):
        acceptedPos = [[(j, i) for j in range(10) if self.grid[i][j] == (0,0,0)] for i in range(20)]
        acceptedPos = [j for sub in acceptedPos for j in sub]

        formatted = self.convShape(shape)

        for pos in formatted:
            if pos not in acceptedPos:
                if pos[1] > -1:
                    return False

        return True

    def convShape(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
        
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def isTopReached(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def drawNextShape(self, shape):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255,255,255))

        sx =self.top_left_x + self.w + 50
        sy = self.top_left_y + self.h/2 - 100

        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(self.display, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)
        
        self.display.blit(label, (sx + 10, sy - 30))
    
    def clearRows(self, locked):
        inc = 0
        for i in range(len(self.grid)-1, -1, -1):
            row = self.grid[i]
            if (0,0,0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j,i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

        return inc  
    
if __name__ == '__main__':
    game = TetrisGame()
    while True:
        game_over, score = game.playStep()
        if game_over:
            print(f"Final Score:{score}")
            break
        print("in loop")

    pygame.quit()