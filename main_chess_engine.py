import sys
import os
import copy

import pygame

from chess_piece_position import *
from array2d import Array2D

class Game_themes:

    def __init__(self, lg_background, dark_background, 
                       light_trace, dark_trace,
                       light_moves, dark_moves):
        
        self.bg = Shades(lg_background, dark_background)
        self.trace = Shades(light_trace, dark_trace)
        self.moves = Shades(light_moves, dark_moves)

# this class contains property of each chess piece 
class Piece_Properties:

    def __init__(self, piece_name, color, texture=None, texture_rect=None):
        self.piece_name = piece_name
        self.color = color
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def reset_moves(self):
        self.moves = []

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'resources/images/imgs-{size}px/{self.color}_{self.piece_name}.png')

#  this method will add all moves that the particular piece can make into move list
    def add_move(self, move):
        self.moves.append(move)

class King(Piece_Properties):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color)

class Pawn(Piece_Properties):
    # creates a pawn  image by calling super  and set attributes 
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color)

class Knight(Piece_Properties):

    def __init__(self, color):
        super().__init__('knight', color)

class Rook(Piece_Properties):

    def __init__(self, color):
        super().__init__('rook', color)

class King(Piece_Properties):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color)

class Bishop(Piece_Properties):

    def __init__(self, color):
        super().__init__('bishop', color)

class Queen(Piece_Properties):

    def __init__(self, color):
        super().__init__('queen', color)


class Sound_Effect:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)

class Piece_Move_Position:
    
    # it will save initial anf final position of piece

    def __init__(self, initial, final):
        # initial and final are squares
        self.initial = initial
        self.final = final
    

    # checking if the two are equal
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

