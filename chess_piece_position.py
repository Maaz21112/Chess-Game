import pygame
from pyarray import Array

# window dimensions
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# CHESS BOARD dimensions
CHESS_ROWS = 8
CHESS_COLS = 8
# SQSIZE is size of one square of chess board
SQSIZE = 700 // CHESS_COLS

class Mouse_motion:

    def __init__(self):
        self.piece = None
        self.mouse_motion = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def new_mouse_position(self, pos):
        self.mouseX, self.mouseY = pos # (xcor, ycor)

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def undrag_piece(self):
        self.piece = None
        self.mouse_motion = False



    # in order to show selected piece motion we will change that selected piece image size to a bigger size by using image of 128 px
    def update_image(self, surface):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # img
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)

    def drag_piece(self, piece):
        self.piece = piece
        self.mouse_motion= True

    

class Chess_Square_Space:
    
    SQUARE_NAME=Array(8)
    
    SQUARE_NAME =['a','b','c','d','e','f','g','h']

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.square_name = self.SQUARE_NAME[col]
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
     
    # checking for a piece at that particular square ,piece=none (default)
    def has_piece(self):
        return self.piece != None

    
    def isempty(self):
        return not self.has_piece()
    
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color


    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        
        return True


    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    


    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    

    @staticmethod
    def get_square_name(col):
        SQUARE_NAME =['a','b','c','d','e','f','g','h']
        return SQUARE_NAME[col]