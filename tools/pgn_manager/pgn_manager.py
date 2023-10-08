'''
TIROCINIO 2023 - CORSO DI LAUREA DI INFORMATICA TRIENNALE
pgn_manager è un'applicazione che permette la gestione e la manipolazione dei file PGN - Luca Canali 744802

'''
from os.path import exists
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Text
import glob
from pgnmanager import _readPGN
from pgnmanager import merge_pgn
from pgnmanager import split_pgn
from pgnmanager import writeMatchesIntoCsv

'''
    The following functions manage the buttons of the graphical user interface.
'''
    
#functions for managing the gui buttons
def on_button_search_file(text_box):
    file = filedialog.askopenfilename()
    text_box.delete(1.0, "end")
    text_box.insert(1.0, file)

def on_button_search_path(text_box):
    percorso = filedialog.askdirectory()
    text_box.delete(1.0, "end")
    text_box.insert(1.0, percorso)

def on_button_merge():
    text1 = str(text_box_search_file_fmerge.get(1.0, 'end-1c'))
    text2 = str(text_box_path_pgns_fmerge.get(1.0, 'end-1c'))
    text3 = str(text_box_pgn_destination_fmerge.get(1.0, 'end-1c'))
    if text3 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    if text1 == '' and text2 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    if text1 != '':
        merge_pgn(text1, text3)
        messagebox.showinfo('Success!', 'merge from PGN completed')
    if text2 != '':
        files = glob.glob(os.path.join(text2, "*.pgn"))
        for pgn in files:
            with open(pgn, "r") as f:
                merge_pgn(pgn, text3) #problems
        messagebox.showinfo('Success!', 'merge from folder completed')
        return 
    
def on_button_split():
    text1 = str(text_box_search_file_pgn_split.get(1.0, 'end-1c'))
    text2 = str(text_box_path_pgn_split.get(1.0, 'end-1c'))
    if text1 == '' or text2 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    split_pgn(text1, text2)
    messagebox.showinfo('Success!', 'split completed')

def on_button_append_csv():
    text1 = str(text_box_search_file_frame_csv.get(1.0, 'end-1c'))
    text2 = str(text_box_search_csv.get(1.0, 'end-1c'))
    if text1 == '' or text2 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    writeMatchesIntoCsv(text1, text2)
    messagebox.showinfo('Success!')

'''
def on_button_delete_duplicate():
    text1 = str(text_box_search_file_pgn_duplicate.get(1.0, 'end-1c'))
    text2 = str(text_box_path_pgn_duplicate.get(1.0, 'end-1c'))
    if text1 == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
        return
    delete_duplicate(text1, text2)
'''

'''
    --------------------------------------------------------------------------------------------------------GUI--------------------------------------------------------------------------------------------------------
'''
root = tk.Tk()
root.title("pgn_manager")
root.geometry("580x280")

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
button_append_csv = ttk.Button(frame_csv, text = 'Append', command=on_button_append_csv)
#positioning button
button_search_file_csv_frame.grid(row=0, column=0, padx=10, pady=10)
button_search_csv.grid(row=1, column=0, padx=10, pady=10)
button_append_csv.grid(row=2, column=0, padx=10, pady=10)
text_box_search_file_frame_csv.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_search_csv.grid(row=1, column=1, padx=0, pady=10, sticky='ew')

#menu "pgn_merge"
frame_pgn_merge = ttk.Frame(notebook, width=400, height=280)
button_search_file_pgn_merge = ttk.Button(frame_pgn_merge, text='PGN file', 
                                          command=lambda: on_button_search_file(text_box_search_file_fmerge))
button_search_path_pgns = ttk.Button(frame_pgn_merge, text='PATH',
                              command=lambda: on_button_search_path(text_box_path_pgns_fmerge))
button_destination_pgn_merge = ttk.Button(frame_pgn_merge, text='Destination PGN', 
                                   command=lambda: on_button_search_file(text_box_pgn_destination_fmerge))
text_box_search_file_fmerge = tk.Text(frame_pgn_merge, width=50, height=1)
text_box_pgn_destination_fmerge = tk.Text(frame_pgn_merge, width=50, height=1)
text_box_path_pgns_fmerge = tk.Text(frame_pgn_merge, width=50, height=1)
button_merge = ttk.Button(frame_pgn_merge, text='Merge', command=on_button_merge)
#positioning buttons
button_destination_pgn_merge.pack
button_search_file_pgn_merge.grid(row=0, column=0, padx=10, pady=10)
button_destination_pgn_merge.grid(row=2, column=0, padx=10, pady=10)
button_search_path_pgns.grid(row=1, column=0, padx=10, pady=10)
button_merge.grid(row=3, column=0, padx=10, pady=10)
text_box_search_file_fmerge.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_path_pgns_fmerge.grid(row=1, column=1, padx=10, pady=10)
text_box_pgn_destination_fmerge.grid(row=2, column=1, padx=0, pady=10, sticky='ew')

#menu "pgn_split"
frame_pgn_split = ttk.Frame(notebook, width=400, height=280)
button_search_file_pgn_split = ttk.Button(frame_pgn_split, text='PGN file', 
                                          command=lambda: on_button_search_file(text_box_search_file_pgn_split))
button_search_path_pgn_split = ttk.Button(frame_pgn_split, text='Destination path', 
                                          command=lambda: on_button_search_path(text_box_path_pgn_split))
text_box_search_file_pgn_split = tk.Text(frame_pgn_split, width=50, height=1)
text_box_path_pgn_split = tk.Text(frame_pgn_split, width=50, height=1)
button_split = ttk.Button(frame_pgn_split, text='Split', command=on_button_split)
#positioning buttons
button_search_file_pgn_split.grid(row=0, column=0, padx=10, pady=10)
button_search_path_pgn_split.grid(row=1, column=0, padx=10, pady=10)
button_split.grid(row=2, column=0, padx=10, pady=10)
text_box_search_file_pgn_split.grid(row=0, column=1, padx=0, pady=10, sticky='ew')
text_box_path_pgn_split.grid(row=1, column=1, padx=0, pady=10, sticky='ew')

#menu "pgn_duplicate"
frame_pgn_duplicate = ttk.Frame(notebook, width=400, height=280)
button_search_file_pgn_duplicate = ttk.Button(frame_pgn_duplicate, text='PGN file', 
                                              command = lambda: on_button_search_file(text_box_search_file_pgn_duplicate))
button_search_path_pgn_duplicate = ttk.Button(frame_pgn_duplicate, text='Destination path', 
                                              command=lambda: on_button_search_path(text_box_path_pgn_duplicate))
text_box_search_file_pgn_duplicate = tk.Text(frame_pgn_duplicate, width=50, height=1)
text_box_path_pgn_duplicate = tk.Text(frame_pgn_duplicate, width=50, height=1)
button_delete_duplicate = ttk.Button(frame_pgn_duplicate, text = 'Delete duplicate', command = lambda:messagebox.showerror('ERROR','Function not ready') ) #on_button_delete_duplicate
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
