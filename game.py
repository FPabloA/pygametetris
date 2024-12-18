import pygame


pygame.init()
pygame.font.init()
font = pygame.font.SysFont('arial', 25)

class TetrisGame():
    def __init_(self, w=200, h = 400):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

    def spawnPiece(self):
        #TODO write code for placing a starting piece
    
    def playStep(self):
        #TODO write code for advancing the game a step

    def isTopReached(self):
        #TODO write code for checking if game lost

    def move(self):
        #TODO write code for moving pieces left or right (maybe rotation should be in here)

    def rotate(self):
        #TODO write code for rotating pieces CW
    
if __name__ == '__main__':
    game = TetrisGame()
    while True:
        game_over, score = game.play_step()
        if game_over:
            print(f"Final Score:{score}")
            break
    pygame.quit()