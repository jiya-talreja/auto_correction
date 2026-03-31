import cv2
import numpy as np
import pytesseract
import re
def run_ocr(pil_image):
    img = np.array(pil_image)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, None, fx=2, fy=2)
    img = cv2.medianBlur(img, 3)
    thresh = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 11
    )
    text = pytesseract.image_to_data(thresh, config="--oem 3 --psm 4",output_type=pytesseract.Output.DICT)
    fl=ocr_to_lines(text)
    print(fl)
    return fl
def ocr_to_lines(data,con_thres=40):
    line_dict={}
    for i,word in enumerate(data['text']):
        word=word.strip()
        if word=="":
            continue
        w=word.split()
        if len(w)<=1 and w is not w.isdigit():
            continue
        try:
            if(int(data['conf'][i])<=con_thres):
                continue
        except:
            continue
        block=data['block_num'][i]
        line=data['line_num'][i]
        key=(block,line)
        if key not in line_dict:
            line_dict[key]=[]
        line_dict[key].append(word)
        print("LINE DICT : ",line_dict)
    final_list=[]
    