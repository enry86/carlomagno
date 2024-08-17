import torch
from torch import nn
import torch.optim
import carlomagno as cm
from carlomagno.evaluator import nn_evaluator
import os
import chess
import random

class BoardEvaluator():
    
    def __init__(self, model=None, sigma=0.0, look_ahead=0):
        self.boards = set()
        self.boards.clear()
        self.sigma = sigma
        self.look_ahead = look_ahead
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        device = torch.device(dev)
        if model is not None and os.path.exists(model):
            #print(f'Loading model from file: [{model}] with sigma: [{self.sigma}]')
            self.model = nn_evaluator.NNEvalutator(65, 1, 128, 3)
            self.model.load_state_dict(torch.load(model, map_location=device))
        else:
            #print(f'Loading new model with sigma: [{self.sigma}]')
            self.model = nn_evaluator.NNEvalutator(65, 1, 128, 3)                    
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
        moves = list(self.eval_moves(board))        
        checkmate_moves = filter(lambda x: x[2], moves)
        for m in checkmate_moves:
            return m[0:2]
        res = None
                
        try:
            if board.turn:
                res = min(moves, key=lambda x: x[1])
            else:
                res = max(moves, key=lambda x: x[1])
        except Exception as e:
            return (None, 0.0)
        return res[0:2]
        

    def eval_moves(self, board, level=0, source_move=None):
        for m in board.legal_moves:
            board.push(m)
            str_b = cm.board_to_string(board)                
            if str_b in self.boards:
                board.pop()
                continue
            if level < self.look_ahead:
                if level == 0:
                    source_move = m
                for nm in self.eval_moves(board, level+1, source_move):            
                    yield (source_move, nm[1], nm[2])
            else:                       
                v = cm.board_to_vector(board)
                score = self.evaluate(v) + random.gauss(0, self.sigma)            
                yield (m, score, board.is_checkmate())
            board.pop()
    
    
    def apply_move(self, board, move):
        board.push(move)
        str_b = cm.board_to_string(board)
        if str_b in self.boards:
            board.pop()
        else:
            self.boards.add(str_b)
            
    
    def reset_boards(self):
        self.boards.clear()
