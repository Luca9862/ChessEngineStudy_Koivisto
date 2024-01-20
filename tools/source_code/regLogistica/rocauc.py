import chess
from chess import pgn
import io
import matplotlib.pyplot as plt
import numpy as np
from pgn_manager import _readPGN
import csv

player_bianco_avg_score = np.array([])
player_nero_avg_score = np.array([])

avg_score_player_1 = []
avg_score_player_2 = []

varianza_player_1 = []
varianza_player_2 = []

mediana_player_1 = []
mediana_player_2 = []

game_result = []
game_playcount = []
game_moveTime = []

pgn_path = r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\game_script_eros\koiv_berserk\all.pgn"
#pgn_temp = r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\game_script_eros\koiv_berserk\all.pgn"
numero_game = 1200

csv_path = r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\allScores.csv"
#csv_path_pima = "pima.csv"
#temp_pgn = "temp.pgn"

def win_draw_loss(pgn_path):
    with open(pgn_path) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        games = _readPGN(pgn_path)
        for game in games:
            result = game.headers.get('Result')      
            if result == '1-0':
                game_result.append(1)
            elif result == '0-1':
                game_result.append(0)
            elif result == '1/2-1/2': 
                game_result.append(0)
    return game_result

game_result = win_draw_loss(pgn_path)
game_result_np = np.array(game_result)
print(game_result_np)

def playcount(pgn_path):
    with open(pgn_path) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        games = _readPGN(pgn_path)
        for game in games:  
            playCount = game.headers.get('PlayCount')
            play = float(playCount)
            game_playcount.append(play)
    return game_playcount

def _moveTime(pgn_path):
    with open(pgn_path) as pgn:
        # Leggi la partita dal file PGN
        game = chess.pgn.read_game(pgn)
        games = _readPGN(pgn_path)
        for game in games:  
            moveTime = game.headers.get('TimeControl')
            play = float(moveTime)
            game_moveTime.append(play)
    return game_moveTime

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
            #print("Partita numero: "+str(partita_numero))
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

def _avg_score_per_game(csv_path, diff_white, diff_black):
 
    with open(csv_path, "r") as f:
        lines = csv.reader(f)
        avg1 = []
        avg2 = []    
        # Inizializza un contatore per tener traccia delle righe
        total_lines = 0.0

        #for i in range(1, 94):
        for line in lines:
            avg_player_1_temp = []
            avg_player_2_temp = []
            # Incrementa il contatore di riga
            total_lines += 1
            i = len(line)
            #print(i)
            # Verifica se il numero di riga è pari o dispari
            if total_lines % 2 == 0:
                #del avg_player_1_temp
                # Questa è una riga pari
                for x in range(1, i):
                    try:
                        #print(line[x])
                        avg_player_2_temp.append()
                        #temp2 = float(line[i])
                        #avg2.append(temp2)
                        #print(float(line[i]))
                    except:
                        diff_black += 1
                #print(f"Player 2: {line[i]}")
            else:
                for x in range(1, i):
                    try:
                        avg_player_1_temp.append(float(line[x]))
                    except:
                        diff_white += 1
            if avg_player_1_temp != []:
                array1 = np.array(avg_player_1_temp)
                #mean_player_1 = np.array([])
                mean = np.mean(array1)
                avg1.append(mean)
                #print(mean)
    print(avg1)
    
    return avg1

def _delete_content(temp_pgn, csv_path):
    with open(temp_pgn, 'w') as pgn:
        pgn.write("")
    with open(csv_path, 'w')as csv:
        csv.write("")

getScore(pgn_path, csv_path)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.metrics import f1_score

game_playcount = playcount(pgn_path)
game_playcount_np = np.array(game_playcount)
print(game_playcount_np)

game_score = _avg_score_per_game(csv_path, 0, 0)
game_score_np = np.array(game_score)

'''game_moveTime = _moveTime(pgn_temp)
game_moveTime_np = np.array(game_moveTime)'''

import csv

