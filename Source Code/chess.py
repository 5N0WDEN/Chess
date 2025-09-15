import pygame
import PATHS

# 70, 75, 80 Pixel
white_pawn = pygame.image.load(PATHS.WHITE_PAWN_BIG_PATH)
white_king = pygame.image.load(PATHS.WHITE_KING_BIG_PATH)
white_queen = pygame.image.load(PATHS.WHITE_QUEEN_BIG_PATH)
white_bishop = pygame.image.load(PATHS.WHITE_BISHOP_BIG_PATH)
white_knight = pygame.image.load(PATHS.WHITE_KNIGHT_BIG_PATH)
white_rook = pygame.image.load(PATHS.WHITE_ROOK_BIG_PATH)

black_pawn = pygame.image.load(PATHS.BLACK_PAWN_BIG_PATH)
black_king = pygame.image.load(PATHS.BLACK_KING_BIG_PATH)
black_queen = pygame.image.load(PATHS.BLACK_QUEEN_BIG_PATH)
black_bishop = pygame.image.load(PATHS.BLACK_BISHOP_BIG_PATH)
black_knight = pygame.image.load(PATHS.BLACK_KNIGHT_BIG_PATH)
black_rook = pygame.image.load(PATHS.BLACK_ROOK_BIG_PATH)

# 20 Pixel 
# s stands for small resolution
s_white_pawn = pygame.image.load(PATHS.WHITE_PAWN_SMALL_PATH)
s_white_king = pygame.image.load(PATHS.WHITE_KING_SMALL_PATH)
s_white_queen = pygame.image.load(PATHS.WHITE_QUEEN_SMALL_PATH)
s_white_bishop = pygame.image.load(PATHS.WHITE_BISHOP_SMALL_PATH)
s_white_knight = pygame.image.load(PATHS.WHITE_KNIGHT_SMALL_PATH)
s_white_rook = pygame.image.load(PATHS.WHITE_ROOK_SMALL_PATH)

s_black_pawn = pygame.image.load(PATHS.BLACK_PAWN_SMALL_PATH)
s_black_king = pygame.image.load(PATHS.BLACK_KING_SMALL_PATH)
s_black_queen = pygame.image.load(PATHS.BLACK_QUEEN_SMALL_PATH)
s_black_bishop = pygame.image.load(PATHS.BLACK_BISHOP_SMALL_PATH)
s_black_knight = pygame.image.load(PATHS.BLACK_KNIGHT_SMALL_PATH)
s_black_rook = pygame.image.load(PATHS.BLACK_ROOK_SMALL_PATH)

#We are assigning unique score the every valid move
# Pawn = 1
# Bishop = 3
# Rook = 5
# Knight = 3
# Queen = 9
# King = 10 

class ChessPieces:
    def __init__(self, white_pieces, black_pieces, white_captured_pieces, black_captured_pieces):
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.white_captured_pieces = white_captured_pieces
        self.black_captured_pieces = black_captured_pieces
        self.toadd = [300, 0]
