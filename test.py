#!/usr/bin/python

import carlomagno as cm
from carlomagno.evaluator import board_evaluator
import chess
import chess.pgn
import random

be_w = board_evaluator.BoardEvaluatorSmall('models/be_norm_v0.0.0.state', 0.01, look_ahead=0)
be_b = board_evaluator.BoardEvaluator('models/be_big_v0.0.1.state', 0.01)

def test_evaluation(b):    
    best_score = 0.0
    best_move = None
    current_turn = b.turn

    v = cm.board_to_vector(b)
    print(f'Board: {v}')
    
    if current_turn:
        print('WHITE')
    else:
        print('BLACK')
    for m in b.legal_moves:
        b.push(m)                        
        v = cm.board_to_vector(b)
        score = be.evaluate(v)
        print(f'Board: {v}')
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
        move, score = be_w.select_move(board)
        #print(f'RND WHITE: MOVE: [{move}], SCORE: [{score}]')
        if move == None:
            #print('DRAW')
            draw = True
            game_ended = True
            continue
        be_w.apply_move(board, move)
        game_ended = board.is_checkmate() or board.is_stalemate()
        if not game_ended:
            move, score = be_b.select_move(board)
            #print(f'CM BLACK: MOVE: [{move}], SCORE: [{score}]')   
            if move == None:
                #print('DRAW')
                draw = True
                game_ended = True
                continue
            be_b.apply_move(board, move)
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


def get_random_move(board):
    moves = []
    for m in board.legal_moves:
        moves.append(m)
        board.push(m)
        if board.is_checkmate():
            board.pop()
            return (m, 1.0)
        board.pop()
    return (random.choice(moves), 0.0)
    
    


def test_play_sequence(games):
    counts = {}
    for g in range(games):
        be_w.reset_boards()
        be_b.reset_boards()
        res = test_play()
        if res not in counts:
            counts[res] = 1.0 / games
        else:
            counts[res] += 1.0 / games
        print(f'Game {g+1}: [{res}] {counts}')
        be_rnd = None
    print(counts)        
    
    
def test_eval_recursive():
    b = chess.Board()
    move = be_w.select_move(b)
    move_b = be_b.select_move(b)
    print(move, move_b)
    
    
test_play_sequence(10)
#test_eval_recursive()
    

