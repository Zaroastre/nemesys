from platform import python_version
from sqlite3 import Cursor, connect as connect_to_sql, Connection as SqlConnection;
import logging;

from menu import Menu

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("./program.log"),
        logging.StreamHandler()
    ]
);

def is_valid_python_version() -> bool:
    """Check if the running Python is a valid version.

    Returns:
        bool: True if it's a valid Python version, else False.
    """
    is_valid = False;
    minimal_major: int = 3;
    minimal_minor: int = 10;
    version_parts: list[int] = [int(part) for part in python_version().split(".")];
    if (version_parts[0] >= minimal_major and version_parts[1] >= minimal_minor):
        is_valid = True;
    return is_valid;

def initialize_database():
    """Initialize the database for the game.
    """
    RESOURCES_FOLDER: str = "./resources/sql";
    sql_connection: SqlConnection = connect_to_sql("./nemesys.db");
    cursor: Cursor = sql_connection.cursor();
    sql_files: list[str] = ["authentication.sql", "amunition.sql", "player.sql"]

    for file_name in sql_files:
        logging.debug("Executing SQL script file: {}/{}".format(RESOURCES_FOLDER, file_name))
        with open("{}/{}".format(RESOURCES_FOLDER, file_name), 'r') as file:
            script: str = file.read();
            logging.debug("Script to execute: {}".format(script))
            cursor.executescript(script);
    sql_connection.commit();
    cursor.close();
    sql_connection.close();

def main():
    logging.info("Application is starting...");
    logging.debug("Checking requirements...");
    if (is_valid_python_version()):
        logging.debug("A valid Python version is used.");
        logging.debug("Initializing database...")
        initialize_database();
        logging.debug("Database is successully initialized.")
        menu: Menu = Menu();
        menu.display_menu();
    else:
        logging.error("Python version is outdated. Please, upgrade to the lastest Python version. (Python 3.10 is minimal required version)");
    logging.info("Application is exiting...")
if (__name__ == "__main__"):
    main();
