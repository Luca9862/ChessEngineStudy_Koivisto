import pandas as pd
import numpy as np

# Carica il file CSV
df = pd.read_csv(r'')

# Calcola la media per ogni colonna (mossa)
media_per_mossa = df.mean()

# Calcola la deviazione standard per ogni colonna (mossa)
deviazione_standard_per_mossa = df.std()

# Ora hai la media e la deviazione standard per ogni mossa

# Puoi anche plottare la media e la deviazione standard per avere una visualizzazione
import matplotlib.pyplot as plt

# Plot della media
plt.plot(media_per_mossa, label='Media')

# Plot della deviazione standard
plt.plot(deviazione_standard_per_mossa, label='Deviazione Standard')

plt.xlabel('Numero di mossa')
plt.ylabel('Punteggio')
plt.legend()
plt.show()