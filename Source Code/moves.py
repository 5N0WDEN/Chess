import pygame
import time
import chess
import random

pygame.init()

class Move:
    def __init__(self, drawChess, white_pieces, black_pieces, match_type):
        self.my_pieces = white_pieces
        self.oppo_pieces = black_pieces
        self.drawChess = drawChess
        self.posibleOpponentMoves = []
        self.moveStatus = "White"
        self.isCheck = False
        self.attacker = None
        self.kingPos = None
        self.vsComp = False
        self.ScoreW = 0
        self.ScoreB = 0
        self.match_type = match_type


    def clientOBJ(self, clent, username, clientMove):
        self.clent = clent
        self.username = username
        self.clientMove = clientMove

    def update(self, pos, my_pieces, oppo_pieces, oppo_captured_pieces, vsComp):
        self.pos = pos
        self.my_pieces = my_pieces
        self.oppo_pieces = oppo_pieces
        self.oppo_captured_pieces = oppo_captured_pieces
        self.vsComp = vsComp

    def updateCurrentScore(self):
        return self.ScoreW, self.ScoreB

    def mainMove(self, pos, my_pieces, oppo_pieces, oppo_captured_pieces, currntMove):#Ensures all the self methods implements properly
        self.moveStatus = currntMove
        self.pos = pos
        self.pos = [int((self.pos[0] - 300) / 87.5) * 87.5 + 300, int(self.pos[1] / 87.5) * 87.5]
        self.my_pieces = my_pieces
        self.oppo_pieces = oppo_pieces
        self.oppo_captured_pieces = oppo_captured_pieces
        self.posibleOpponentMoves = []
        for piece in my_pieces:
            if piece[4] == "Selected" and piece[3][0:5] == self.moveStatus:
                self.allPossibleOpponentMoves()
                #print(self.posibleOpponentMoves)
                self.check()
                possiblePosition = self.calcutePosiblePositions(piece)
                self.drawChess.updatemapPosiblePosition(possiblePosition)
                print(possiblePosition)
                for points in possiblePosition:
                    pos = [int((pos[0] - 300) / 87.5) * 87.5 + 300, int(pos[1] / 87.5) * 87.5]
                    if points[0] == pos[0] and points[1] == pos[1]:
                        if self.isCheck and points[2] != "Defence":
                            break
                        if points[2] == "Block":
                            break
                        self.changeXYPosition(points)
                        self.updateCapturedStatus(points)
        return self.my_pieces, self.oppo_pieces, self.oppo_captured_pieces, self.moveStatus
    
    def change_WtoB_BtoW(self):
        if self.moveStatus == "White":
            self.moveStatus = "Black"
        elif self.moveStatus == "Black":
            self.moveStatus = "White"

    def promotion(self, changePiece):       
        if self.vsComp:
            Chess = chess.ChessPieces([], [], [], [])
            white_pieces, black_pieces, white_captured_pieces, black_captured_pieces = Chess.create()
            typeOfPieces = ["Queen", "Queen", "Queen", "Rook", "Queen", "Queen", "Queen"]
            pieceType = random.choice(typeOfPieces)
            if changePiece[3][0:5] == "White":
                for piece in white_pieces:
                    if piece[3][6:] == pieceType:
                        changePiece[2] = piece[2]
                        changePiece[3] = piece[3]
            if changePiece[3][0:5] == "Black":
                for piece in black_pieces:    
                    if piece[3][6:] == pieceType:   
                        changePiece[2] = piece[2]
                        changePiece[3] = piece[3]
            return changePiece
        else:
            run = True
            while run:
                self.drawChess.actualPosition1()
                self.drawChess.promostionButtonOnhover()
                self.drawChess.drawPromotion()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.drawChess.checkButtonPromotion()

                    if event.type == pygame.MOUSEBUTTONUP:
                        run, pieceType = self.drawChess.buttonActions1()
                    self.drawChess.drawPromotion()
                pygame.display.update()
            Chess = chess.ChessPieces([], [], [], [])
            white_pieces, black_pieces, white_captured_pieces, black_captured_pieces = Chess.create()
            if changePiece[3][0:5] == "White":
                for piece in white_pieces:
                    if piece[3][6:] == pieceType:
                        changePiece[2] = piece[2]
                        changePiece[3] = piece[3]
                        self.ScoreW += 15
            if changePiece[3][0:5] == "Black":
                for piece in black_pieces:    
                    if piece[3][6:] == pieceType:   
                        changePiece[2] = piece[2]
                        changePiece[3] = piece[3] 
                        self.ScoreW += 15
            return changePiece
                    
    def changeXYPosition(self, points): # changes x and y position as per the user moves 
        changeRook = False
        for i, my in enumerate(self.my_pieces):
            if my[4] == "Selected":
                changePiece = self.my_pieces.pop(i)
                changePiece = list(changePiece)
                if changePiece[5] == "FirstMove":
                    changePiece[5] = "Not FirstMove"
                    if (changePiece[3] == "Black King" or changePiece[3] == "White King") and (points[2] == "LeftCasteling" or points[2] == "RightCasteling"):
                        changeRook = True
                    else:
                        changeRook = False
                change = tuple(changePiece)
                if points[2] == "Promotion":
                    changePiece = self.promotion(changePiece)
                changePiece[0], changePiece[1], changePiece[4] = points[0], points[1], "Not Selected"
                if changePiece[3][0:5] == "White":
                    self.ScoreW += changePiece[6]
                if changePiece[3][0:5] == "Black":
                    self.ScoreB += changePiece[6]
                self.my_pieces.insert(i, tuple(changePiece))
                self.change_WtoB_BtoW()
                if self.match_type == "OnServer":
                    self.clent.send_data_once(tuple((change, self.pos)))
                break
        if changeRook:
            for i, my in enumerate(self.my_pieces):
                if points[2] == "LeftCasteling":
                    if my[3] == "Black Rook" and my[0] == 300:
                        changePiece = self.my_pieces.pop(i)
                        changePiece = list(changePiece)
                        changePiece[0] += 2 * 87.5
                        self.my_pieces.insert(i, tuple(changePiece))
                        self.change_WtoB_BtoW()
                        self.ScoreB += 20
                        break
                    elif my[3] == "White Rook" and my[0] == 300:
                        changePiece = self.my_pieces.pop(i)
                        changePiece = list(changePiece)
                        changePiece[0] += 2 * 87.5
                        self.my_pieces.insert(i, tuple(changePiece))
                        self.change_WtoB_BtoW()
                        self.ScoreW += 20
                        break
                elif points[2] == "RightCasteling":
                    if my[3] == "Black Rook" and my[0] == 912.5:
                        changePiece = self.my_pieces.pop(i)
                        changePiece = list(changePiece)
                        changePiece[0] -= 3 * 87.5
                        self.my_pieces.insert(i, tuple(changePiece))
                        self.change_WtoB_BtoW()
                        self.ScoreB += 20
                        break
                    elif my[3] == "White Rook" and my[0] == 912.5:
                        changePiece = self.my_pieces.pop(i)
                        changePiece = list(changePiece)
                        changePiece[0] -= 3 * 87.5
                        self.my_pieces.insert(i, tuple(changePiece)) 
                        self.change_WtoB_BtoW()
                        self.ScoreW += 20
                        break  

    def updateCapturedStatus(self, points): # update captured lists
        for i, enemy in enumerate(self.oppo_pieces):
            if enemy[0] == points[0] and enemy[1] == points[1]:
                captured = self.oppo_pieces.pop(i)
                for j, capturedPieces in enumerate(self.oppo_captured_pieces):
                    if capturedPieces[1] == captured[3]:
                        update = self.oppo_captured_pieces.pop(j)
                        update = list(update)
                        update[2] += 1
                        self.oppo_captured_pieces.insert(j, tuple(update))
    
    def deselect(self, pieces): # Deselects a previously selected distinct piece
        for i, piece in enumerate(pieces):
            if piece[4] == "Selected":
                newPiece = pieces.pop(i)
                newPiece = list(newPiece)
                newPiece[4] = "Not Selected"
                newPiece = tuple(newPiece)
                pieces.insert(i, newPiece)
        return pieces
                
    
    def selection(self, pos, pieces): # Selectes a distinct piece on board
        for count, piece in enumerate(pieces):
            if (pos[0] - piece[0] > 0 and pos[0] - piece[0] < 85) and (pos[1] - piece[1] > 0 and pos[1] - piece[1] < 85):
                if piece[4] != "Selected":
                    newPiece = pieces.pop(count)
                    newPiece = list(newPiece)
                    newPiece[4] = "Selected"
                    newPiece = tuple(newPiece)
                    pieces.insert(count, newPiece)
        return pieces
    
    # Calculates all the possiblePosition for all pieces
    # whitePawn() and blackPawn() calculates respectively black and white moves
    # rook(), knight(), bishop(), queen() and king() works for both black and white pieces
    def calcutePosiblePositions(self, piece): 
        possiblePosition = []
        poping = []
        if piece[3] == "White Pawn":
            possiblePosition = self.whitePawn(piece)
        elif piece[3] == "Black Pawn":
            possiblePosition = self.blackPawn(piece)
        elif piece[3] == "Black Rook" or piece[3] == "White Rook":
            possiblePosition = self.rook(piece)
        elif piece[3] == "Black Knight" or piece[3] == "White Knight":
            possiblePosition = self.knight(piece)
        elif piece[3] == "Black Bishop" or piece[3] == "White Bishop":
            possiblePosition = self.bishop(piece)
        elif piece[3] == "Black Queen" or piece[3] == "White Queen":
            possiblePosition = self.queen(piece)
        elif piece[3] == "Black King" or piece[3] == "White King":
            possiblePosition = self.king(piece)
            if len(possiblePosition):
                for oppoPosition in self.posibleOpponentMoves:
                    for i, position in enumerate(possiblePosition):
                        if position[0] == oppoPosition[0] and position[1] == oppoPosition[1]:
                            poping.append(i)
                poping = set(poping)
                poping = list(poping)
                poping.sort()
                poping.reverse()
                for x in poping:
                    possiblePosition.pop(x)
        return possiblePosition
    
    def whitePawn(self, piece):# Calculate possiblePosition for white pawn
        possiblePosition = []
        possiblePosition.append((piece[0], piece[1] + 87.5, "Attack", "White Pawn", piece))
        if piece[5] == "FirstMove":
            possiblePosition.append((piece[0], piece[1] + 87.5 * 2, "Attack", "White Pawn", piece))
        allpieces = self.oppo_pieces + self.my_pieces
        for i, position in enumerate(possiblePosition):
            for all in allpieces:
                if position[0] == all[0] and position[1] == all[1]:
                    possiblePosition.pop(i)
                    if i == 0 and piece[5] == "FirstMove":
                        possiblePosition.pop()
                    if len(possiblePosition) == 0:
                        break
        for oppo in self.oppo_pieces:
            if oppo[0] == piece[0] + 87.5 and oppo[1] == piece[1] + 87.5:
                possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5, "Attack", "White Pawn", piece))
            if oppo[0] == piece[0] - 87.5 and oppo[1] == piece[1] + 87.5:
                possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5, "Attack", "White Pawn", piece))
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        temp[2] = "Defence"
                        possiblePosition.insert(i, tuple(temp))
        for i, posit in enumerate(possiblePosition):
            if posit[1] == 612.5:
                temp = possiblePosition.pop(i)
                temp = list(temp)
                temp[2] = "Promotion"
                possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkInFuture(possiblePosition, piece)
        return possiblePosition
    
    def checkInFuture(self, possiblePosition, piece):
        ischeck1 = self.isCheck
        if not ischeck1:
            for i, my in enumerate(self.my_pieces):
                if my == piece:
                    replace = my
                    for j, posits in enumerate(possiblePosition):
                        if posits[2] == "Attack":
                            temp = self.my_pieces.pop(i)
                            temp = list(temp)
                            temp[0], temp[1] = posits[0], posits[1]
                            self.my_pieces.insert(i, tuple(temp))
                            self.check()
                            ischeck2 = self.isCheck
                            if ischeck2:
                                changetoAttack = possiblePosition.pop(j)
                                changetoAttack = list(changetoAttack)
                                changetoAttack[2] = "Block"
                                possiblePosition.insert(j, tuple(changetoAttack))
                    temp = self.my_pieces.pop(i)
                    self.my_pieces.insert(i, replace)
        self.check()
        return possiblePosition

    def blackPawn(self, piece): # calculate possiblePosition for black Pawn
        possiblePosition = []
        possiblePosition.append((piece[0], piece[1] - 87.5, "Attack", "Black Pawn", piece))
        if piece[5] == "FirstMove":
            possiblePosition.append((piece[0], piece[1] - 87.5 * 2, "Attack", "Black Pawn", piece))
        allpieces = self.oppo_pieces + self.my_pieces
        for i, position in enumerate(possiblePosition):
            for all in allpieces:
                if position[0] == all[0] and position[1] == all[1]:
                    possiblePosition.pop(i)
                    if i == 0 and piece[5] == "FirstMove":
                        possiblePosition.pop()
                    if len(possiblePosition) == 0:
                        break
        for oppo in self.oppo_pieces:
            if oppo[0] == piece[0] + 87.5 and oppo[1] == piece[1] - 87.5:
                possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5, "Attack", "Black Pawn", piece))
            if oppo[0] == piece[0] - 87.5 and oppo[1] == piece[1] - 87.5:
                possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5, "Attack", "Black Pawn", piece))
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        temp[2] = "Defence"
                        possiblePosition.insert(i, tuple(temp))
        for i, posit in enumerate(possiblePosition):
            if posit[1] == 0:
                temp = possiblePosition.pop(i)
                temp = list(temp)
                temp[2] = "Promotion"
                possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkInFuture(possiblePosition, piece)
        return possiblePosition
    
    def rook(self, piece): # calculates all possiblePosition for rook 
        possiblePosition = []
        i = 1
        while piece[1] - 87.5 * i >= 0:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] and oppo[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0], piece[1] - 87.5 * i, "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] and my[1] == piece[1] - 87.5 * i:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0], piece[1] - 87.5 * i, "Attack", "Rook", piece))
            i += 1
        i = 1
        while piece[1] + 87.5 * i < 700:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] and oppo[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0], piece[1] + 87.5 * i, "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] and my[1] == piece[1] + 87.5 * i:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0], piece[1] + 87.5 * i, "Attack", "Rook", piece))
            i += 1
        i = 1
        while piece[0] - 87.5 * i >= 300:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] - 87.5 * i and oppo[1] == piece[1]:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1], "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] - 87.5 * i and my[1] == piece[1]:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] - 87.5 * i, piece[1], "Attack", "Rook", piece))
            i += 1
        i = 1
        while piece[0] + 87.5 * i < 950:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] + 87.5 * i and oppo[1] == piece[1]:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1], "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] + 87.5 * i and my[1] == piece[1]:
                    i = 10 
            if i == 10:
                break
            possiblePosition.append((piece[0] + 87.5 * i, piece[1], "Attack", "Rook", piece))
            i += 1
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        temp[2] = "Defence"
                        possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkInFuture(possiblePosition, piece)
        return possiblePosition
    
    def knight(self, piece): # Calculates all the valide moves for knight
        possiblePosition = []
        if self.knightValidate(piece[0] + 87.5, piece[1] + 87.5 * 2):
            possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] + 87.5, piece[1] - 87.5 * 2):
            possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] - 87.5, piece[1] + 87.5 * 2):
            possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] - 87.5, piece[1] - 87.5 * 2):
            possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] + 87.5 * 2, piece[1] - 87.5):
            possiblePosition.append((piece[0] + 87.5 * 2, piece[1] - 87.5, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] + 87.5 * 2, piece[1] + 87.5):
            possiblePosition.append((piece[0] + 87.5 * 2, piece[1] + 87.5, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] - 87.5 * 2, piece[1] - 87.5):
            possiblePosition.append((piece[0] - 87.5 * 2, piece[1] - 87.5, "Attack", "Knight", piece))
        if self.knightValidate(piece[0] - 87.5 * 2, piece[1] + 87.5):
            possiblePosition.append((piece[0] - 87.5 * 2, piece[1] + 87.5, "Attack", "Knight", piece))
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        temp[2] = "Defence"
                        possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkInFuture(possiblePosition, piece)
        return possiblePosition
    
    def knightValidate(self, xpoint, ypoint): # Helps knight() to validate the move 
        if (xpoint >= 300 and xpoint < 950) and (ypoint >= 0 and ypoint < 700):
            value = True
        else:
            value = False
        for oppo in self.oppo_pieces:
            if oppo[0] == xpoint and oppo[1] == ypoint:
                value = True
        for my in self.my_pieces:
            if my[0] == xpoint and my[1] == ypoint:
                value = False
        return value

    def bishop(self, piece): # Calculates all the possible positions of bishop and validate the position and append all possitions in list possiblePosition
        possiblePosition = []
        i = 1
        while piece[0] + 87.5 * i < 950 and piece[1] - 87.5 * i >= 0:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] + 87.5 * i and oppo[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] + 87.5 * i and my[1] == piece[1] - 87.5 * i:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] + 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        i = 1
        while piece[0] - 87.5 * i >= 300 and piece[1] - 87.5 * i >= 0:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] - 87.5 * i and oppo[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] - 87.5 * i and my[1] == piece[1] - 87.5 * i:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] - 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        i = 1
        while piece[0] + 87.5 * i < 950 and piece[1] + 87.5 * i < 700:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] + 87.5 * i and oppo[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] + 87.5 * i and my[1] == piece[1] + 87.5 * i:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] + 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        i = 1
        while piece[0] - 87.5 * i >= 300 and piece[1] + 87.5 * i < 700:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] - 87.5 * i and oppo[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] - 87.5 * i and my[1] == piece[1] + 87.5 * i:
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] - 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        temp[2] = "Defence"
                        possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkInFuture(possiblePosition, piece)
        return possiblePosition
    
    def queen(self, piece): # Uses rook() and bishop() to find the possible moves of queen
        possiblePosition = self.rook(piece) + self.bishop(piece)
        '''for i, position in enumerate(possiblePosition):
            temp = possiblePosition.pop(i)
            temp = list(temp)
            temp[3] = "Queen"
            possiblePosition.insert(i, tuple(temp))'''
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        temp[2] = "Defence"
                        possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkInFuture(possiblePosition, piece)
        return possiblePosition
    
    def king(self, piece): # Calculates all possible moves of King
        possiblePosition = []
        if (piece[0] + 87.5 >= 300 and piece[0] + 87.5 < 950) and (piece[1] >= 0 and piece[1] < 700):
            possiblePosition.append((piece[0] + 87.5, piece[1], "Attack", "King", piece))

        if (piece[0] + 87.5 >= 300 and piece[0] + 87.5 < 950) and (piece[1] + 87.5 >= 0 and piece[1] + 87.5 < 700):
            possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5, "Attack", "King", piece))

        if (piece[0] >= 300 and piece[0] < 950) and (piece[1] + 87.5 >= 0 and piece[1] + 87.5 < 700):
            possiblePosition.append((piece[0], piece[1] + 87.5, "Attack", "King", piece))

        if (piece[0] - 87.5 >= 300 and piece[0] - 87.5 < 950) and (piece[1] + 87.5 >= 0 and piece[1] + 87.5 < 700):
            possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5, "Attack", "King", piece))

        if (piece[0] - 87.5 >= 300 and piece[0] - 87.5 < 950) and (piece[1] >= 0 and piece[1] < 700):
            possiblePosition.append((piece[0] - 87.5, piece[1], "Attack", "King", piece))

        if (piece[0] - 87.5 >= 300 and piece[0] - 87.5 < 950) and (piece[1]  - 87.5 >= 0 and piece[1] - 87.5 < 700):
            possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5, "Attack", "King", piece))

        if (piece[0] >= 300 and piece[0] < 950) and (piece[1] - 87.5 >= 0 and piece[1] - 87.5 < 700):
            possiblePosition.append((piece[0], piece[1] - 87.5, "Attack", "King", piece))

        if (piece[0] + 87.5 >= 300 and piece[0] + 87.5 < 950) and (piece[1] - 87.5 >= 0 and piece[1] - 87.5 < 700):
            possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5, "Attack", "King", piece))

        poping = []
        for my in self.my_pieces:
            for j, position in enumerate(possiblePosition):
                if position[0] == my[0] and position[1] == my[1]:
                    poping.append(j)
        poping.sort()
        poping.reverse()
        for x in poping:
            possiblePosition.pop(x)
        if self.isCheck:
            for i, position in enumerate(possiblePosition):
                temp = possiblePosition.pop(i)
                temp = list(temp)
                temp[2] = "Defence"
                possiblePosition.insert(i, tuple(temp))
        possiblePosition = self.checkCastelling(possiblePosition, piece)
        if self.isCheck:
            posibleDefencePoint = self.calDefenceMoves()
            #print(posibleDefencePoint, self.attacker)
            for defence in posibleDefencePoint:
                for i, position in enumerate(possiblePosition):
                    if position[0] == defence[0] and position[1] == defence[1]:
                        temp = possiblePosition.pop(i)
                        temp = list(temp)
                        if position[0] == self.attacker[4][0] and position[1] == self.attacker[4][1]:
                            for possi in self.posibleOpponentMoves:
                                if possi[0] == self.attacker[4][0] and possi[1] == self.attacker[4][1]:
                                    temp[2] = "Attack"
                                else:
                                    temp[2] = "Defence"
                                    break
                        else:
                            temp[2] = "Attack"
                        possiblePosition.insert(i, tuple(temp))
        for i, my in enumerate(self.my_pieces):
            if my == piece:
                replace = my
                for j, posits in enumerate(possiblePosition):
                    temp = self.my_pieces.pop(i)
                    temp = list(temp)
                    temp[0], temp[1] = posits[0], posits[1]
                    self.my_pieces.insert(i, tuple(temp))
                    self.check()
                    ischeck2 = self.isCheck
                    if ischeck2:
                        changetoAttack = possiblePosition.pop(j)
                        changetoAttack = list(changetoAttack)
                        changetoAttack[2] = "Block"
                        possiblePosition.insert(j, tuple(changetoAttack))
                temp = self.my_pieces.pop(i)
                self.my_pieces.insert(i, replace)
        self.check()
        return possiblePosition

    def checkIsEmpty(self, pos, allpieces): # Helps checkCastelling() to decide wheather castelling is posible or not
        value = True
        for all in allpieces:
            if all[0] == pos[0] and all[1] == pos[1]:
                value = False
        return value

    def checkCastelling(self, possiblePosition, piece): # With help of checkIsEmpty() decides is castelling is possible or not
        if piece[3] == "Black King" and piece[5] == "FirstMove":
            for my in self.my_pieces:
                if my[3] == "Black Rook" and my[5] == "FirstMove":
                    allpieces = self.oppo_pieces + self.my_pieces
                    if my[0] > piece[0]:
                        if self.checkIsEmpty((my[0] - 87.5, my[1]), allpieces) and self.checkIsEmpty((my[0] - 87.5 * 2, my[1]), allpieces) and self.checkIsEmpty((my[0] - 87.5 * 3, my[1]), allpieces):
                            possiblePosition.append((piece[0] + 87.5 * 2, piece[1], "RightCasteling", "King", piece))
                    else:
                        if self.checkIsEmpty((my[0] + 87.5, my[1]), allpieces) and self.checkIsEmpty((my[0] + 87.5 * 2, my[1]), allpieces):
                            possiblePosition.append((piece[0] - 87.5 * 2, piece[1], "LeftCasteling", "King", piece))
        if piece[3] == "White King" and piece[5] == "FirstMove":
            for my in self.my_pieces:  
                if my[3] == "White Rook" and my[5] == "FirstMove":
                    allpieces = self.oppo_pieces + self.my_pieces
                    if my[0] > piece[0]:
                        if self.checkIsEmpty((my[0] - 87.5, my[1]), allpieces) and self.checkIsEmpty((my[0] - 87.5 * 2, my[1]), allpieces) and self.checkIsEmpty((my[0] - 87.5 * 3, my[1]), allpieces):
                            possiblePosition.append((piece[0] + 87.5 * 2, piece[1], "RightCasteling", "King", piece))
                    else:
                        if self.checkIsEmpty((my[0] + 87.5, my[1]), allpieces) and self.checkIsEmpty((my[0] + 87.5 * 2, my[1]), allpieces):
                            possiblePosition.append((piece[0] - 87.5 * 2, piece[1], "LeftCasteling", "King", piece))
        return possiblePosition

    '''def pawn(self, piece):
        possiblePosition = []
        if piece[3] == "White Pawn":
            possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5, "Attack", "White Pawn", piece))
            possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5, "Attack", "White Pawn", piece))
        if piece[3] == "Black Pawn":
            possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5, "Attack", "Black Pawn", piece))
            possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5, "Attack", "Black Pawn", piece))
        poping = []
        for my in self.my_pieces:
            for i, pos in enumerate(possiblePosition):
                if pos[0] == my[0] and pos[1] == my[1]:
                    poping.append(i)
        poping.sort()
        poping.reverse()
        if len(poping):
            for x in poping:
                possiblePosition.pop(x)
        return possiblePosition'''

    def pawnPOS(self, piece):
        possiblePosition = []
        if piece[3] == "White Pawn":
            possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5, "Attack", "White Pawn", piece))
            possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5, "Attack", "White Pawn", piece))
        if piece[3] == "Black Pawn":
            possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5, "Attack", "Black Pawn", piece))
            possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5, "Attack", "Black Pawn", piece))
        return possiblePosition

    def rookPOS(self, piece): # calculates all possiblePosition for rook 
        possiblePosition = []
        i = 1
        while piece[1] - 87.5 * i >= 0:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] and oppo[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0], piece[1] - 87.5 * i, "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] and my[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0], piece[1] - 87.5 * i, "Attack", "Rook", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0], piece[1] - 87.5 * i, "Attack", "Rook", piece))
            i += 1
        i = 1
        while piece[1] + 87.5 * i < 700:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] and oppo[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0], piece[1] + 87.5 * i, "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] and my[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0], piece[1] + 87.5 * i, "Attack", "Rook", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0], piece[1] + 87.5 * i, "Attack", "Rook", piece))
            i += 1
        i = 1
        while piece[0] - 87.5 * i >= 300:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] - 87.5 * i and oppo[1] == piece[1]:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1], "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] - 87.5 * i and my[1] == piece[1]:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1], "Attack", "Rook", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] - 87.5 * i, piece[1], "Attack", "Rook", piece))
            i += 1
        i = 1
        while piece[0] + 87.5 * i < 950:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] + 87.5 * i and oppo[1] == piece[1]:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1], "Attack", "Rook", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] + 87.5 * i and my[1] == piece[1]:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1], "Attack", "Rook", piece))
                    i = 10 
            if i == 10:
                break
            possiblePosition.append((piece[0] + 87.5 * i, piece[1], "Attack", "Rook", piece))
            i += 1
        return possiblePosition
    
    def knightPOS(self, piece): # Calculates all the valide moves for knight
        possiblePosition = []
        if self.knightValidatePOS(piece[0] + 87.5, piece[1] + 87.5 * 2):
            possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] + 87.5, piece[1] - 87.5 * 2):
            possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] - 87.5, piece[1] + 87.5 * 2):
            possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] - 87.5, piece[1] - 87.5 * 2):
            possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5 * 2, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] + 87.5 * 2, piece[1] - 87.5):
            possiblePosition.append((piece[0] + 87.5 * 2, piece[1] - 87.5, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] + 87.5 * 2, piece[1] + 87.5):
            possiblePosition.append((piece[0] + 87.5 * 2, piece[1] + 87.5, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] - 87.5 * 2, piece[1] - 87.5):
            possiblePosition.append((piece[0] - 87.5 * 2, piece[1] - 87.5, "Attack", "Knight", piece))
        if self.knightValidatePOS(piece[0] - 87.5 * 2, piece[1] + 87.5):
            possiblePosition.append((piece[0] - 87.5 * 2, piece[1] + 87.5, "Attack", "Knight", piece))
        return possiblePosition
    
    def knightValidatePOS(self, xpoint, ypoint): # Helps knight() to validate the move 
        if (xpoint >= 300 and xpoint < 950) and (ypoint >= 0 and ypoint < 700):
            value = True
        else:
            value = False
        for oppo in self.oppo_pieces:
            if oppo[0] == xpoint and oppo[1] == ypoint:
                value = True
        for my in self.my_pieces:
            if my[0] == xpoint and my[1] == ypoint:
                value = True
        return value
    
    def bishopPOS(self, piece): # Calculates all the possible positions of bishop and validate the position and append all possitions in list possiblePosition
        possiblePosition = []
        i = 1
        while piece[0] + 87.5 * i < 950 and piece[1] - 87.5 * i >= 0:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] + 87.5 * i and oppo[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] + 87.5 * i and my[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] + 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        i = 1
        while piece[0] - 87.5 * i >= 300 and piece[1] - 87.5 * i >= 0:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] - 87.5 * i and oppo[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] - 87.5 * i and my[1] == piece[1] - 87.5 * i:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] - 87.5 * i, piece[1] - 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        i = 1
        while piece[0] + 87.5 * i < 950 and piece[1] + 87.5 * i < 700:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] + 87.5 * i and oppo[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] + 87.5 * i and my[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0] + 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] + 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        i = 1
        while piece[0] - 87.5 * i >= 300 and piece[1] + 87.5 * i < 700:
            for oppo in self.oppo_pieces:
                if oppo[0] == piece[0] - 87.5 * i and oppo[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            for my in self.my_pieces:
                if my[0] == piece[0] - 87.5 * i and my[1] == piece[1] + 87.5 * i:
                    possiblePosition.append((piece[0] - 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
                    i = 10
            if i == 10:
                break
            possiblePosition.append((piece[0] - 87.5 * i, piece[1] + 87.5 * i, "Attack", "Bishop", piece))
            i += 1
        return possiblePosition
    
    def queenPOS(self, piece): # Uses rook() and bishop() to find the possible moves of queen
        possiblePosition = self.rookPOS(piece) + self.bishopPOS(piece)
        return possiblePosition

    def kingPOS(self, piece): # Calculates all possible moves of King
        possiblePosition = []
        if (piece[0] + 87.5 >= 300 and piece[0] + 87.5 < 950) and (piece[1] >= 0 and piece[1] < 700):
            possiblePosition.append((piece[0] + 87.5, piece[1], "Attack", "King", piece))
        if (piece[0] + 87.5 >= 300 and piece[0] + 87.5 < 950) and (piece[1] + 87.5 >= 0 and piece[1] + 87.5 < 700):
            possiblePosition.append((piece[0] + 87.5, piece[1] + 87.5, "Attack", "King", piece))
        if (piece[0] >= 300 and piece[0] < 950) and (piece[1] + 87.5 >= 0 and piece[1] + 87.5 < 700):
            possiblePosition.append((piece[0], piece[1] + 87.5, "Attack", "King", piece))
        if (piece[0] - 87.5 >= 300 and piece[0] - 87.5 < 950) and (piece[1] + 87.5 >= 0 and piece[1] + 87.5 < 700):
            possiblePosition.append((piece[0] - 87.5, piece[1] + 87.5, "Attack", "King", piece))
        if (piece[0] - 87.5 >= 300 and piece[0] - 87.5 < 950) and (piece[1] >= 0 and piece[1] < 700):
            possiblePosition.append((piece[0] - 87.5, piece[1], "Attack", "King", piece))
        if (piece[0] - 87.5 >= 300 and piece[0] - 87.5 < 950) and (piece[1]  - 87.5 >= 0 and piece[1] - 87.5 < 700):
            possiblePosition.append((piece[0] - 87.5, piece[1] - 87.5, "Attack", "King", piece))
        if (piece[0] >= 300 and piece[0] < 950) and (piece[1] - 87.5 >= 0 and piece[1] - 87.5 < 700):
            possiblePosition.append((piece[0], piece[1] - 87.5, "Attack", "King", piece))
        if (piece[0] >= 300 and piece[0] < 950) and (piece[1] - 87.5 >= 0 and piece[1] - 87.5 < 700):
            possiblePosition.append((piece[0] + 87.5, piece[1] - 87.5, "Attack", "King", piece))
        return possiblePosition
    
    def allPossibleOpponentMoves(self): # This fuctions is for calculating all the possible opponents moves
        self.posibleOpponentMoves = []
        temp = self.my_pieces
        self.my_pieces = self.oppo_pieces
        oppo_pieces = self.oppo_pieces
        self.oppo_pieces = temp
        for piece in oppo_pieces:
            if piece[3] == "White Pawn" or piece[3] == "Black Pawn":
                self.posibleOpponentMoves += self.pawnPOS(piece)
            elif piece[3] == "Black Rook" or piece[3] == "White Rook":
                self.posibleOpponentMoves += self.rookPOS(piece)
            elif piece[3] == "Black Knight" or piece[3] == "White Knight":
                self.posibleOpponentMoves += self.knightPOS(piece)
            elif piece[3] == "Black Bishop" or piece[3] == "White Bishop":
                self.posibleOpponentMoves += self.bishopPOS(piece)
            elif piece[3] == "Black Queen" or piece[3] == "White Queen":
                self.posibleOpponentMoves += self.queenPOS(piece)
            elif piece[3] == "Black King" or piece[3] == "White King":
                self.posibleOpponentMoves += self.kingPOS(piece)
        temp = self.my_pieces
        self.my_pieces = self.oppo_pieces
        self.oppo_pieces = temp

    def check(self): #This fuction is for check detection
        for my in self.my_pieces:
            if my[3] == "Black King" or my[3] == "White King":
                point = (my[0], my[1])
        self.allPossibleOpponentMoves()
        for pos in self.posibleOpponentMoves:
            if point[0] == pos[0] and point[1] == pos[1]:
                #self.drawChess.checkDraw(True, point)
                self.isCheck = True
                self.attacker = pos
                self.kingPos = point
                break
            else:
                #self.drawChess.checkDraw(False, point)
                self.isCheck = False
                self.attacker = None
                self.kingPos = None

    def defenceBishop(self):
        posibleDefencePoint = []
        if self.kingPos[0] < self.attacker[4][0] and self.kingPos[1] > self.attacker[4][1]:
            i = 0
            while self.attacker[4][0] - 87.5 * i > self.kingPos[0] and self.attacker[4][1] + 87.5 * i < self.kingPos[1]:
                posibleDefencePoint.append((self.attacker[4][0] - 87.5 * i, self.attacker[4][1] + 87.5 * i, "Defence"))
                i += 1
        elif self.kingPos[0] > self.attacker[4][0] and self.kingPos[1] > self.attacker[4][1]:
            i = 0
            while self.attacker[4][0] + 87.5 * i < self.kingPos[0] and self.attacker[4][1] + 87.5 * i < self.kingPos[1]:
                posibleDefencePoint.append((self.attacker[4][0] + 87.5 * i, self.attacker[4][1] + 87.5 * i, "Defence"))
                i += 1
        elif self.kingPos[0] < self.attacker[4][0] and self.kingPos[1] < self.attacker[4][1]:
            i = 0
            while self.attacker[4][0] - 87.5 * i > self.kingPos[0] and self.attacker[4][1] - 87.5 * i > self.kingPos[1]:
                posibleDefencePoint.append((self.attacker[4][0] - 87.5 * i, self.attacker[4][1] - 87.5 * i, "Defence"))
                i += 1
        elif self.kingPos[0] > self.attacker[4][0] and self.kingPos[1] < self.attacker[4][1]:
            i = 0
            while self.attacker[4][0] + 87.5 * i < self.kingPos[0] and self.attacker[4][1] - 87.5 * i > self.kingPos[1]:
                posibleDefencePoint.append((self.attacker[4][0] + 87.5 * i, self.attacker[4][1] - 87.5 * i, "Defence"))
                i += 1
        return posibleDefencePoint
    
    def defenceKnight(self):
        posibleDefencePoint = []
        posibleDefencePoint.append((self.attacker[4][0], self.attacker[4][1], "Defence"))
        return posibleDefencePoint
    
    def defenceRook(self):
        posibleDefencePoint = []
        if self.attacker[4][0] > self.kingPos[0] and self.attacker[4][1] == self.kingPos[1]:
            i = 0
            while self.attacker[4][0] - 87.5 * i > self.kingPos[0]:
                posibleDefencePoint.append((self.attacker[4][0] - 87.5 * i, self.attacker[4][1], "Defence"))
                i += 1
        elif self.attacker[4][0] < self.kingPos[0] and self.attacker[4][1] == self.kingPos[1]:
            i = 0
            while self.attacker[4][0] + 87.5 * i < self.kingPos[0]:
                posibleDefencePoint.append((self.attacker[4][0] + 87.5 * i, self.attacker[4][1], "Defence"))
                i += 1
        elif self.attacker[4][1] > self.kingPos[1] and self.attacker[4][0] == self.kingPos[0]:
            i = 0
            while self.attacker[4][1] - 87.5 * i > self.kingPos[1]:
                posibleDefencePoint.append((self.attacker[4][0], self.attacker[4][1] - 87.5 * i, "Defence"))
                i += 1
        elif self.attacker[4][1] < self.kingPos[1] and self.attacker[4][0] == self.kingPos[0]:
            i = 0
            while self.attacker[4][1] + 87.5 * i < self.kingPos[1]:
                posibleDefencePoint.append((self.attacker[4][0], self.attacker[4][1] + 87.5 * i, "Defence"))
                i += 1
        return posibleDefencePoint
    
    def defencePawn(self):
        posibleDefencePoint = []
        posibleDefencePoint.append((self.attacker[4][0], self.attacker[4][1], "Defence"))
        return posibleDefencePoint

    def calDefenceMoves(self): # Queen is actually combination of Bishop and Rook. Thus, it's not considered
        posibleDefencePoint = []
        if self.isCheck:
            if self.attacker[3] == "Bishop":
                posibleDefencePoint = self.defenceBishop()
            elif self.attacker[3] == "Knight":
                posibleDefencePoint = self.defenceKnight()
            elif self.attacker[3] == "Rook":
                posibleDefencePoint = self.defenceRook()
            elif self.attacker[3] == "White Pawn" or self.attacker[3] == "Black Pawn":
                posibleDefencePoint = self.defencePawn()
        return posibleDefencePoint
    
    def checkMate(self):
        restart = False
        posibleDefencePoint = []
        if self.isCheck:
            for piece in self.my_pieces:
                if piece[3] == "White Pawn":
                    posibleDefencePoint += self.whitePawn(piece)
                elif piece[3] == "Black Pawn":
                    posibleDefencePoint += self.blackPawn(piece)
                elif piece[3] == "Black Rook" or piece[3] == "White Rook":
                    posibleDefencePoint += self.rook(piece)
                elif piece[3] == "Black Knight" or piece[3] == "White Knight":
                    posibleDefencePoint += self.knight(piece)
                elif piece[3] == "Black Bishop" or piece[3] == "White Bishop":
                    posibleDefencePoint += self.bishop(piece)
                elif piece[3] == "Black Queen" or piece[3] == "White Queen":
                    posibleDefencePoint += self.queen(piece)
                elif piece[3] == "Black King" or piece[3] == "White King":
                    posibleDefencePoint += self.king(piece)
            posibleDefencePoint = [x for x in posibleDefencePoint if x[2] == "Defence"]
            if len(posibleDefencePoint) == 0:
                if self.my_pieces[0][3][0:5] == "White":
                    run, restart = self.drawChess.gameOver("WHITE")
                if self.my_pieces[0][3][0:5] == "Black":
                    run, restart = self.drawChess.gameOver("BLACK")
        return restart

    def checkDrawvalue(self):
        self.check()
        self.drawChess.checkDraw(self.isCheck, self.kingPos)