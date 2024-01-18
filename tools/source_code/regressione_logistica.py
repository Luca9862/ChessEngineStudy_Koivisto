import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, classification_report
import io
import chess
import csv
from chess import pgn
from sklearn.metrics import auc
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pgn_manager import _readPGN
from ChessScoreAnalyze import average_calculation

game_results = []
game_plycount = []
game_moveTime = []

def get_dataset(pgn_path, output_csv_path):
    with open(pgn_path) as pgn_file:
        pgn_content = pgn_file.read()

    pgn = io.StringIO(pgn_content)
    
    with open(output_csv_path, "w", newline='') as output_file:
        writer = csv.writer(output_file)

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

            # Estrapolare i primi dieci valori
            first_ten_scores = white_scores[:10]

            # Scrivere i primi dieci valori nel nuovo file CSV
            writer.writerow(first_ten_scores)

# Utilizzo della funzione
get_dataset("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/0,1sec/Koivisto_Berserk_0.1_fix.pgn",
             "primi_dieci_valori.csv")

def calculate_average_score(csv_path):
    sums = {}
    counts = {}

    file_path = csv_path

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

def get_results(pgn_path):
    with open(pgn_path) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        games = _readPGN(pgn_path)
        for game in games:
            result = game.headers.get('Result')      
            if result == '1-0':
                game_results.append(1)
            elif result == '0-1':
                game_results.append(0)
            elif result == '1/2-1/2': 
                game_results.append(0)

def get_playcount(pgn_path):
    with open(pgn_path) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        games = _readPGN(pgn_path)
        for game in games:  
            playCount = game.headers.get('PlayCount')
            play = float(playCount)
            game_plycount.append(play)

def _moveTime(pgn_path):
    with open(pgn_path) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        games = _readPGN(pgn_path)
        for game in games:  
            moveTime = game.headers.get('TimeControl')
            if moveTime:
                play = float(moveTime.split(":")[1])  # Divide la stringa e prendi la seconda parte
                game_moveTime.append(play)


averages_score = average_calculation('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/primi_dieci_valori.csv')
print(averages_score)            
get_results("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn")
#get_fwten_moves('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn')
get_playcount("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn")
_moveTime("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn")

data = {
    'Results': game_results,
    'PlyCount': game_plycount,
    'MoveTime': game_moveTime,
    'Score': averages_score
    }

df = pd.DataFrame(data)

X = df.iloc[:, 1:]  # Usa le colonne 1 e successive come feature
y = df['Results']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Inizializza il modello di regressione logistica
model = LogisticRegression()

# Addestra il modello
model.fit(X_train, y_train)

# Fai previsioni
y_pred = model.predict(X_test)

# Valuta le prestazioni del modello
print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))