from ast import literal_eval;

def save_game(data_to_save: dict, backup_file: str):
    """Save the game.

    Args:
        data_to_save (dict): Data to save.
        backup_file (str): Destination backup file that will contains data to save.

    Raises:
        error: Access backup file exception.
    """
    try:
        with open(backup_file, "wb") as file:
            file.write(str(data_to_save).encode("UTF-8"));
    except Exception as error:
        raise error;

def load_game(backup_file: str) -> dict:
    """Load a backup game.

    Args:
        backup_file (str): Destination backup file that will contains data to load.

    Raises:
        error: Access backup file exception.

    Returns:
        dict: Loaded game data.
    """
    game_data: dict = None
    try:
        with open(backup_file, "rb") as file:
            game_data = literal_eval(file.read().decode("UTF-8"));

    except Exception as error:
        raise error;

    return game_data;