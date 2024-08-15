import chess
import chess.pgn

def board_to_vector(board):    
    vec = []
    index = 0     
    for square in chess.SQUARES:        
        piece = board.piece_at(square)
        if piece:
            piece_val = piece.piece_type * (1.0 if piece.color else -1.0)
            vec.append(float(piece_val))
        else:
            vec.append(0.0)
    turn = -1.0
    if board.turn:
        turn = 1.0
    vec.append(turn)
    return vec

def get_boards_from_game(game):
    res = []        
    if game.headers['Termination'] != 'Normal':
        return res
    
    prize = 1.0
    if game.headers['Result'] == '1-0':
        prize = -1.0
    elif game.headers['Result'] != '0-1':
        return res        
        
    moves = game.mainline_moves()
    board = game.board()
    for move in moves:
        board.push(move)
        board_vec = board_to_vector(board)        
        res.append([board_vec, 0.0])
    
    mov_cnt = len(res)
    prize_step = prize / mov_cnt
    curr_prize = 0.0
    for elem in res:
        curr_prize += prize_step
        elem[1] = float(curr_prize)        
    return res
        

def read_games_from_file(file, count=None, offset=0):
    with open(file) as pgn:
        inputs = []
        outputs = []
        game_cnt = 0
        entries = 0
        game = chess.pgn.read_game(pgn)
        while game and (count == None or game_cnt < count):            
            entries += 1
            if entries <= offset:
                game = chess.pgn.read_game(pgn)
                continue
            boards = get_boards_from_game(game)                    
            if len(boards):
                game_cnt += 1
                for board in boards:
                    inputs.append(board[0])
                    outputs.append([board[1]])
            game = chess.pgn.read_game(pgn)
            
        print(f'Read {game_cnt} games: {len(inputs)} moves')
        return inputs, outputs
    
    