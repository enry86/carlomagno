#!/usr/bin/python

import carlomagno as cm
from carlomagno.evaluator import board_evaluator
import chess
import chess.pgn

be = board_evaluator.BoardEvaluator('be_norm_v0.0.0.model')


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
    
    
    
b = chess.Board()
while not b.is_checkmate():
    test_evaluation(b)
    

