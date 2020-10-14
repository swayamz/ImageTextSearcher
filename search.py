import pyautogui
import cv2 
import pytesseract 
import numpy as np
import webbrowser
import re

pyautogui.FAILSAFE = True
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract'


image = pyautogui.screenshot(region=(500,300, 1200, 100))
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("in_memory_to_disk.png", image)
img = cv2.imread("in_memory_to_disk.png") 

  
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
  
# Specify structure shape and kernel size.  
# Kernel size increases or decreases the area  
# of the rectangle to be detected. 
# A smaller value like (10, 10) will detect  
# each word instead of a sentence. 
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13)) 

dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
  
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                 cv2.CHAIN_APPROX_NONE) 
  
im2 = img.copy() 
file = open("recognized.txt", "w+") 
file.write("") 
file.close() 
  
for cnt in contours: 
    x, y, w, h = cv2.boundingRect(cnt) 
      
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
      
    cropped = im2[y:y + h, x:x + w] 
      
    file = open("recognized.txt", "a") 
      
    text = pytesseract.image_to_string(cropped) 
      
    file.write(text) 
    file.write("\n") 
      
    file.close 


webbrowser.open_new_tab('http://www.google.com/search?btnG=1&q=%s' % open('recognized.txt', 'r').read().replace("", ""))