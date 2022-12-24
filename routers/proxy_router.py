from .datatypes import Protocols
from fastapi import APIRouter, Form
from unsafe import Unsafe
from fastapi.responses import JSONResponse

app = APIRouter()
unsafe = Unsafe()


@app.post('/proxy-wrapper', tags=["Proxy"], response_class=JSONResponse)
async def proxy_wrapper_router(protocol: Protocols = Form("http"), max_ping: int = Form(200)):
    proxies = unsafe.proxy_wrapper(protocol=protocol, max_ping=max_ping)
    return {"status": "success", "data": {"proxies": proxies, "protocol": protocol}}


@app.post('/proxy-checker', tags=["Proxy"], response_class=JSONResponse)
async def proxy_checker_router(proxy_host: str = Form(...), proxy_port: str = Form(...), protocol: Protocols = Form("http"), timeout: int = Form(10)):
    status = unsafe.proxy_checker(
        proxy_host=proxy_host, proxy_port=proxy_port, protocol=protocol, timeout=timeout)
    return {"status": "success", "data": {"proxy_status": status, "protocol": protocol}}
