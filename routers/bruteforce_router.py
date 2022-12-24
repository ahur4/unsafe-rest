from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from .DataTypes.datatypes import Extentions
from typing import Optional
import random
from unsafe.utils.strings import ua
from unsafe import Unsafe

app = APIRouter()
unsafe = Unsafe()


@app.post('/admin-finder', tags=["Brute Force"], response_class=JSONResponse)
async def admin_finder_router(domain: str = Form(...), workers: int = Form(5), timeout: int = Form(10), ext: Extentions = Form("php"), user_agent: Optional[str] = Form(random.choice(ua)), cookie: Optional[str] = Form(""), proxy: Optional[str] = Form(""), proxies: Optional[list] = Form([])):
    if cookie and proxy and proxies != ['']:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie, proxy=proxy, proxies=proxies)
    elif cookie and proxy:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie, proxy=proxy)
    elif cookie and proxies != ['']:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie, proxies=proxies)
    elif cookie:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, cookie=cookie)
    elif proxy:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, proxy=proxy)
    elif proxies != ['']:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent, proxies=proxies)
    else:
        admin_panels = unsafe.admin_finder(domain=domain, workers=workers, timeout=timeout,
                                           ext=ext, user_agent=user_agent)
    return {"status": "success", "data": {"proxy_status": admin_panels, "site_extention": ext}}


@app.post('/filemanager-finder', tags=["Brute Force"], response_class=JSONResponse)
async def filemanager_finder_router(domain: str = Form(...), workers: int = Form(5), timeout: int = Form(10), user_agent: Optional[str] = Form(random.choice(ua)), cookie: Optional[str] = Form(""), proxy: Optional[str] = Form(""), proxies: Optional[list] = Form([])):
    if cookie and proxy and proxies != ['']:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent, cookie=cookie, proxy=proxy, proxies=proxies)
    elif cookie and proxy:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent, cookie=cookie, proxy=proxy)
    elif cookie and proxies != ['']:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent, cookie=cookie, proxies=proxies)
    elif cookie:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent, cookie=cookie)
    elif proxy:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent, proxy=proxy)
    elif proxies != ['']:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent, proxies=proxies)
    else:
        filemanagers = unsafe.filemanager_finder(domain=domain, workers=workers, timeout=timeout,
                                                 user_agent=user_agent)
    return {"status": "success", "data": {"proxy_status": filemanagers}}


@app.post('/cloudflare-bypasser', tags=["Brute Force"], response_class=JSONResponse)
async def cloudflare_bypasser_router(domain: str = Form(...), workers: int = Form(5)):
    host_ips = unsafe.cloudflare_bypasser(domain=domain, workers=workers)
    return {"status": "success", "data": {"proxy_status": host_ips}}
