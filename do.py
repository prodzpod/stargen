import cv2 as cv
import numpy as np
import math
import random

PAGE_SIZE = (1335 * 2, 285 * 2)
CIRCLE_STARS = None # none: no circle optimization, number: pixel of offset from bottom to set rotate from

STAR_DIST = (1000, 2500, 5000, 0, 10000, 0, 50000) # inverse of chance for star size (idx+1)px, 0 = none
SQUARE_STAR = False # false if circle, square if square

if CIRCLE_STARS is None:
    page = (PAGE_SIZE[1], PAGE_SIZE[0])
else:
    _w = math.dist(PAGE_SIZE, (0, 0))
    w = int(math.ceil(_w * (1 + (max(0, CIRCLE_STARS) / PAGE_SIZE[1]))))
    page = (w, w)
image = np.zeros(page, np.float32)
for x in range(page[0]):
    for y in range(page[1]):
        if CIRCLE_STARS is not None:
            d = math.dist((x, y), (page[0] / 2, page[1] / 2))
            if (w / 2) < d or d < _w * (max(0, CIRCLE_STARS) / PAGE_SIZE[1]):
                continue
        for i, chance in enumerate(STAR_DIST):
            if chance <= 0:
                continue
            if random.uniform(0, 1) < (1 / chance):
                xmin = max(0, x - (i // 2))
                ymin = max(0, y - (i // 2))
                xmax = min(page[0] - 1, x + (i // 2) + (i % 2)) + 1
                ymax = min(page[1] - 1, y + (i // 2) + (i % 2)) + 1
                for x2 in range(xmin, xmax):
                    for y2 in range(ymin, ymax):
                        if not SQUARE_STAR:
                            if i % 2 == 0:
                                d = math.hypot(x2 - x, y2 - y)
                            else:
                                d = math.hypot(x2 - x - .5, y2 - y - .5)
                            if d > i / 2:
                                continue
                        image[x2, y2] = 0xFF
image = cv.cvtColor(image, cv.COLOR_GRAY2BGRA)
image[:, :, 3] = image[:, :, 0]
status = cv.imwrite("output.png", image)