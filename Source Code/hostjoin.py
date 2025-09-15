import pygame
import time
import PATHS

pygame.init()
background = pygame.image.load(PATHS.BACKGROUND_PATH)
cursor1 = pygame.transform.scale(pygame.image.load(PATHS.CURSOR1), (25, 25))

class HostJoin:
    def __init__(self):
        print("obj")
        self.screen = pygame.display.set_mode((1300, 700))
        pygame.display.set_caption("Chess")
        self.color1_top = self.color2_top = self.color3_top = self.color4_top = self.topColor = (159, 100, 60)
        self.color1_bottom = self.color2_bottom = self.color3_bottom = self.color4_bottom = (97, 63, 46)
        self.onHoverColor = (186, 128, 82)
        self.textColor = (0, 0, 0)
        self.pyfont = pygame.font.Font(None, 50)
        self.y = 25

    def drawCursor(self, pos):
        if pos[0] > 0 and pos[1] > 0:
            self.screen.blit(cursor1, (pos[0], pos[1]))

    def actualPosition(self):
        self.rect1_top = pygame.Rect((500, 100 - self.y, 300, 100))
        self.rect1_bottom = pygame.Rect((500, 110 - self.y, 300, 100))
        self.rect2_top = pygame.Rect((500, 250 - self.y, 300, 100))
        self.rect2_bottom = pygame.Rect((500, 260 - self.y, 300, 100))
        self.rect3_top = pygame.Rect((500, 400 - self.y, 300, 100))
        self.rect3_bottom = pygame.Rect((500, 410 - self.y, 300, 100))
        self.rect4_top = pygame.Rect((500, 550 - self.y, 300, 100))
        self.rect4_bottom = pygame.Rect((500, 560 - self.y, 300, 100))

    def drawMenu(self):
        text = self.pyfont.render("CONNECT", True, self.textColor)
        pygame.draw.rect(self.screen, self.color1_bottom, self.rect1_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color1_top, self.rect1_top, border_radius = 15)
        self.screen.blit(text, (self.rect1_top.centerx - 80, self.rect1_top.centery - 15))

        text = self.pyfont.render("HOST", True, self.textColor)
        pygame.draw.rect(self.screen, self.color2_bottom, self.rect2_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color2_top, self.rect2_top, border_radius = 15)
        self.screen.blit(text, (self.rect2_top.centerx - 50, self.rect2_top.centery - 15))

        text = self.pyfont.render("JOIN", True, self.textColor)
        pygame.draw.rect(self.screen, self.color3_bottom, self.rect3_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color3_top, self.rect3_top, border_radius = 15)
        self.screen.blit(text, (self.rect3_top.centerx - 45, self.rect3_top.centery - 15))

        text = self.pyfont.render("BACK", True, self.textColor)
        pygame.draw.rect(self.screen, self.color4_bottom, self.rect4_bottom, border_radius = 15)
        pygame.draw.rect(self.screen, self.color4_top, self.rect4_top, border_radius = 15)
        self.screen.blit(text, (self.rect4_top.centerx - 50, self.rect4_top.centery - 15))
    
    def checkCollision(self):
        self.pos = pygame.mouse.get_pos()
        if self.rect1_top.collidepoint(self.pos):
            self.color1_top = self.onHoverColor
            self.rect1_top = pygame.Rect((490, 100 - self.y, 320, 120))
            self.rect1_bottom = pygame.Rect((490, 110 - self.y, 320, 120))
        else:
            self.rect1_top = pygame.Rect((500, 100 - self.y, 300, 100))
            self.rect1_bottom = pygame.Rect((500, 110 - self.y, 300, 100))
            self.color1_top = self.topColor
        
        if self.rect2_top.collidepoint(self.pos):
            self.color2_top = self.onHoverColor
            self.rect2_top = pygame.Rect((490, 250 - self.y, 320, 120))
            self.rect2_bottom = pygame.Rect((490, 260 - self.y, 320, 120))
        else:
            self.rect2_top = pygame.Rect((500, 250 - self.y, 300, 100))
            self.rect2_bottom = pygame.Rect((500, 260 - self.y, 300, 100))
            self.color2_top = self.topColor
        
        if self.rect3_top.collidepoint(self.pos):
            self.color3_top = self.onHoverColor
            self.rect3_top = pygame.Rect((490, 400 - self.y, 320, 120))
            self.rect3_bottom = pygame.Rect((490, 410 - self.y, 320, 120))
        else:
            self.rect3_top = pygame.Rect((500, 400 - self.y, 300, 100))
            self.rect3_bottom = pygame.Rect((500, 410 - self.y, 300, 100))
            self.color3_top = self.topColor

        if self.rect4_top.collidepoint(self.pos):
            self.color4_top = self.onHoverColor
            self.rect4_top = pygame.Rect((490, 550 - self.y, 320, 120))
            self.rect4_bottom = pygame.Rect((490, 560 - self.y, 320, 120))
        else:
            self.rect4_top = pygame.Rect((500, 550 - self.y, 300, 100))
            self.rect4_bottom = pygame.Rect((500, 560 - self.y, 300, 100))
            self.color4_top = self.topColor

    def run(self):
        hold = True
        self.actualPosition()
        self.drawMenu()
        connection = False
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
                if event.type == pygame.MOUSEBUTTONUP:
                    self.actualPosition()
                    if self.rect1_top.collidepoint(self.pos):
                        print("CONNECT")
                        connection = True
                        hold = False
                    elif self.rect2_top.collidepoint(self.pos):
                        print("HOST")
                    elif self.rect3_top.collidepoint(self.pos):
                        print("JOIN")
                    elif self.rect4_top.collidepoint(self.pos):
                        hold = False
            self.drawMenu()
            #self.drawCursor(pygame.mouse.get_pos())
            pygame.display.update()
        return connection

'''if __name__ == '__main__':
    hostjoin = HostJoin()
    hostjoin.run()'''