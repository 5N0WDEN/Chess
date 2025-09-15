import pygame
import time
import random

class Computer:
    def __init__(self, compMove) -> None:
        self.compMove = compMove
        self.vsComp = True

    def update(self, white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, move, currentMove, drawChess):
        self.drawChess = drawChess
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.white_captured_pieces = white_captured_pieces
        self.black_captured_pieces = black_captured_pieces
        self.move = move
        self.compMove = currentMove

    def play(self):
        self.move.checkDrawvalue()
        if self.compMove == "Black":
            self.white_pieces = self.move.deselect(self.white_pieces)
            self.black_pieces = self.move.deselect(self.black_pieces)
            return self.white_pieces, self.black_pieces, self.white_captured_pieces, self.black_captured_pieces, self.selectb()
        if self.compMove == "White":
            self.white_pieces = self.move.deselect(self.white_pieces)
            self.black_pieces = self.move.deselect(self.black_pieces)
            return self.white_pieces, self.black_pieces, self.white_captured_pieces, self.black_captured_pieces, self.selectw()
        
    def selectw(self):
        run = True
        if not self.move.checkMate():
            while run:
                pos = pygame.mouse.get_pos()
                i = random.randint(0, len(self.white_pieces) - 1)
                temp = self.white_pieces.pop(i)
                temp = list(temp)
                temp[4] = "Selected"
                self.white_pieces.insert(i, tuple(temp))
                self.move.update(pos, self.white_pieces, self.black_pieces, self.black_captured_pieces, self.vsComp)
                for piece in self.white_pieces:
                    if piece[4] == "Selected":
                        self.move.allPossibleOpponentMoves()
                        self.move.check()
                        possiblePosition = self.move.calcutePosiblePositions(piece)
                        self.drawChess.updatemapPosiblePosition(possiblePosition)
                        if len(possiblePosition) != 0:
                            if self.move.isCheck:
                                if len([x for x in possiblePosition if x[2] == "Defence"]) != 0:
                                    choice = random.choice([x for x in possiblePosition if x[2] == "Defence"])
                                    choice = random.choice([x for x in possiblePosition if x[2] == "Defence"])
                                    run = False
                                else:
                                    self.white_pieces = self.move.deselect(self.white_pieces)
                            elif not self.move.isCheck:
                                if len([x for x in possiblePosition if x[2] == "Attack" or x[2] == "Defence" or x[2] == "LeftCasteling" or x[2] == "RightCasteling" or x[2] == "Promotion"]) != 0:
                                    choice = random.choice([x for x in possiblePosition if x[2] == "Attack" or x[2] == "Defence" or x[2] == "LeftCasteling" or x[2] == "RightCasteling" or x[2] == "Promotion"])
                                    choice = random.choice([x for x in possiblePosition if x[2] == "Attack" or x[2] == "Defence" or x[2] == "LeftCasteling" or x[2] == "RightCasteling" or x[2] == "Promotion"])
                                    if choice != "Block":
                                        run = False
                                    else:
                                        self.white_pieces = self.move.deselect(self.white_pieces)
                                else:
                                    self.white_pieces = self.move.deselect(self.white_pieces)
                        else:
                            self.white_pieces = self.move.deselect(self.white_pieces)
                        '''if len(possiblePosition) != 0:
                            run = False
                        else:
                            self.white_pieces = self.move.deselect(self.white_pieces)'''

            #choice = random.choice(possiblePosition)
            self.move.changeXYPosition(choice)
            self.move.updateCapturedStatus(choice)
            print(f"{choice} is the my move.")
            time.sleep(0.05)
            self.drawChess.updatemapPosiblePosition([])
            return "Black"
        

    def selectb(self):
        run = True
        if not self.move.checkMate():
            while run:
                pos = pygame.mouse.get_pos()
                i = random.randint(0, len(self.black_pieces) - 1)
                temp = self.black_pieces.pop(i)
                temp = list(temp)
                temp[4] = "Selected"
                self.black_pieces.insert(i, tuple(temp))
                self.move.update(pos, self.black_pieces, self.white_pieces, self.white_captured_pieces, self.vsComp)
                for piece in self.black_pieces:
                    if piece[4] == "Selected":
                        self.move.allPossibleOpponentMoves()
                        self.move.check()
                        possiblePosition = self.move.calcutePosiblePositions(piece)
                        self.drawChess.updatemapPosiblePosition(possiblePosition)
                        if len(possiblePosition) != 0:
                            if self.move.isCheck:
                                if len([x for x in possiblePosition if x[2] == "Defence"]) != 0:
                                    choice = random.choice([x for x in possiblePosition if x[2] == "Defence"])
                                    run = False
                                else:
                                    self.black_pieces = self.move.deselect(self.black_pieces)
                            elif not self.move.isCheck:
                                if len([x for x in possiblePosition if x[2] == "Attack" or x[2] == "Defence" or x[2] == "LeftCasteling" or x[2] == "RightCasteling" or x[2] == "Promotion"]) != 0:
                                    choice = random.choice([x for x in possiblePosition if x[2] == "Attack" or x[2] == "Defence" or x[2] == "LeftCasteling" or x[2] == "RightCasteling" or x[2] == "Promotion"])
                                    if choice != "Block":
                                        run = False
                                    else:
                                        self.black_pieces = self.move.deselect(self.black_pieces)
                                else:
                                    self.black_pieces = self.move.deselect(self.black_pieces)
                        else:
                            self.black_pieces = self.move.deselect(self.black_pieces)

            self.move.changeXYPosition(choice)
            self.move.updateCapturedStatus(choice)
            print(f"{choice} is the my move.")
            time.sleep(0.05)
            self.drawChess.updatemapPosiblePosition([])
            return "White"