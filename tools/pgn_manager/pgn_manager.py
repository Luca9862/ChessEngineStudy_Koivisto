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
from tkinter import messagebox
from tkinter import Text

def _createCSV(path, *columns):
    """
    The function creates a CSV file in the desired path and with the desired column names.

    Args:
        a: PGN path
        b: Names of column

    Returns:
        csv file

    """
    csv_exists = os.path.exists(path)
    if not csv_exists:
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)

def _readPGN(pgn_path):
    """
    The function creates a list that contains all the games in the PGN file.

    Args:
        a: PGN path

    Returns:
        A list that contains chess.pgn.game objects.

    """
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
    """
    A function that creates a unique ID for a chess game.

    Args:
        a: chess.pgn.game

    Returns:
        ID created with the SHA-256 function

    """
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

    #Create ID using SHA-256 hash function
    hashed_id = hashlib.sha256(data.encode()).hexdigest()

    return hashed_id

def _isRecorded(game, csv_file):
    """
    A function that tells if a specific game exists in a CSV file.

    Args:
        a: chess.pgn.game
        b: csv file

    Returns:
        boolean

    """
    id = str(_createID(game))
    with open(csv_file,'r') as csv_object:
        reader = csv.reader(csv_object)
        next(reader)
        for row in reader:
            if(row[0] == id):
                return True
        return False

def writeMatchesIntoCsv(pgn_file, csv_file):
    """
    A function that writes the games from a PGN file to a CSV file.

    Args:
        a: PGN file
        b: CSV file

    Returns:
        csv file

    """
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
                
#function that takes a pgn argument and saves all matches in the target pgn            
def merge_pgn(pgn_file, pgn_destination):
    """
    The function that merges two PGN files in the second PGN/argument

    Args:
        a: PGN file
        b: PGN file

    Returns:
        pgn_destination

    """
    games_to_save = _readPGN(pgn_file)
    with open(pgn_destination, "a") as f:
        for game in games_to_save:
            f.write(str(game))
            f.write('\n\n')

def split_pgn(pgn_file, path_destination):
    """
    The function splits the games in the PGN file and creates a PGN for each game in the desired path

    Args:
        a: PGN file
        b: path

    Returns:
        pgn

    """
    games = _readPGN(pgn_file)
    for game in games:
        id = _createID(game)
        with open(os.path.join(path_destination, game.headers.get('White') + 'vs' + game.headers.get('Black') + id + ".pgn"), "w") as f:
            f.write(str(game))

#function that delete duplicates match in a PGN file
def delete_duplicate(pgn_file, destination_path):
    #TEST PHASE! DON'T USE THIS FUNCTION!
    """
    The function removes duplicate games from a PGN file and creates new PGN where it save the games without duplicates

    Args:
        a: PGN file
        b: path

    Returns:
        pgn

    """
    partite = _readPGN(pgn_file)
    d = {}
    for partita in partite:
        if partita not in d:
            d[partita] = True
        else:
            partite.remove(partita)
    file_path = os.path.join(destination_path, "no_duplicated.pgn")
    with open(file_path,"w") as f:
        for partita in partite:
            f.write(str(partita))

'''
    The following functions manage the buttons of the graphical user interface.
'''
    
#functions for managing the gui buttons
def on_button_search_file(text_box):
    file = filedialog.askopenfilename()
    text_box.delete(1.0, "end")
    text_box.insert(1.0, file)

def on_button_path(text_box):
    percorso = filedialog.askdirectory()
    text_box.delete(1.0, "end")
    text_box.insert(1.0, percorso)

def on_button_merge():
    text1 = str(text_box_search_file.get(1.0, 'end-1c'))
    text2 = str(text_box_path.get(1.0, 'end-1c'))
    if text1 == '' or text2 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    merge_pgn(text1, text2)
    messagebox.showinfo('Success!', 'Merge completed')

def on_button_split():
    text1 = str(text_box_search_file_pgn_split.get(1.0, 'end-1c'))
    text2 = str(text_box_path_pgn_split.get(1.0, 'end-1c'))
    if text1 == '' or text2 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    split_pgn(text1, text2)
    messagebox.showinfo('Success!')

def on_button_append_csv():
    text1 = str(text_box_search_file_frame_csv.get(1.0, 'end-1c'))
    text2 = str(text_box_search_csv.get(1.0, 'end-1c'))
    if text1 == '' or text2 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    writeMatchesIntoCsv(text1, text2)
    messagebox.showinfo('Success!')

def on_button_delete_duplicate():
    text1 = str(text_box_search_file_pgn_duplicate.get(1.0, 'end-1c'))
    text2 = str(text_box_path_pgn_duplicate.get(1.0, 'end-1c'))
    if text1 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    delete_duplicate(text1, text2)

'''
    --------------------------------------------------------------------------------------------------------GUI--------------------------------------------------------------------------------------------------------
'''
root = tk.Tk()
root.title("pgn_manager")
root.geometry("380x250")

#notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

#menu "append csv"
frame_csv = ttk.Frame(notebook, width=400, height=280)
button_search_file_csv_frame = ttk.Button(frame_csv, text = 'PGN file', 
                                          command=lambda: on_button_search_file(text_box_search_file_frame_csv))
