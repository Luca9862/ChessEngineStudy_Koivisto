import numpy as np

# Esempio di matrice delle caratteristiche X
X = np.array([
    [1, 0, 1, 0, 0, 1],  # Apertura A
    [0, 2, 0, 1, 0, 0],  # Apertura B
    [0, 1, 0, 0, 1, 1],  # Apertura C
])

# Normalizzazione dei dati
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Esegui l'algoritmo k-means
from sklearn.cluster import KMeans

k = 2  # Numero di cluster desiderato
kmeans = KMeans(n_clusters=k)
kmeans.fit(X_normalized)

# Etichette dei cluster assegnate a ciascuna apertura
cluster_labels = kmeans.labels_

# Visualizza le etichette dei cluster
print("Etichette dei Cluster:", cluster_labels)