#prendo i dati nelle posizioni i, li scrivo all'interno di un CSV, il numero i deve corrispondere al numero delle partite
for i in range(0,numero_game):
    with open(r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\test.csv", 'a', newline='') as file:
        # Crea un oggetto writer per scrivere nel file CSV
        writer = csv.writer(file)
        # Scrivi i dati nelle colonne
        dati_da_scrivere = [game_result_np[i], game_playcount_np[i], game_score_np[i]]
        writer.writerow(dati_da_scrivere)

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import statsmodels.api as sm

#import pandas
import pandas as pd
col_names = ['risultato', 'playcount', 'score']
# load dataset
pima = pd.read_csv(r"C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\test.csv", header=None, names=col_names)
pima.head()
print(pima)
#X=game_score_np.reshape(-1,1)



#split dataset in features and target variable
feature_cols = ['playcount', 'score']
X = pima[feature_cols] # Features
y = pima.risultato # Target variable

#_delete_content(temp_pgn, csv_path_pima)

# Dividi i dati in set di addestramento e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crea un'istanza del modello di regressione logistica
model = LogisticRegression()

# Addestra il modello utilizzando i dati di addestramento
model.fit(X_train, y_train)

coefficients = model.coef_
intercept = model.intercept_

# Effettua previsioni sui dati di test
y_pred_test = model.predict(X_test)
y_prob_test = model.predict_proba(X_test)
# Effettua previsioni sui dati di train
y_pred_train = model.predict(X_train)
y_prob_train = model.predict_proba(X_train)
# Calcola l'accuratezza del modello
accuracy = accuracy_score(y_test, y_pred_test)
cm = confusion_matrix(y_test, y_pred_test)
'''
cm_train = confusion_matrix(y_train, y_pred_train)
accuracy_train = accuracy_score(y_train, y_pred_train)'''

print(cm)
#print(cm_train)

print(f'Accuratezza del modello: {accuracy:.2f}')

#print(f'Accuratezza del modello: {accuracy_train:.2f}')
print("----")
# Stampa una relazione di classificazione
print(classification_report(y_test, y_pred_test))
# Grafico di dispersione di Y rispetto a X1
plt.figure(figsize=(12, 5))

x1 = pima.playcount # Target variable
x2 = pima.score # Target variable


from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
# Calcola la curva ROC

print(len(y_train))
print(len(y_pred_test))
fpr, tpr, _ = roc_curve(y_train, y_pred_train)
# Calcola l'area sotto la curva ROC (AUC)
roc_auc = auc(fpr, tpr)

print(roc_auc)

# Traccia la curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='Curva ROC (area = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('Tasso Falsi Positivi (FPR)')
plt.ylabel('Tasso Veri Positivi (TPR)')
plt.title('Curva ROC per Regressione Logistica')
plt.legend(loc="lower right")
plt.show()

print("-----------------------------")

n = len(y_test)
x_array_1 = []
for i in range(1, n+1):
    x_array_1.append(i)
    
n = len(y_train)
x_array_2 = []
for i in range(1, n+1):
    x_array_2.append(i)

print(y_test)
print(y_prob_test)
print(x_array_1)

y_ticks = [0,1]
y_ticks_label = ["0","1"]

from sklearn.metrics import roc_auc_score, roc_curve

roc_auc = roc_auc_score(y_train, y_pred_train)

fpr, tpr, thresholds = roc_curve(y_train, y_pred_train)

'''plt.plot(fpr, tpr, color='darkorange')
plt.plot([0,1], [0,1], color='navy')
plt.show()'''

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, 
            xticklabels=["Negativo (0)", "Positivo (1)"],
            yticklabels=["Negativo (0)", "Positivo (1)"])
plt.xlabel("Previsto")
plt.ylabel("Effettivo")
plt.title("Matrice di Confusione")
plt.show()

#x_data = X_train[:, 0]
#print(x_data)
#plt.subplot(1, 2, 1)
plt.plot(x_array_2, y_train, color='orange' ,label='Dati trainati')
plt.scatter(x_array_2, y_pred_train, color='blue', s=10, linewidth=2, label='Predizioni dati trainati')
#plt.plot(fpr, tpr, color='darkorange')
#plt.plot([0,1], [0,1], color='navy')
plt.xlabel('Partite')
plt.ylabel('Risultato')
plt.yticks(y_ticks, y_ticks_label)
plt.title('Grafico di previsione sulle y_train')
plt.show()

# Grafico di dispersione di Y rispetto a X2
#plt.subplot(1, 2, 2)
plt.plot(x_array_1, y_test, color='orange', label='Dati veri')
plt.scatter(x_array_1, y_pred_test, color='blue', s=10, linewidth=2, label='Dati predetti')
plt.xlabel('Partite')
plt.ylabel('Risultato')
plt.yticks(y_ticks, y_ticks_label)
plt.title('Grafico di previsione sulle y_test')
#plt.tight_layout()
plt.show()

print(X_test)

print(str(coefficients)+str(intercept))


