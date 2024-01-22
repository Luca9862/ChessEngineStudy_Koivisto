import scipy.stats as stats
from ChessScoreAnalyze import get_dataset, average_calculation

# Funzione che prende un pgn, estrapola gli score e li salva in un csv dove ogni riga rappresenta una partita e ogni colonna è un turno di gioco
get_dataset('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/dataset/game_script_eros/koiv_berserk/0,1sec/Koivisto_Berserk_0.1_fix.pgn')

# Funzione che prende un csv, calcola la media dello score per ogni turno di gioco e salva le medie in una lista
mean_scores = average_calculation('allScores.csv')

# Rimuovi eventuali elementi None dalla lista
averages = [score for score in mean_scores if score is not None]

# Esegui il test t per campioni indipendenti rispetto al valore di riferimento (ad esempio, zero)
t_statistic, p_value = stats.ttest_1samp(averages, 0)

# Stampare i risultati del test t
print("Statistiche test t t =", t_statistic)
print("Valore p =", p_value)

# Confronto della media con il valore di riferimento
if p_value < 0.05:
    print("La media è significativamente diversa dal valore di riferimento.")
else:
    print("Non ci sono differenze significative dalla media al valore di riferimento.")



