#!/usr/env python

import torch
from torch import nn
from collections import OrderedDict
import copy

device = "cuda" if torch.cuda.is_available() else "cpu"

class NNEvalutator(nn.Module):
    def __init__(self, inputs, outputs, hidden, layers_cnt):
        super().__init__()
        layers = []

        layers.append(('input', nn.Linear(in_features=inputs, out_features=hidden)))
        layers.append(('relu_1', nn.ReLU()))
        for i in range(layers_cnt):
            layers.append((f"hidden_{i}", nn.Linear(in_features=hidden, out_features=hidden)))
            layers.append((f"relu_{i+2}", nn.ReLU()))
        layers.append(('output', nn.Linear(in_features=hidden, out_features=outputs)))

        self.layers_stack = nn.Sequential(OrderedDict(layers))
        
        self.loss_fn = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.0001)


    def forward(self, x):
        return self.layers_stack(x)

    def evaluate(self, features):
        x = torch.tensor(features)        
        return self.forward(x)        

    def start_training(self, train_x, train_y, test_x, test_y, epochs, output):
        if len(train_x) == 0 or len(test_x) == 0:
            return
        
        min_loss = None        
        best_model = None
        
        for epoch in range(epochs):
            self.train()
            pred_y = self.forward(train_x)
            loss = self.loss_fn(pred_y, train_y)
            
            self.optimizer.zero_grad()
            loss.backward()
            
            self.optimizer.step()
            
            self.eval()
            test_pred_y = self.forward(test_x)
            test_loss = self.loss_fn(test_pred_y, test_y)
            test_loss = float(test_loss)            
            
            if epoch % 10 == 0:
                print(f"Epoch: {epoch} | Loss: {loss:.5f} | Test Loss: {test_loss:.5f}")
            
            if min_loss == None or test_loss < min_loss:
                min_loss = test_loss
                best_model = copy.deepcopy(self)
            
        torch.save(best_model, output)
        print(f"Model stored in [{output}] with Loss {min_loss:.5f}")