#In self.toadd = [xPosition, yPosition, image, Type of pawn piece, Selected or Not selected, FirstMove] for all the present pieces
    def pawn(self):
        self.toadd.append(white_pawn)
        self.toadd.append("White Pawn")
        self.toadd[0], self.toadd[1] = 300, 87.5
        self.toadd.append("Not Selected")
        self.toadd.append("FirstMove")
        self.toadd.append(1)
        times = 8
        while times:
            self.white_pieces.append(tuple(self.toadd))
            self.toadd[0] += 87.5
            times -= 1
        self.toadd[0], self.toadd[1] = 300, 525
        self.toadd[2] = black_pawn
        self.toadd[3] = "Black Pawn"
        times = 8
        while times:
            self.black_pieces.append(tuple(self.toadd))
            self.toadd[0] += 87.5
            times -= 1
        
    def knight(self):
        self.toadd[0], self.toadd[1] = 300 + 87.5, 0
        self.toadd[2] = white_knight
        self.toadd[3] = "White Knight"
        self.toadd[6] = 3
        times = 2
        while times:
            self.white_pieces.append(tuple(self.toadd))
            self.toadd[0] += 5 * 87.5
            times -= 1
        self.toadd[0], self.toadd[1] = 300 + 87.5, 612.5  
        self.toadd[2] = black_knight
        self.toadd[3] = "Black Knight"
        times = 2
        while times:
            self.black_pieces.append(tuple(self.toadd))
            self.toadd[0] += 5 * 87.5
            times -= 1

    def rook(self):
        self.toadd[0], self.toadd[1] = 300, 0
        self.toadd[2] = white_rook
        self.toadd[3] = "White Rook"
        self.toadd[6] = 5
        times = 2
        while times:
            self.white_pieces.append(tuple(self.toadd))
            self.toadd[0] += 7 * 87.5
            times -= 1
        self.toadd[0], self.toadd[1] = 300, 612.5
        self.toadd[2] = black_rook
        self.toadd[3] = "Black Rook"
        times = 2
        while times:
            self.black_pieces.append(tuple(self.toadd))
            self.toadd[0] += 7 * 87.5
            times -= 1

    def bishop(self):
        self.toadd[0], self.toadd[1] = 300 + 175, 0
        self.toadd[2] = white_bishop
        self.toadd[3] = "White Bishop"
        self.toadd[6] = 3
        times = 2
        while times:
            self.white_pieces.append(tuple(self.toadd))
            self.toadd[0] += 3 * 87.5
            times -= 1
        self.toadd[0], self.toadd[1] = 300 + 175, 612.5
        self.toadd[2] = black_bishop
        self.toadd[3] = "Black Bishop"
        times = 2
        while times:
            self.black_pieces.append(tuple(self.toadd))
            self.toadd[0] += 3 * 87.5
            times -= 1

    def king(self):
        self.toadd[0], self.toadd[1] = 300 + (3 * 87.5), 0
        self.toadd[2] = white_king
        self.toadd[3] = "White King"
        self.toadd[6] = 10
        self.white_pieces.append(tuple(self.toadd))
        self.toadd[1] = 612.5
        self.toadd[2] = black_king
        self.toadd[3] = "Black King"
        self.black_pieces.append(tuple(self.toadd))

    def queen(self):
        self.toadd[0], self.toadd[1] = 300 + (4 * 87.5), 0
        self.toadd[2] = white_queen
        self.toadd[3] = "White Queen"
        self.toadd[6] = 9
        self.white_pieces.append(tuple(self.toadd))
        self.toadd[1] = 612.5
        self.toadd[2] = black_queen
        self.toadd[3] = "Black Queen"
        self.black_pieces.append(tuple(self.toadd))
    
    #For the captured pieces in toadd = [small PieceImg, Piece Type, No. of pieces captured] for all the captured pieces
    def captured(self):
        while len(self.toadd):
            self.toadd.pop()
        # For the White guys
        self.toadd.append(s_white_pawn)
        self.toadd.append("White Pawn")
        self.toadd.append(0)
        self.white_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_white_rook
        self.toadd[1] = "White Rook"
        self.white_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_white_king
        self.toadd[1] = "White King"
        self.white_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_white_knight
        self.toadd[1] = "White Knight"
        self.white_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_white_bishop
        self.toadd[1] = "White Bishop"
        self.white_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_white_queen
        self.toadd[1] = "White Queen"
        self.white_captured_pieces.append(tuple(self.toadd))

        # For the Black guys
        self.toadd[0] = s_black_pawn
        self.toadd[1] = "Black Pawn"
        self.black_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_black_rook
        self.toadd[1] = "Black Rook"
        self.black_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_black_king
        self.toadd[1] = "Black King"
        self.black_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_black_knight
        self.toadd[1] = "Black Knight"
        self.black_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_black_bishop
        self.toadd[1] = "Black Bishop"
        self.black_captured_pieces.append(tuple(self.toadd))
        self.toadd[0] = s_black_queen
        self.toadd[1] = "Black Queen"
        self.black_captured_pieces.append(tuple(self.toadd))
        
    def create(self):
        self.pawn()
        self.knight()
        self.rook()
        self.bishop()
        self.king()
        self.queen()
        self.captured()
        return self.white_pieces, self.black_pieces, self.white_captured_pieces, self.black_captured_pieces