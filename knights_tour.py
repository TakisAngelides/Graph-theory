import numpy as np
from itertools import filterfalse

#L = int(input('Enter the dimension of the board (minimum 3): '))
L = 5
N = L*L

def get_board():
    board_list = [i for i in range(N)]
    return board_list

def valid(i, j, moves):
    if i>=0 and i<L and j>=0 and j<L and (i, j) not in moves:
        return True
    return False

def get_neighbours():
    neighbours = {}
    for i in range(N):
        up_right = i-2*L + 1
        up_left = i-2*L - 1
        down_right = i+2*L + 1
        down_left = i+2*L - 1
        diagonal_up_left = i-L - 2
        diagonal_up_right = i-L + 2
        diagonal_down_left = i + L - 2
        diagonal_down_right = i + L + 2
        neighbours[i] = [up_right, up_left, down_right, down_left,
                         diagonal_up_left, diagonal_up_right, diagonal_down_left, diagonal_down_right]
    # Logic hell - provides a dictionary of neighbours for each site - not necessary for program 
    for i in range(N):
        next_line = []
        next_next_line = []
        for j in range(len(neighbours[i])):
            if abs(int(neighbours[i][j]/L) - int(i/L)) == 1:
                next_line.append(neighbours[i][j])
            else:
                next_next_line.append(neighbours[i][j])
        neighbours[i] = list(filterfalse(lambda x: x<0 or x>N-1 or abs(int(i/5)-int(x/5))==0, neighbours[i]))
        neighbours[i] = list(filter(lambda x: (x in next_line and abs(i%L-x%L) == 2)
                                                   or (x in next_next_line and abs(i%L - x%L) == 1), neighbours[i]))
    return neighbours

def play(x, y):
    moves = []
    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]
    moves.append((x,y))

    def get_moves(x, y, x_move, y_move):

        if len(moves) == N:
            return True
        for i in range(len(x_move)):
            next_x = x + x_move[i]
            next_y = y + y_move[i]
            if valid(next_x, next_y, moves):
                moves.append((next_x, next_y))
                if get_moves(next_x, next_y, x_move, y_move):
                    return True
                moves.remove(moves[-1])
        return False

    if get_moves(x, y, x_move, y_move):
        return moves
    return ['X']*N

def animate(moves):
    board = ['X' for _ in range(N)]
    for move in moves:
        x = move[0]
        y = move[1]
        idx = x*L + y
        board[idx] = 'O'
        print(np.array(board).reshape(L, L))
        print('----------------------')

moves = play(0, 0)
print(moves)
animate(moves)


