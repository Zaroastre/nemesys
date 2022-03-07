from game_loader import save_game, load_game;

SAVE_FILE: str = "./backup.json";

def test_save_game():
    player_data: dict = {"name": "Thierry", "level": 10};
    try:
        save_game(data_to_save=player_data, backup_file=SAVE_FILE);
    except Exception as error:
        print("Save game test has failed.");
        raise error;

def test_load_game():
    player_data: dict = None;
    try:
        player_data = load_game(backup_file=SAVE_FILE);
        print(player_data);
        if (player_data == None):
            raise Exception("Loading game test has failed. Player data is null.");
    except Exception as error:
        print("Loading game test has failed.");
        raise error;

if (__name__ == "__main__"):
    test_save_game();
    test_load_game();