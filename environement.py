from abc import abstractmethod;
from amunation import Weapon, OneHandSwordBuilder, TwoHandsAxeBuilder;
from random import randint;
from threading import Thread;
from time import sleep;

HEALTH_POTION: str = "Health Potion";

class Attackable:
    """Interface that represent a thing that able to attack.
    """
    @abstractmethod
    def attack(self):
        """Attack another thing.
        """
        raise Exception("Not implemented.");

class Liveable:
    """Interface that represent a thing that able to live or die.
    """
    @abstractmethod
    def get_current_life_points(self) -> int:
        """Get current life points that left.

        Returns:
            int: Life points.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def get_maximal_life_points(self) -> int:
        """Get maximal life points.

        Returns:
            int: Life points.
        """
        raise Exception("Not implemented.");
    
    @abstractmethod
    def decrease_life_points(self, damage: int):
        """Decrease current life points.

        Args:
            damage (int): Damage.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def increase_life_points(self, life_points: int):
        """Increase current life points.

        Args:
            life_points (int): Life points.
        """
        raise Exception("Not implemented.");
    
    @abstractmethod
    def is_alive(self) -> bool:
        """Check if is alive.

        Returns:
            bool: True if it's alive, else False if die.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def die(self):
        """Die.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def born(self):
        """Born.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def get_name(self) -> str:
        """Get the name.

        Returns:
            str: The name.
        """
        raise Exception("Not implemented.");

class Evolveable:
    """Interface that represent a thing that able to evolve.
    """

    @abstractmethod
    def get_current_experience_points(self) -> int:
        """Get the current experience points.

        Returns:
            int: Experience points.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def get_maximal_experience_points(self) -> int:
        """Get the maximal experience points.

        Returns:
            int: Maximal experience points.
        """
        raise Exception("Not implemented.");
    
    @abstractmethod
    def increase_experience(self, total_experience_to_win: int):
        """Increase experience with win experience.

        Args:
            total_experience_to_win (int): Experience points to use.
        """
        raise Exception("Not implemented.");

    @abstractmethod
    def increase_level(self, total_levels_to_win: int = 1):
        """Increase the level with win level.

        Args:
            total_levels_to_win (int, optional): Total level to win. Defaults to 1.
        """
        raise Exception("Not implemented.");

class Player(Attackable, Liveable, Evolveable):
    """CLass that represents a Player.

    Args:
        Attackable (Attackable): Interface to implement to repesct the Attackable API.
        Liveable (Liveable): Interface to implement to repesct the Liveable API.
        Evolveable (Evolveable): Interface to implement to repesct the Evolveable API.
    """

    def __init__(self) -> None:
        """Player Constructor.
        """
        self.__name: str = "Nicolas";
        self.__maximal_life_points: int = 100; 
        self.__current_life_points: int = self.__maximal_life_points;
        self.__maximal_experience_points: int = 100; 
        self.__current_experience_points: int = 0;
        self.__level: int = 1;
        self.__weapon: Weapon = OneHandSwordBuilder().with_damage_min(1).with_damage_max(10).with_speed(0.8).build();
        self.__inventory: dict = {};

    def get_level(self) -> int:
        """Get the player level.

        Returns:
            int: The level.
        """
        return self.__level;

    def get_current_life_points(self) -> int:
        return self.__current_life_points;

    def get_maximal_life_points(self) -> int:
        return self.__maximal_life_points

    def get_name(self) -> str:
        return self.__name;

    def decrease_life_points(self, damage: int):
        self.__current_life_points -= damage;
        if (not self.is_alive()):
            self.die();

    def increase_life_points(self, life_points: int):
        self.__current_life_points += life_points;

    def is_alive(self) -> bool:
        return self.__current_life_points > 0;

    def die(self):
        self.__current_life_points = 0;

    def born(self):
        self.__current_life_points = self.__maximal_life_points;

    def get_current_experience_points(self) -> int:
        return self.__current_experience_points;
    
    def get_maximal_experience_points(self) -> int:
        return self.__maximal_experience_points;
    
    def increase_level(self, total_levels_to_win: int = 1):
        if (total_levels_to_win < 1):
            raise Exception("Invalid value: negative and zero value are prohibited.");
        self.__level += total_levels_to_win;
        if (self.__level > 10):
            self.__level = 10;
        self.__current_experience_points = 0;
        self.__maximal_experience_points = 100 * self.__level;
    
    def increase_experience(self, total_experience_to_win: int):
        if (total_experience_to_win < 1):
            raise Exception("Invalid value: negative and zero value are prohibited.");
        self.__current_experience_points += total_experience_to_win;
        if (self.__current_experience_points >= self.__maximal_experience_points):
            self.increase_level();

    def __get_loot(self, loot: dict):
        """Get loot.

        Args:
            loot (dict): Loot to retrieve.
        """
        for loot_key in loot.keys():
            if (loot_key in self.__inventory.keys()):
                self.__inventory[loot_key] = self.__inventory.get(loot_key) + loot.get(loot_key);
            else:
                self.__inventory[loot_key] = loot.get(loot_key);
        loot.clear();

    def __attack(self) -> int:
        """Throw an attack.

        Returns:
            int: Damage to inflict.
        """
        damage:int = self.__weapon.inflict_damage();
        return damage;

    def hit(self, target: Liveable):
        """Attack the target.

        Args:
            target (Liveable): Target to attack.
        """
        damage: int = self.__attack();
        print("{} is attacking the target named {} and inflict {} damage.".format(self.__name, target.get_name(), damage));
        target.decrease_life_points(damage);
    
    def attack(self, target: Liveable, auto_attack: bool):
        """Attack the target repetly.

        Args:
            target (Liveable): Target to attack.
            auto_attack (bool): True to repeat attack on target.
        """
        if (auto_attack):
            while (target.is_alive() and self.is_alive()):
                self.hit(target);
                sleep(1-self.__weapon.get_speed());
                print("{} left {} PV.".format(target.get_name(), target.get_current_life_points()));
        else:
            self.hit(target);

        if (not target.is_alive()):
            target.die();
            if (isinstance(target, Trash)):
                self.increase_experience(target.get_experience());
                self.__get_loot(target.get_inventory());

