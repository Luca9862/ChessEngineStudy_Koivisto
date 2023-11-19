import chess.pgn
import chess.engine

# Carica il file PGN
pgn_file_path = '/Users/lucacanali/Documents/GitHub/tirocinio_lucacanali/prova.pgn'
pgn = open(pgn_file_path)

# Configura il motore scacchistico (assicurati di avere un motore scacchistico installato)
engine_path = '/Users/lucacanali/Documents/Chess_engines/Stockfish-16_Mac_Apple_Silicon/Stockfish-16_Mac_Apple_Silicon'
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Ciclo attraverso tutte le partite nel file PGN
while True:
    game = chess.pgn.read_game(pgn)
    if game is None:
        break

    # Ottieni la rappresentazione della partita in formato UCI
    uci_moves = [move.uci() for move in game.mainline_moves()]

    # Analizza la partita con il motore scacchistico
    board = game.board()
    '''
    for uci_move in uci_moves:
        result = engine.play(board, chess.engine.Limit(time=1.0))
        board.push(chess.Move.from_uci(uci_move))
        print("Mossa:", uci_move, "Analisi:", result)
    '''

    for uci_move in uci_moves:
        result = engine.play(board, chess.engine.Limit(time=1.0))  # Modifica il tempo a tuo piacimento

        # Estrai e stampa informazioni dettagliate
        move = chess.Move.from_uci(uci_move)
        print(f"Mossa: {move.uci()}")
        print(f"Analisi: Migliore Mossa: {result.move}, Ponder: {result.ponder}")
        if result.info and 'score' in result.info:
            score = result.info['score']
            print(f"Valutazione: {score.relative.score()}")  # Accedi alla valutazione
        else:
            print("Valutazione non disponibile")

        print("-" * 30)

        board.push(move)

# Chiudi il motore scacchistico
engine.quit()