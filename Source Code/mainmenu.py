import pygame
import time
import hostjoin
import PATHS

pygame.init()
background = pygame.image.load(PATHS.BACKGROUND_PATH)
cursor1 = pygame.transform.scale(pygame.image.load(PATHS.CURSOR1), (25, 25))
        
class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1300, 700))
        #self.screen = pygame.display.set_mode()
        pygame.display.set_caption("Chess")
        #pygame.mouse.set_visible(False)
        self.color1_top = self.color2_top = self.color3_top = self.color4_top = self.color5_top = self.color6_top = self.color7_top = self.topColor = (159, 100, 60)
        self.color1_bottom = self.color2_bottom = self.color3_bottom = self.color4_bottom = self.color5_bottom = self.color6_bottom = self.color7_bottom= (97, 63, 46)
        self.onHoverColor = (186, 128, 82)
        self.textColor = (0, 0, 0)
        self.pyfont = pygame.font.Font(None, 50)
    
    def actualPosition(self):
        self.rect1_top = pygame.Rect((500, 75, 300, 100))
        self.rect1_bottom = pygame.Rect((500, 85, 300, 100))
        self.rect2_top = pygame.Rect((500, 225, 300, 100))
        self.rect2_bottom = pygame.Rect((500, 235, 300, 100))
        self.rect3_top = pygame.Rect((500, 375, 300, 100))
        self.rect3_bottom = pygame.Rect((500, 385, 300, 100))
        self.rect4_top = pygame.Rect((500, 525, 300, 100))
        self.rect4_bottom = pygame.Rect((500, 535, 300, 100))

    def drawMenu(self):
        text = self.pyfont.render("PLAY", True, self.textColor)
        pygame.draw.rect(self.screen, self.color1_bottom, self.rect1_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect1_top, border_radius = 15)
        self.screen.blit(text, (self.rect1_top.centerx - 45, self.rect1_top.centery - 15))

        text = self.pyfont.render("ON SERVER", True, self.textColor)
        pygame.draw.rect(self.screen, self.color2_bottom, self.rect2_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color2_top, self.rect2_top, border_radius = 15)
        self.screen.blit(text, (self.rect2_top.centerx - 100, self.rect2_top.centery - 15))

        text = self.pyfont.render("VS COMPUTER", True, self.textColor)
        pygame.draw.rect(self.screen, self.color3_bottom, self.rect3_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color3_top, self.rect3_top, border_radius = 15)
        self.screen.blit(text, (self.rect3_top.centerx - 127, self.rect3_top.centery - 15))
        
        text = self.pyfont.render("EXIT", True, self.textColor)
        pygame.draw.rect(self.screen, self.color4_bottom, self.rect4_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color4_top, self.rect4_top, border_radius = 15)
        self.screen.blit(text, (self.rect4_top.centerx - 50, self.rect4_top.centery - 15))
    
    def checkCollision(self):
        self.pos = pygame.mouse.get_pos()
        if self.rect1_top.collidepoint(self.pos):
            self.color1_top = self.onHoverColor
            self.rect1_top = pygame.Rect((490, 65, 320, 120))
            self.rect1_bottom = pygame.Rect((490, 75, 320, 120))
        else:
            self.color1_top = self.topColor
            self.rect1_top = pygame.Rect((500, 75, 300, 100))
            self.rect1_bottom = pygame.Rect((500, 85, 300, 100))

        if self.rect2_top.collidepoint(self.pos):
            self.color2_top = self.onHoverColor
            self.rect2_top = pygame.Rect((490, 215, 320, 120))
            self.rect2_bottom = pygame.Rect((490, 225, 320, 120))
        else:
            self.color2_top = self.topColor
            self.rect2_top = pygame.Rect((500, 225, 300, 100))
            self.rect2_bottom = pygame.Rect((500, 235, 300, 100))
            
        if self.rect3_top.collidepoint(self.pos):
            self.color3_top = self.onHoverColor
            self.rect3_top = pygame.Rect((490, 365, 320, 120))
            self.rect3_bottom = pygame.Rect((490, 375, 320, 120))
        else:
            self.color3_top = self.topColor
            self.rect3_top = pygame.Rect((500, 375, 300, 100))
            self.rect3_bottom = pygame.Rect((500, 385, 300, 100))


        if self.rect4_top.collidepoint(self.pos):
            self.color4_top = self.onHoverColor
            self.rect4_top = pygame.Rect((490, 515, 320, 120))
            self.rect4_bottom = pygame.Rect((490, 525, 320, 120))
        else:
            self.color4_top = self.topColor
            self.rect4_top = pygame.Rect((500, 525, 300, 100))
            self.rect4_bottom = pygame.Rect((500, 535, 300, 100))

    def actualPos(self):
        self.rect5_top = pygame.Rect((500, 150, 300, 100))
        self.rect5_bottom = pygame.Rect((500, 160, 300, 100))

        self.rect6_top = pygame.Rect((500, 300, 300, 100))
        self.rect6_bottom = pygame.Rect((500, 310, 300, 100))

        self.rect7_top = pygame.Rect((500, 450, 300, 100))
        self.rect7_bottom = pygame.Rect((500, 460, 300, 100))

    def drawButton(self):
        pyfont = pygame.font.Font(None, 45)
        text = pyfont.render("PLAYER VS COMP", True, self.textColor)
        pygame.draw.rect(self.screen, self.color5_bottom, self.rect5_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color5_top, self.rect5_top, border_radius = 15)
        self.screen.blit(text, (self.rect5_top.centerx - 135, self.rect5_top.centery - 15))

        text = pyfont.render("COMP VS COMP", True, self.textColor)
        pygame.draw.rect(self.screen, self.color6_bottom, self.rect6_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color6_top, self.rect6_top, border_radius = 15)
        self.screen.blit(text, (self.rect6_top.centerx - 120, self.rect6_top.centery - 15))

        text = pyfont.render("BACK", True, self.textColor)
        pygame.draw.rect(self.screen, self.color7_bottom, self.rect7_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color7_top, self.rect7_top, border_radius = 15)
        self.screen.blit(text, (self.rect7_top.centerx - 50, self.rect7_top.centery - 15))

    def collision(self):
            self.pos = pygame.mouse.get_pos()
            if self.rect5_top.collidepoint(self.pos):
                self.color5_top = self.onHoverColor
                self.rect5_top = pygame.Rect((490, 150, 320, 120))
                self.rect5_bottom = pygame.Rect((490, 160, 320, 120))
            else:
                self.color5_top = self.topColor
                self.rect5_top = pygame.Rect((500, 150, 300, 100))
                self.rect5_bottom = pygame.Rect((500, 160, 300, 100))

            if self.rect6_top.collidepoint(self.pos):
                self.color6_top = self.onHoverColor
                self.rect6_top = pygame.Rect((490, 300, 320, 120))
                self.rect6_bottom = pygame.Rect((490, 310, 320, 120))
            else:
                self.color6_top = self.topColor
                self.rect6_top = pygame.Rect((500, 300, 300, 100))
                self.rect6_bottom = pygame.Rect((500, 310, 300, 100))

            if self.rect7_top.collidepoint(self.pos):
                self.color7_top = self.onHoverColor
                self.rect7_top = pygame.Rect((490, 450, 320, 120))
                self.rect7_bottom = pygame.Rect((490, 460, 320, 120))
            else:
                self.color7_top = self.topColor
                self.rect7_top = pygame.Rect((500, 450, 300, 100))
                self.rect7_bottom = pygame.Rect((500, 460, 300, 100))
        
    def run(self):
        hold = True
        self.actualPosition()
        self.drawMenu()
        player, vsComp = False, False
        match_type = ""
        while hold:
            self.screen.fill((152, 180, 212))
            background.set_alpha(215)
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.checkCollision()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect1_top.collidepoint(self.pos):
                        self.rect1_top = self.rect1_bottom
                    elif self.rect2_top.collidepoint(self.pos):
                        self.rect2_top = self.rect2_bottom
                    elif self.rect3_top.collidepoint(self.pos):
                        self.rect3_top = self.rect3_bottom
                    elif self.rect4_top.collidepoint(self.pos):
                        self.rect4_top = self.rect4_bottom
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.rect1_top.collidepoint(self.pos):
                        hold = False
                        match_type = "Offline"
                    elif self.rect2_top.collidepoint(self.pos):
                        #hold = False
                        host = hostjoin.HostJoin()
                        connection = host.run()
                        del host
                        print("del obj")
                        self.screen.fill((152, 180, 212))
                        background.set_alpha(215)
                        self.screen.blit(background, (0, 0))
                        self.drawMenu()
                        pygame.display.update()
                        if connection:
                            match_type = "OnServer"
                            hold = False
                    elif self.rect3_top.collidepoint(self.pos):
                        print("VS COMPUTER")
                        vsComp, player = self.compStart()
                        if vsComp == False and player == False:
                            match_type = ""
                            hold = True
                        else:
                            if vsComp and player:
                                match_type = "PlayerVSComp"
                            elif vsComp and not player:
                                match_type = "CompVSComp"
                            hold = False
                    elif self.rect4_top.collidepoint(self.pos):
                        self.drawMenu()
                        text = self.pyfont.render("EXIT", True, self.textColor)
                        pygame.draw.rect(self.screen, self.topColor, self.rect4_top, border_radius = 15)
                        self.screen.blit(text, (self.rect4_top.centerx - 50, self.rect4_top.centery - 15))
                        pygame.display.update()
                        time.sleep(0.25)
                        pygame.quit()
            self.drawMenu()
            #self.drawCursor(pygame.mouse.get_pos())
            pygame.display.update()
        return match_type
    
    def drawCursor(self, pos):
        if pos[0] > 0 and pos[1] > 0:
            self.screen.blit(cursor1, (pos[0], pos[1]))

    def compStart(self) -> bool:
        player = False
        run = True
        self.actualPos()
        self.drawButton()
        while run:
            self.screen.fill((152, 180, 212))
            background.set_alpha(215)
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                self.collision()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect5_top.collidepoint(self.pos):
                        self.rect5_top = self.rect5_bottom
                    elif self.rect6_top.collidepoint(self.pos):
                        self.rect6_top = self.rect6_bottom
                    elif self.rect7_top.collidepoint(self.pos):
                        self.rect7_top = self.rect7_bottom
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.rect5_top.collidepoint(self.pos):
                        vsComp = True
                        player = True
                        run = False
                    elif self.rect6_top.collidepoint(self.pos):
                        vsComp = True
                        player = False
                        run = False
                    elif self.rect7_top.collidepoint(self.pos):
                        print("BACK")
                        player = False
                        vsComp = False
                        self.screen.fill((152, 180, 212))
                        background.set_alpha(215)
                        self.screen.blit(background, (0, 0))
                        pygame.display.update()
                        run = False
            self.drawButton()
            #self.drawCursor(pygame.mouse.get_pos())
            pygame.display.update()
        return vsComp, player
    
if __name__ == '__main__':
    mainmenu = MainMenu()
    mainmenu.run()