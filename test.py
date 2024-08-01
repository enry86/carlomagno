#!/usr/bin/python

import carlomagno as cm
from carlomagno.evaluator import board_evaluator


game = cm.read_games_from_file('data/lichess_db_standard_rated_2013-01.pgn', 1)

be = board_evaluator.BoardEvaluator()
res = be.evaluate(game[0])

print (res)

