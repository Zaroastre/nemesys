CREATE TABLE IF NOT EXISTS Player (
    identifier INTEGER PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    maximal_life_points INTEGER,
    current_life_points INTEGER,
    maximal_experience_points INTEGER,
    current_experience_points INTEGER,
    level INTEGER,
    weapon INTEGER NOT NULL,
    cretical_rate REAL,
    speed REAL,
    FOREIGN KEY(weapon) REFERENCES Weapon(identifier)
);

CREATE TABLE IF NOT EXISTS Inventory (
    player INTEGER NOT NULL,
    item INTEGER NOT NULL,
    FOREIGN KEY(player) REFERENCES Player(identifier)
);