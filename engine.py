from abc import abstractmethod
from sqlite3 import Cursor, connect as connect_to_sql, Connection as SqlConnection;
from threading import Thread;
from socket import socket as Socket, AF_INET, SOCK_STREAM

class Powerable:
    @abstractmethod
    def start(self):
        raise Exception("Not yet implemented.")
        
    @abstractmethod
    def stop(self):
        raise Exception("Not yet implemented.")

class ClientConnection(Thread):

    __ENCODING: str = "UTF-8";

    def __init__(self, server: Socket, client: Socket) -> None:
        Thread.__init__(self);
        self.__server: Socket = server;
        self.__client: Socket = client;
        self.__is_running: bool = False;
    
    def login(self) -> bool:
        self.__client.send("401".encode(ClientConnection.__ENCODING));
        raw_credentials: bytes = self.__client.recv(1024)
        credentials: list[str] = raw_credentials.decode(ClientConnection.__ENCODING).split(':');
        # username:password
        sql_connection: SqlConnection = connect_to_sql("./nemesys.db");
        cursor: Cursor = sql_connection.cursor();
        cursor.execute("SELECT * FROM Player WHERE username=? AND password=?;", (credentials[0], credentials[1]));
        result: list = cursor.fetchall();
        for line in result:
            print(line);        
        return len(result) == 1;

    def run(self) -> None:
        self.__is_running = True;
        self.__client.send("Welcome on the moon!".encode(ClientConnection.__ENCODING));
        is_authenticated: bool = self.login();
        print(is_authenticated);
        if (is_authenticated):
            while (self.__is_running):
                self.__is_running = False;

class Engine(Thread):
    def __init__(self) -> None:
        Thread.__init__(self);
        self.__socket: Socket = Socket(AF_INET, SOCK_STREAM);
        self.__is_running: bool = False;
        self.__connections: list[ClientConnection] = [];

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
                print("Game server will be stopped...");
                self.__is_running = False;
            else:
                connection: ClientConnection = ClientConnection(server=self.__socket, client=client_socket);
                self.__connections.append(connection);
                connection.start();


    def terminate(self):
        self.__is_running = False;
        self.__socket.close();

class ServerGame(Powerable):
    __INSTANCE = None;
    
    def __init__(self) -> None:
        self.__engine: Engine = Engine();
        self.__initialize_database();
    
    def __initialize_database(self):
        sql_connection: SqlConnection = connect_to_sql("./nemesys.db");
        cursor: Cursor = sql_connection.cursor();
        cursor.execute("CREATE TABLE IF NOT EXISTS Player (identifier INT PRIMARY KEY, username VARCHAR(30) UNIQUE NOT NULL, password VARCHAR(250) NOT NULL);");
        sql_connection.commit();
        cursor.close();
        sql_connection.close();

    @staticmethod
    def get_instance():
        if (ServerGame.__INSTANCE == None):
            ServerGame.__INSTANCE = ServerGame();
        return ServerGame.__INSTANCE;

    def start(self):
        self.__engine.start();
    
    def stop(self):
        self.__engine.terminate();

server = ServerGame.get_instance();
