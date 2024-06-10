from utils import *

board = init_board()
board = scan(board)
mat = create_mat(board)
find_mines(mat, board)
# print(create_mat(board))
# print_board(board)


# check if easy clicks
# flag easy mines