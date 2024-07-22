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
    count_x = 0
    count_o = 0
    for rows in board:
        for cells in rows:
            if cells == X:
                count_x += 1
            elif cells == O:
                count_o += 1
    if count_x > count_o:
        return O
    elif count_x == count_o:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.append((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board):
        return None
    if action not in actions(board):
        raise Exception("Not valid action")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #rows
    for row in board:
        if row[0] == row[1] == row[2]:
            if row[0] == X:
                return X
            if row[0] == O: 
                return O 
    #columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            if board[0][i] == O: 
                return O 
    #main diagonal
    if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == X:
                return X
            if board[0][0] == O: 
                return O 
    #second diagonal
    if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == X:
                return X
            if board[0][2] == O: 
                return O 
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None) or (actions(board) == []):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win != None:
        if win == O: return -1
        if win == X: return 1
    return 0


def printb(board):
    for row in board:
        print(row)
    print(" ")

def minimax(board):
    results = minimax_inner(board)
    for i in range(len(results)):
        if results[i] == max(results):
            return actions(board)[i]

def minimax_inner(board):
    """
    Returns the optimal action for the current player on the board.
    """
    printb(board)
    
    if terminal(board):
        return [utility(board)]
    
    new_board = copy.deepcopy(board)
    new_states = [result(new_board, action) for action in actions(board)]
    scores = []
    for state in new_states:
        if not terminal(state):
            temp = minimax(copy.deepcopy(state))
            if (player(state) == X):
                return max(temp) if type(temp) == list else temp
            elif (player(state) == O):
                return min(temp) if type(temp) == list else temp
        else:
            scores.append(utility(state))
    """if new_board == board:
        for i in range(len(scores)):
            if scores[i] == max(scores):
                return actions(board)[i]
    else:"""
    return scores

    
    
    
        
    
    