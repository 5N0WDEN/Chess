import socket
import threading
import time

# After Each 15s server will send a message to client to check wheather the connection is live or not

class Server:
    def __init__(self, PORT) -> None:
        self.PORT = PORT
        self.IPv4 = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IPv4, self.PORT))
        self.active_clients = []
        self.client_to_client = []
        self.content = [] # Basically it will work as FIFO Queue for storing messages.

    def client_helper(self, client):
        username = client.recv(2048).decode('utf-8')
        if username != "":
            self.active_clients.append(tuple([username, client, f"T~{int(time.time())}"]))
            print(self.active_clients)
        else:
            print("Client username is empty")
        while True:
            message = client.recv(2048).decode('utf-8')
            print(message)
            if message[0] == "T": # message format = T~USERNAME~f"{now}"
                username = message.split("~")[1]
                for i, clay in enumerate(self.active_clients):
                    if clay[1] == username:
                        change = list(self.active_clients.pop(i))
                        change[2] = f"T{message.split("~")[2]}"
                        self.active_clients.insert(i, tuple(change))
            username = message.split("~")[0]
            username = username[1::]
            data = message.split("~")[1]
            if len(self.client_to_client):
                for x in self.client_to_client:
                    if x[0][0] == username or x[1][0] == username:
                        x[1][1].sendall(message.encode())
                        x[0][1].sendall(message.encode())
                
    def connect_client_to_client(self):
        while True:
            if len(self.active_clients) > 1:
                first = self.active_clients.pop(0)
                first[1].sendall("White".encode())
                second = self.active_clients.pop(0)
                second[1].sendall("Black".encode())
                self.client_to_client.append(tuple((first, second))) 

    def check_active_clients(self):
        now = int(time.time())
        while True:
            if int(time.time()) - now == 4:
                print("[CHECKING FOR ACTIVE STATUS]...")
                if len(self.active_clients):
                    for client in self.active_clients:
                        print(f"T~{now} {client}")
                        client[1].sendall(f"T~{now}".encode('utf-8'))
                    time.sleep(1)
                    for client in self.active_clients:
                        if client[2] != f"T~{now}":
                            print(f"{client[2]} T~{now}")
                            print("deleted")
                            self.active_clients.remove(client)
                now = int(time.time())
                    

    def run(self) -> None:
        self.server.listen(10)
        threading.Thread(target=self.connect_client_to_client, daemon=True, args=()).start()
        #threading.Thread(target=self.check_active_clients, daemon=True, args=()).start()
        while True:
            client, address = self.server.accept()
            client.sendall((str(address[1])).encode('utf-8'))
            print(f"Successfully connected to client on port {address[1]}")
            try:
                threading.Thread(target=self.client_helper, daemon=True, args=(client, )).start()
            except:
                print("Client forcefully exited")

if __name__ == '__main__':
    server = Server(PORT=8080)
    server.run()