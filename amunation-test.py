from amunation import Weapon, OneHandSword, WeaponBuilder, OneHandSwordBuilder, WeaponType;

def test_weapon_creation():
    weapon: Weapon = None;
    try:
        weapon = OneHandSword("Aiguille", 1, 10, 1, 0.5, 2.0);
    except Exception as error:
        raise error;
    try:
        weapon = OneHandSword("DeuilleGivre", 285, 875, 80, 2, 0.5);
    except Exception as error:
        raise error;

def test_weapon_damage():
    weapon: Weapon = OneHandSword("Aiguille", 1, 10, 1, 0.5, 2.0);
    damage =  weapon.inflict_damage();
    if ((damage < weapon.get_damage_min()) or (damage > (weapon.get_damage_max()*3))):
        raise "Damage are not valid.";

def test_one_hand_builder():
    builder: WeaponBuilder = OneHandSwordBuilder();
    builder = builder.with_name("Dragon Slayer").with_damage_min(10) \
        .with_damage_max(20) \
        .with_required_level(10) \
        .with_critical_rate(1.0) \
        .with_speed(1.0);
    sword: OneHandSword = builder.build();
    if (sword == None):
        raise Exception("Fail to build the sword.");

def test_1hs_inflict_damage():
    builder: WeaponBuilder = OneHandSwordBuilder();
    builder = builder.with_name("Deuillegivre").with_damage_min(10) \
        .with_damage_max(20) \
        .with_required_level(10) \
        .with_critical_rate(1.0) \
        .with_speed(1.0);
    sword: OneHandSword = builder.build();
    damage: int = sword.inflict_damage();
    print("Inflicted damages: {}".format(damage));

if (__name__ == "__main__"):
    builder: WeaponBuilder =  WeaponBuilder.create_builder(WeaponType.BOW);
    weapon: Weapon = builder.build();
    print(type(weapon))

    arc: Weapon = WeaponBuilder.create_builder(WeaponType.BOW).build();
    # test_weapon_creation();
    # test_weapon_damage();
    # test_one_hand_builder();
    test_1hs_inflict_damage();
    print("All tests are successfuly terminated.");