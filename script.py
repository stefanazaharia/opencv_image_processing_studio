import cv2
import numpy as np
import os
import random

def load_image(path):
    img = cv2.imread(path)   # <----- ?
    if img is None: return None
    return cv2.resize(img, (450, 450))    # <-----  [1]  din lista

def apply_blur(img):
    return cv2.GaussianBlur(img, (15, 15), 0)    # <-----  [2]  din lista

def apply_stack_blur(img):
    return cv2.stackBlur(img, (19, 19))    # <-----  [3]

def apply_grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # <-----  [4]  din lista
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def apply_edges(img):
    edges = cv2.Canny(img, 100, 200)  # <-----  [5]  din lista
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_rotate(img):
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)   # <-----  [6]

def apply_vortex(img):
    # efect de vartej, mapare polara
    rows, cols = img.shape[:2]
    map_x = np.zeros((rows, cols), np.float32)
    map_y = np.zeros((rows, cols), np.float32)
    center_x, center_y = cols / 2, rows / 2
    
    for i in range(rows):
        for j in range(cols):
            offset_x, offset_y = j - center_x, i - center_y
            radius = np.sqrt(offset_x**2 + offset_y**2)
            if radius < center_x:
                # calculam unghiul de rotatie bazat pe distanta fata de centru
                theta = np.arctan2(offset_y, offset_x) + (center_x - radius) / 50.0
                map_x[i, j] = center_x + radius * np.cos(theta)
                map_y[i, j] = center_y + radius * np.sin(theta)
            else:
                map_x[i, j] = j
                map_y[i, j] = i
    return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)   # <-----  [7]


def apply_rotate_45(img):
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 0.7)    # <-----  [8]   ??
    return cv2.warpAffine(img, M, (cols, rows))   # <-----  [9]

def apply_flip(img):
    return cv2.flip(img, 1)    # <-----  [10]

def apply_waves(img):
    #efect de valuri
    rows, cols = img.shape[:2]
    map_x = np.zeros((rows, cols), np.float32)
    map_y = np.zeros((rows, cols), np.float32)
    for i in range(rows):
        for j in range(cols):
            map_x[i, j] = j
            map_y[i, j] = i + 10 * np.sin(2 * np.pi * j / 120)
    return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def apply_sharpen(img):   #clarifica poza
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    return cv2.filter2D(img, -1, kernel)  # <-----  [11]

def apply_watermark(img):
    # watermark
    overlay = img.copy()
    rect_area = overlay[380:440, 50:400]
    #cv2.boxFilter folosesc pentru un fundal usor blurat la watermark
    overlay[380:440, 50:400] = cv2.boxFilter(rect_area, -1, (10,10))    # <-----  [12]   ??
    cv2.putText(overlay, "WATERMARK - STEF", (100, 420), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)   # <-----  [13]
    return cv2.addWeighted(overlay, 0.6, img, 0.4, 0)   # <-----  [14]

def apply_shapes(img):
    temp = img.copy()
    h, w = temp.shape[:2]
    cv2.line(temp, (0,0), (w, h), (255, 0, 0), 5)   #(255, 0, 0) pentru culoarea albastru  # <-----  [15]
    cv2.line(temp, (w,0), (0,h), (0, 255, 0), 5)  #pentru culoarea verde
    return cv2.convertScaleAbs(temp, alpha=1.2, beta=10)   # <-----  [16]

def apply_frame(img):
    return cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 0, 0])  # <-----  [17]

def apply_pixelate(img):
    h, w = img.shape[:2]
    # micsoram
    temp = cv2.resize(img, (30, 30), interpolation=cv2.INTER_LINEAR)
    # revenim la marime mare
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

def apply_negative(img):
    return cv2.bitwise_not(img)   # <-----  [18] din lista

def apply_zoom(img):
    large = cv2.pyrUp(img)   # <-----  [19]
    # tai centrul pentru a mentine marimea 450x450
    return large[225:675, 225:675]

def apply_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)   # <-----  [20]
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)


def get_random_image(folder_path):
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    return os.path.join(folder_path, random.choice(files)) if files else None
