from environement import Player, Trash;

def test_player_increase_level():
    player: Player = Player();
    assert(player.get_level() == 1);
    player.increase_level(2);
    assert(player.get_level() == 3);
    player.increase_level(1);
    assert(player.get_level() == 4);
    player.increase_level(2);
    assert(player.get_level() == 6);

def test_player_increase_experience():
    player: Player = Player();
    assert(player.get_level() == 1);
    assert(player.get_current_experience_points() == 0);
    player.increase_experience(50);
    assert(player.get_current_experience_points() == 50);
    player.increase_experience(50);
    assert(player.get_level() == 2);
    assert(player.get_current_experience_points() == 0);
    player.increase_level(5);
    assert(player.get_level() == 7);

def test_player_attack():
    player: Player = Player();
    counter_trashs : int = 0
    while (counter_trashs < 10):
        arthas: Trash = Trash();
        player.attack(arthas, auto_attack=True);
        counter_trashs += 1;

def test_player_and_trash_fight():
    player: Player = Player();
    mob: Trash = Trash();
    mob.attack(player);
    mob.start();
    player.attack(mob, True);
    print("{} is {} with {} points of life.".format(player.get_name(), "alive" if player.is_alive() else "dead", player.get_current_life_points()));
    print("{} is {} with {} points of life.".format(mob.get_name(), "alive" if mob.is_alive() else "dead", mob.get_current_life_points()));


if (__name__ == "__main__"):
    # test_player_increase_level();
    # test_player_increase_experience();
    test_player_and_trash_fight();
    # test_player_attack();