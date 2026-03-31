from pdf2image import convert_from_bytes
from services.img_ext import run_ocr


from docx import Document
import io
from PIL import Image
import fitz
POPPLER_PATH = r"C:\Users\DELL\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
def pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text_data = []
    tesxt=""
    fil=[]
    for page in doc:
        text = page.get_text().strip()
        if text:
            tesxt += text + "\n"
    if tesxt.strip():
        print("TEXT PDF")
        return text_data
    print("SCANNED PDF")
    images = convert_from_bytes(file_bytes, dpi=300, poppler_path=POPPLER_PATH)
    for img in images:
        text_data.append(run_ocr(img))
    return text_data
def docs(file_bytes):
    docx = Document(io.BytesIO(file_bytes))
    text_data = ""
    for para in docx.paragraphs:
        text_data += para.text + "\n"
    for table in docx.tables:
        for row in table.rows:
            for cell in row.cells:
                text_data += cell.text + "\n"
    return text_data
def img_in(img_bytes_list):
    text_data = ""
    for img_b in img_bytes_list:
        img = Image.open(io.BytesIO(img_b))
        #text_data += run_ocr(img) + "\n"
        #print("TEXTTTTT : ",text_data)
    return run_ocr(img)