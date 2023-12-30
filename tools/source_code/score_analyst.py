from pgn_manager import _readPGN
import matplotlib.pyplot as plt
import chess
import chess.pgn


def main(pgn):
    scores = []
    with open(pgn) as f:
        game = chess.pgn.read_game(f)

        node = game
        while not node.is_end():
            move = node.board().san(node.move)
            print(move, end=" ")
            node = node.variations[0]  # Vai alla prossima mossa



main(r'/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/0,1sec/Koivisto_Berserk_0.1_fix.pgn')