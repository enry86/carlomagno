import torch
from torch import nn
import torch.optim
import carlomagno as cm
from carlomagno.evaluator import nn_evaluator
import os
import chess
import random

class BoardEvaluator():
    boards = set()
    
    def __init__(self, model=None, sigma=0.0):
        self.sigma = sigma
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        device = torch.device(dev)
        if model is not None and os.path.exists(model):
            print(f'Loading model from file: [{model}] with sigma: [{self.sigma}]')
            self.model = nn_evaluator.NNEvalutator(65, 1, 128, 3)
            self.model.load_state_dict(torch.load(model, map_location=device))
        else:
            print(f'Loading new model with sigma: [{self.sigma}]')
            self.model = nn_evaluator.NNEvalutator(65, 1, 128, 3)            
        self.boards.clear()
        self.model.eval()
        
    def evaluate(self, input):
        input_t = torch.tensor(input)
        return self.model(input_t)
    
    def train(self, train_ds, test_ds, epochs, filename):
        train_x = torch.tensor(train_ds[0])
        train_y = torch.tensor(train_ds[1])
        test_x = torch.tensor(test_ds[0])
        test_y = torch.tensor(test_ds[1])
        
        self.model.start_training(train_x, train_y, test_x, test_y, epochs, filename)
        
    
    def select_move(self, board):
        sel_board = None
        best_move = None
        best_score = 0.0
        current_turn = board.turn 
        for m in board.legal_moves:                   
            board.push(m)                        
            v = cm.board_to_vector(board)
            str_v = '|'.join(map(lambda x: str(x), v))             
            if str_v in self.boards:
                #print(f'Board [{str_v}] already played, skip move to avoid loops')
                board.pop()
                continue
            
            score = self.evaluate(v) + random.gauss(0, self.sigma)
            #print(f'Move [{m}]: Score: [{score}]')

            if board.is_checkmate():
                best_move = m
                best_score = score
                sel_board = str_v
                board.pop()
                break

            if best_move == None:
                best_move = m
                best_score = score
                sel_board = str_v
            else:
                if current_turn and score < best_score:
                    best_move = m
                    best_score = score
                    sel_board = str_v
                elif not current_turn and score > best_score:
                    best_move = m
                    best_score = score        
                    sel_board = str_v
            board.pop()
        
        self.boards.add(sel_board)
        return (best_move, best_score)

    def eval_moves(self, board):
        for m in board.legal_moves:
            board.push(m)
            
    
    
    def reset_boards(self):
        self.boards.clear()
    