from fastapi.responses import JSONResponse, RedirectResponse
import os
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Request, Response, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from unsafe import Unsafe
from enum import Enum
from unsafe.utils.strings import ua
import random

# FastApi Instance
app = FastAPI()

# Unsafe Instance
unsafe = Unsafe()

# CorsMiddleware Handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HashMethods(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha224 = "sha224"
    sha256 = "sha256"
    sha384 = "sha384"
    sha512 = "sha512"
    sha3_224 = "sha3-224"
    sha3_256 = "sha3-256"
    sha3_384 = "sha3-384"
    sha3_512 = "sha3-512"
    shake128 = "shake128"
    shake256 = "shake256"
    base16 = "base16"
    base32 = "base32"
    base64 = "base64"
    base85 = "base85"
    ascii85 = "ascii85"
    caesar = "caesar"


class Protocols(str, Enum):
    http = "http"
    socks4 = "socks4"
    socks5 = "socks5"


class Extentions(str, Enum):
    php = "php"
    asp = "asp"
    aspx = "aspx"
    js = "js"
    slash = "slash"
    cfm = "cfm"
    cgi = "cgi"
    brf = "brf"
    html = "html"


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


@app.post('/proxy-wrapper', tags=["Proxy"], response_class=JSONResponse)
async def proxy_wrapper_router(protocol: Protocols = Form("http"), max_ping: int = Form(200)):
    proxies = unsafe.proxy_wrapper(protocol=protocol, max_ping=max_ping)
    return {"status": "success", "data": {"proxies": proxies, "protocol": protocol}}


@app.post('/proxy-checker', tags=["Proxy"], response_class=JSONResponse)
async def proxy_checker_router(proxy_host: str = Form(...), proxy_port: str = Form(...), protocol: Protocols = Form("http"), timeout: int = Form(10)):
    status = unsafe.proxy_checker(
        proxy_host=proxy_host, proxy_port=proxy_port, protocol=protocol, timeout=timeout)
    return {"status": "success", "data": {"proxy_status": status, "protocol": protocol}}


@app.post('/admin-finder', tags=["Brute Force"], response_class=JSONResponse)
async def admin_finder_router(domain: str = Form(...), workers: int = Form(5), timeout: int = Form(10), ext: Extentions = Form("php"), user_agent: Optional[str] = Form(random.choice(ua)), cookie: Optional[str] = Form(""), proxy: Optional[str] = Form(""), proxies: Optional[list] = Form([])):
    if cookie and proxy and proxies:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie, proxy=proxy, proxies=proxies)
    elif cookie and proxy:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie, proxy=proxy)
    elif cookie and proxies:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie, proxies=proxies)
    elif cookie:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie)
    elif proxy:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, proxy=proxy)
    elif proxies:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, proxies=proxies)
    else:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent)
    return {"status": "success", "data": {"proxy_status": admin_panels, "site_extention": ext}}




# this handler return all errors and they type's
@app.exception_handler(Exception)
async def handle_exception(request, exc: Exception):
    return JSONResponse({
        "status": "faild",
        "data": {
            "detail": str(exc),
            "exc_type": str(type(exc).__name__)
        }}, status_code=500)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    # for route in app.routes:
    #     body_field = getattr(route, 'body_field', None)
    #     if body_field:
    #         body_field.type_.__name__ = 'name'
    openapi_schema = get_openapi(
        title="Unsafe Rest-API",
        version="1.2.0",
        description="RESTful API Service for unsafe Module",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
