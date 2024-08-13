#!/usr/bin/python

import carlomagno as cm
from carlomagno.evaluator import board_evaluator
import chess
import chess.pgn

be = board_evaluator.BoardEvaluator('models/be_norm_v0.0.0.state')
be_rnd = board_evaluator.BoardEvaluator()

def test_evaluation(b):    
    best_score = 0.0
    best_move = None
    current_turn = b.turn
    next_turn = 1.0
    if current_turn:
        next_turn = -1.0
        
    if current_turn:
        print('WHITE')
    else:
        print('BLACK')
    for m in b.legal_moves:
        b.push(m)                        
        v = cm.board_to_vector(b, next_turn)
        score = be.evaluate(v)
        print(f'Move [{m}]: Score: [{score}]')
        
        if b.is_checkmate():
            best_move = m
            best_score = score
            break
        
        if best_move == None:
            best_move = m
            best_score = score
        else:
            if current_turn and score < best_score:
                best_move = m
                best_score = score
            elif not current_turn and score > best_score:
                best_move = m
                best_score = score        
        b.pop()

    b.push(best_move)
    print('BEST MOVE:')
    print(b)
    print(m, 'Best Score:', best_score)
    
def test_features():
    print(cm.read_games_from_file('data/lichess_db_standard_rated_2013-01.pgn', 1))
    
    
def test_eval():    
    b = chess.Board()
    moves = 0
    while not b.is_checkmate() and moves < 10:
        test_evaluation(b)
        moves += 1  
        
def test_rating():
    fin = open('data/lichess_db_standard_rated_2013-01.pgn')
    game = chess.pgn.read_game(fin)
    b = game.board()    
    for m in game.mainline_moves():
        turn = 1.0
        b.push(m)
        if not b.turn:
            turn = -1.0
        v = cm.board_to_vector(b, turn)    
        print('Turn:', turn)
        print(b)        
        print('Score:', be.evaluate(v))
    print(game.headers['Result'])
    print(b.is_checkmate())
    
    
def test_play():
    white_win = False
    draw = False
    score = 0.0
    res = 0
    board = chess.Board()
    game_ended = board.is_checkmate() or board.is_stalemate()
    while not game_ended:
        move, score = be_rnd.select_move(board)
        #print(f'RND WHITE: MOVE: [{move}], SCORE: [{score}]')
        if move == None:
            #print('DRAW')
            draw = True
            game_ended = True
            continue
        board.push(move)
        game_ended = board.is_checkmate() or board.is_stalemate()
        if not game_ended:
            move, score = be.select_move(board)
            #print(f'CM BLACK: MOVE: [{move}], SCORE: [{score}]')   
            if move == None:
                #print('DRAW')
                draw = True
                game_ended = True
                continue
            board.push(move)
            game_ended = board.is_checkmate() or board.is_stalemate()
        else:
            white_win = True
            res = -1
            #print('WHITE WINS')
    if not white_win and not draw:
        res = 1
        #print('BLACK WINS')
    #print(f'GAME ENDED: LAST SCORE [{score}]')
    
    return res



def test_play_sequence(games):
    counts = {}
    for g in range(games):
        be.reset_boards()
        be_rnd = board_evaluator.BoardEvaluator()
        res = test_play()
        if res not in counts:
            counts[res] = 1.0 / games
        else:
            counts[res] += 1.0 / games
    print(counts)        
    
test_play_sequence(10)    
    

