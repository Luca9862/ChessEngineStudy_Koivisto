import matplotlib.pyplot as plt
import pandas as pd
from pgn_manager import _readPGN
import tkinter as tk

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
    y_data_winning = []
    print("NUMBER OF GAMES:", len(games))
    print("NUMBER OF CHESS OPENING:", len(ecos))
    print("Opening:")
    for eco, frequence in opening_sorted:
        percentage_of_use = (frequence / len(games)) * 100
        percentage_of_wins = (wins_for_opening.get(eco, 0) / frequence) * 100
        name = opening_name.get(eco, "UNKNOWN")
        x_data_usage.append(str(eco))
        y_data_usage.append(percentage_of_use)
        y_data_winning.append(percentage_of_wins)
        print(f"({eco}) {name}: (Percentage of use: {percentage_of_use:.2f}%) (Percentage of win: {percentage_of_wins:.2f}%)" + " Number of use: " + str(frequence))

    '''----------GRAPH USE----------'''
    df = pd.DataFrame({'Openings': x_data_usage, 'Percentage of use': y_data_usage})
    df_truncated = df.head(20)
    plt.bar(df_truncated['Openings'], df_truncated['Percentage of use'], width=0.8, color='green')
    plt.xticks(df_truncated['Openings'], size=8)
    plt.xlabel('Openings')
    plt.ylabel('Percentage of use')
    plt.title('Opening analyst')

    plt.show()

    '''----------GRAPH WIN----------'''
    df_win = pd.DataFrame({'Openings': x_data_usage, 'Percentage of win': y_data_winning})
    df_win_truncated = df_win.head(20)
    plt.bar(df_win_truncated['Openings'], df_win_truncated['Percentage of win'], width=0.8, color='green')
    plt.xticks(df_win_truncated['Openings'], size = 8)
    plt.xlabel('Openings')
    plt.ylabel('Percentage of win')
    plt.title('Opening analyst - win')

    plt.show()

main('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/Koivisto_9_0_64-bit.bare.[3174].pgn (1)/Koivisto_9_0_64-bit.bare.[3174].pgn')
## change main parameter to use the script