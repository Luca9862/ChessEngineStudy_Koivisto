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
        count = 1

        # Trattamento delle mosse e dei commenti per ogni partita
        for node in game.mainline():
            move = node.move
            comments = node.comment
            scores.append(comments)

        for i, elemento in enumerate(scores):
            if i%2==0:
                white_scores.append(elemento)

        with open("allScores.csv", "a") as file:
            partita = "Game: "+str(count)
            writer = csv.writer(file)
            writer.writerow(white_scores)
        file.close

        count += 1

def avarage_calculate(csv_file):
    # Inizializza un dizionario per memorizzare le somme parziali e il conteggio delle colonne
    sums = {}
    counts = {}

    # Percorso del tuo file CSV
    file_path = csv_file

    # Leggi il file CSV e calcola le somme parziali e i conteggi delle colonne
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for i, value in enumerate(row):
                if i not in sums:
                    sums[i] = 0.0
                    counts[i] = 0
                try:
                    # Aggiungi il valore alla somma parziale
                    sums[i] += float(value)
                    # Incrementa il conteggio
                    counts[i] += 1
                except ValueError:
                    # Gestisci eventuali errori nella conversione del valore a float
                    pass

        # Creazione del grafico
    
    # Calcola le medie
    averages = [sums[i] / counts[i] if counts[i] > 0 else 0.0 for i in range(max(sums.keys()) + 1)]

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


#get_dataset(r'/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_lc0/0,1sec/Koivisto_lc0_0.1_fix.pgn')
avarage_calculate('allScores.csv')