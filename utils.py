import pyautogui
import time
import math
import cProfile
from PIL import Image
from row_echelon import *
import numpy as np

pyautogui.FAILSAFE = True

class Coord:
    x: int
    y: int

class Tile:
    loc: Coord
    value: int # -2 = bomb, -1 = covered, 0 = blank, number is number
    covered: bool
    checked: bool

mode = 'easy_half'
# mode = 'hard_full'

if mode == 'hard_full':
    LEN = 24
    HEIGHT = 20

    XOFFSET=(1654-905)/24 # distance between center of squares along x
    TRX = 905

    YOFFSET=31.2 #distance between center of squares along y
    TRY = 499 # y coord of top left of top left square

elif mode == 'easy_half':
    LEN = 10
    HEIGHT = 8

    XOFFSET = (2201-1639)/10
    TRX  = 1639
    YOFFSET = (1037-588)/8
    TRY = 588

TRX_INIT = TRX + XOFFSET / 2
X_CHECK = int(XOFFSET / 3)
TRY_INIT = TRY + YOFFSET / 2 # y coord of center of top left square
Y_CHECK = int(YOFFSET / 3) # how far in each square to check

def print_board(board):
    for j in range(HEIGHT):
        for i in range(LEN):
            val = board[j][i].value
            if val == -2:
                rep = 'X'
            elif val == -1:
                rep = '-'
            elif val == 0:
                rep = ' '
            else: 
                rep = val

            print(rep, end=' ')
        print()

def uncovered(r, g, b):
    if (r == 170 and g == 215 and b == 81) or (r == 162 and g == 209 and b == 73):
        return False
    else:
        return True
    
eps = 50
def check_rgb(r,g,b):
    p = [r,g,b]
    if math.dist(p,[59, 132, 205]) < eps:
        return True, 1
    elif math.dist(p,[56, 142, 60]) < eps:
        return True, 2
    elif math.dist(p,[212, 60, 57]) < eps:
        return True, 3
    elif math.dist(p,[153, 78, 161]) < eps:
        return True, 4
    elif math.dist(p,[255, 143, 0]) < eps :
        return True, 5
    else:
        return False, 0

def check_num(loc, img):
    x = loc[0]
    y = loc[1]
    down = y + Y_CHECK
    for j in range(y, down):
        color = img.getpixel(((x,j)))
        r = color[0]; g = color[1]; b = color[2]
        found, val = check_rgb(r,g,b)
        if found:
            return val
    return 0

# initialize board with coords
def init_board():
    board = [[Tile() for i in range(LEN)] for j in range(HEIGHT)]
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            tile.value = -1
            tile.loc = Coord()
            tile.checked = False
            tile.loc.x = int(TRX_INIT + i*XOFFSET)
            tile.loc.y = int(TRY_INIT + j*YOFFSET)
    return board

def test_mouse():
    for j in range(HEIGHT):
        for i in range(LEN):
            print(board[j][i].loc.x, board[j][i].loc.y)
            pyautogui.moveTo(board[j][i].loc.x, board[j][i].loc.y)
            time.sleep(0.1)

def scan(board):
    img = pyautogui.screenshot()
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            loc = [tile.loc.x, tile.loc.y]
            color = img.getpixel(((int(loc[0]), int(loc[1]))))
            r = color[0]; g = color[1]; b = color[2]
            if uncovered(r,g,b):
                num = check_num(loc, img)
                board[j][i].value = num
    return board

def get_neighbors(i,j):
    ret = []
    if i == 0:
        start_x = 0
        end_x = i+1
    elif i == LEN-1:
        start_x = i-1
        end_x = i
    else:
        start_x = i-1
        end_x = i+1

    if j == 0:
        start_y = j
        end_y = j+1
    elif j == HEIGHT-1:
        start_y = j-1
        end_y = j
    else:
        start_y = j-1
        end_y =j+1

    for y in range(start_y, end_y+1):
        for x in range(start_x, end_x+1):
            if not (x == i and y == j):
                ret.append((x,y))
    
    return ret

#takes a board and returns matrix for unknown squares in ROE form, and dictionary of values
def create_mat(board):
    dic = {}
    idx = 0
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            val = tile.value

            if val < 1 or tile.checked:
                continue

            adj = get_neighbors(i,j)
            for (x,y) in adj:

                curr = board[y][x]
                if curr.value == -1:
                    if (x,y) not in dic:
                        dic[(x,y)] = idx
                        idx += 1

    mat_len = len(dic) + 1
    mat = np.empty((0,mat_len))

    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            val = tile.value

            if val < 1 or tile.checked:
                continue

            adj = get_neighbors(i,j)
            row = [0 for i in range(mat_len)]
            for (x,y) in adj:
                if (x,y) in dic:
                    row[dic[(x,y)]] = 1
            
            row[-1] = val
            mat = np.vstack([mat,row])

    print(dic)
    return row_echelon_form(mat)

# takes ROE matrix and board to get mines from matrix, sets board values accordingly
def find_mines(mat, board):
    mines = []
    clear = []
    to_check = []

    rows, cols = mat.shape
    for i in range(rows):
        row = mat[[i],:][0]
        # print(row)
        squares = row[:-1]
        val = row[-1]

        # skip rows with no info
        sum_sq = np.sum(squares)
        if sum_sq == 0:
            continue
        
        # if val == 0:
            # all 1's are clear
        
        # if sum_sq == val:
            # all 1's are mines

        # to_check.append(row)
    
    # keep looping over until list is empty, or no changes made (no new info)
    changes = False
    while not to_check:
        # if changes made, set changes to True

        if not changes:
            break



        # get easy ones, where last val is 0, or sum is last value (all mines)
        # print(squares)
        # print(np.sum(row))
        


def check_squares_around(dic):
    board = init_board()
    for (x,y) in dic:
        board[y][x].value = 1
    print_board(board)




