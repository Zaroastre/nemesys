import logging

class Logger:

    __INSTANCE = None;

    def __init__(self) -> None:
        format = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.__logger = logging.getLogger()

        file_handler = logging.FileHandler("{}/{}.log".format("./", "video-game.log"))
        file_handler.setFormatter(format)
        self.__logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(format)
        self.__logger.addHandler(console_handler)
    
    @staticmethod
    def get_instance():
        """_summary_

        Returns:
            _type_: _description_
        """
        if (Logger.__INSTANCE == None):
            Logger.__INSTANCE = Logger();
        return Logger.__INSTANCE;
    
    def debug(self, message: str):
        self.__logger.debug(message);
    def info(self, message: str):
        self.__logger.info(message);
    def warn(self, message: str):
        self.__logger.warn(message);
    def warning(self, message: str):
        self.__logger.warning(message);
    def error(self, message: str):
        self.__logger.error(message);
    def exception(self, message: str):
        self.__logger.exception(message);