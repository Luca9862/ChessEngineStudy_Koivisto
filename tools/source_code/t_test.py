from scipy.stats import ttest_ind
import csv
from scipy.stats import f_oneway

def main(csv_file):
    sums = {}
    counts = {}

    with open(csv_file, newline='') as csvfile:
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
    
    # Calcola le medie
    averages = [sums[i] / counts[i] if counts[i] > 0 else None for i in range(max(sums.keys()) + 1)]
    print(averages)

    # Esegui il test ANOVA
    _, p_value = f_oneway(*[list(map(float, row)) for row in csv.reader(open(csv_file, newline=''))])
    
    if p_value < 0.05:
        print("Il test ANOVA è significativo, ci sono differenze tra almeno due gruppi.")
    else:
        print("Il test ANOVA non è significativo, non ci sono differenze tra i gruppi.")


main('/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/results/0,1/Koivisto_Berserk/allScores.csv')