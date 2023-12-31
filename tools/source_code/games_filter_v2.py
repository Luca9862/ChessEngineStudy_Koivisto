import chess
import io
import chess.pgn


def filter_player_win_white(pgn_path):
    """
    Filters a PGN file to only include games where the specified player wins as White.

    Args:
        pgn: The filename of the PGN file to filter.
        player: The name of the player to filter for.

    Returns:
        A list of games where the specified player wins as White.
    """
    with open(pgn_path) as pgn_file:
        pgn_content = pgn_file.read()

    pgn = io.StringIO(pgn_content)
    games_filtered = []

    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break  # Esci dal loop se non ci sono più giochi nel file PGN
    
        result = game.headers["Result"]
    
        if result == "1-0":
            games_filtered.append(game)

    return games_filtered

path = r'C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\game_script_eros\koiv_berserk\1sec\Koivisto_Berserk_1_fix.pgn'
partite_vinte = filter_player_win_white(path)
print(partite_vinte)
print(len(partite_vinte))


