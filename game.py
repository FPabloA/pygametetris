import pygame
import random

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
        rows = 20   #y
        cols = 10   #x

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

        self.display = pygame.display.set_mode((window_w, window_h))
        pygame.display.set_caption('Tetris')

        self.clock = pygame.time.Clock()
    
    def createGrid(self, locked_positions={}):
        #grid is initially filled with white spaces as no pieces have been placed
        grid=[[(0,0,0) for x in range(10)] for x in range(20)] 

        #fill in colors for pieces that are already placed (from dictionary of positions?)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_positions:
                    c = locked_positions[(j,i)]
                    grid[i][j] = c
        return grid

    def getPiece(self):
        global shapes, shape_colors
        return Piece(5, 0, random.choice(shapes))
    
    def drawGrid(self, surface, row, col):
        pass

    
    def playStep(self):
        print("playing step")
        locked_positions = {}   #(x,y):(255,0,0)
        self.grid = self.createGrid(locked_positions)

        changePiece = False
        run = True
        currPiece = self.getPiece()
        nextPiece = self.getPiece()
        fall_time = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        currPiece.x -= 1
                        if not self.validSpace(currPiece, self.grid):
                            currPiece.x += 1
                    
                    elif event.key == pygame.K_RIGHT:
                        currPiece.x += 1
                        if not self.validSpace(currPiece, self.grid):
                            currPiece.x -= 1

                    elif event.key == pygame.K_UP:
                        #rotate shape
                        currPiece.rotation = currPiece.rotation + 1 % len(currPiece.shape)
                        if not self.validSpace(currPiece, self.grid):
                            currPiece.rotation = currPiece.rotation - 1 % len(currPiece.shape)
                    
                    elif event.key == pygame.K_DOWN:
                        currPiece.y += 1
                        if not self.validSpace(currPiece, self.grid):
                            currPiece.y -= 1
        
        self.drawWindow(self.display)

    def drawWindow(self, surface):
        print("in draw window")
        surface.fill((0,0,0))

        #Title
        font= pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255,255,255))

        surface.blit(label, (self.top_left_x + self.w / 2 - (label.get_width() / 2), 30))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(surface, self.grid[i][j], (self.top_left_x + j*30, self.top_left_y + i*30, 30, 30), 0)
        
        #draw grid and border
        self.drawGrid(surface, 20, 10)
        pygame.draw.rect(surface, (255, 0, 0), (self.top_left_x, self.top_left_y, self.w, self.h), 5)
        pygame.display.update()

    def validSpace(self):
        pass

    def isTopReached(self):
        #TODO write code for checking if game lost
        pass

    def move(self):
        #TODO write code for moving pieces left or right (maybe rotation should be in here)
        pass

    def rotate(self):
        #TODO write code for rotating pieces CW
        pass
    
if __name__ == '__main__':
    game = TetrisGame()
    while True:
        game_over, score = game.playStep()
        if game_over:
            print(f"Final Score:{score}")
            break
        print("in loop")

    pygame.quit()