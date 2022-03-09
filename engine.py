from abc import abstractmethod;
from threading import Thread;
from socket import socket as Socket, AF_INET, SOCK_STREAM
from time import sleep

class Powerable:
    @abstractmethod
    def start(self):
        raise Exception("Not yet implemented.")
        
    @abstractmethod
    def stop(self):
        raise Exception("Not yet implemented.")

class Engine(Thread):
    def __init__(self) -> None:
        Thread.__init__(self);
        self.__socket: Socket = Socket(AF_INET, SOCK_STREAM);
        self.__is_running: bool = False;
        self.__connections: list[Socket] = [];

    def __disconnect_all_clients(self):
        for client in self.__connections:
            try:
                client.close();
            finally:
                print("Client is disconnected.");
        self.__connections.clear();
        

    def run(self) -> None:
        self.__disconnect_all_clients();
        self.__socket.bind(("0.0.0.0", 9600));
        self.__socket.listen(7);
        self.__is_running = True;
        while (self.__is_running):
            client_socket, client_info = (None, None);
            try:
                client_socket, client_info = self.__socket.accept();
            except:
                print("Server is closed.");
            else:
                print(client_info)
        print("Bye bye");

    def terminate(self):
        self.__is_running = False;
        self.__socket.close();

class ServerGame(Powerable):
    __INSTANCE = None;
    def __init__(self) -> None:
        self.__engine: Engine = Engine();

    @staticmethod
    def get_instance():
        if (ServerGame.__INSTANCE == None):
            ServerGame.__INSTANCE = ServerGame();
        return ServerGame.__INSTANCE;

    def start(self):
        self.__engine.start();
    
    def stop(self):
        self.__engine.terminate();
