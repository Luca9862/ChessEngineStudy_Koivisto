from pgn_manager import _readPGN
import matplotlib.pyplot as plt
import chess
import chess.pgn
import io
import csv
import pandas as pd
import numpy as np

def get_dataset(pgn_path):
    with open(pgn_path) as pgn_file:
        pgn_content = pgn_file.read()

    pgn = io.StringIO(pgn_content)
    
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        scores = []
        white_scores = []

        # Trattamento delle mosse e dei commenti per ogni partita
        for node in game.mainline():
            comments = node.comment
            scores.append(comments)

        for i, elemento in enumerate(scores):
            if i%2==0:
                white_scores.append(elemento)

        with open("allScores.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(white_scores)
        file.close

def average_calculation(csv_file):
    sums = {}
    counts = {}

    file_path = csv_file

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for i, value in enumerate(row):
                if i not in sums:
                    sums[i] = 0.0
                    counts[i] = 0
                try:
                    sums[i] += float(value)
                    counts[i] += 1
                except ValueError:
                    pass
    
    averages = [sums[i] / counts[i] if counts[i] > 0 else None for i in range(max(sums.keys()) + 1)]
    return averages

def get_graph(list):
    averages = list
    plt.figure(figsize=(8, 6))
    plt.plot(averages, label='Koivisto')

    # Etichette degli assi
    plt.xlabel('Mosse')
    plt.ylabel('Score medio')

    # Legenda
    plt.legend()

    # Titolo del grafico
    plt.title('Grafico score medio')

    # Visualizza il grafico
    plt.grid()
    plt.savefig('grafico_score')
    plt.show()

    print("Medie per colonna:")
    for i, average in enumerate(averages):
        print(f"Colonna {i + 1}: {average}")


get_dataset(r'C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\game_script_eros\koiv_berserk\all.pgn')
data = average_calculation('allScores.csv')
get_graph(data)