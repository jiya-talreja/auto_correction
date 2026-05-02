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
    questions=extract_questions(fl)
    return questions
def ocr_to_lines(data,con_thres=40):
    line_dict={}
    for i,word in enumerate(data['text']):
        word=word.strip()
        if word=="":
            continue
        w=word.strip()
        if len(w)<=1 and not w.isdigit():
            continue
        try:
            if(int(data['conf'][i])<=con_thres):
                continue
        except:
            continue
        block=data['block_num'][i]
        line=data['line_num'][i]
        key=(block,line)
        if key not in line_dict:#if line dict empty
            line_dict[key]=[]
        line_dict[key].append(word)
        
    final_list=[]
    for k in sorted(line_dict.keys()):
        sentence=" ".join(line_dict[k])
        final_list.append(sentence)
    return final_list
def extract_questions(lines):#list of lines in paper
    use_words=["how","when","why","which","where","who","whom",
        "what","define","explain","difference",
        "distinguish","short notes"
    ]
    ignore_words=[
        "note","notes","instruction","general instructions",
        "compulsory","permitted","max time",
        "attempt","question paper","section",
        "sections","marks","mark","attempted","paper"]
    current_q=""
    questions=[]
    in_main=False
    for line in lines:
        line=line.lower().strip()
        if not line:
            continue
        if any(word in line for word in ignore_words):
            label="noise"
        elif(
            re.match(r'^\(?\d+[\).\s]', line) or#1. 1)
            re.match(r'^q[\.\s-]*\d+', line)#Q..
        ):
            label="main"
        elif(
            re.match(r'^[a-z]\)', line) or#a) a.
            re.match(r'^\([ivx]+\)', line) or#roman
            re.match(r'^\d+\.\d+', line)#1.1
        ):
            label="subq"
        elif(
            "?" in line or
            any(word in line for word in use_words)
        ):
            label="con"
        else:
            label="con"
        if label=="noise":
            continue
        elif label=="main":
            if current_q:
                questions.append(current_q.strip())
            current_q=line
            in_main=True
        elif label=="subq":
            if in_main:
                current_q+=" "+line
        elif label=="con":
                if current_q:
                    current_q+=" "+line
    if current_q:
            questions.append(current_q.strip())
    return questions
