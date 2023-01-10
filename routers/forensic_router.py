from fastapi import APIRouter, Form, File
from fastapi.responses import FileResponse, JSONResponse
from unsafe import Unsafe
import os

unsafe = Unsafe()
app = APIRouter()


@app.post('/delete-exif-img', tags=["Forensic"], response_class=JSONResponse)
async def delete_exif_img_router(file: bytes = File()):
    if not os.path.exists("cache"):
        os.mkdir("cache")
    file_path = f"cache/{unsafe._string_generator()}.jpg"
    with open(file_path, "wb") as f:
        f.write(file)
        f.close()
    isDeleted = unsafe.delete_exif_img(file_path)
    return {"status": "success", "data": {"is_deleted": isDeleted}}


@app.post('/edit-exif-img', tags=["Forensic"], response_class=FileResponse)
async def edit_exif_img_router(file: bytes = File(...), key: str = Form(...), value: str = Form(...)):
    if not os.path.exists("cache"):
        os.mkdir("cache")
    file_path = f"cache/{unsafe._string_generator()}.jpg"
    with open(file_path, "wb") as f:
        f.write(file)
        f.close()
    isEdited = unsafe.edit_exif_img(path=file_path, key=key, value=value)
    return file_path


@app.post('/extract-exif-img', tags=["Forensic"], response_class=JSONResponse)
async def extract_exif_img_router(file: bytes = File(...)):
    if not os.path.exists("cache"):
        os.mkdir("cache")
    file_path = f"cache/{unsafe._string_generator()}.jpg"
    with open(file_path, "wb") as f:
        f.write(file)
        f.close()
    Exifed = unsafe.extract_exif_img(file_path)
    return {"status": "success", "data": {"metadata": Exifed}}
