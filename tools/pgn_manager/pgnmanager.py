def _createCSV(path, *columns):
    """
    The function creates a CSV file in the desired path and with the desired column names.

    Args:
        a: PGN path
        b: Names of column

    Returns:
        csv file

    """
    csv_exists = os.path.exists(path)
    if not csv_exists:
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)

def _readPGN(pgn_path):
    """
    The function creates a list that contains all the games in the PGN file.

    Args:
        a: PGN path

    Returns:
        A list that contains chess.pgn.game objects.

    """
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
    """
    A function that creates a unique ID for a chess game.

    Args:
        a: chess.pgn.game

    Returns:
        ID created with the SHA-256 function

    """
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

    #Create ID using SHA-256 hash function
    hashed_id = hashlib.sha256(data.encode()).hexdigest()

    return hashed_id


'''
def _isRecorded(game, csv_file):
    """
    SUSPENDED FUNCTION ------------> DON'T USE!
    A function that tells if a specific game exists in a CSV file.
    Used into writeMatchesIntoCsv (rwo 150)
    The function has been put on hold because it increases the complexity of the algorithm too much and it caused file reading errors.
    Args:
        a: chess.pgn.game
        b: csv file

    Returns:
        boolean

    """
    id = str(_createID(game))
    with open(csv_file,'r') as csv_object:
        reader = csv.reader(csv_object)
        if not reader:
            return False
        next(reader)
        for row in reader:
            if(row[0] == id):
                return True
        return False
'''

def writeMatchesIntoCsv(pgn_file, csv_file):
    """
    A function that writes the games from a PGN file to a CSV file.

    Args:
        a: PGN file
        b: CSV file

    Returns:
        csv file

    """
    _createCSV(csv_file, 'ID', 'Event', 'White', 'Black', 'WhiteFIDEId', 'BlackFIDEId', 'Result', 'WhiteElo', 'BlackElo', 'Round', 'TimeControl', 'Date', 'WhiteClock', 'BlackClock', 'PlyCount' ,'Time' , 'Termination' ,'Moves')
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
        plycount = game.headers.get('PlyCount')
        time = game.headers.get('Time')
        termination = game.headers.get('Termination')

        moves = [str(move) for move in game.mainline_moves()]

        #if not (_isRecorded(game, csv_file)):
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id, event, white, black, whitefideid, blackfideid,
                                result, whiteElo, blackElo, round, time_control, date, white_clock, black_clock, plycount, time, termination, moves])
                
def merge_pgn(pgn_file, pgn_destination):
    """
    The function that merges two PGN files in the second PGN/argument

    Args:
        a: PGN file
        b: PGN file

    Returns:
        pgn_destination

    """
    games_to_save = _readPGN(pgn_file)
    with open(pgn_destination, "a") as f:
        for game in games_to_save:
            f.write(str(game))
            f.write('\n\n')

def split_pgn(pgn_file, path_destination):
    """
    The function splits the games in the PGN file and creates a PGN for each game in the desired path

    Args:
        a: PGN file
        b: path

    Returns:
        pgn

    """
    games = _readPGN(pgn_file)
    for game in games:
        id = _createID(game)
        with open(os.path.join(path_destination, game.headers.get('White') + 'vs' + game.headers.get('Black') + id + ".pgn"), "w") as f:
            f.write(str(game))

def delete_duplicate(pgn_file, destination_path):

    #TEST PHASE! DON'T USE THIS FUNCTION!

    """
    The function removes duplicate games from a PGN file and creates new PGN where it save the games without duplicates

    Args:
        a: PGN file
        b: path

    Returns:
        pgn

    """
    matches = _readPGN(pgn_file)
    matches_nodp = []
    print(matches)
    d = []
    for match in matches:
        id = _createID(match)
        for i in d:
            if id != i:
                d.append(id)
                matches_nodp.append(match)
                print(id)
            else:
                continue
    file_path = os.path.join(destination_path, "no_duplicated.pgn")
    with open(os.path.join(file_path), 'w') as f:
        for partita in matches_nodp:
            f.write(str(partita))
            f.write('\n\n')