import pygame
import chess
import draw
import mainmenu
import time
import moves
import computer
import client
import server

#from pyautogui import click

# To locate every piece on the chess board we need to create a tuple 
# tuple with first element as x then y and then image of the chess piece
# the last element tells what type of the iece is like king, queen, bishop

def mAin():
    if __name__ == '__main__':
        gameruns = True
        while gameruns:
            menu = mainmenu.MainMenu()
            match_type = menu.run()
            time.sleep(0.25)
            WIDTH = 1300
            HEIGHT = 700
            screen = pygame.display.set_mode((WIDTH, HEIGHT))

            clicked = False
            run = True
            ScoreW = 0
            ScoreB = 0

            restart = False
            chessPieces = chess.ChessPieces([], [], [], [])
            white_pieces, black_pieces, white_captured_pieces, black_captured_pieces = chessPieces.create()
            drawChess = draw.DrawChess(screen, match_type)
            move = moves.Move(drawChess, white_pieces, black_pieces, match_type)
            currntMove = "White"

            match match_type:
                case "Offline":
                    print('herjh')
                case "OnServer":
                    clent = client.Client(8080, screen)
                    clent.updateMove(move)
                    username, clientMove = clent.run()
                    move.clientOBJ(clent, username, clientMove)
                    clent.update_game(white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove)
                    content, IPv4, PORT, address = clent.fetch_content()
                    drawChess.obj(clent)
                case "PlayerVSComp":
                    compMove = "Black"
                    comp = computer.Computer(compMove)
                case "CompVSComp":
                    compMove = "Black"
                    comp = computer.Computer(compMove)
            
            while run:
                
                if restart:
                    print("[RESTARTING...]")
                    del chessPieces, drawChess, move
                    chessPieces = chess.ChessPieces([], [], [], [])
                    white_pieces, black_pieces, white_captured_pieces, black_captured_pieces = chessPieces.create()
                    drawChess = draw.DrawChess(screen, match_type)
                    move = moves.Move(drawChess, white_pieces, black_pieces, match_type)
                    currntMove = "White"
                    restart = False

                pos = pygame.mouse.get_pos()
                ScoreW, ScoreB = move.updateCurrentScore()
                drawChess.update(white_pieces, black_pieces,white_captured_pieces, black_captured_pieces, currntMove, ScoreW, ScoreB)
                drawChess.drawAll()
                drawChess.select(pos[0], pos[1])

                match match_type:
                    case "Offline":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                del clent
                                run = False
                                pygame.quit()
                            
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                drawChess.checkButton()
                                if clicked == False:
                                    if currntMove == "White":
                                        black_pieces = move.deselect(black_pieces)
                                        white_pieces = move.selection(pos, white_pieces)
                                        if len([x for x in white_pieces if x[4] == "Selected"]) > 1:
                                            white_pieces = move.deselect(white_pieces)
                                            white_pieces = move.selection(pos, white_pieces)
                                    if currntMove == "Black":
                                        white_pieces = move.deselect(white_pieces)
                                        black_pieces = move.selection(pos, black_pieces)
                                        if len([x for x in black_pieces if x[4] == "Selected"]) > 1:
                                            black_pieces = move.deselect(black_pieces)
                                            black_pieces = move.selection(pos, black_pieces)
                                    clicked = True
                            
                            if event.type == pygame.MOUSEBUTTONUP:
                                restart, run = drawChess.buttonActions()
                                if clicked == True:
                                    if currntMove == "White":
                                        white_pieces, black_pieces, black_captured_pieces, currntMove = move.mainMove(pos, white_pieces, black_pieces, black_captured_pieces, currntMove)
                                    elif currntMove == "Black":
                                        black_pieces, white_pieces, white_captured_pieces, currntMove = move.mainMove(pos, black_pieces, white_pieces, white_captured_pieces, currntMove)
                                clicked = False
                            drawChess.drawButtons()
                        move.check()
                        move.checkDrawvalue()
                        if move.checkMate():
                            restart = True
                    case "OnServer":
                        drawChess.messages_draw(content, IPv4, PORT, address)
                        if clientMove != currntMove:
                            white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove = clent.reflect_changes()
                        clent.updateMove(move)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                clent.client.close()
                                pygame.quit()
                            
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                drawChess.checkButton()
                                if clicked == False:
                                    if clientMove == currntMove:
                                        if clientMove == "White":
                                            black_pieces = move.deselect(black_pieces)
                                            white_pieces = move.selection(pos, white_pieces)
                                            if len([x for x in white_pieces if x[4] == "Selected"]) > 1:
                                                white_pieces = move.deselect(white_pieces)
                                                white_pieces = move.selection(pos, white_pieces)
                                        if clientMove == "Black":
                                            white_pieces = move.deselect(white_pieces)
                                            black_pieces = move.selection(pos, black_pieces)
                                            if len([x for x in black_pieces if x[4] == "Selected"]) > 1:
                                                black_pieces = move.deselect(black_pieces)
                                                black_pieces = move.selection(pos, black_pieces)
                                        clent.update_game(white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove)
                                        clicked = True
                            if event.type == pygame.MOUSEBUTTONUP:
                                restart, run = drawChess.buttonActions()
                                if clicked == True:
                                    white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove = clent.reflect_changes()
                                    if clientMove == currntMove:
                                        if clientMove == "White":
                                            white_pieces, black_pieces, black_captured_pieces, currntMove = move.mainMove(pos, white_pieces, black_pieces, black_captured_pieces, currntMove)
                                        if clientMove == "Black":
                                            black_pieces, white_pieces, white_captured_pieces, currntMove = move.mainMove(pos, black_pieces, white_pieces, white_captured_pieces, currntMove)
                                        clent.update_game(white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove)
                                clicked = False
                            drawChess.drawButtons()
                        move.check()
                        move.checkDrawvalue()
                        if move.checkMate():
                            restart = True
                    case "PlayerVSComp":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                pygame.quit()
                            
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                drawChess.checkButton()
                                if clicked == False:
                                    if currntMove == "White":
                                        black_pieces = move.deselect(black_pieces)
                                        white_pieces = move.selection(pos, white_pieces)
                                        if len([x for x in white_pieces if x[4] == "Selected"]) > 1:
                                            white_pieces = move.deselect(white_pieces)
                                            white_pieces = move.selection(pos, white_pieces)
                                    if currntMove == "Black":
                                        white_pieces = move.deselect(white_pieces)
                                        black_pieces = move.selection(pos, black_pieces)
                                        if len([x for x in black_pieces if x[4] == "Selected"]) > 1:
                                            black_pieces = move.deselect(black_pieces)
                                            black_pieces = move.selection(pos, black_pieces)
                                    clicked = True
                            
                            elif event.type == pygame.MOUSEBUTTONUP:
                                restart, run = drawChess.buttonActions()
                                if clicked == True:
                                    if currntMove == "Black":
                                        black_pieces, white_pieces, white_captured_pieces, currntMove = move.mainMove(pos, black_pieces, white_pieces, white_captured_pieces, currntMove)
                                clicked = False
                            drawChess.drawButtons()
                        move.check()
                        move.checkDrawvalue()
                        if move.checkMate():
                            restart = True
                        if not restart:
                            try:
                                if currntMove == "White":
                                    comp.update(white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, move, currntMove, drawChess)
                                    if move.checkMate():
                                        restart = True
                                    white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove = comp.play()
                            except:
                                restart = True
                    case "CompVSComp":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                pygame.quit()
                            
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                drawChess.checkButton()
                            if event.type == pygame.MOUSEBUTTONUP:
                                restart, run = drawChess.buttonActions()
                            
                            drawChess.drawButtons()

                        if not restart:
                            comp.update(white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, move, currntMove, drawChess)
                            if move.checkMate():
                                restart = True
                            white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove = comp.play()
                #drawChess.drawCursor(pygame.mouse.get_pos())
                pygame.display.update()

if __name__ == '__main__':
    mAin()