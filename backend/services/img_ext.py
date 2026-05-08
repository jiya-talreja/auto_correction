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
fixes = {
    "11.": "ii.",
    "Il.": "ii.",
    "il.": "iii.",
    "Ill.": "iii.",
    "vil.": "vii.",
    "Vill.": "viii.",
    "vill.": "viii.",
    "1s": "is"
}
def normalize(text):
    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)
    return text
def extract_questions(lines):
    chunks = []
    current = None
    for line in lines:
        line = normalize(line).strip()
        if not line:
            continue
        if re.match(r'^(Q\.?\s*)?\d+\.', line, re.I) or re.match(r'^Q\.?\s*\d+', line, re.I):
            if current:
                content = current["content"]
                roman = list(re.finditer(r'(?<=\s)(i|ii|iii|iv|v|vi|vii|viii|ix|x)\.', content, re.I))
                if roman and "multiple choice" not in content.lower():
                    for i, m in enumerate(roman):
                        start = m.start()
                        end = roman[i + 1].start() if i + 1 < len(roman) else len(content)
                        chunks.append({
                            "q_no": f'{current["q_no"]}.{m.group(1).lower()}',
                            "content": content[start:end].strip()
                        })
                else:
                    chunks.append(current)
            q = re.search(r'Q\.?\s*(\d+)|^(\d+)\.', line, re.I)
            num = q.group(1) if q.group(1) else q.group(2)
            current = {
                "q_no": f"Q{num}",
                "content": line
            }
        elif current:
            current["content"] += " " + line
    if current:
        chunks.append(current)
    return chunks