button_search_csv = ttk.Button(frame_csv, text = 'csv', command=lambda: on_button_search_file(text_box_search_csv))
text_box_search_file_frame_csv = tk.Text(frame_csv, width=50, height=1)
text_box_search_csv = tk.Text(frame_csv, width=50, height=1)
text1_frame_csv = str(text_box_search_file_frame_csv)
text2 = str(text_box_search_csv)
button_append_csv = ttk.Button(frame_csv, text = 'Append', command=on_button_append_csv)
text_append_csv = Text(root, height = 5, width = 52)
#positioning button
button_search_file_csv_frame.grid(row=0, column=0, padx=10, pady=10)
button_search_csv.grid(row=1, column=0, padx=10, pady=10)
button_append_csv.grid(row=2, column=0, padx=10, pady=10)
text_box_search_file_frame_csv.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_search_csv.grid(row=1, column=1, padx=0, pady=10, sticky='ew')
text_append_csv.insert(tk.END, 'Load the PGN file and add the path to a CSV file. The script will write all the games in the file to the CSV. Each game will have a unique ID.')
text_append_csv.state = "normal"

#menu "pgn_merge"
frame_pgn_merge = ttk.Frame(notebook, width=400, height=280)
button_search_file_pgn_merge = ttk.Button(frame_pgn_merge, text='PGN file', command=lambda: on_button_search_file(text_box_search_file))
button_path_pgn_merge = ttk.Button(frame_pgn_merge, text='Destination PGN', command=lambda: on_button_search_file(text_box_path))
text_box_search_file = tk.Text(frame_pgn_merge, width=50, height=1)
text_box_path = tk.Text(frame_pgn_merge, width=50, height=1)
text1_pgn_merge = str(text_box_search_file.get(1.0, 'end'))
text2_pgn_merge = str(text_box_path.get(1.0, 'end'))
button_merge = ttk.Button(frame_pgn_merge, text='Merge', command=on_button_merge)
#positioning buttons
button_search_file_pgn_merge.grid(row=0, column=0, padx=10, pady=10)
button_path_pgn_merge.grid(row=1, column=0, padx=10, pady=10)
button_merge.grid(row=2, column=0, padx=10, pady=10)
text_box_search_file.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_path.grid(row=1, column=1, padx=0, pady=10, sticky='ew')

#menu "pgn_split"
frame_pgn_split = ttk.Frame(notebook, width=400, height=280)
button_search_file_pgn_split = ttk.Button(frame_pgn_split, text='PGN file', 
                                          command=lambda: on_button_search_file(text_box_search_file_pgn_split))
button_search_path_pgn_split = ttk.Button(frame_pgn_split, text='Destination path', 
                                          command=lambda: on_button_path(text_box_path_pgn_split))
text_box_search_file_pgn_split = tk.Text(frame_pgn_split, width=50, height=1)
text_box_path_pgn_split = tk.Text(frame_pgn_split, width=50, height=1)
text1_pgn_split=str(text_box_search_file_pgn_split.get(1.0, 'end'))
text2_pgn_split=str(text_box_path_pgn_split.get(1.0, 'end'))
button_split = ttk.Button(frame_pgn_split, text='Split', command=on_button_split)
#positioning buttons
button_search_file_pgn_split.grid(row=0, column=0, padx=10, pady=10)
button_search_path_pgn_split.grid(row=1, column=0, padx=10, pady=10)
button_split.grid(row=2, column=0, padx=10, pady=10)
text_box_search_file_pgn_split.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_path_pgn_split.grid(row=1, column=1, padx=0, pady=10, sticky='ew')

#menu "pgn_duplicate"
frame_pgn_duplicate = ttk.Frame(notebook, width=400, height=280)
button_search_file_pgn_duplicate = ttk.Button(frame_pgn_duplicate, text='PGN file', command = lambda: on_button_search_file(text_box_search_file_pgn_duplicate))
button_search_path_pgn_duplicate = ttk.Button(frame_pgn_duplicate, text='Destination path', command=lambda: on_button_path(text_box_path_pgn_duplicate))
text_box_search_file_pgn_duplicate = tk.Text(frame_pgn_duplicate, width=50, height=1)
text_box_path_pgn_duplicate = tk.Text(frame_pgn_duplicate, width=50, height=1)
text1_pgn_duplicate = str(text_box_search_file_pgn_duplicate.get(1.0, 'end'))
text2_pgn_duplicate = str(text_box_path_pgn_duplicate.get(1.0, 'end'))
button_delete_duplicate = ttk.Button(frame_pgn_duplicate, text = 'Delete duplicate', command = on_button_delete_duplicate)
#positioning button
button_search_file_pgn_duplicate.grid(row=0, column=0, padx=10, pady=10)
button_search_path_pgn_duplicate.grid(row=1, column=0, padx=10, pady=10) 
button_delete_duplicate.grid(row=2, column=0, padx=10, pady=10)
text_box_search_file_pgn_duplicate.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
text_box_path_pgn_duplicate.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

frame_csv.pack(fill='both', expand=True)
frame_pgn_merge.pack(fill='both', expand=True)

notebook.add(frame_csv, text='csv_creator')
notebook.add(frame_pgn_merge, text='pgn_merge')
notebook.add(frame_pgn_split, text='pgn_split')
notebook.add(frame_pgn_duplicate, text='delete_duplicates')

root.mainloop()