class Display_Valid_Moves_On_Board:

    # this class creates chess pieces and their valid moves 

    def __init__(self):
        #2D array (for each column creates a list of 8 zeros)
        self.squares=Array2D(8,8)
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(CHESS_COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound_Effect(
                        os.path.join('resources/sounds/capture.wav'))
                    sound.play()
            
            # pawn promotion
            else:
                self.pawn_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.king_castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.reset_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def pawn_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def king_castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, Pawn):
            return

        for row in range(CHESS_ROWS):
            for col in range(CHESS_COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(CHESS_ROWS):
            for col in range(CHESS_COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        return False

    def calc_moves(self, piece, row, col, bool=True):
        # Calculate all the possible (valid) moves of a specific piece on a specific position
        
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Chess_Square_Space.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Chess_Square_Space(row, col)
                        final = Chess_Square_Space(possible_move_row, col)
                        # create a new move
                        move = Piece_Move_Position(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Chess_Square_Space.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Chess_Square_Space(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Chess_Square_Space(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Piece_Move_Position(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en pessant
            if Chess_Square_Space.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Chess_Square_Space(row, col)
                            final = Chess_Square_Space(fr, col-1, p)
                            # create a new move
                            move = Piece_Move_Position(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
            
            # right en pessant
            if Chess_Square_Space.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Chess_Square_Space(row, col)
                            final = Chess_Square_Space(fr, col+1, p)
                            # create a new move
                            move = Piece_Move_Position(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)


        def knight_moves():
            # 8 possible moves
            possible_moves=Array2D(8,2)
            possible_moves = [[row-2, col+1],[row-1, col+2],[row+1, col+2],[row+2, col+1],[row+2, col-1],[row+1, col-2],[row-1, col-2],[row-2, col-1]]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Chess_Square_Space.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Chess_Square_Space(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Chess_Square_Space(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Piece_Move_Position(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Chess_Square_Space.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Chess_Square_Space(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Chess_Square_Space(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Piece_Move_Position(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs=Array2D(8,2)
            adjs = [[row-1, col+0], [row-1, col+1], [row+0, col+1],[row+1, col+1],[row+1, col+0], [row+1, col-1], [row+0, col-1], [row-1, col-1]]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Chess_Square_Space.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Chess_Square_Space(row, col)
                        final = Chess_Square_Space(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = Piece_Move_Position(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Chess_Square_Space(row, 0)
                                final = Chess_Square_Space(row, 3)
                                moveR = Piece_Move_Position(initial, final)

                                # king move
                                initial = Chess_Square_Space(row, col)
                                final = Chess_Square_Space(row, 2)
                                moveK = Piece_Move_Position(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Chess_Square_Space(row, 7)
                                final = Chess_Square_Space(row, 5)
                                moveR =Piece_Move_Position(initial, final)

                                # king move
                                initial = Chess_Square_Space(row, col)
                                final = Chess_Square_Space(row, 6)
                                moveK = Piece_Move_Position(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()

        elif isinstance(piece, Bishop):   
            straightline_moves([[-1, 1],[-1, -1], [1, 1],[1, -1]])

        elif isinstance(piece, Rook): 
            straightline_moves([[-1, 0],[0, 1],[1, 0],[0, -1]])

        elif isinstance(piece, Queen): 
            straightline_moves([[-1, 1], [-1, -1],[1, 1],[1, -1],[-1, 0],[0, 1],[1, 0],[0, -1]])

        elif isinstance(piece, King): 
            king_moves()

    def _create(self):

        # for each chess board square creates an instance of square class
        for row in range(CHESS_ROWS):
            for col in range(CHESS_COLS):
                self.squares[row][col] = Chess_Square_Space(row, col)

    def _add_pieces(self, color):
        # for white pieces we will use row 6 and 7
        if color == 'white':
                     row_pawn=6
                     row_other=7
        # for black pieces we will use row 0 and 1
        else:
            row_pawn=1
            row_other= 0
            
        #  adding pawns to chess board
        for i in range(CHESS_COLS):
            # loop runs for every column of chess board and adds a pawn to that particular row
            # the square that was initially set to piece=none will reset to piece=pawn  on that particular row and column 
            self.squares[row_pawn][i] = Chess_Square_Space(row_pawn, i, Pawn(color))

        # adding knights to chess board
        self.squares[row_other][1] = Chess_Square_Space(row_other, 1, Knight(color))
        self.squares[row_other][6] = Chess_Square_Space(row_other, 6, Knight(color))

        #  adding bishops to chess board
        self.squares[row_other][2] = Chess_Square_Space(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Chess_Square_Space(row_other, 5, Bishop(color))

        # adding rooks to chess boardto chess board
        self.squares[row_other][0] = Chess_Square_Space(row_other, 0, Rook(color))
        self.squares[row_other][7] = Chess_Square_Space(row_other, 7, Rook(color))

        # adding queen to chess board
        self.squares[row_other][3] = Chess_Square_Space(row_other, 3, Queen(color))

        # adding king to chess board
        self.squares[row_other][4] = Chess_Square_Space(row_other, 4, King(color))



class Shades:

    def __init__(self, light_shade, dark_shade):
        self.light_shade = light_shade
        self.dark_shade = dark_shade
 
class Display_theme:

    def __init__(self):
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound_Effect(
            os.path.join('resources/sounds/move.wav'))
        self.capture_sound = Sound_Effect(
            os.path.join('resources/sounds/capture.wav'))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Game_themes((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Game_themes((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Game_themes((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Game_themes((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')

        self.themes = [gray, brown, blue,green]

class Display_Game:

    def __init__(self):
        self.player = 'white'
        self.board = Display_Valid_Moves_On_Board()
        self.dragger = Mouse_motion()
        self.config = Display_theme()

    # display background color 

    def show_bg(self, surface):
         # default gray theme
        theme = self.config.theme
        
        for row in range(CHESS_ROWS):
            for col in range(CHESS_COLS):
                # colors
                
                if (row + col) % 2 == 0 :
                    color = theme.bg.light_shade
                else:
                 color= theme.bg.dark_shade

                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark_shade if row % 2 == 0 else theme.bg.light_shade
                    # label
                    lbl = self.config.font.render(str(CHESS_ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark_shade if (row + col) % 2 == 0 else theme.bg.light_shade
                    # label
                    lbl = self.config.font.render(Chess_Square_Space.get_square_name(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, WINDOW_HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)
    
    # display chess pieces
    def show_pieces(self, surface):
        for row in range(CHESS_ROWS):
            for col in range(CHESS_COLS):
                # first check if it has piece 
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.mouse_motion:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light_shade if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark_shade
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light_shade if (pos.row + pos.col) % 2 == 0 else theme.trace.dark_shade
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    # other methods

    def next_turn(self):
        self.player = 'white' if self.player == 'black' else 'black'

 
    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()

class Start_game_events:
    # display main window/game main_screen
    pygame.init()
    window = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    pygame.display.set_caption('CHESS ENGINE')
    game = Display_Game()


    
    def main_events(self):
    # responsible for calling all other classes functions

        main_screen = self.window
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # show methods

            game.show_bg(main_screen)
            game.show_last_move(main_screen)
            game.show_moves(main_screen)
            game.show_pieces(main_screen)
           

            if dragger.mouse_motion:
                dragger.update_image(main_screen)
            #  To get the state of various input devices
            for event in pygame.event.get():

                # click events
                # mousebuttondown is selecting chess piece event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # event.pos is position of the point selected in x ,y plane
                    dragger.new_mouse_position(event.pos)
                    # the actual column and actual row of selected point or square on chess board
                    clicked_row = dragger.mouseY // SQSIZE 
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    #  after selecting a square we need to check whether that square contains a chess piece or not 
                    # if it does then we need to check if the square contains same  color piece as that of the player 
                    # finally we display all possible moves or valid moves  that this piece can make with red squares 
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(main_screen)
                            game.show_last_move(main_screen)
                            game.show_moves(main_screen)
                            game.show_pieces(main_screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                

                    if dragger.mouse_motion:
                        dragger.new_mouse_position(event.pos)
                        # show methods
                        game.show_bg(main_screen)
                        game.show_last_move(main_screen)
                        game.show_moves(main_screen)
                        game.show_pieces(main_screen)
                      
                        dragger.update_image(main_screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.mouse_motion:
                        dragger.new_mouse_position(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Chess_Square_Space(dragger.initial_row, dragger.initial_col)
                        final = Chess_Square_Space(released_row, released_col)
                        move = Piece_Move_Position(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)                            

                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(main_screen)
                            game.show_last_move(main_screen)
                            game.show_pieces(main_screen)
                            # next turn
                            game.next_turn()

                        else:
                            break

                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                     # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # to make the display Surface actually appear on the user's monitor.
            pygame.display.update()





# main_game = Start_game_events()
# main_game.main_events()