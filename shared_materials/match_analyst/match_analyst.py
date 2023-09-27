from chess import pgn
import io
import chess

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

def main(filename):
    partite = _readPGN(filename)
    aperture = {}
    chiusure = {}
    altre_chiusure = 0
    mosse = {}

    for partita in partite:
        apertura = partita.headers.get("ECO")
        chiusura = partita.headers.get("Result")
        mosse = partita.mainline()

        if apertura not in aperture:
            aperture[apertura] = 0
        aperture[apertura] += 1

        if chiusura not in chiusure:
            chiusure[chiusura] = 0
        else:
            chiusure[chiusura] += 1

        if chiusura not in ["1-0", "0-1", "1/2-1/2"]:
            altre_chiusure += 1

    print("Aperture:")
    aperture_sorted = sorted(aperture.items(), key=lambda x: x[1], reverse=True)
    for apertura, frequenza in aperture_sorted:
        frequenza = frequenza / len(partite)
        tot = aperture.get(apertura, 0)
        print(f"{apertura}: {frequenza * 100:.2f}%" + " " + str(tot))

    print("Chiusure:")
    frequenza = frequenza / len(partite)
    for chiusura, frequenza in chiusure.items():
        print(f"{chiusura}: {frequenza * 100:.2f}%")

    print("Altre chiusure:", altre_chiusure)

#per testare lo script modificare l'argomento della funzione con il percorso del PGN desiderato
if __name__ == "__main__":
    main("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/all_pgn_koivisto_white.pgn")
