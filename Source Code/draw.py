import pygame
import time
import chess
import PATHS

pygame.init()

blue_square = pygame.image.load(PATHS.BLUE_OVAL_SQUARE_PATH)
board = pygame.image.load(PATHS.BOARD_PATH)
icon = pygame.image.load(PATHS.ICON_PATH)
background = pygame.image.load(PATHS.BACKGROUND_PATH)
bluesqaure = pygame.image.load(PATHS.BLUE_SQUARE_PATH)
redsqaure = pygame.image.load(PATHS.RED_SQUARE_PATH)
scoreBackground = pygame.image.load(PATHS.BLUE_RECT_PATH)
cursor1 = pygame.transform.scale(pygame.image.load(PATHS.CURSOR1), (25, 25))

font = pygame.font.Font('freesansbold.ttf', 25)

class DrawChess:
    def __init__(self, screen, match_type):
        self.screen = screen
        pygame.display.set_icon(icon)
        pygame.display.set_caption("CHESS")
        self.color1_top = self.color2_top = self.color3_top = self.color4_top = self.color5_top = self.color6_top = self.topColor = (159, 100, 60)
        self.color1_bottom = self.color2_bottom = self.color3_bottom = self.color4_bottom = self.color5_bottom = self.color6_bottom =  self.bottomColor =(97, 63, 46)
        self.onHoverColor = (170, 115, 70)
        self.textColor = (0, 0, 0)
        self.pyfont = pygame.font.Font(None, 30)
        self.possiblePosition = []
        self.check = False
        self.checkpoint = (0, 0)
        self.isShow = True
        self.lastMove = "White"
        self.currntMove = "White"
        self.isCheck = False
        self.run = True
        self.match_type = match_type
        self.text = ""
        self.content = []

    def update(self, white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove, ScoreW, ScoreB):
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.white_captured_pieces = white_captured_pieces
        self.black_captured_pieces = black_captured_pieces
        self.lastMove = self.currntMove
        self.currntMove = currntMove
        self.ScoreW = ScoreW
        self.ScoreB =  ScoreB
    
    def updateScore(self, ScoreW, ScoreB):
        self.ScoreW = ScoreW
        self.ScoreB = ScoreB

    def drawAll(self) -> None: # This function uses another function to draw the ui for game
        self.background()
        self.drawChessPieces()
        self.show_captured_pieces()
        self.actualPosition()
        self.checkCollision()
        self.show_text()
        self.drawButtons()
        #self.messages_draw()

    def drawCursor(self, pos):
        if pos[0] > 0 and pos[1] > 0:
            self.screen.blit(cursor1, (pos[0], pos[1]))

    def messages_draw(self, content, IPv4, Server_PORT, address):
        x, y = 1015, 240
        Client_PORT = address
        statusfont = pygame.font.Font(None, 35)
        status1 = statusfont.render(f"IPv4: {IPv4}", True, (0, 0, 0))
        self.screen.blit(status1, (1040, 65))
        status2 = statusfont.render(f"SERVER PORT: {Server_PORT}", True, (0, 0, 0))
        self.screen.blit(status2, (1030, 100))
        status3 = statusfont.render(f"CLIENT PORT: {Client_PORT}", True, (0, 0, 0))
        self.screen.blit(status3, (1030, 135))
        chatfont = pygame.font.Font(None, 25)
        for i, message in enumerate(content):
            '''if len(message) > 40:
                info1 = chatfont.render(f"{message[1:29]}-", True, (0, 0, 0))
                info2 = chatfont.render(f"{message[29::]}", True, (0, 0, 0))
                self.screen.blit(info1, (x, y + i * 35))
                self.screen.blit(info2, (x, y + i * 35 + 15))
            else:'''
            info = chatfont.render(f"{[(message.split("~")[0])[1::]]}", True, (0, 0, 0))
            self.screen.blit(info, (x, y + i * 35))
            info = chatfont.render(f"{message.split("~")[1]}", True, (0, 0, 0))
            self.screen.blit(info, (x + 3, y + 17 + i * 35))

    def background(self):
        scorefont = pygame.font.Font(None, 35)
        self.screen.fill((152, 180, 212))
        background.set_alpha(215)
        self.screen.blit(background, (0, 0))
        self.screen.blit(board, (300, 0))
        scoreBackground.set_alpha(50)
        self.screen.blit(scoreBackground, (10, 10))
        self.screen.blit(scoreBackground, (10, 525))
        text = font.render("WHITE STATUS", True, (0, 0, 0))
        white_score = scorefont.render(f"{self.ScoreW}", True, (0, 0, 0))
        if self.currntMove == "White":
            text = font.render("WHITE STATUS", True, (0, 160, 0))
            white_score = scorefont.render(f"{self.ScoreW}", True, (0, 160, 0))
        self.screen.blit(white_score, (255, 25))
        self.screen.blit(text, (50, 25))
        text = font.render("BLACK STATUS", True, (0, 0, 0))
        black_score = scorefont.render(f"{self.ScoreB}", True, (0, 0, 0))
        if self.currntMove == "Black":
            text = font.render("BLACK STATUS", True, (0, 160, 0))
            black_score = scorefont.render(f"{self.ScoreB}", True, (0, 160, 0))
        self.screen.blit(black_score, (255, 540))
        self.screen.blit(text, (50, 540))
        surphase1 = pygame.Surface((280, 165))
        surphase1.set_alpha(150)
        surphase1.fill(self.onHoverColor)
        self.screen.blit(surphase1, (1010, 10))
        fonts = pygame.font.Font('freesansbold.ttf', 23)
        text = fonts.render("CONNECTION STATUS", True, (0, 0, 0))
        self.screen.blit(text, (1022, 30))
        fontb = pygame.font.Font('freesansbold.ttf', 55)
        text = fontb.render("OFFLINE", True, (0, 0, 0))
        if self.match_type != "OnServer":
            self.screen.blit(text, (1030, 75))
        rect1 = pygame.Rect((1010, 10, 280, 165))
        pygame.draw.rect(self.screen, self.onHoverColor, rect1, width = 5)
        surphase2 = pygame.Surface((280, 505))
        surphase2.set_alpha(150)
        surphase2.fill(self.onHoverColor)
        self.screen.blit(surphase2, (1010, 185))
        rect2 = pygame.Rect((1010, 185, 280, 505))
        pygame.draw.rect(self.screen, self.onHoverColor, rect2, width = 5)
        rect3 = pygame.Rect((1020, 630, 260, 50))
        #pygame.draw.rect(self.screen, self.onHoverColor, rect3, border_radius = 15, width = 5)
        fonts = pygame.font.Font('freesansbold.ttf', 35)
        text = fonts.render("CHAT BOX", True, (0, 0, 0))
        self.screen.blit(text, (1060, 200))
        fonts = pygame.font.Font('freesansbold.ttf', 15)
        text = fonts.render("ENTER YOUR TEXT HERE...", True, (0, 0, 0))
        #self.screen.blit(text, (1030, 650))
        if len(self.possiblePosition) > 0 : 
            self.mapPosiblePosition() 


    def chess_pawn(self, pawn):
        self.screen.blit(pawn[2], (pawn[0] + 8.5, pawn[1] + 8.5))

    def chess_king(self, king):
        self.screen.blit(king[2], (king[0] + 3.5, king[1] + 3.5))

    def chess_queen(self, queen):
        self.screen.blit(queen[2], (queen[0] + 3.5, queen[1] + 3.5))

    def chess_bishop(self, bishop):
        self.screen.blit(bishop[2], (bishop[0] + 6, bishop[1] + 6))

    def chess_knight(self, knight):
        self.screen.blit(knight[2], (knight[0] + 6, knight[1] + 6))

    def chess_rook(self, rook):
        self.screen.blit(rook[2], (rook[0] + 6, rook[1] + 6))
    
    def updatemapPosiblePosition(self, possiblePosition):
        self.possiblePosition = possiblePosition

    def mapPosiblePosition(self):
        if self.lastMove != self.currntMove:
            self.possiblePosition = []
        if self.isShow:
            if not self.isCheck:
                for positions in self.possiblePosition:
                    if positions[2] == "Attack" or positions[2] == "LeftCasteling" or positions[2] == "RightCasteling" or positions[2] == "Promotion":
                        bluesqaure.set_alpha(100)
                        self.screen.blit(bluesqaure, (positions[0] - 0.6, positions[1] - 0.5))
            if self.isCheck:
                for positions in self.possiblePosition:
                    if positions[2] == "Defence":
                        bluesqaure.set_alpha(100)
                        self.screen.blit(bluesqaure, (positions[0] - 0.6, positions[1] - 0.5))

    def select(self, x, y):
        if (x > 300 and x < 980) and (y > 0 and y < 700):
            xtime = int((x - 300) / 87.5)
            ytime = int(y / 87.5)
            xpos = 87.5 * xtime + 300
            ypos = 87.5 * ytime
            self.screen.blit(blue_square, (xpos, ypos))

    def draw_pieces(self, pieces):
        for piece in pieces:
            match piece[3]:
                case "White Pawn":
                    self.chess_pawn(piece)    
                    continue
                case "White King":
                    self.chess_king(piece)    
                    continue
                case "White Queen":
                    self.chess_queen(piece)    
                    continue
                case "White Rook":
                    self.chess_rook(piece)    
                    continue
                case "White Knight":
                    self.chess_knight(piece)    
                    continue
                case "White Bishop":
                    self.chess_bishop(piece)    
                    continue
                case "Black Pawn":
                    self.chess_pawn(piece)    
                    continue
                case "Black King":
                    self.chess_king(piece)    
                    continue
                case "Black Queen":
                    self.chess_queen(piece)    
                    continue
                case "Black Rook":
                    self.chess_rook(piece)    
                    continue
                case "Black Knight":
                    self.chess_knight(piece)    
                    continue
                case "Black Bishop":
                    self.chess_bishop(piece)    
                    continue

    def drawChessPieces(self):
        self.draw_pieces(self.white_pieces)
        self.draw_pieces(self.black_pieces)

    def show_captured_pieces(self):
        if len(self.white_captured_pieces) != 0:
            x , y, z = 10, 590, 1
            for piece in self.white_captured_pieces:
                times = piece[2]
                while times:
                    self.screen.blit(piece[0], (x, y))
                    times -= 1
                    x += 35
                    if z == 8:
                        y += 40
                        x = 10
                        z = 0
                    z += 1
        if len(self.black_captured_pieces) != 0:
            x , y, z = 10, 75, 1
            for piece in self.black_captured_pieces:
                times = piece[2]
                while times:
                    self.screen.blit(piece[0], (x, y))
                    times -= 1
                    x += 35
                    if z == 8:
                        y += 40
                        x = 10
                        z = 0
                    z += 1
    
    def drawButtons(self):
        text = self.pyfont.render("RESTART", True, self.textColor)
        pygame.draw.rect(self.screen, self.color3_bottom, self.rect3_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color3_top, self.rect3_top, border_radius = 15)
        self.screen.blit(text, (self.rect3_top.centerx - 40, self.rect3_top.centery - 10))

        text = self.pyfont.render("BY WIN", True, self.textColor)
        pygame.draw.rect(self.screen, self.color4_bottom, self.rect4_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color4_top, self.rect4_top, border_radius = 15)
        self.screen.blit(text, (self.rect4_top.centerx - 35, self.rect4_top.centery - 10))

        #SHOW MOVES AND HIDE MOVES
        pygame.draw.rect(self.screen, self.color5_bottom, self.rect5_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color5_top, self.rect5_top, border_radius = 15)
        if not self.isShow:
            text = self.pyfont.render("SHOW MOVES", True, self.textColor)
            self.screen.blit(text, (self.rect5_top.centerx - 70, self.rect5_top.centery - 10))
        if self.isShow:
            text = self.pyfont.render("HIDE MOVES", True, self.textColor)
            self.screen.blit(text, (self.rect5_top.centerx - 60, self.rect5_top.centery - 10))
        

        text = self.pyfont.render("BACK", True, self.textColor)
        pygame.draw.rect(self.screen, self.color6_bottom, self.rect6_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color6_top, self.rect6_top, border_radius = 15)
        self.screen.blit(text, (self.rect6_top.centerx - 30, self.rect6_top.centery - 10))

        pygame.draw.rect(self.screen, (220, 220, 220), self.rect_chat_s, border_radius=8)

    def checkCollision(self):
        self.pos = pygame.mouse.get_pos()

        if self.rect3_top.collidepoint(self.pos):
            self.color3_top = self.onHoverColor
            self.rect3_top = pygame.Rect((20, 202.5, 260, 60))
            self.rect3_bottom = pygame.Rect((20, 207.5, 260, 60))
        else:
            self.rect3_top = pygame.Rect((25, 207.5, 250, 50))
            self.rect3_bottom = pygame.Rect((25, 212.5, 250, 50))
            self.color3_top = self.topColor

        if self.rect4_top.collidepoint(self.pos):
            self.color4_top = self.onHoverColor
            self.rect4_top = pygame.Rect((20, 272.5, 260, 60))
            self.rect4_bottom = pygame.Rect((20, 277.5, 260, 60))
        else:
            self.rect4_top = pygame.Rect((25, 277.5, 250, 50))
            self.rect4_bottom = pygame.Rect((25, 282.5, 250, 50))
            self.color4_top = self.topColor

        if self.rect5_top.collidepoint(self.pos):
            self.color5_top = self.onHoverColor
            self.rect5_top = pygame.Rect((20, 342.5, 260, 60))
            self.rect5_bottom = pygame.Rect((20, 347.5, 260, 60))
        else:
            self.rect5_top = pygame.Rect((25, 347.5, 250, 50))
            self.rect5_bottom = pygame.Rect((25, 352.5, 250, 50))
            self.color5_top = self.topColor

        if self.rect6_top.collidepoint(self.pos):
            self.color6_top = self.onHoverColor
            self.rect6_top = pygame.Rect((20, 412.5, 260, 60))
            self.rect6_bottom = pygame.Rect((20, 417.5, 260, 60))
        else:
            self.rect6_top = pygame.Rect((25, 417.5, 250, 50))
            self.rect6_bottom = pygame.Rect((25, 422.5, 250, 50))
            self.color6_top = self.topColor

    
    def actualPosition(self):
        x = -62.5
        self.rect3_top = pygame.Rect((25, 270 + x, 250, 50))
        self.rect3_bottom = pygame.Rect((25, 275 + x, 250, 50))
        self.rect4_top = pygame.Rect((25, 340 + x, 250, 50))
        self.rect4_bottom = pygame.Rect((25, 345 + x, 250, 50))
        self.rect5_top = pygame.Rect((25, 410 + x, 250, 50))
        self.rect5_bottom = pygame.Rect((25, 415 + x, 250, 50))
        self.rect6_top = pygame.Rect((25, 480 + x, 250, 50))
        self.rect6_bottom = pygame.Rect((25, 485 + x, 250, 50))
        self.rect_chat_s = pygame.Rect((1025, 635, 250, 40))
        self.rect_chat_b = pygame.Rect((1020, 640, 260, 50))

    def actualPosition1(self):
        self.rectbgborder = pygame.Rect(((300 + 87.5 * 2.6, 87.5 * 2.6, 87.5 * 2.75, 87.5 * 2.8)))
        self.rectbg = pygame.Rect((300 + 87.5 * 2.6, 87.5 * 2.6, 87.5 * 2.75, 87.5 * 2.8))
        self.rect1 = pygame.Rect((300 + 87.5 * 2.5, 87.5 * 2.75, 87.5, 87.5))
        self.rectb1 = pygame.Rect((300 + 87.5 * 2.5, 87.5 * 2.75 + 5, 87.5, 87.5))
        self.rect2 = pygame.Rect((300 + 87.5 * 4.06, 87.5 * 2.75, 87.5, 87.5))
        self.rectb2 = pygame.Rect((300 + 87.5 * 4.06, 87.5 * 2.75 + 5, 87.5, 87.5))
        self.rect3 = pygame.Rect((300 + 87.5 * 2.8 + 5, 87.5 * 4.06, 87.5, 87.5))
        self.rectb3 = pygame.Rect((300 + 87.5 * 2.8 + 5, 87.5 * 4.06 + 5, 87.5, 87.5))
        self.rect4 = pygame.Rect((300 + 87.5 * 4.06 + 5, 87.5 * 4.06, 87.5, 87.5))
    
    def checkButton(self):
        if self.rect3_top.collidepoint(self.pos):
            self.rect3_top = self.rect3_bottom
        if self.rect4_top.collidepoint(self.pos):
            self.rect4_top = self.rect4_bottom
        if self.rect5_top.collidepoint(self.pos):
            self.rect5_top = self.rect5_bottom
        if self.rect6_top.collidepoint(self.pos):
            self.rect6_top = self.rect6_bottom
    
    def buttonActions(self):
        restart = False
        run = True
        if self.rect3_top.collidepoint(self.pos):
            print("RESTART")
            restart = True
        elif self.rect4_top.collidepoint(self.pos):
            print("BY WIN")
            run, restart = self.gameOver(self.currntMove)
            print(run, restart)
            if restart:
                run = True
        elif self.rect5_top.collidepoint(self.pos):
            if self.isShow:
                self.isShow = False
                print("HIDE MOVES")
            else:
                self.isShow = True
                print("SHOW MOVES")
        elif self.rect6_top.collidepoint(self.pos):
            print("BACK")
            run = False
        elif self.rect_chat_s.collidepoint(self.pos):
            font = pygame.font.Font(None, 25)
            chat = True
            while chat:
                self.drawAll()
                pygame.draw.rect(self.screen, (220, 220, 220), self.rect_chat_s, border_radius=8)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP_ENTER:
                            continue
                        if event.key == pygame.K_ESCAPE:
                            chat = False
                            continue
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[0:(len(self.text) - 1)]
                            continue
                        self.text += event.unicode
                if len(self.text) > 30:
                    length = len(self.text)
                    text = font.render(f"{self.text[(length - 30)::]}", True, (0, 0, 0))
                else:
                    text = font.render(f"{self.text}", True, (0, 0, 0))
                self.screen.blit(text, (1030, 645))
                #self.drawCursor(pygame.mouse.get_pos())
                pygame.display.update()
            if self.match_type == "OnServer":
                if self.text:
                    self.clent.send_data(self.text)
                self.text = ""
            else:
                self.content.append(self.text)
                if len(self.content) > 11:
                    self.content.pop(0)
                self.text = ""
        return restart, run
    
    def obj(self, clent):
        self.clent = clent
    
    def show_text(self):
        if self.match_type != "OnServer" and len(self.content):
            x, y = 1015, 240
            chatfont = pygame.font.Font(None, 25)
            for i, message in enumerate(self.content):
                info = chatfont.render(f"{message}", True, (0, 0, 0))
                #info = chatfont.render(f"{[(message.split("~")[0])]}", True, (0, 0, 0))
                self.screen.blit(info, (x, y + i * 35))
                #info = chatfont.render(f"{message.split("~")[1]}", True, (0, 0, 0))
                #self.screen.blit(info, (x + 3, y + 17 + i * 35))
        
    def buttonActions1(self):
        position = pygame.mouse.get_pos()
        if self.rect1.collidepoint(position):
            print("Queen")
            self.drawPromotion()
            pygame.display.update()
            time.sleep(0.2)
            return False, "Queen"
        elif self.rect2.collidepoint(position):
            print("Bishop")
            self.drawPromotion()
            pygame.display.update()
            time.sleep(0.2)
            return False, "Bishop"
        elif self.rect3.collidepoint(position):
            print("Knight")
            self.drawPromotion()
            pygame.display.update()
            time.sleep(0.2)
            return False, "Knight"
        elif self.rect4.collidepoint(position):
            print("Rook")
            self.drawPromotion()
            pygame.display.update()
            time.sleep(0.2)
            return False, "Rook"
        else:
            return True, None
        
    def checkDraw(self, isCheck, kingPos):
        self.isCheck = isCheck
        self.kingPos = kingPos
        if self.isCheck and self.isShow:
            redsqaure.set_alpha(200)
            self.screen.blit(redsqaure, (self.kingPos[0] - 4.5, self.kingPos[1] - 3))
            pygame.display.update()

    def drawPromotion(self):
        self.piecesPromotion()
        pygame.draw.rect(self.screen, self.onHoverColor, self.rectbg, border_radius = 15)

        pygame.draw.rect(self.screen, (170, 115, 70), self.rectbgborder, border_radius = 15, width = 5)

        pygame.draw.rect(self.screen, self.color1_bottom, self.rectb1, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect1, border_radius = 15)
        self.screen.blit(self.queen[2], (self.rect1.centerx - 40, self.rect1.centery - 40))

        pygame.draw.rect(self.screen, self.color1_bottom, self.rectb2, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect2, border_radius = 15)
        self.screen.blit(self.bishop[2], (self.rect2.centerx - 38, self.rect2.centery - 35))
        
        pygame.draw.rect(self.screen, self.color1_bottom, self.rectb3, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect3, border_radius = 15)
        self.screen.blit(self.knight[2], (self.rect3.centerx - 40, self.rect3.centery - 35))

        pygame.draw.rect(self.screen, self.color1_bottom, self.rectb4, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect4, border_radius = 15)
        self.screen.blit(self.rook[2], (self.rect4.centerx - 37, self.rect4.centery - 35))
        

    def piecesPromotion(self):
        cheese = chess.ChessPieces([], [], [], [])
        white_pieces, black_pieces, white_captured_pieces, black_captured_pieces = cheese.create()
        if self.currntMove == "Black":
            for piece in black_pieces:
                if piece[3] == "Black Queen":
                    self.queen = piece
                elif piece[3] == "Black Rook":
                    self.rook = piece
                elif piece[3] == "Black Knight":
                    self.knight = piece
                elif piece[3] == "Black Bishop":
                    self.bishop = piece
        elif self.currntMove == "White":
            for piece in white_pieces:
                if piece[3] == "White Queen":
                    self.queen = piece
                elif piece[3] == "White Rook":
                    self.rook = piece
                elif piece[3] == "White Knight":
                    self.knight = piece
                elif piece[3] == "White Bishop":
                    self.bishop = piece
        del cheese
        
    def promostionButtonOnhover(self):
        position = pygame.mouse.get_pos()
        if self.rect1.collidepoint(position):
            self.rect1 = pygame.Rect((300 + 87.5 * 2.75 + 5, 87.5 * 2.75, 95, 95))
            self.rectb1 = pygame.Rect((300 + 87.5 * 2.75 + 5, 87.5 * 2.75 + 5, 95, 95))
        else:
            self.rect1 = pygame.Rect((300 + 87.5 * 2.8 + 5, 87.5 * 2.8, 87.5, 87.5))
            self.rectb1 = pygame.Rect((300 + 87.5 * 2.8 + 5, 87.5 * 2.8 + 5, 87.5, 87.5))
        if self.rect2.collidepoint(position):
            self.rect2 = pygame.Rect((300 + 87.5 * 4.01 + 5, 87.5 * 2.75, 95, 95))
            self.rectb2 = pygame.Rect((300 + 87.5 * 4.01 + 5, 87.5 * 2.75 + 5, 95, 95))
        else:
            self.rect2 = pygame.Rect((300 + 87.5 * 4.06 + 5, 87.5 * 2.8, 87.5, 87.5))
            self.rectb2 = pygame.Rect((300 + 87.5 * 4.06 + 5, 87.5 * 2.8 + 5, 87.5, 87.5))
        if self.rect3.collidepoint(position):
            self.rect3 = pygame.Rect((300 + 87.5 * 2.75 + 5, 87.5 * 4.01, 95, 95))
            self.rectb3 = pygame.Rect((300 + 87.5 * 2.75 + 5, 87.5 * 4.01 + 5, 95, 95))
        else:
            self.rect3 = pygame.Rect((300 + 87.5 * 2.8 + 5, 87.5 * 4.06, 87.5, 87.5))
            self.rectb3 = pygame.Rect((300 + 87.5 * 2.8 + 5, 87.5 * 4.06 + 5, 87.5, 87.5))
        if self.rect4.collidepoint(position):
            self.rect4 = pygame.Rect((300 + 87.5 * 4.01 + 5, 87.5 * 4.01, 95, 95))
            self.rectb4 = pygame.Rect((300 + 87.5 * 4.01 + 5, 87.5 * 4.01 + 5, 95, 95))
        else:
            self.rect4 = pygame.Rect((300 + 87.5 * 4.06 + 5, 87.5 * 4.06, 87.5, 87.5))
            self.rectb4 = pygame.Rect((300 + 87.5 * 4.06 + 5, 87.5 * 4.06 + 5, 87.5, 87.5))

    def checkButtonPromotion(self):
        position = pygame.mouse.get_pos()
        if self.rect1.collidepoint(position):
            self.rect1 = self.rectb1
            #print("Queen")
        elif self.rect2.collidepoint(position):
            self.rect2 = self.rectb2
            #print("Bishop")
        elif self.rect3.collidepoint(position):
            self.rect3 = self.rectb3
            #print("Knight")
        elif self.rect4.collidepoint(position):
            self.rect4 = self.rectb4
            #print("Rook")

    def actualPosition2(self):
        self.rectbgGameOver = pygame.Rect((300 + 87.5 * 1.5, 87.5 * 2.5, 437.5, 262.5))
        

        self.rect1GameOver = pygame.Rect((300 + 87.5 * 1.75, 87.5 * 4.25, 87.5 * 2, 87.5))
        self.rectb1GameOver = pygame.Rect((300 + 87.5 * 1.75, 87.5 * 4.25 + 10, 87.5 * 2, 87.5))
        
        self.rect2GameOver = pygame.Rect((300 + 87.5 * 4, 87.5 * 4.25, 87.5 * 2.25, 87.5))
        self.rectb2GameOver = pygame.Rect((300 + 87.5 * 4, 87.5 * 4.25 + 10, 87.5 * 2.25, 87.5))

    def drawGameOver(self):
        #pygame.draw.rect(self.screen, self.onHoverColor, self.rectbgGameOver, border_radius = 15)

        surphase = pygame.Surface((437.5, 262.5))
        surphase.set_alpha(200)
        surphase.fill(self.onHoverColor)
        self.screen.blit(surphase, (300 + 87.5 * 1.5, 87.5 * 2.5))

        fontl = pygame.font.Font("freesansbold.ttf", 35)
        loser = fontl.render(f"THE {self.loser} IS", True, (0, 0, 0))
        self.screen.blit(loser, (self.rectbgGameOver.centerx - 120, self.rectbgGameOver.centery - 100))

        fontc = pygame.font.Font("freesansbold.ttf", 45)
        checkMate = fontc.render("\"CHECKMATE\"", True, (200, 25, 30))
        self.screen.blit(checkMate, (self.rectbgGameOver.centerx - 87.5 * 1.85, self.rectbgGameOver.centery - 44))

        fonts = pygame.font.Font("freesansbold.ttf", 30)
        rematch = fonts.render("REMATCH", True, (0, 0, 0))
        pygame.draw.rect(self.screen, self.color1_bottom, self.rectb1GameOver, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect1GameOver, border_radius = 15)
        self.screen.blit(rematch, (self.rect1GameOver.centerx - 75, self.rect1GameOver.centery - 10))

        back = fonts.render("BACK", True, (0, 0, 0))
        pygame.draw.rect(self.screen, self.color1_bottom, self.rectb2GameOver, border_radius = 15)
        pygame.draw.rect(self.screen, self.color2_top, self.rect2GameOver, border_radius = 15)
        self.screen.blit(back, (self.rect2GameOver.centerx - 45, self.rect2GameOver.centery - 10))

    def drawGameOverHover(self):
        self.pos = pygame.mouse.get_pos() 

        if self.rect1GameOver.collidepoint(self.pos):
            self.rect1GameOver = pygame.Rect((300 + 87.5 * 1.6, 87.5 * 4.15, 87.5 * 2.4, 100))
            self.rectb1GameOver = pygame.Rect((300 + 87.5 * 1.6, 87.5 * 4.15 + 10, 87.5 * 2.4, 100))
            self.color1_top = self.onHoverColor
        else:
            self.rect1GameOver = pygame.Rect((300 + 87.5 * 1.7, 87.5 * 4.25, 87.5 * 2.2, 80))
            self.rectb1GameOver = pygame.Rect((300 + 87.5 * 1.7, 87.5 * 4.25 + 10, 87.5 * 2.2, 80))
            self.color1_top = self.topColor

        if self.rect2GameOver.collidepoint(self.pos):
            self.rect2GameOver = pygame.Rect((300 + 87.5 * 4, 87.5 * 4.15, 87.5 * 2.4, 100))
            self.rectb2GameOver = pygame.Rect((300 + 87.5 * 4, 87.5 * 4.15 + 10, 87.5 * 2.4, 100))
            self.color2_top = self.onHoverColor
        else:
            self.rect2GameOver = pygame.Rect((300 + 87.5 * 4.1, 87.5 * 4.25, 87.5 * 2.2, 80))
            self.rectb2GameOver = pygame.Rect((300 + 87.5 * 4.1, 87.5 * 4.25 + 10, 87.5 * 2.2, 80))
            self.color2_top = self.topColor

    def checkButtonGameOver(self):
        if self.rect1GameOver.collidepoint(self.pos):
            self.rect1GameOver = self.rectb1GameOver
        elif self.rect2GameOver.collidepoint(self.pos):
            self.rect2GameOver = self.rectb2GameOver

    def buttonActionsGameOver(self):
        run = True
        restart = False
        if self.rect1GameOver.collidepoint(self.pos):
            print("REMATCH")
            run, restart = False, True 
        elif self.rect2GameOver.collidepoint(self.pos):
            print("BACK")
            run = False
        return run, restart
        
    def gameOver(self, loser): #This is for the checkmate User Interface
        self.loser = loser.upper()
        restart = False
        run = True
        self.actualPosition2()
        while run:
            self.background()
            self.drawChessPieces()
            self.show_captured_pieces()
            self.drawButtons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    
                self.drawGameOverHover()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkButtonGameOver()
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    run, restart = self.buttonActionsGameOver()


            self.drawGameOver()
            pygame.display.update()
        return run, restart