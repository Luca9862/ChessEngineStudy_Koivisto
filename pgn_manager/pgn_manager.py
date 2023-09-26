import chess
import io
import chess.pgn
import csv
from os.path import exists
import os
import hashlib

#funzione che prende come argomento un csv ed il relativo percorso per crearlo
def _createCSV(path, *columns):
    csv_exists = os.path.exists(path)
    if not csv_exists:
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)

#funzione che legge un pgn e restituisce un oggetto chess.pgn.Game che rappresenta la partita
def _readPGN(pgn_path):
    pgn_file = open(pgn_path)
    pgn_content = pgn_file.read()
    pgn_file.close()

    pgn_games = []
    pgn = io.StringIO(pgn_content)
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        pgn_games.append(game)

    return pgn_games

def _createID(game):
    event = game.headers.get('Event') or ''
    white = game.headers.get('White') or ''
    black = game.headers.get('Black') or ''
    whitefideid = game.headers.get('WhiteFideId') or ''
    blackfideid = game.headers.get('BlackFideId') or ''
    result = game.headers.get('Result') or ''
    whiteElo = game.headers.get('WhiteElo') or ''
    blackElo = game.headers.get('BlackElo') or ''
    round = game.headers.get('Round') or ''
    time_control = game.headers.get('TimeControl') or ''
    date = game.headers.get('Date') or ''
    white_clock = game.headers.get('WhiteClock') or ''
    black_clock = game.headers.get('BlackClock') or ''
    moves = [str(move) for move in game.mainline_moves()]

    data = (event +  white + black + whitefideid + blackfideid + result + whiteElo + blackElo + round  + time_control + date + white_clock + black_clock +''.join(moves))

    # Crea l'ID utilizzando la funzione hash SHA-256
    hashed_id = hashlib.sha256(data.encode()).hexdigest()

    return hashed_id

def _isRecorded(game, csv_file):
    id = str(_createID(game))
    with open(csv_file,'r') as csv_object:
        reader = csv.reader(csv_object)
        next(reader)
        for row in reader:
            if(row[0] == id):
                return True
        return False

#funzione che prende come argomento un pgn e un csv per aggiungere i dati della partita in quest'ultimo
def writeMatch(pgn_file, csv_file):
    _createCSV(csv_file, 'ID', 'Event', 'White', 'Black', 'WhiteFIDEId', 'BlackFIDEId', 'Result', 'WhiteElo', 'BlackElo', 'Round', 'TimeControl', 'Date', 'WhiteClock', 'BlackClock', 'Moves')

    games = _readPGN(pgn_file)

    for game in games:
        id = _createID(game)
        event = game.headers.get('Event')
        white = game.headers.get('White')
        black = game.headers.get('Black')
        whitefideid = game.headers.get('WhiteFideId')
        blackfideid = game.headers.get('BlackFideId')
        result = game.headers.get('Result')
        whiteElo = game.headers.get('WhiteElo')
        blackElo = game.headers.get('BlackElo')
        round = game.headers.get('Round')
        time_control = game.headers.get('TimeControl')
        date = game.headers.get('Date')
        white_clock = game.headers.get('WhiteClock')
        black_clock = game.headers.get('BlackClock')
        moves = [str(move) for move in game.mainline_moves()]

        if not (_isRecorded(game, csv_file)):
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([id, event, white, black, whitefideid, blackfideid,
                                result, whiteElo, blackElo, round, time_control, date, white_clock, black_clock, moves])

csv_ex = '/Users/lucacanali/Desktop/csv_creator/all_games.csv'

path = '/Users/lucacanali/Desktop/csv_creator/pgn_games'

file_list = os.listdir(path)
for file in file_list:
    pgn_file = path + '/' + file
    writeMatch(pgn_file, csv_ex)
