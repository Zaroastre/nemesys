from abc import abstractmethod
import logging
from socket import AF_INET, SOCK_STREAM, socket as Socket;
from threading import Thread;

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

class GameClientEngine(Thread):
    """Class that represents the game server's engine.

    Args:
        Thread (Thread): Super class.
    """
    def __init__(self, server: str, port: int) -> None:
        """Default Engine Constructor

        Args:
            server (str): Remote Game Server IP address or hostname.
            port (int): Remote Game Server port. 
        """
        Thread.__init__(self);
        self.__connection: Socket = Socket(AF_INET, SOCK_STREAM);
        self.__server: str = server;
        self.__port: str = port;
        self.__is_running: bool = False;

    def run(self) -> None:
        self.__is_running = True;
        try:
            self.__connection.connect((self.__server, self.__port));
            raw_banner: bytes = self.__connection.recv(1024);
            banner: str = raw_banner.decode("UTF-8");
            print(banner);
            raw_status_code: bytes = self.__connection.recv(1024);
            status_code: int = int(raw_status_code.decode("UTF-8"));
            match (status_code):
                case 401:
                    self.__connection.send("nicolas.metivier:Nemesys".encode("UTF-8"));
        except:
            print("Game server is not available.");


    def terminate(self):
        """Stop engine.
        """
        self.__is_running = False;
        self.__connection.close();

class ClientGame(Powerable):
    """Class that represents a Game Client.

    Args:
        Powerable (Powerable): Interface to implement to repesct the Powerable API.
    """
    __INSTANCE = None;
    
    def __init__(self, server: str, port: int) -> None:
        """Default Client Game Constructor

        Args:
            server (str): Remote Game Server IP address or hostname.
            port (int): Remote Game Server port. 
        """
        self.__server: str = server;
        self.__port: int = port;
        self.__engine: GameClientEngine = GameClientEngine(server=self.__server, port=self.__port);

    @staticmethod
    def get_instance(server: str = None, port: int = 0):
        """Get the unique Client Game instance.

        Returns:
            ClientGame: The ClientGame unique instance.
        """
        if (ClientGame.__INSTANCE == None):
            if (server == None or port == 0):
                raise Exception("'server' and 'port' parameters are mandatory but one of these was not found.")
            ClientGame.__INSTANCE = ClientGame(server, port);
        else:
            if (server == None or port == 0):
                logging.warning("Some paramters was redefined but will be ignored: server: {}, port: {}".format(server, port));
        return ClientGame.__INSTANCE;

    def start(self):
        self.__engine.start();
    
    def stop(self):
        self.__engine.terminate();

client = ClientGame("127.0.0.1", 9600);
client.start()