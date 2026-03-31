from fastapi import APIRouter, UploadFile, File # pyright: ignore[reportMissingImports]
from typing import List
from services.input_handle import pdf
from services.input_handle import img_in
from services.input_handle import docs
from typing_extensions import Annotated
router=APIRouter()

@router.post("/upload-teacher")
async def upload_teacher(files:UploadFile=File(...)):
    documents=[]
   
    name=files.filename.lower()
    content=await files.read()
    if name.endswith(".pdf"):
        result=pdf(content)
    elif name.endswith(".docx"):
        result=docs(content)
    elif name.endswith((".png",".jpg",".jpeg")):
        result=img_in([content])
    else:
        return {"error":"Invalid file"}
    documents.append({
        "filename":name,
        "contents":result
    }
    )
    return documents
