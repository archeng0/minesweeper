import pyautogui
import time
import math
import cProfile
from PIL import Image

pyautogui.FAILSAFE = True

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


class Coord:
    x: int
    y: int

class Tile:
    loc: Coord
    value: int # -2 = bomb, -1 = covered, 0 = blank, number is number
    covered: bool

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
    # maybe check individual colors? close to 50, ...
    # 229 194 159
    # 215 184 153
    # if r < 80:
    #     if b > 150:
    #         return True, 1
    #     else: 
    #         print(r,g,b)
    #         return True, 2
    # elif r < 180: return True, 4
    # elif b < 30: return True, 5
    # elif b < 80 : return True, 3
    # else: return False, 0

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
    # right = x + X_CHECK
    for j in range(y, down):
        # r,g,b = pyautogui.pixel(x,j)

        color = img.getpixel(((x,j)))
        
        # pyautogui.moveTo(x,j)
        r = color[0]; g = color[1]; b = color[2]
        

        found, val = check_rgb(r,g,b)
        if found:
            return val
        # print(r,g,b)
    return 0

# img = pyautogui.screenshot()
# print(check_num((1835, 672),img))

# initialize board with coords
board = [[Tile() for i in range(LEN)] for j in range(HEIGHT)]
for j in range(HEIGHT):
    for i in range(LEN):
        tile = board[j][i]
        tile.value = -1
        tile.loc = Coord()
        tile.loc.x = int(TRX_INIT + i*XOFFSET)
        tile.loc.y = int(TRY_INIT + j*YOFFSET)

#test coords
# for j in range(HEIGHT):
#     for i in range(LEN):
#         print(board[j][i].loc.x, board[j][i].loc.y)
#         pyautogui.moveTo(board[j][i].loc.x, board[j][i].loc.y)
#         time.sleep(0.1)

# print(board[1][3].loc.x,board[1][3].loc.y)


def foo():
    # time.sleep(0.5)
    # t0 = time.time()
    img = pyautogui.screenshot()
    # color = im.getpixel()
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            loc = [tile.loc.x, tile.loc.y]
            # r,g,b = pyautogui.pixel(int(loc[0]), int(loc[1]))
            color = img.getpixel(((int(loc[0]), int(loc[1]))))
            r = color[0]; g = color[1]; b = color[2]
            if uncovered(r,g,b):
                # print(f"check {i} {j}")
                num = check_num(loc, img)
                # if not num == 0:
                #     print(num)
                board[j][i].value = num
            # print(r,g,b)
    # t1 = time.time()
    print_board(board)
    # print(t1-t0)

cProfile.run('foo()')