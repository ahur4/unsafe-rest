from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import JSONResponse
from .DataTypes.datatypes import HashMethods
from typing import Optional
from unsafe import Unsafe
import os

app = APIRouter()
unsafe = Unsafe()


@app.post('/encryption', tags=["Encryption & Decryption"], response_class=JSONResponse)
async def encryption_router(text: str = Form(...), hash_method: HashMethods = Form("md5"), encode: Optional[str] = Form(""), count: Optional[int] = Form("")):
    if count:
        hashed = unsafe.text_encrypt(
            words=text, encode=encode, hash_method=hash_method, count=count)
    else:
        hashed = unsafe.text_encrypt(
            words=text, encode=encode, hash_method=hash_method)
    return {"status": "success", "data": {"hash": hashed, "hash_method": hash_method}}


@app.post('/decryption', tags=["Encryption & Decryption"], response_class=JSONResponse)
async def decryption_router(hash: Optional[str | bytes] = Form(...), hash_method: HashMethods = Form("md5"), word: Optional[str | list] = Form(""), wordlist: UploadFile = None):
    if wordlist:
        file_name = unsafe._string_generator()
        if not os.path.exists("cache"):
            os.mkdir("cache")
        with open(f"cache/{file_name}.txt", "w") as file:
            file.write(str(await wordlist.read()))
            file.close()
        with open(f"cache/{file_name}.txt", "r") as f:
            wordlist = f.read().split("\\n")[13:]
            print(wordlist)
        unhashed = unsafe.text_decrypt(
            hash=hash, word=wordlist, hash_method=hash_method)
        os.remove(f"cache/{file_name}.txt")
    elif word == "":
        unhashed = unsafe.text_decrypt(hash=hash, hash_method=hash_method)
    else:
        unhashed = unsafe.text_decrypt(
            hash=hash, word=word, hash_method=hash_method)
    return {"status": "success", "data": {"hash": unhashed, "hash_method": hash_method}}
