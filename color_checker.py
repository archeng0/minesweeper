import pyautogui
import time
from PIL import Image


x = 1295
y = 514

time.sleep(0.4)
print(pyautogui.position())
pyautogui.moveTo(1723,784)

# img = pyautogui.screenshot()
# color = img.getpixel((1840,666))
# print(color)
# for i in range(10):
#     print(i)
# r,g,b = pyautogui.pixel(2054,780)
# print(r,g,b)

# pyautogui.moveTo(x,y)
# r,g,b = pyautogui.pixel(x,y)
# print(r,g,b)

# r = 153
# g = 78
# b = 161
# rgb = (r << 16) + (g << 8) + b
# print(rgb)


# colors = [3900621, 3706428, 13909049, 8794528, 16748288]
# colors2 = [13843513, 10047137]
# def check_num(loc):
#     print("checking")
#     r,g,b = pyautogui.pixel(loc[0], loc[1])
#     # print(r,g,b)
#     rgb = (r << 16) + (g << 8) + b
#     # print(rgb)
#     if rgb in colors:
#         return colors.index(rgb) + 1
#     elif rgb in colors2:
#         return colors2.index(rgb) + 3
#     # if rgb == 3900621:
#     #     return 1
#     # elif rgb == 3706428:
#     #     return 2
#     # elif rgb == 13909049 or rgb == 13843513:
#     #     return 3
#     # elif rgb == 8794528 or rgb == 10047137:
#     #     return 4
#     # elif rgb == 16748288:
#     #     return 5
    
#     x = loc[0]
#     y = loc[1]
#     down = y + Y_CHECK
#     right = x + X_CHECK
#     for j in range(y, down):
#         r,g,b = pyautogui.pixel(x,j)
#         # print(r,g,b)
#         rgb = (r << 16) + (g << 8) + b
#         if rgb in colors:
#             return colors.index(rgb) + 1
#         elif rgb in colors2:
#             return colors2.index(rgb) + 3

#         # if blue, 1, center. 59 132 205 = 3900621
#         # green, 2, not center56 142 60 = 3706428
#         # red, 3, center. 
#         # 212 60 57 = 13909049 or 211 60 57 = 13843513
#         # purple, 4, not center. 
#         # 153 78 161 = 10047137 or 134 49 160 = 8794528
#         # orange, 5, center. 255 143 0 = 16748288
#     return 0