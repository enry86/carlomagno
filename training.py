#!/usr/bin/python

import carlomagno as cm
from carlomagno.evaluator import board_evaluator


train_ds = cm.read_games_from_file('data/lichess_db_standard_rated_2013-01.pgn', 5000)
test_ds = cm.read_games_from_file('data/lichess_db_standard_rated_2013-01.pgn', 500, 5000)

be = board_evaluator.BoardEvaluator('models/be_big_v0.0.1.state')
be.train(train_ds, test_ds, 6000, 'models/be_big_v0.0.1.state')

