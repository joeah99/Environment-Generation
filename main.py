import numpy as np
import time
import random
import sys

# first I import the modules I need: numpy to create the matrix,
# sys for the command line arguments, as well as
# time and random for use later on.

ESC = '\x1b'
WHITE = ESC + '[37m'
YELLOW = ESC + '[43m'
GREEN = ESC + '[42m'
BLUE = ESC + '[44m'
water = BLUE + '~'
sand = YELLOW + '.'
grass = GREEN + ','
snow = WHITE + '*'
hill = '^'
# here I created all of my land elements by combining an ASCII color with a character

size = 33
arr = np.full((size, size), 0)
# here I created my 33 x 33 matrix using numpy. I originally filled it with zeros
# so that it could update to other
# integers easily later on.

magnitude = int(sys.argv[2])
offset = random.randint(-magnitude, magnitude)
seed_num = int(sys.argv[1])
random.seed(seed_num)
top_left = (0, 0)
top_right = (0, size - 1)
bot_left = (size - 1, 0)
bot_right = (size - 1, size - 1)
# I made my magnitude and seed a command line argument here using sys. Then I made
# the offset a random number between
# the negative and positive magnitude, and I randomized the seed. Below the seed
# and magnitude, I coded the coordinates
# of the original four corners of the matrix as tuples.

arr[0][0] = random.randint(0, 100)
arr[0][size - 1] = random.randint(0, 100)
arr[size - 1][0] = random.randint(0, 100)
arr[size - 1][size - 1] = random.randint(0, 100)
# Here I made the matrix coordinates of the original four corners assigned to a
# random number between 0 and 100, which
# will replace the 0 that was originally there.

def print_func(land, blue, yellow, green, gray, white):
    for y in range(size):
        for x in range(size):
# print("%3d" % land[y][x], end='')
            if land[y][x] < 20:
                print(blue, end='')
            elif 20 <= land[y][x] < 40:
                print(yellow, end='')
            elif 40 <= land[y][x] < 70:
                print(green, end='')
            elif 70 <= land[y][x] < 80:
                print(gray, end='')
            elif 80 <= land[y][x]:
                print(white, end='')
            print(ESC + '[0m', end='')
        print()
    return land
# Above is my print function. My arguments were the matrix (land)
# and all the landtypes named as their colors.
# The integer assigned with every matrix coordinate is checked here, and depending
# on how high or low the integer is,
# the coordinate will be colored as water, sand, grass, a hill, or snow. Then, I
# made sure to stop printing color
# and print the updated matrix. Finally, I return the updated matrix.

def land_gen(land, tl, tr, bl, br, depth, mag):
    print_func(arr, water, sand, grass, hill, snow)
    if depth == 5:
        return
# This is my recursive function. First, I call the print function immediately.
# Then the function checks to make sure
# depth is less than 5. If depth == 5, the function returns and ends. If not,
# it continues on.

    middle = ((br[0] + tl[0]) // 2, (tr[1] + bl[1]) // 2)
    top_side = (tl[0], (tr[1] + tl[1]) // 2)
    right_side = ((br[0] + tr[0]) // 2, tr[1])
    bot_side = (bl[0], (br[1] + bl[1]) // 2)
    left_side = ((bl[0] + tl[0]) // 2, tl[1])
# Here, I code the middle and sides of the original matrix as tuples of their
# coordinates. I will be able to use
# all these variables in my recursive calls later on. I also use the double
# division symbol to ensure all results
# are integers and not floats. These tuples are also not specific to one point
# on the matrix, because they are only
# dependent on where 'center' , 'top left', etc. is relative to them, so they
# can work with recursion.

    land[middle[0]][middle[1]] = ((land[tl[0]][tl[1]] + land[tr[0]][tr[1]] + land[bl[0]][bl[1]] + land[br[0]][br[1]]) // 4) + mag
    land[top_side[0]][top_side[1]] = ((land[tl[0]][tl[1]] + land[middle[0]][middle[1]] + land[tr[0]][tr[1]]) // 3) + mag
    land[right_side[0]][right_side[1]] = ((land[tr[0]][tr[1]] + land[middle[0]][middle[1]] + land[br[0]][br[1]]) // 3) + mag
    land[bot_side[0]][bot_side[1]] = ((land[bl[0]][bot_side[1]] + land[middle[0]][middle[1]] + land[br[0]][br[1]]) // 3) + mag
    land[left_side[0]][left_side[1]] = ((land[tl[0]][tl[1]] + land[middle[0]][middle[1]] + land[bl[0]][bl[1]]) // 3) + mag
# Here I actually provide integer values to the coordinates of the center and
# sides. I use the x plus method to
# do the math for them and add the random offset to each.

    land_gen(land, tl, top_side, left_side, middle, depth + 1, mag // 2)
    land_gen(land, top_side, tr, middle, right_side, depth + 1, mag // 2)
    land_gen(land, middle, right_side, bot_side, br, depth + 1, mag // 2)
    land_gen(land, left_side, middle, bl, bot_side, depth + 1, mag // 2)
# Here are my four recursive calls. These represent the first four squares that
# the original matrix will break into.
# Such as the top left square, the top right square, etc. whose corners include
# the center and sides of the
# original matrix. Then I have 'depth + 1' and 'mag // 2' as arguments instead
# of just depth and mag so that
# they will increase and decrease accordingly as recursion takes place, and the
# function will eventually return once
# depth == 5 for each of the four recursive calls, and move to the next
# recursive call (next of the 4 squares).

    print("\033[33A", end="\r")
    return land
# Here I first used the line from the maze lab to try to prevent excess
# flickering. Then I finally return the completed matrix.

print("\033[33A", end="\r")
final_call = land_gen(arr, top_left, top_right, bot_left, bot_right, 0, magnitude)
# final_call is the first and only time I actually call the recursive function.
# That's all folks.
