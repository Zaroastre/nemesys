class MenuItem:
    def __init__(self, id: int, text: str) -> None:
        self.__id: int = id;
        self.__text: str = text;
    
    def get_id(self) -> int:
        return self.__id;

    def get_text(self) -> str:
        return self.__text;

class Menu:
    def __start_new_game(self):
        """Start a new game.
        """
        print("New game will start.");

    def __continue_game(self):
        """Continue game loading an existing backup.
        """
        print("Loading...");

    def __quit(self):
        """Exit the game.
        """
        print("Bye bye");
    
    def display_menu(self):
        """Display menu's items and allow user to select action to process.
        """
        items: list[MenuItem] = [
            MenuItem(1, "Start new game"),
            MenuItem(2, "Continue game"),
            MenuItem(3, "Quit"),
        ];
        user_choice: int = 0;
        valid_values: list[int] = [value.get_id() for value in items];
        while (user_choice not in valid_values):
            for item in items:
                print("[{}] - {}".format(item.get_id(), item.get_text()));
            try:
                user_choice = int(input("User choice: "));
            except:
                print("Invalid user choice.");
        self.__process_user_choice(user_choice);

    def __process_user_choice(self, user_choice: int):
        """Execute the user choice.

        Args:
            user_choice (int): User choice to process.

        Raises:
            Exception: Invalid user choice.
        """
        match (user_choice):
            case 1:
                self.__start_new_game();
            case 2:
                self.__continue_game();
            case 3:
                self.__quit();
            case _:
                raise Exception("Invalid user choice.");
