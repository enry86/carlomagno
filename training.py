#!/usr/bin/python

import carlomagno as cm
from carlomagno.evaluator import board_evaluator


train_ds = cm.read_games_from_file('data/lichess_db_standard_rated_2013-01.pgn', 1000)
test_ds = cm.read_games_from_file('data/lichess_db_standard_rated_2013-01.pgn', 100, 1000)

be = board_evaluator.BoardEvaluator('be_v0.0.0.model')
be.train(train_ds, test_ds, 10000, 'be_v0.0.0.model')

