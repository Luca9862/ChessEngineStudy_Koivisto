from pgn_manager import _readPGN
import matplotlib.pyplot as plt

# Lista per memorizzare gli scores
def main(pgn):
    scores = []
    games = _readPGN(pgn)

    for game in games:
        while game:
            comment = game.move
            print(comment)



main(r'/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/0,1sec/Koivisto_Berserk_0.1_fix.pgn')