import chess.pgn
from pgn_manager import _readPGN

#pgn_path = "data_2\\Berserk_Koivisto_1.pgn"
#pgn_path = "data_2\\Berserk_LC0_0.5.pgn"
#"data_space_2\\Berserk_RubiChess_0.5.pgn"
#pgn_path = "pgn\\berserk_rubi_05.pgn"
pgn_path = "/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/0,1sec/Koivisto_Berserk_0.1_fix.pgn"
'''pgn_path = "pgn\\berserk_koi_01.pgn"
pgn_path = "data_2\\Berserk_Koivisto_0.1.pgn"
pgn_path = "data_2\\Berserk_Koivisto_0.5.pgn"
pgn_path = "data_2\\Berserk_Koivisto_1.pgn"
pgn_path = "data_2\\all_vs_koivisto.pgn"
pgn_path = "data_2\\Berserk_lc0_0.1.pgn"
pgn_path = "data_2\\Berserk_LC0_0.5.pgn"
pgn_path = "data_2\\Berserk_LC0_1.pgn"
pgn_path = "data_2\\all_vs_LC0.pgn"
pgn_path = "data_2\\Berserk_RubiChess_0.1.pgn"
pgn_path = "data_2\\Berserk_RubiChess_0.5.pgn"
pgn_path = "data_2\\Berserk_RubiChess_1.pgn"
pgn_path = "data_2\\all_vs_RubiChess.pgn"'''

csv_path = "allScores_2112023.csv"

def getScore(fromPGNFile, destinationFile):
    partita_numero = 1
    # Apri il file PGN
    with open(fromPGNFile) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        #cartella e
        games = _readPGN(fromPGNFile)
        for game in games:
            player_bianco = ""
            player_nero = ""
            print("Partita numero: "+str(partita_numero))
            partita_numero += 1
            n=1
            # Ottieni il nodo radice della partita
            node = game
            # Itera attraverso tutte le mosse della partita
            while node is not None:
                comment = node.comment
                if comment:
                    if n % 2 == 0:
                        #print(str(n)+ " - "+comment + " - Nero")
                        player_nero += comment+","
                    else:
                        #print(str(n)+ " - "+comment + " - Bianco")  
                        player_bianco += comment+","
                    n += 1
                    #print(str(n)+ " - "+comment)
                    game = chess.pgn.read_game(pgn)
                # Passa al nodo successivo
                node = node.variations[0] if node.variations else None
            with open(destinationFile, "a") as file:
                file.write(player_bianco+"\n")
                file.write(player_nero+"\n")
            #print(player_bianco)
            #print(player_nero)

getScore(pgn_path, csv_path)