from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from unsafe import Unsafe
from typing import Optional

unsafe = Unsafe()
app = APIRouter()


@app.post('/wp-extract-users', tags=["Wordpress"], response_class=JSONResponse)
async def wp_extract_users_router(domain: str = Form(...)):
    Users = unsafe.wp_get_users(domain=domain)
    return {"status": "success", "data": {"users": Users}}


@app.post('/wp-plugin-scanner', tags=["Wordpress"], response_class=JSONResponse)
async def wp_plugin_scanner_router(domain: str = Form(...), timeout: int = Form(5), workers: int = Form(3), proxy: Optional[str] = Form(''), proxies: Optional[list] = Form([])):
    if proxy:
        plugins = unsafe.wp_plugin_scanner(
            domain=domain,
            timeout=timeout,
            workers=workers,
            proxy=proxy
        )
    elif proxies != ['']:
        plugins = unsafe.wp_plugin_scanner(
            domain=domain,
            timeout=timeout,
            workers=workers,
            proxy=proxies
        )
    else:
        plugins = unsafe.wp_plugin_scanner(
            domain=domain,
            timeout=timeout,
            workers=workers,
        )

    return {"status": "success", "data": {"plugins": plugins}}