class Trash(Thread, Attackable, Liveable):
    """Class that represents a Trash.

    Args:
        Attackable (Attackable): Interface to implement to repesct the Attackable API.
        Liveable (Liveable): Interface to implement to repesct the Liveable API.
    """
    def __init__(self) -> None:
        """Trash Constrcutor.
        """
        Thread.__init__(self);
        self.__name: str = "Arthas";
        self.__level: int = 1;
        self.__experience: int = 5;
        self.__maximal_life_points: int = 100; 
        self.__current_life_points: int = self.__maximal_life_points;
        self.__weapon: Weapon = TwoHandsAxeBuilder().with_damage_min(10).with_damage_max(30).with_speed(0.1).build();
        self.__inventory: dict = self.__generate_inventory();
        self.__target: Liveable = None;
    
    def __generate_inventory(self) -> dict:
        """Generate randomly an inventory.

        Returns:
            dict: The generated inventory.
        """
        inventory: dict = {};
        chance: int = randint(0,100);
        if (chance >= 80):
            inventory[HEALTH_POTION] = 1;
        return inventory;
    
    def get_experience(self) -> int:
        """Get the experience.

        Returns:
            int: Experience
        """
        return self.__experience;

    def get_inventory(self) -> dict:
        """Get the inventory.

        Returns:
            dict: Inventory.
        """
        return self.__inventory;

    def get_current_life_points(self) -> int:
        return self.__current_life_points;

    def get_maximal_life_points(self) -> int:
        return self.__maximal_life_points

    def get_name(self) -> str:
        return self.__name;

    def decrease_life_points(self, damage: int):
        self.__current_life_points -= damage;
        if (not self.is_alive()):
            self.die();

    def increase_life_points(self, life_points: int):
        self.__current_life_points += life_points;

    def is_alive(self) -> bool:
        return self.__current_life_points > 0;

    def die(self):
        self.__current_life_points = 0;

    def born(self):
        self.__current_life_points = self.__maximal_life_points;

    def __attack(self):
        damage:int = self.__weapon.inflict_damage();
        print("{} The weapon inflict: {} damage.".format(self.__name, damage));
        return damage;
    
    def attack(self, target: Liveable):
        """Hit/Attack the target.

        Args:
            target (Liveable): Target to attack.
        """
        self.__target = target;
        damage: int = self.__attack();
        print("{} is attacking the target named {} and inflict {} damage.".format(self.__name, self.__target.get_name(), damage));
        self.__target.decrease_life_points(damage);
        print("{} left {} PV.".format(target.get_name(), target.get_current_life_points()));

    
    def run(self) -> None:
        while (self.is_alive() and self.__target.is_alive()):
            self.attack(self.__target);
            sleep(1-self.__weapon.get_speed());
        if (not self.is_alive()):
            self.die();
