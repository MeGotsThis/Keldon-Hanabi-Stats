import sqlite3


def create_tables(connection):
    queries = ['''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    variant INTEGER NOT NULL,
    num_players INTEGER NOT NULL,
    score INTEGER NOT NULL,
    starting INTEGER NOT NULL,
    ts TIMESTAMP NOT NULL
)''','''
CREATE TABLE IF NOT EXISTS game_players (
    id INTEGER,
    position INTEGER NOT NULL,
    player NOT NULL COLLATE NOCASE,
    PRIMARY KEY (id, position),
    FOREIGN KEY(id) REFERENCES games(id)
)''','''
CREATE INDEX IF NOT EXISTS player_names ON game_players(player)''','''
CREATE VIEW IF NOT EXISTS game_info(
    id,
    variant,
    num_players,
    score,
    win,
    zero,
    ts
) AS
SELECT
    id, CASE variant WHEN 0 THEN 'None' WHEN 1 THEN 'Black Suit' WHEN 2 THEN '1 of each Black' WHEN 3 THEN 'Rainbow' ELSE 'Unknown' END, num_players, score, score = (CASE variant WHEN 0 THEN 25 ELSE 30 END), score = 0, ts
    FROM games''','''
CREATE VIEW IF NOT EXISTS players(
    player
) AS
SELECT
    DISTINCT player
    FROM game_players''']
    for q in queries:
        connection.execute(q)
    connection.commit()


def game_record_exists(connection, id):
    cursor = connection.cursor()
    cursor.execute('''SELECT EXISTS(SELECT 1 FROM games WHERE id=?)''', (id,))
    row = cursor.fetchone()
    cursor.close()
    return bool(row[0])


def insert_game_record(connection, id, variant, numPlayers, score, starting, timestamp, players):
    connection.execute('''
INSERT INTO games (id, variant, num_players, score, starting, ts) VALUES (?, ?, ?, ?, ?, ?)''',
                       (id, variant, numPlayers, score, starting, timestamp))
    connection.executemany('''
INSERT INTO game_players (id, position, player) VALUES (?, ?, ?)''',
                           [(id, i, player) for i, player in enumerate(players)])
    connection.commit()
