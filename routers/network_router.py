from unsafe import Unsafe
from typing import Optional
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

app = APIRouter()
unsafe = Unsafe()


@app.post("/port-scanner", tags=["Network"], response_class=JSONResponse)
async def port_scanner_router(host: str = Form(...), ports: Optional[list] = Form([]), port: Optional[int] = Form(80)):
    if port:
        result = unsafe.port_scanner(host=host, port=port)
    elif ports != ['']:
        result = unsafe.port_scanner(host=host, ports=ports)
    return {
        "status": "success",
        "data": {
            "open_ports": result
        }
    }


@app.post("/mac-address-lookup", tags=["Network"], response_class=JSONResponse)
async def mac_address_lookup_router(mac: str = Form(...)):
    return {
        "status": "success",
        "data": {
            "company": unsafe.mac_address_lookup(mac=mac)
        }
    }
