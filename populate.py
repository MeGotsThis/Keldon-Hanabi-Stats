from collections import OrderedDict
import configparser
import socketIO_client
import hashlib
import six
import datetime
import sqlite3
import sys

import database

if sys.version_info >= (3, 0):
    six.b = lambda s: s.encode()


waitTime = 0.1

history = OrderedDict()
currentHistory = 0

def on_message(*args):
    if not args or isinstance(args[0], bytes):
        return
    #print(args)
    mtype = args[0]['type']
    if mtype == 'game_history':
        history[args[0]['resp']['id']] = args[0]['resp']
    if mtype == 'history_detail':
        if args[0]['resp']['you']:
            history[args[0]['resp']['id']]['ts'] = args[0]['resp']['ts']
    if currentHistory:
        if mtype == 'init':
            history[currentHistory]['players'] = args[0]['resp']['names']
        if mtype == 'notify':
            ntype = args[0]['resp']['type']
            if ntype == 'turn' and args[0]['resp']['num'] == 0:
                history[currentHistory]['starting'] = args[0]['resp']['who']


user = configparser.ConfigParser()
user.read('user.ini')

connection = sqlite3.connect(
    user['USER']['database'],
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
database.create_tables(connection)

conn = socketIO_client.SocketIO('keldon.net', 32221)
conn.on('message', on_message)
    
username = user['USER']['username']
password = user['USER']['password']
passSha = hashlib.sha256(b'Hanabi password ' + password.encode()).hexdigest()

conn.emit('message', {'type': 'login',
                      'resp': {'username': username, 'password': passSha}})
conn.wait(seconds=1)

for i in history.keys():
    h = history[i]
    if database.game_record_exists(connection, h['id']):
        continue
    currentHistory = h['id']
    conn.emit('message', {'type': 'history_details', 'resp': {'id': h['id']}})
    conn.emit('message', {'type': 'start_replay', 'resp': {'id': h['id']}})
    conn.wait(seconds=waitTime)
    conn.emit('message', {'type': 'hello', 'resp': {}})
    conn.emit('message', {'type': 'ready', 'resp': {}})
    conn.emit('message', {'type': 'abort', 'resp': {}})
    conn.wait(seconds=waitTime)
    print(h)
    timestamp = datetime.datetime.strptime(h['ts'], "%Y-%m-%dT%H:%M:%S.%fZ")
    database.insert_game_record(connection, h['id'], h['variant'],
                                h['num_players'], h['score'], h['starting'],
                                timestamp, h['players'])
