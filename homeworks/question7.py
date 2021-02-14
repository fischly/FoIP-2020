# -*- coding: utf-8 -*-
"""
Homeworks - Question 6
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import sys

# one can start the debug mode, where each puzzle piece with it's guessed position on the reference image is
# displayed - one after another. this will open a new window for each piece.
# just start the program with: 'python question7.py --debug'
# if debug is not specified, only the resulting numbering is shown.

# at first, look if there was the debug flag specified in the arguments that started this script
show_debug =  ('debug' in sys.argv or '-debug' in sys.argv or '--debug' in sys.argv)


# --- loading the images ---
img_pces = cv2.imread('./imagesHW/hw5_puzzle_pieces.jpg', 0)
img_ref = cv2.imread('./imagesHW/hw5_puzzle_reference.jpg', 0)

# --- crop out the single pieces ---
# we found no way to reliably cut the pieces out programmatically, so we cut them out by hand
piece_pos = [
    { 'x': 56,  'y': 72,  'w': 50, 'h': 75 },
    { 'x': 131, 'y': 220, 'w': 51, 'h': 60 },
    { 'x': 212, 'y': 379, 'w': 65, 'h': 53 },
    { 'x': 267, 'y': 43,  'w': 52, 'h': 75 },
    { 'x': 273, 'y': 185, 'w': 55, 'h': 76 },
    { 'x': 385, 'y': 358, 'w': 53, 'h': 66 },
    { 'x': 420, 'y': 146, 'w': 58, 'h': 72 },
    { 'x': 488, 'y': 262, 'w': 66, 'h': 64 },
    { 'x': 547, 'y': 35,  'w': 51, 'h': 75 },
    { 'x': 597, 'y': 317, 'w': 61, 'h': 75 },
    { 'x': 665, 'y': 103,  'w': 50, 'h': 58 },
    { 'x': 694, 'y': 250, 'w': 64, 'h': 68},
    { 'x': 798, 'y': 77,  'w': 51, 'h': 69 },
    { 'x': 811, 'y': 196, 'w': 61, 'h': 66 },
    { 'x': 845, 'y': 343, 'w': 61, 'h': 60 },
    { 'x': 928, 'y': 139, 'w': 44, 'h': 67 },
    { 'x': 952, 'y': 19,  'w': 54, 'h': 63 },
    { 'x': 981, 'y': 346, 'w': 64, 'h': 73 },
    { 'x': 1008, 'y': 226, 'w': 52, 'h': 76 },
    { 'x': 1105, 'y': 95, 'w': 44, 'h': 62 }
]

# the list that contains the cropped out piece images
pieces = []
for pos in piece_pos:
    piece = img_pces[pos['y']:pos['y'] + pos['h'], pos['x']:pos['x']+pos['w']]
    pieces.append(piece)
# ----------------------------------------------------------------------------------------
# --- template matching to try to find where a piece belongs to on the reference image ---
# ----------------------------------------------------------------------------------

def find_piece(ref, pce, draw_debug=False):    
    # use template matching to try to find where the piece belongs to
    # I found to be TM_CCORR_NORMED to work the best in this case, even though it is unable to accuratelly find pieces that 
    # nearly look identical, like the background of the mona lisa 
    res = cv2.matchTemplate(ref, pce, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # get the found bounding rectangle
    w, h = pce.shape[::-1]
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # draw the result
    if draw_debug:
        ref_copy = ref.copy()
        cv2.rectangle(ref_copy, top_left, bottom_right, 255, 2)

        fig, axs = plt.subplots(1, 2)

        fig.set_figheight(10.80);
        fig.set_figwidth(10)
        axs[0].imshow(pce, cmap='gray'); axs[0].set_title('The puzzle piece'); axs[0].axis('off')
        axs[1].imshow(ref_copy, cmap='gray'); axs[1].set_title('The puzzle piece marked in the reference image'); axs[1].axis('off')

        plt.show()
    # return the rectangle the thought piece position
    return (top_left[0], top_left[1], w, h)
    
# find_piece(img_ref, pieces[8], True)

# ----------------------------------------------------------------------------------
# --- map the found rectangle to a position index, so we can numerate the pieces ---
# ----------------------------------------------------------------------------------

# the puzzle consists of 4x5 puzzle pieces - so split the reference image size into a 4x5 grid
cell_w = img_ref.shape[1] / 4
cell_h = img_ref.shape[0] / 5

# helper functions
def get_underlying_cell(x, y):
    """Returns on which cell the given point lies."""
    cell_x = math.floor(x / cell_w)
    cell_y = math.floor(y / cell_h)
    
    return (cell_x, cell_y)

def cell_to_index(cx, cy):
    # each row has 4 cells, so for example cell (1,1) will get index 5
    return cx + cy * 4

def get_center_of_rect(x, y, w, h):
    """Returns the center of the given rectangle."""
    return (int(x + (w/2)), int(y + (h / 2)))


# load the puzzle piece image again in color to be able to write the resulting numbering on it
output = cv2.imread('./imagesHW/hw5_puzzle_pieces.jpg')

# iterate over each piece
for i,pos in enumerate(piece_pos):
    # try to find where this piece belongs to on the reference image using template matching
    (x, y, w, h) = find_piece(img_ref, pieces[i], show_debug)
    # get the center of the found rectangle
    found_center = get_center_of_rect(x, y, w, h)
    
    # get the cell to which the found points belong - this allows us to estimate the position of the piece 
    found_cell = get_underlying_cell(found_center[0], found_center[1])
    # get the index using the found cell
    cell_index = cell_to_index(found_cell[0], found_cell[1])
    
#     print('Found center for piece {0}: {1}. Cell: {2} -> index = {3}'.format(i, found_center, found_cell, cell_index))
    
    # print the found index onto the output image
    piece_center = (int(pos['x'] + pos['w'] / 2) - 10, int(pos['y'] + pos['h'] / 2))
    cv2.putText(output, str(cell_index), piece_center, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
    
# draw the result
fig, axs = plt.subplots(1, 1)

fig.set_figheight(10.80)
fig.set_figwidth(19.20)
axs.imshow(output, cmap='gray'); axs.set_title('Result'); axs.axis('off')

plt.show()

# --- save resulting image ---
plt.imsave('./results/question7_puzzle_pieces_numbered.jpg', output, cmap = 'gray')
