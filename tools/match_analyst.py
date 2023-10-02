from chess import pgn
import io
import chess
import matplotlib.pyplot as plt
import numpy as np

#al momento il codice è ottimizzato solo per le aperture.
#TODO: analisi chiusure, analisi mosse, analisi approcci

#funzione presa da pgn_manager. Da sistemare la gestione dei moduli per importare la funzione
def _readPGN(pgn_path):
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

#DA CONTROLLARE
def calcola_percentuale_vittoria(apertura, partite, aperture_tot):
    vittorie = 0
    sconfitte = 0
    for partita in partite:
        if apertura == partita.headers.get("ECO"):
            if partita.headers.get("Result") == "1-0":
                vittorie += 1
            elif partita.headers.get("Result") == "0-1":
                sconfitte += 1
    if vittorie != 0:
        return (vittorie * 100) / aperture_tot
    else:
        return 0


def main(filename):
    partite = _readPGN(filename)
    ecos = {}
    vittorie_per_apertura = {}  # Dizionario per mantenere il conteggio delle vittorie per apertura
    nome_aperture = {}

    for partita in partite:
        opening = partita.headers.get("Opening")
        eco = partita.headers.get("ECO")
        risultato = partita.headers.get("Result")

        if eco not in ecos:
            ecos[eco] = 0

        ecos[eco] += 1

        if risultato == "1-0":
            if eco not in vittorie_per_apertura:
                vittorie_per_apertura[eco] = 0
            vittorie_per_apertura[eco] += 1

        if eco not in nome_aperture:
            nome_aperture[eco] = opening

    aperture_sorted = sorted(ecos.items(), key=lambda x: x[1], reverse=True)
    x_data_usage = []
    y_data_usage = []

    print("NUMERO DI PARTITE:", len(partite))
    print("NUMERO TOTALE DI APERTURE:", len(ecos))
    print("Aperture:")
    for eco, frequenza in aperture_sorted:
        percentuale_utilizzo = (frequenza / len(partite)) * 100
        percentuale_vittoria = (vittorie_per_apertura.get(eco, 0) / frequenza) * 100
        nome = nome_aperture.get(eco, "Sconosciuta")
        x_data_usage.append(str(eco) + '\n' + str(nome))
        y_data_usage.append(percentuale_utilizzo)
        print(f"({eco}) {nome}: {percentuale_utilizzo:.2f}% (Percentuale Vittoria: {percentuale_vittoria:.2f}%)" + " Numero di utlizzi: " + str(frequenza))

    plt.bar(x_data_usage, y_data_usage, width=0.8, color='green')
    plt.xticks(x_data_usage, size=6)
    #plt.yticks(np.arange(0, 100, 10), size=4)
    plt.xlabel('Openings')
    plt.ylabel('Percentage of use')
    plt.title('')

    plt.show()


if __name__ == "__main__":
    main(r"/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/all_pgn_koivisto_white.pgn")


