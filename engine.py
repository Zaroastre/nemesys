from abc import abstractmethod
import logging
from sqlite3 import Cursor, connect as connect_to_sql, Connection as SqlConnection;
from threading import Thread;
from socket import socket as Socket, AF_INET, SOCK_STREAM

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("./program.log"),
        logging.StreamHandler()
    ]
);

class Powerable:
    """Interface that represents a thing able to be turned on/off.
    """
    @abstractmethod
    def start(self):
        """Turn on.
        """
        raise Exception("Not yet implemented.")
        
    @abstractmethod
    def stop(self):
        """Turn off.
        """
        raise Exception("Not yet implemented.")

class ClientConnection(Thread):
    """Class that represents a Client Connection.

    Args:
        Thread (Thread): Super class.
    """

    __ENCODING: str = "UTF-8";

    def __init__(self, server: Socket, client: Socket) -> None:
        """Default Client Connection Constructor.

        Args:
            server (Socket): Server connection.
            client (Socket): Client connection.
        """
        Thread.__init__(self);
        self.__server: Socket = server;
        self.__client: Socket = client;
        self.__is_running: bool = False;
    
    def login(self) -> bool:
        """Authenticate the connection.

        Returns:
            bool: True is is successfully authenticated, else False.
        """
        logging.debug("Starting login process...")
        self.__client.send("401".encode(ClientConnection.__ENCODING));
        raw_credentials: bytes = self.__client.recv(1024)
        logging.debug("Credentials: {}".format(raw_credentials));
        credentials: list[str] = raw_credentials.decode(ClientConnection.__ENCODING).split(':');
        sql_connection: SqlConnection = connect_to_sql("./nemesys.db");
        cursor: Cursor = sql_connection.cursor();
        SQL_QUERY: str = "SELECT * FROM User WHERE username=? AND password=?;";
        logging.debug("SQL query to execute: {}".format(SQL_QUERY));
        logging.debug("SQL values: {}".format(credentials));
        cursor.execute(SQL_QUERY, (credentials[0], credentials[1]));
        result: list = cursor.fetchall();
        logging.debug("SQL result: {}".format(result));
        return len(result) == 1;

    def run(self) -> None:
        logging.debug("Client and server are starting exchanges.");
        self.__is_running = True;
        self.__client.send("Welcome on the moon!".encode(ClientConnection.__ENCODING));
        is_authenticated: bool = self.login();
        if (is_authenticated):
            while (self.__is_running):
                self.__is_running = False;

class GameServerEngine(Thread):
    """Class that represents the game server's engine.

    Args:
        Thread (Thread): Super class.
    """
    def __init__(self, port: int) -> None:
        """Default Engine Constructor.

        Args:
            port (int): Port to use for incomming clients connections.
        """
        Thread.__init__(self);
        self.__port: int = port;
        self.__socket: Socket = Socket(AF_INET, SOCK_STREAM);
        self.__is_running: bool = False;
        self.__connections: list[ClientConnection] = [];

    def __disconnect_all_clients(self):
        """Disconnect all clients.
        """
        for client in self.__connections:
            try:
                client.close();
            finally:
                print("Client is disconnected.");
        self.__connections.clear();
        

    def run(self) -> None:
        self.__disconnect_all_clients();
        self.__socket.bind(("0.0.0.0", self.__port));
        self.__socket.listen(7);
        self.__is_running = True;
        while (self.__is_running):
            client_socket, client_info = (None, None);
            logging.debug("Waiting for client connection...");
            try:
                client_socket, client_info = self.__socket.accept();
            except:
                print("Game server will be stopped...");
                self.__is_running = False;
            else:
                logging.debug("A new client is connected: {}".format(client_info));
                connection: ClientConnection = ClientConnection(server=self.__socket, client=client_socket);
                self.__connections.append(connection);
                connection.start();


    def terminate(self):
        """Stop engine.
        """
        self.__is_running = False;
        self.__socket.close();

class ServerGame(Powerable):
    """Class that represents a Game Server.

    Args:
        Powerable (Powerable): Interface to implement to repesct the Powerable API.
    """
    __INSTANCE = None;
    
    def __init__(self, port: int) -> None:
        """Default Server Game Constructor.
        
        Args:
            port (int): Port to use for incomming clients connections.
        """
        self.__engine: GameServerEngine = GameServerEngine(port);

    @staticmethod
    def get_instance(port: int):
        """Get the unique Server Game instance.

        Args:
            port (int): Port to use for incomming clients connections.

        Returns:
            ServerGame: The ServerGame unique instance.
        """
        if (ServerGame.__INSTANCE == None):
            ServerGame.__INSTANCE = ServerGame(port);
        return ServerGame.__INSTANCE;

    def start(self):
        logging.debug("Server Game is starting GameServerEngine...");
        self.__engine.start();
    
    def stop(self):
        self.__engine.terminate();

server = ServerGame.get_instance(9600);
server.start();