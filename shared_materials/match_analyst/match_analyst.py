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

#DA SISTEMARE
def calcola_percentuale_vittoria(apertura, partite):
    vittorie = 0
    sconfitte = 0
    for partita in partite:
        if apertura == partita.headers.get("ECO"):
            if partita.headers.get("Result") == "1-0":
                vittorie += 1
            elif partita.headers.get("Result") == "0-1":
                sconfitte += 1
    if vittorie != 0:
        return (vittorie * 100) / len(partite)
    else:
        return 0


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

    print("NUMERO DI PARTITE: " + str(len(partite)))
    print("Aperture:")
    aperture_sorted = sorted(aperture.items(), key=lambda x: x[1], reverse=True)
    tot_perce_provv = 0
    for apertura in aperture_sorted:
        percentuale_vittoria = calcola_percentuale_vittoria(apertura, partite)
        #frequenza = frequenza / len(partite)
        tot = aperture[apertura]
        percentuale = tot*100/len(partite)
        tot_perce_provv += percentuale_vittoria
        print(percentuale + "%" + " " + "Totale utilizzi:  " + str(tot) + " " + "Percentuale vittoria: ") # + f"{percentuale_vittoria:.5f}%"

    print("Chiusure:")
    frequenza = frequenza / len(partite)
    for chiusura, frequenza in chiusure.items():
        print(f"{chiusura}: {frequenza * 100:.2f}%")

    print("Altre chiusure:", altre_chiusure)
    print(tot_perce_provv)

#per testare lo script modificare l'argomento della funzione con il percorso del PGN desiderato
if __name__ == "__main__":
    main(r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\shared_materials\match_analyst\Kasparov.pgn")
