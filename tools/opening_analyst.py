from chess import pgn
import io
import chess
import matplotlib.pyplot as plt
import numpy as np
from pgn_manager import _readPGN

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
    wins_for_opening = {}  # Dizionario per mantenere il conteggio delle vittorie per apertura
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
    plt.bar(x_data_usage, y_data_usage, width=0.8, color='green')
    plt.xticks(x_data_usage, size=6)
    #plt.yticks(np.arange(0, 100, 10), size=4)
    plt.xlabel('Openings')
    plt.ylabel('Percentage of use')
    plt.title('')

    plt.show()


if __name__ == "__main__":
    main(r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\all_pgn_koivisto_white.pgn")


