import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
import csv
import numpy as np
import seaborn as sns
import io
import chess
import chess.pgn
from pgn_manager import _readPGN

def main(filename):
    csv_columns = ["eco_code", "percentage_of_use %", "percentage_of_win %", "number_of_use", "number_of_wins"]
    csv_data = []
    games = _readPGN(filename)
    wins = 0
    loses = 0
    draws = 0
    ecos = {}
    wins_for_opening = {}
    opening_name = {}
    time_control = games[0].headers.get("TimeControl")
    t_boolean = True

    for game in games:
        opening = game.headers.get("Opening")
        eco = game.headers.get("ECO")
        result = game.headers.get("Result")

        if not game.headers.get("TimeControl") == time_control:
            t_boolean = False

        if eco not in ecos:
            ecos[eco] = 0

        ecos[eco] += 1

        if result == "1-0":
            if eco not in wins_for_opening:
                wins_for_opening[eco] = 0
            wins_for_opening[eco] += 1
            wins += 1
        elif result == "0-1":
            loses += 1
        elif result == "1/2-1/2":
            draws += 1

        if eco not in opening_name:
            opening_name[eco] = opening

    opening_sorted = sorted(ecos.items(), key=lambda x: x[1], reverse=True)
    x_data_usage = []
    y_data_usage = []
    y_data_winning = []
    wins_percentage = (wins/len(games)*100)
    loses_percentage = (loses/len(games)*100)
    draws_percentage = (draws/len(games)*100)
    wins_percentage_formatted = "{:.2f}".format(wins_percentage)
    loses_percentage_formatted = "{:.2f}".format(loses_percentage)
    draws_percentage_formatted = "{:.2f}".format(draws_percentage)
    print(filename)
    if t_boolean:
        print(game.headers.get("TimeControl"))
    else:
        print("This PGN has games with different TimeControl")
    print("NUMBER OF GAMES:", len(games))
    print("NUMBER OF WHITE WINS:", str(wins), '-', str(wins_percentage_formatted) + '%')
    print("NUMBER OF WHITE LOSES:", str(loses), '-', str(loses_percentage_formatted)+ '%')
    print("NUMBER OF DRAWS:", str(draws), '-', str(draws_percentage_formatted) + '%')
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
        csv_data.append([
            eco,
            f"{round(percentage_of_use, 2)}%",
            f"{round(percentage_of_wins, 2)}%",
            round(frequence, 2),
            round(wins_for_opening.get(eco), 2) if wins_for_opening.get(eco) is not None else None
        ])

    output_csv = 'csv_exported.csv'
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        writer.writerows(csv_data) 

    output_txt = 'txt_exported.txt'
    with open(output_txt, 'w') as file:
        file.write(game.headers.get("TimeControl") + ' seconds' + '\n')
        file.write('NUMBER OF GAMES:' + ' ' + str(len(games)) + '\n')
        file.write("NUMBER OF WHITE WINS:" + ' ' + str(wins) + '-' + str(wins_percentage_formatted) + '%' + '\n')
        file.write("NUMBER OF WHITE LOSES:" + ' ' +  str(loses) + '-' + str(loses_percentage_formatted) + '%' + '\n')
        file.write("NUMBER OF DRAWS:" + str(draws) +  '-' + str(draws_percentage_formatted) + '%' + '\n')
        file.write("NUMBER OF CHESS OPENING:" + str(len(ecos)))

    '''----------GRAPH USE----------'''
    df_usage = pd.DataFrame({'Openings': x_data_usage, 'Percentage of use': y_data_usage})
    df_truncated = df_usage.head(20)
    fig, ax = plt.subplots()
    plt.bar(df_truncated['Openings'], df_truncated['Percentage of use'], width=0.8, color='green')
    ax.yaxis.grid(True, linestyle='-', alpha=0.5)
    plt.xticks(df_truncated['Openings'], size=8)
    plt.xlabel('Codice ECO')
    plt.ylabel('Percentuale di uso')
    plt.title('Grafico percentuale di utilizzo')
    plt.savefig('use_graph.png')
    plt.show()

    '''----------GRAPH WIN----------'''
    # Creazione del DataFrame
    df_win = pd.DataFrame({'Openings': x_data_usage, 'Percentage of win': y_data_winning})
    df_win_truncated = df_win.head(10)
    # Creazione del grafico a barre con griglia
    fig, ax = plt.subplots()
    bars = ax.bar(df_win_truncated['Openings'], df_win_truncated['Percentage of win'], width=0.8, color='green')
    # Aggiunta della griglia
    ax.yaxis.grid(True, linestyle='-', alpha=0.5)
    # Impostazioni delle etichette e del titolo
    plt.xticks(df_win_truncated['Openings'], size=8, rotation=90)
    plt.xlabel('Codice ECO')
    plt.ylabel('Percentuale vittoria')
    plt.title('Grafico vittorie - apertura')
    # Salvataggio e visualizzazione del grafico
    plt.savefig('win_graph.png')
    plt.show()

    '''----------TORTA----------'''
    data = [wins, loses, draws]
    labels = ['Wins', 'Loses', 'Draws']

    # Filtra i dati e le etichette in base a valori diversi da zero
    non_zero_data = [value for value in data if value != 0]
    non_zero_labels = [label for label, value in zip(labels, data) if value != 0]

    # Crea il grafico solo se ci sono valori diversi da zero
    if non_zero_data:
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(non_zero_data)))

        # Plot
        fig, ax = plt.subplots(figsize=(5, 5))

        wedges, texts, autotexts = ax.pie(non_zero_data, labels=non_zero_labels, autopct='%1.1f%%',
                                        colors=colors, radius=1.2, center=(0, 0),
                                        wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False)

        # Personalizza i testi all'interno delle fette
        for text, autotext in zip(texts, autotexts):
            text.set(size=12, weight='bold')
            autotext.set(size=10, weight='bold')

        # Aggiungi la legenda
        ax.legend(non_zero_labels, title='Results', loc='lower right')

        ax.set_aspect('equal')
        ax.set_title('300 partite - Koivisto vs Berserk')

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        plt.tight_layout()

        plt.savefig('results_graph.png')
        plt.show()

    df_scatter = pd.DataFrame({
    'Opening': x_data_usage,
    'Percentage of use': y_data_usage,
    'Percentage of win': y_data_winning
})
   
main(r'/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_lc0/0,1sec/Koivisto_lc0_0,1sec_fix_exported.pgn')
