from socket import socket, AF_INET, SOCK_STREAM, error, SOL_SOCKET, SO_REUSEADDR
import random
import threading

BUFFSIZE = 2048


class Server:
    def __init__(self):
        print("Server is initiated but not started")

    def start(self, host='', port=7557):
        print("Server is starting....")
        BUFFSIZE = 2048
        clients = set()
        clients_r = {}
        clients_lock = threading.Lock()
        Currentid = 0
        print("37%")
        try:
            s = socket()
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1000)
            th = []
            print("89%")
        except error as ex:
            print("Something went wrong during server binding : " + str(ex))
            exit(7557642)

        def processdata(data, client, clients_r):
            if data == "ID":
                client.send(bytes(str(Currentid), encoding="utf8"))
            elif data.split('|')[0] == "S":
                data = data.split('|')
                if int(data[1]) in clients_r:
                    clients_r[int(data[1])].send(bytes(data[2], encoding="utf8"))  # Do your stuff

        def listener(client, address):
            try:
                print("Accepted connection from: ", address)
                with clients_lock:
                    clients.add(client)
                    clients_r[Currentid] = client
                try:
                    while True:
                        data = client.recv(BUFFSIZE).decode("utf-8")
                        print("Received :" + str(data) + " from " + str(address))
                        with clients_lock:
                            processdata(data, client, clients_r)
                finally:
                    with clients_lock:
                        clients.remove(client)
                        client.close()
            except error as ex:
                print("Something went wrong during server execution\nError code" + str(
                    ex.errno) + "\nError text:" + str(ex.strerror))

        print("100%")
        print("Server is running stable")
        while True:
            Currentid += random.randint(10, 150)
            client, address = s.accept()
            th.append(threading.Thread(target=listener, args=(client, address)).start())

        s.close()


class Client:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 7557
        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        self.id = -1
        try:
            self.tcp_client.connect((self.host, self.port))
            self.requestid()
        except error as ex:
            print("Something went wrong while trying to connect to server\nError code: " + str(
                ex.errno) + "\nError text:" + str(ex.strerror))

    def send(self, message):
        try:
            self.tcp_client.send(bytes(message, encoding="utf8"))
        except error as ex:
            print("Something went wrong while sending the message\nError code: " + str(
                ex.errno) + "\nError text:" + str(ex.strerror))

    def recv(self):
        try:
            return self.tcp_client.recv(BUFFSIZE).decode("utf-8")
        except error as ex:
            print("Something went wrong while receiving data from server\nError code: " + str(
                ex.errno) + "\nError text:" + str(ex.strerror))

    def requestid(self):
        try:
            self.tcp_client.send(bytes("ID", encoding="utf8"))
            self.id = int(self.recv())
        except error as ex:
            print("Something went wrong while requesting id from the server\nError code: " + str(
                ex.errno) + "\nError text:" + str(ex.strerror))

    def sendtoid(self, ID, message):
        try:
            self.tcp_client.send(bytes("S|" + str(ID) + "|" + str(message), encoding="utf8"))
        except error as ex:
            print("Something went wrong while sending data to id " + str(ID) + "\nError code: " + str(
                ex.errno) + "\nError text:" + str(ex.strerror))
