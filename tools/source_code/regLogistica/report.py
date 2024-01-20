'''
calcolo di varianza e mediana
'''
#rom pgn_manager.pgn_manager import _readPGN
import chess
from chess import pgn
import io
import matplotlib.pyplot as plt
import csv
import numpy as np
from pgn_manager import _readPGN
player_bianco = []
player_nero = []

avg_score_player_1 = []
avg_score_player_2 = []

varianza_player_1 = []
varianza_player_2 = []

mediana_player_1 = []
mediana_player_2 = []

media_player_1 = []
media_player_2 = []

tot=0
partite_selezionate = 0
partite_vinte = 0
partite_patte = 0
partite_perse = 0
info_partita = ""

'''pgn_path = "pgn_gameSim_v3\\berserk_koi_0.1.pgn"'''

title = "Riepilogo partite: Berserk vs RubiChess - 1"

pgn_path = "data_2\\Berserk_RubiChess_0.1.pgn"
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

'''pgn_path = "pgn\\berserk_rubi_05.pgn"
maxMosse = 135
'''
csv_path = "score/allScores_v2_prova_223.csv"
temp_pgn = "Grafici/temp.pgn"

with open(pgn_path) as pgn:
    # Leggi la partita dal file PGN
    game = chess.pgn.read_game(pgn)
    games = _readPGN(pgn_path)
    for game in games:
        tot += 1
        n = 1
        node = game
        result = game.headers.get('Result')
        if result == '1-0':
            partite_selezionate += 1
            partite_vinte += 1
            info_partita = "partite vinte"
        elif result == '0-1':
            partite_selezionate += 1
            partite_perse += 1
            info_partita = "partite perse"
            #print(game)             
        elif result == '1/2-1/2':
            info_partita = "partite patte"
            partite_patte += 1
            partite_selezionate += 1 
            
    
    #impostare il range nel numero di mosse massimo      

'''y_ticks = [0, 2.5, 5, 7.5, 10]
y_ticks_label = ["0","2.5", "5", "7.5", "10"]'''

print(partite_selezionate)

print(partite_vinte)
print(partite_patte)
print(partite_perse)

percentuale_vittorie = (partite_vinte/partite_selezionate) * 100
percentuale_patte = (partite_patte/partite_selezionate) * 100
percentuale_sconfitte = (partite_perse/partite_selezionate) * 100

labels = ['Vittorie', 'Patte', 'Sconfitte']
sizes = [percentuale_vittorie, percentuale_patte, percentuale_sconfitte]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'skyblue', 'coral'])
# Titolo del grafico
plt.title(title)
# Visualizza il grafico
plt.grid()
plt.show()