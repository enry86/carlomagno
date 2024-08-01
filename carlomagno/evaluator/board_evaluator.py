import torch
from torch import nn
import torch.optim
from carlomagno.evaluator import nn_evaluator
import os

class BoardEvaluator():
    
    def __init__(self, model=None):
        if model is not None and os.path.exists(model):            
            self.model = torch.load(model)
        else:
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