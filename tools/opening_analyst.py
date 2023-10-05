from chess import pgn
import io
import chess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pgn_manager import _readPGN

'----------BETA----------'

def calculate_win_percentage(opening, matches, tot_opening):
    wins = 0
    losses = 0
    for match in matches:
        if opening == match.headers.get("ECO"):
            if match.headers.get("Result") == "1-0":
                wins += 1
            elif match.headers.get("Result") == "0-1":
                losses += 1
    if wins != 0:
        return (wins * 100) / tot_opening
    else:
        return 0


def main(filename):
    games = _readPGN(filename)
    ecos = {}
    wins_for_opening = {}
    opening_name = {}

    for game in games:
        opening = game.headers.get("Opening")
        eco = game.headers.get("ECO")
        result = game.headers.get("Result")

        if eco not in ecos:
            ecos[eco] = 0

        ecos[eco] += 1

        if result == "1-0":
            if eco not in wins_for_opening:
                wins_for_opening[eco] = 0
            wins_for_opening[eco] += 1

        if eco not in opening_name:
            opening_name[eco] = opening


    opening_sorted = sorted(ecos.items(), key=lambda x: x[1], reverse=True)
    x_data_usage = []
    y_data_usage = []
    print("NUMBER OF GAMES:", len(games))
    print("NUMBER OF CHESS OPENING:", len(ecos))
    print("Opening:")
    for eco, frequence in opening_sorted:
        percentage_of_use = (frequence / len(games)) * 100
        percentage_of_wins = (wins_for_opening.get(eco, 0) / frequence) * 100
        name = opening_name.get(eco, "UNKNOWN")
        x_data_usage.append(str(eco) + '\n' + str(name))
        y_data_usage.append(percentage_of_use)
        print(f"({eco}) {name}: {percentage_of_use:.2f}% (Percentage of win: {percentage_of_wins:.2f}%)" + " Number of use: " + str(frequence))

    '''----------GRAPH----------'''
    df = pd.DataFrame({'Openings': x_data_usage, 'Percentage of use': y_data_usage})
    df_truncated = df.head(20)
    plt.bar(df_truncated['Openings'], df_truncated['Percentage of use'], width=0.8, color='green')
    plt.xticks(df_truncated['Openings'], size=8)
    plt.xlabel('Openings')
    plt.ylabel('Percentage of use')
    plt.title('')

    plt.show()

if __name__ == "__main__":
    main(r"C:\Users\canal\Desktop\koiv_berserk_500_marsioscript.pgn")


