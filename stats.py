import configparser
import datetime
import sqlite3


variants = ['None', 'Black Suit', '1 of each Black', 'Rainbow']
maxScore = [25, 30, 30, 30]

player = configparser.ConfigParser()
player.read('user.ini')

connection = sqlite3.connect(
    player['USER']['database'],
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = connection.cursor()

query = '''
SELECT variant, num_players, COUNT(*),
        SUM(score = (CASE variant WHEN 0 THEN 25 ELSE 30 END)), SUM(score=0)
    FROM games
    GROUP BY variant, num_players'''

print('ALL GAMES')
for row in cursor.execute(query):
    print('{variant} - {players} players: {total} games, {wins} wins, '
          '{losses} 0-points'.format(
        variant=variants[row[0]],
        players=row[1],
        total=row[2],
        wins=row[3],
        losses=row[4],
        ))
print()

for player, in cursor.execute('SELECT player FROM players').fetchall():
    print(player)
    query = '''
SELECT variant, num_players, COUNT(*),
        SUM(score = (CASE variant WHEN 0 THEN 25 ELSE 30 END)), SUM(score=0)
    FROM games
    WHERE id IN (SELECT id FROM game_players WHERE player=?)
    GROUP BY variant, num_players'''
    for row in cursor.execute(query, [player]):
        print('{variant} - {players} players: {total} games, {wins} wins, '
              '{losses} 0-points'.format(
            variant=variants[row[0]],
            players=row[1],
            total=row[2],
            wins=row[3],
            losses=row[4],
            ))
    print()


print('Score Distribution')
print()
query = '''
SELECT DISTINCT variant, num_players
    FROM games
    ORDER BY variant, num_players'''
for variant, numPlayers in cursor.execute(query).fetchall():
    print('{variant} - {players} players'.format(
        variant=variants[variant],
        players=numPlayers,
        ))
    query = '''
SELECT score, COUNT(*)
    FROM games
    WHERE variant=? AND num_players=?
    GROUP BY score
    ORDER BY score'''
    for score, count in cursor.execute(query, [variant, numPlayers]):
        print('Score: {score} - {count} games'.format(score=score, count=count))
    print()
