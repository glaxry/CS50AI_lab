"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None
    count_x = 0
    count_o = 0
    for row in board:
        for elem in row:
            if elem == X:
                count_x = count_x + 1
            elif elem == O:
                count_o = count_o + 1

    return X if count_x == count_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
   
    result_ = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                tup = (i, j)
                result_.add(tup)
    return result_


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if terminal(board):
        raise ValueError("Game over.")
    elif action not in actions(board):
        raise ValueError("Invalid action.")
    else:
        p = player(board)
        result_board = copy.deepcopy(board)
        (i, j) = action
        result_board[i][j] = p

    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != None:
            return X if board[i][0] == X else O
    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] != None:
            return X if board[i][0] == X else O
    if board[0][0] == board[1][1] == board[2][2] != None:
        return X if board[i][0] == X else O
    if board[0][2] == board[1][1] == board[2][0] != None:
        return X if board[i][0] == X else O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for elem in row:
            if elem == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if X == win:
        return 1
    elif O == win:
        return -1
    return 0


def _min(board):
    if terminal(board):
        return utility(board), None
    re_set = actions(board)
    
    min_return_value = 3
    min_return = ()
    for elem in re_set:
        l_ = _max(result(board, elem))
        
        if l_[0] <= min_return_value:
            min_return = (l_[0], elem)
    return min_return


def _max(board):
    if terminal(board):
        return utility(board), None
    re_set = actions(board)
    
    max_return_value = -3
    max_return = ()
    for elem in re_set:
        l_ = _min(result(board, elem))
        
        if l_[0] >= max_return_value:
            max_return = (l_[0], elem)
    return max_return


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    p = player(board)

    # If empty board is provided as input, return corner.
    if board == [[EMPTY]*3]*3:
        return (0,0)

    if p == X:
    	result = _max(board)
    else:
    	result = _min(board)
    print(result)
    return result[1]
    
    
    
