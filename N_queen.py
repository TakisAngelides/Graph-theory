import numpy as np

while True:
    N = int(input('Enter the value of N: '))
    positions = []

    def valid(x, y, position_list):
        for position in position_list:
            x_pos = position[0]
            y_pos = position[1]
            if x == x_pos or y_pos == y or (y-x) == (y_pos-x_pos):
                return False
        return True

    def N_queens(k):
        if k == N:
            return True
        for i in range(N):
            for j in range(N):
                if valid(i, j, positions):
                    positions.append([i, j])
                    if N_queens(k + 1):
                        return True
                    positions.remove(positions[-1])
        return False

    def display(position_list):
        tmp = []
        board = []
        for position in position_list:
            x = position[0]
            y = position[1]
            idx = x*N+y
            tmp.append(idx)
        for i in range(N*N):
            if i in tmp:
                board.append('Q')
            else:
                board.append('-')
        print(np.array(board).reshape(N, N))

    if N_queens(0):
        display(positions)
