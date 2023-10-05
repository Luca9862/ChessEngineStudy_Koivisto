import chess
import io
from pgn_manager import _readPGN
import tkinter as tk
from tkinter import ttk
from pgn_manager import on_button_search_file
from pgn_manager import on_button_search_path

##########! DANGEROUS AREA !##########
#! This script needs testing
#TODO: GUI, filter_time, filter match score better
#1--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def filter_white(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White'):
            games_filtered.append(game)
    return games_filtered

def filter_black(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('Black'):
            games_filtered.append(game)
    return games_filtered
#2--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def filter_player_win(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and game.headers.get('Result') == '1-0':
            games_filtered.append(game)
            continue
        if player in game.headers.get('Black') and game.headers.get('Result') == '0-1':
            games_filtered.append(game)
    return games_filtered

def filter_player_win_white(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and game.headers.get('Result') == '1-0':
            games_filtered.append(game)
    return games_filtered

def filter_player_win_black(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('Black') and game.headers.get('Result') == '0-1':
            games_filtered.append(game)
    return games_filtered
#3--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def filter_player_lose(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and game.headers.get('Result') == '0-1':
            games_filtered.append(game)
            continue
        if player in game.headers.get('Black') and game.headers.get('Result') == '1-0':
            games_filtered.append(game)
    return games_filtered

def filter_player_lose_white(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and game.headers.get('Result') == '0-1':
            games_filtered.append(game)
    return games_filtered

def filter_player_lose_black(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('Black') and game.headers.get('Result') == '1-0':
            games_filtered.append(game)
    return games_filtered
#4--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TODO:function review necessity (don't use)
def filter_player_draws(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if (player in game.headers.get('White') or player in game.headers.get('Black')) and game.headers.get('Result') == '1/2-1/2': 
            games_filtered.append(game)
    return games_filtered

def filter_player_draw_white(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and game.headers.get('Result') == '1/2-1/2': 
            games_filtered.append(game)
    return games_filtered

def filter_player_draw_black(pgn, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('Black') and game.headers.get('Result') == '1/2-1/2': 
            games_filtered.append(game)
    return games_filtered
#5--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def filter_for_eco(pgn, eco):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if eco == game.headers.get('ECO'):
            games_filtered.append(game)
    return games_filtered

def filter_for_white_player_eco(pgn, eco, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and eco == game.headers.get('ECO'):
            games_filtered.append(game)
    return games_filtered

def filter_for_white_player_eco_win(pgn, eco, player):
    games = _readPGN(pgn)
    games_filtered = []
    for game in games:
        if player in game.headers.get('White') and eco == game.headers.get('ECO') and game.headers.get('Result') == '1-0':
            games_filtered.append(game)
    return games_filtered

'''
#? def filter_for_black_player_eco(pgn, eco, player)
#? def filter_for_black_player_eco_win(pgn, eco, player)
'''
#6--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
def filter_time(pgn, time):
    #TODO
'''

#print(filter_player_draws(r'C:\Users\canal\Documents\GitHub\tirocinio_lucacanali\dataset\Koivisto_9_0_64-bit.bare.[3174].pgn (1)\Koivisto_9_0_64-bit.bare.[3174].pgn', 'Koivisto'))

root = tk.Tk()
root.title("pgn_manager")
root.geometry("580x280")

button_text_box_pgn = ttk.Button(root, text='PGN', command=lambda: on_button_search_file)
button_text_box_destination = ttk.Button(root, text='Path', command=lambda: on_button_search_path)
text_box_path = tk.Text(root, width=50, height=1)
text_box_destination = tk.Text(root, width=50, height=1)

button_text_box_pgn.grid(row=0, column=0, padx=10, pady=10)
button_text_box_destination.grid(row=1, column=0, padx=10, pady=10)
text_box_path.grid(row=0, column=1,padx=10, pady=10, sticky='ew')
text_box_destination.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

root.mainloop()
