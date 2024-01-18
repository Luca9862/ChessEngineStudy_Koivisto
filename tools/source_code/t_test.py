import pandas as pd
from scipy.stats import wilcoxon

# Carica i dati da CSV
df = pd.read_csv('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/results/0,1/Koivisto_Berserk/allScores.csv')

# Rimuovi eventuali NaN
df = df.dropna(axis=1)

# Numero di partite
num_partite = df.shape[0]

# Inizializza una lista per memorizzare i risultati del test per ciascuna coppia di colonne (mosse consecutive)
risultati_test = []

# Applica il test di Wilcoxon per ciascuna coppia di colonne in ogni partita
for i in range(1, df.shape[1]):
    differenze = df.iloc[:, i] - df.iloc[:, i - 1]
    stat, p_value = wilcoxon(differenze)
    risultati_test.append((i - 1, i, stat, p_value))

# Stampa i risultati
for coppia in risultati_test:
    print(f'Mosse {coppia[0] + 1}-{coppia[1]}: Statistica del test={coppia[2]}, Valore p={coppia[3]}')

