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

game_results = []
game_plycount = []
game_moveTime = []
averages = []

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
get_dataset("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn",
             "primi_dieci_valori.csv")

def calculate_average_score_for_game(csv_path):
    with open(csv_path, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            row_values = [float(value) for value in row]
            row_mean = sum(row_values) / len(row_values)
            averages.append(row_mean)

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

calculate_average_score_for_game('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/primi_dieci_valori.csv')
get_results("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn")
#get_fwten_moves('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn')
get_playcount("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn")
_moveTime("/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/all.pgn")

data = {
    'Results': game_results,
    'PlyCount': game_plycount,
    'MoveTime': game_moveTime,
    'Score': averages
    }

df = pd.DataFrame(data)

X = df[['PlyCount', 'MoveTime', 'Score']]
y = df['Results']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Inizializza il modello di regressione logistica
model = LogisticRegression()

# Addestra il modello
model.fit(X_train, y_train)

# Fai previsioni
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Stampa delle metriche di valutazione
print(f'Accuracy: {accuracy}')
print(f'Classification Report:\n{classification_rep}')
print(f'Confusion Matrix:\n{conf_matrix}')