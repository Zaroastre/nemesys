import logging;

from platform import python_version

logging.basicConfig(
    level=logging.DEBUG,
    filename="./program.log"
    );

def is_valid_python_version():
    is_valid = False;
    minimal_major: int = 3;
    minimal_minor: int = 10;
    version_parts: list[int] = [int(part) for part in python_version().split(".")];
    print(version_parts)
    if (version_parts[0] >= minimal_major and version_parts[1] >= minimal_minor):
        is_valid = True;
    return is_valid;

def main():
    if (is_valid_python_version()):
        logging.warning("Application is starting...");
        try:
            with open("C:/Users/nicolas.metivier/Documents/test-logging.txt", "w") as file:
                file.write("Test de sécurité");
        except Exception as error:
            logging.exception(error);
        logging.info("Applciation is stopping...");

if (__name__ == "__main__"):
    main();
