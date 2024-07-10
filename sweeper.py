from utils import *
import time

#random click to start
pyautogui.click(2000,800)

board = init_board()
board = scan(board)
mat, dic = create_mat(board)
print(mat)
# find_mines(mat, board, dic)

# for i in range(15):
#     board = init_board()
#     board = scan(board)
#     mat, dic = create_mat(board)
#     find_mines(mat, board, dic)
#     pyautogui.moveTo(30,30)
#     time.sleep(0.1)
# check if easy clicks
# flag easy mines