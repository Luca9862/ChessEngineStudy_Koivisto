'''
    This logistic regression takes the outcome of the game as the dependent variable and uses the following independent variables:
    
        -The average score of the first ten moves in each game.
        -The time allotted per move for the player (a parameter included in the PGN).
        -The total number of moves in all games (a parameter included in the PGN).
'''

import pandas as pd
import matplotlib.pyplot as plt
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

def main(pgn_path, csv_path):
    get_dataset(pgn_path, csv_path)
    calculate_average_score_for_game(csv_path)
    get_results(pgn_path)
    get_playcount(pgn_path)
    _moveTime(pgn_path)

main(r'C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\game_script_eros\all\all.pgn', 'primi_dieci_valori.csv')

data = {
    'Results': game_results,
    'PlyCount': game_plycount,
    'MoveTime': game_moveTime,
    'Averages': averages
    }

df = pd.DataFrame(data)

X = df[['PlyCount', 'MoveTime', 'Averages']]
y = df['Results']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Inizializza il modello di regressione logistica
model = LogisticRegression()

# Addestra il modello
model.fit(X_train, y_train)

# Fai previsioni
y_pred_test = model.predict(X_test)
y_prob_test = model.predict_proba(X_test)
# Effettua previsioni sui dati di train
y_pred_train = model.predict(X_train)
y_prob_train = model.predict_proba(X_train)
# Calcola l'accuratezza del modello
accuracy = accuracy_score(y_test, y_pred_test)
cm = confusion_matrix(y_test, y_pred_test)

accuracy = accuracy_score(y_test, y_pred_test)
classification_rep = classification_report(y_test, y_pred_test)
conf_matrix = confusion_matrix(y_test, y_pred_test)

# Stampa delle metriche di valutazione
print(f'Accuracy: {accuracy}')
print(f'Classification Report:\n{classification_rep}')
print(f'Confusion Matrix:\n{conf_matrix}')

from sklearn.metrics import roc_curve, precision_recall_curve, auc

# Calcola la probabilità della classe positiva
y_prob_test = model.predict_proba(X_test)[:, 1]

# Calcola la curva ROC
fpr, tpr, _ = roc_curve(y_test, y_prob_test)
roc_auc = auc(fpr, tpr)

# Calcola la curva di precisione-richiamo
precision, recall, _ = precision_recall_curve(y_test, y_prob_test)
pr_auc = auc(recall, precision)

# Plot della curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='red', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='green', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

# Plot della curva di precisione-richiamo
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='blue', lw=2, label=f'PR curve (area = {pr_auc:.2f})')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc='upper right')
plt.show()

import seaborn as sns

# Plot della matrice di confusione
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()