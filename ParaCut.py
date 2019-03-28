import cv2
import numpy as np

'''
#                 ######    ######          
#                 #::::#    #::::#          
#                 #::::#    #::::#          
#            ######::::######::::######     
#            #::::::::::::::::::::::::#     ██╗  ██╗ █████╗ ███████╗██╗  ██╗████████╗ █████╗  ██████╗         ██████╗ ██╗███████╗ ██████╗██╗   ██╗██╗████████╗███████╗
#            ######::::######::::######     ██║  ██║██╔══██╗██╔════╝██║  ██║╚══██╔══╝██╔══██╗██╔════╝         ██╔══██╗██║██╔════╝██╔════╝██║   ██║██║╚══██╔══╝██╔════╝
#                 #::::#    #::::#          ███████║███████║███████╗███████║   ██║   ███████║██║  ███╗        ██████╔╝██║███████╗██║     ██║   ██║██║   ██║   ███████╗
#                 #::::#    #::::#          ██╔══██║██╔══██║╚════██║██╔══██║   ██║   ██╔══██║██║   ██║        ██╔══██╗██║╚════██║██║     ██║   ██║██║   ██║   ╚════██║
#            ######::::######::::######     ██║  ██║██║  ██║███████║██║  ██║   ██║   ██║  ██║╚██████╔╝        ██████╔╝██║███████║╚██████╗╚██████╔╝██║   ██║   ███████║
#            #::::::::::::::::::::::::#     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝         ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝
#            ######::::######::::######     
#                 #::::#    #::::#             
#                 #::::#    #::::#             
#                 ######    ######
'''
def process_rgb(rgb, r, g, b):
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY);
    morphKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, morphKernel)
    # binarize
    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # connect horizontally oriented regions
    morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, morphKernel)
    # find contours
    mask = np.zeros(bw.shape[:2], dtype="uint8")
    contours, hierarchy = cv2.findContours(connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # filter contours
    idx = 0
    x_list, y_list, w_list, h_list = [], [], [], []
    while idx >= 0:
        x, y, w, h = cv2.boundingRect(contours[idx])
        # fill the contour
        cv2.drawContours(mask, contours, idx, (255, 255, 255), cv2.FILLED)
        # ratio of non-zero pixels in the filled region
        r = cv2.contourArea(contours[idx]) / (w * h)
        if (r > 0.45 and h > 5 and w > 5 and w > h):
            cv2.rectangle(rgb, (x, y), (x + w, y + h), (r, g, b), 2)
            x_list.append(x), y_list.append(y), w_list.append(w), h_list.append(h)
        idx = hierarchy[0][idx][0]
    return rgb, x_list, y_list, w_list, h_list


picName = 'page'
large = cv2.imread(picName + '.png')
rgb = cv2.pyrDown(large)
rgb_original = cv2.pyrDown(large)

rgb, x, y, w, h = process_rgb(rgb, 0, 255, 0)
rgb, x, y, w, h = process_rgb(rgb, 220, 220, 220)
rgb, x, y, w, h = process_rgb(rgb, 100, 220, 220)
rgb, x, y, w, h = process_rgb(rgb, 0, 0, 255)
rgb, x, y, w, h = process_rgb(rgb, 0, 0, 0)

i = len(x) - 1
for xi in x:
    if i + 1< len(x) and x[i]:
        crop_img = rgb_original[y[i]:y[i] + h[i], x[i]:x[i] + w[i]]
        cv2.imwrite(picName + str(i + 1) + '.png', crop_img)
        i -= 1

cv2.imwrite('page_out.png', rgb)
