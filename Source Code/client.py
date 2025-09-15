import socket
import threading
import pygame
import draw

pygame.init()

class Client:
    def __init__(self, PORT, screen) -> None:
        self.PORT = PORT
        self.IPv4 = socket.gethostbyname(socket.gethostname())
        #self.IPv4 = "192.168.0.54"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.content = []
        self.color = "White"
        self.change = False
        self.currntMove = "White"
        self.screen = screen
        self.username = ""
    
    def fetch_content(self):
        return self.content, self.IPv4, self.PORT, self.address
    
    def update_game(self, white_pieces, black_pieces, white_captured_pieces, black_captured_pieces, currntMove):
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.white_captured_pieces = white_captured_pieces
        self.black_captured_pieces = black_captured_pieces
        self.currntMove = currntMove

    def reflect_changes(self):
        return self.white_pieces, self.black_pieces, self.white_captured_pieces, self.black_captured_pieces, self.currntMove
    
    #def client_color(self):
    #    return self.color


    def str_to_lists(self, data): # Slice string and covert it to 3 lists then replace the strings with pygame.image.load() surfaces.
        piece = data.split("~")[1] #D1~((562.5, 87.5, <Surface(70x70x32 SW)>, 'White Pawn', 'Selected', 'Not FirstMove', 1), [562.5, 262.5])
        x = piece.split(",")[0]
        x = x[2::]
        y = piece.split(",")[1]
        y = y[1::]
        x, y = float(x), float(y)
        xchange = piece.split(",")[-2]
        xchange = xchange[2::]
        ychange = piece.split(",")[-1]
        ychange = ychange[1:]
        ychange = ychange.split("]")[0]
        xchange, ychange = float(xchange), float(ychange)
        if data[0] == "W":
            self.currntMove = "Black"
            for i, piece in enumerate(self.white_pieces):
                if piece[0] == x and piece[1] == y:
                    change = self.white_pieces.pop(i)
                    change = list(change)
                    change[0], change[1] = xchange, ychange
                    self.move.ScoreW += piece[6]
                    self.white_pieces.insert(i, tuple(change))
            for i, enemy in enumerate(self.black_pieces):
                if enemy[0] == xchange and enemy[1] == ychange:
                    captured = self.black_pieces.pop(i)
                    for j, capturedPieces in enumerate(self.black_captured_pieces):
                        if capturedPieces[1] == captured[3]:
                            update = self.black_captured_pieces.pop(j)
                            update = list(update)
                            update[2] += 1
                            self.black_captured_pieces.insert(j, tuple(update))
        elif data[0] == "B":
            self.currntMove = "White"
            for i, piece in enumerate(self.black_pieces):
                if piece[0] == x and piece[1] == y:
                    change = self.black_pieces.pop(i)
                    change = list(change)
                    change[0], change[1] = xchange, ychange
                    self.move.ScoreB += piece[6]
                    self.black_pieces.insert(i, tuple(change))
            for i, enemy in enumerate(self.white_pieces):
                if enemy[0] == xchange and enemy[1] == ychange:
                    captured = self.white_pieces.pop(i)
                    for j, capturedPieces in enumerate(self.white_captured_pieces):
                        if capturedPieces[1] == captured[3]:
                            update = self.white_captured_pieces.pop(j)
                            update = list(update)
                            update[2] += 1
                            self.white_captured_pieces.insert(j, tuple(update))
        username = data.split("~")[0]
        return username[1::]

    def change_WtoB_BtoW(self):
        if self.currntMove == "White":
            self.currntMove = "Black"
        elif self.currntMove == "Black":
            self.currntMove = "White"

    def listening_for_data(self) -> None:
        while True:
            data = self.client.recv(2048).decode('utf-8')
            print(data)
            if data:
                print(data)
                if data[0] == "T":
                    print("[SENDING ACTIVE STATUS]...")
                    print(f"T~{self.username}~{data.split("~")[1]}")
                    self.client.sendall(f"T~{self.username}~{data.split("~")[1]}")
                if data[0] == "M": # "M" stands for message
                    self.content.append(data)
                    '''if data.split("~")[1] == "--cls|chat--":
                        self.content = []'''
                    if len(self.content) > 11:
                        self.content.pop(0)
                elif data[0] == "W" or data[0] == "B":# "D" stands for data
                    username = self.str_to_lists(data)
                    #print(f"[{username}] {data.split("~")[1]}")
            else:
                print(f"The message received from the client is empty")
    
    def send_data_once(self, data) -> None:
        color = data[0][3].split(" ")[0]
        if color == "White":
            data = f"W{self.username}~{data}"
        elif color == "Black":
            data = f"B{self.username}~{data}"
        self.client.sendall(data.encode('utf-8'))

    def send_data(self, text) -> None:
        #message = input("Enter your message: ")
        text = f"M{self.username}~{text}" 
        # Adding 'M' in start means it's a message and 'D' it means it's a data packet
        #print(message)
        self.client.sendall(text.encode('utf-8'))

    def updateMove(self, move):
        self.move = move

    def receive_clientMove(self):
        return self.client.recv(2048).decode('utf-8')
    
    def kill_program(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

    def start_communication(self) -> None:
        run = True
        drawChess = draw.DrawChess(self.screen, "OnServer")
        font = pygame.font.Font(None, 55)
        self.username = ""
        
        while run:
            drawChess.updateScore(self.move.ScoreW, self.move.ScoreB)
            drawChess.background()
            self.rect = pygame.Rect((400, 300, 500, 100))
            pygame.draw.rect(self.screen, (200, 200, 200), self.rect, border_radius=10)
            text = font.render(f"Enter your username here :)", True, (0, 0, 0))
            self.screen.blit(text, (400, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.username != "":
                            run = False
                            continue
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[0:len(self.username) - 1]
                        continue
                    self.username += event.unicode
            username = font.render(f"{self.username}", True, (0, 0, 0))
            self.screen.blit(username, (410, 335))
            #drawChess.drawCursor(pygame.mouse.get_pos())
            pygame.display.update()
        font = pygame.font.Font(None, 75)
        drawChess.background()
        text = font.render(f"Waiting for other player...", True, (0, 0, 0))
        self.screen.blit(text, (350, 300))
        pygame.display.update()
        if self.username != "":
            self.client.sendall(self.username.encode())
        else:
            print("Uesrname can't be empty")
            exit(0)
        self.clientMove = self.client.recv(2048).decode('utf-8')
        threading.Thread(target=self.listening_for_data, args = ()).start()
        #threading.Thread(target=self.kill_program, daemon=True, args=()).start()
        #threading.Thread(target=self.send_data, daemon=True, args=()).start()


    def run(self) -> None:
        try:
            self.client.connect((self.IPv4, self.PORT))
            self.address = self.client.recv(2056).decode('utf-8')
            print(f"[CONNECTED TO SERVER]...")
        except:
            print(f"[UNABLE TO CONNECT TO SERVER]...")
        self.start_communication()
        return self.username, self.clientMove

if __name__ == '__main__':
    screen = pygame.display.set_mode((1300, 700))
    client = Client(8080, screen)
    client.run()