import torch
from torch import nn
import torch.optim
import carlomagno as cm
from carlomagno.evaluator import nn_evaluator
import os
import chess


class BoardEvaluator():
    boards = set()
    
    def __init__(self, model=None):
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"
        device = torch.device(dev)
        if model is not None and os.path.exists(model):
            print('Loading model from file')
            self.model = nn_evaluator.NNEvalutator(65, 1, 128, 3)
            self.model.load_state_dict(torch.load(model, map_location=device))
        else:
            print('Loading new model')
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
        next_turn = 1.0
        current_turn = board.turn 
        if current_turn:
            next_turn = -1.0
        for m in board.legal_moves:                   
            board.push(m)                        
            v = cm.board_to_vector(board, next_turn)
            str_v = '|'.join(map(lambda x: str(x), v))             
            if str_v in self.boards:
                #print(f'Board [{str_v}] already played, skip move to avoid loops')
                board.pop()
                continue
            
            score = self.evaluate(v)
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

    def reset_boards(self):
        self.boards.clear()
    