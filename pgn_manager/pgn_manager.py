import chess
import io
import chess.pgn
import csv
from os.path import exists
import os
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

#funzione che prende come argomento un csv ed il relativo percorso per crearlo
def _createCSV(path, *columns):
    csv_exists = os.path.exists(path)
    if not csv_exists:
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)

#funzione che legge un pgn e restituisce un oggetto chess.pgn.Game che rappresenta la partita
def _readPGN(pgn_path):
    pgn_file = open(pgn_path)
    pgn_content = pgn_file.read()
    pgn_file.close()

    pgn_games = []
    pgn = io.StringIO(pgn_content)
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        pgn_games.append(game)

    return pgn_games

def _createID(game):
    event = game.headers.get('Event') or ''
    white = game.headers.get('White') or ''
    black = game.headers.get('Black') or ''
    whitefideid = game.headers.get('WhiteFideId') or ''
    blackfideid = game.headers.get('BlackFideId') or ''
    result = game.headers.get('Result') or ''
    whiteElo = game.headers.get('WhiteElo') or ''
    blackElo = game.headers.get('BlackElo') or ''
    round = game.headers.get('Round') or ''
    time_control = game.headers.get('TimeControl') or ''
    date = game.headers.get('Date') or ''
    white_clock = game.headers.get('WhiteClock') or ''
    black_clock = game.headers.get('BlackClock') or ''
    moves = [str(move) for move in game.mainline_moves()]

    data = (event +  white + black + whitefideid + blackfideid + result + whiteElo + blackElo + round  + time_control + date + white_clock + black_clock +''.join(moves))

    # Crea l'ID utilizzando la funzione hash SHA-256
    hashed_id = hashlib.sha256(data.encode()).hexdigest()

    return hashed_id

def _isRecorded(game, csv_file):
    id = str(_createID(game))
    with open(csv_file,'r') as csv_object:
        reader = csv.reader(csv_object)
        next(reader)
        for row in reader:
            if(row[0] == id):
                return True
        return False

#funzione che prende come argomento un pgn e un csv per aggiungere i dati della partita in quest'ultimo
def writeMatch(pgn_file, csv_file):
    _createCSV(csv_file, 'ID', 'Event', 'White', 'Black', 'WhiteFIDEId', 'BlackFIDEId', 'Result', 'WhiteElo', 'BlackElo', 'Round', 'TimeControl', 'Date', 'WhiteClock', 'BlackClock', 'Moves')
    games = _readPGN(pgn_file)

    for game in games:
        id = _createID(game)
        event = game.headers.get('Event')
        white = game.headers.get('White')
        black = game.headers.get('Black')
        whitefideid = game.headers.get('WhiteFideId')
        blackfideid = game.headers.get('BlackFideId')
        result = game.headers.get('Result')
        whiteElo = game.headers.get('WhiteElo')
        blackElo = game.headers.get('BlackElo')
        round = game.headers.get('Round')
        time_control = game.headers.get('TimeControl')
        date = game.headers.get('Date')
        white_clock = game.headers.get('WhiteClock')
        black_clock = game.headers.get('BlackClock')
        moves = [str(move) for move in game.mainline_moves()]

        if not (_isRecorded(game, csv_file)):
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([id, event, white, black, whitefideid, blackfideid,
                                result, whiteElo, blackElo, round, time_control, date, white_clock, black_clock, moves])
                
#funzione che prende come argomento un pgn e salva tutte le partite nel pgn di destinazione            
def merge_pgn(pgn_file, pgn_destination):
    games_to_save = _readPGN(pgn_file)
    with open(pgn_destination, "w") as f:
        for game in games_to_save:
            f.write(str(game))
            f.write('\n\n')

#modificare i percorsi per usare lo script

csv_ex = '/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/pgn_manager/all_games.csv'

path = '/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/pgn_manager/pgn_games/Carlsen.pgn'

pgn_destination = '/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/pgn_manager/all_pgn.pgn'
'''
file_list = os.listdir(path)
for file in file_list:
    pgn_file = path + '/' + file
    writeMatch(pgn_file, csv_ex)
'''

#merge_pgn(path, pgn_destination)

# Funzione per aggiungere il testo del file scelto alla barra di testo
def on_button_cerca_file():
    # Apri la finestra di dialogo di selezione file
    file = filedialog.askopenfilename()

    # Aggiungi il testo del file alla barra di testo
    text_box_cerca_file.delete(1.0, "end")
    text_box_cerca_file.insert(1.0, file)

# Funzione per aggiungere il testo del percorso scelto alla barra di testo
def on_button_percorso():
    # Chiedi all'utente di inserire un percorso
    percorso = filedialog.askdirectory()
    # Aggiungi il testo del percorso alla barra di testo
    text_box_percorso.delete(1.0, "end")
    text_box_percorso.insert(1.0, percorso)

def on_button_merge():
    # Prendi il testo dei widget Text dall'utente
    text1 = str(text_box_cerca_file.get(1.0, 'end-1c'))
    text2 = str(text_box_percorso.get(1.0, 'end-1c'))

    # Verifica se il testo dei widget Text è vuoto
    if text1 == '' or text2 == '':
        # Mostra un messaggio di errore
        messagebox.showerror('Errore', 'I campi non possono essere vuoti.')
        return

    # Esegui la funzione merge_pgn()
    merge_pgn(text1, text2)

root = tk.Tk()
root.title("pgn_manager by Luca Canali")
root.geometry("350x200")

#notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Crea il menu "add into csv"
frame_csv = ttk.Frame(notebook, width=400, height=280)
# Crea il menu "merge pgn"
frame_pgn = ttk.Frame(notebook, width=400, height=280)
button_cerca_file = ttk.Button(frame_pgn, text="Cerca file", command=lambda: on_button_cerca_file())
button_percorso = ttk.Button(frame_pgn, text='Inserisci percorso', command=lambda: on_button_percorso())
# Crea la barra di testo
text_box_cerca_file = tk.Text(frame_pgn, width=50, height=1)
text_box_percorso = tk.Text(frame_pgn, width=50, height=1)
text1 = str(text_box_cerca_file.get(1.0, 'end'))
text2 = str(text_box_percorso.get(1.0, 'end'))
button_merge = ttk.Button(frame_pgn, text='Merge', command=on_button_merge)

# Posiziona i pulsanti
button_cerca_file.grid(row=0, column=0, padx=10, pady=10)
button_percorso.grid(row=1, column=0, padx=10, pady=10)
button_merge.grid(row=2, column=0, padx=10, pady=10)
text_box_cerca_file.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_percorso.grid(row=1, column=1, padx=0, pady=10, sticky='ew')


frame_csv.pack(fill='both', expand=True)
frame_pgn.pack(fill='both', expand=True)

notebook.add(frame_csv, text='csv_creator')
notebook.add(frame_pgn, text='pgn_merge')

root.mainloop()
