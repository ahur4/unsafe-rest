from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from unsafe import Unsafe
from typing import Optional

unsafe = Unsafe()
app = APIRouter()


@app.post('/browser-search', tags=['Crawler'], response_class=JSONResponse)
async def browser_search_router(query: str = Form(...), timeout: int = Form(10), proxy: Optional[str] = Form('')):
    if proxy:
        result = unsafe.browser_search(query, timeout, proxy)
    else:
        result = unsafe.browser_search(query, timeout)
    return {
        "status": "success",
        "data": {
            "result_count": len(result),
            "result": result,
        }
    }


@app.post('/crawl-page', tags=['Crawler'], response_class=JSONResponse)
async def crawl_page_router(url: str = Form(...), timeout: int = Form(10), proxy: Optional[str] = Form(''),
                            proxies: Optional[list] = Form([])):
    if proxy:
        result = unsafe.crawl_page(
            url=url, timeout=timeout, proxy=proxy)
    elif proxies != ['']:
        result = unsafe.crawl_page(url=url, timeout=timeout, proxies=proxies)
    else:
        result = unsafe.crawl_page(url=url, timeout=timeout)
    return {
        "status": "success",
        "data": {
            "result": result
        }
    }


@app.post('/xss-scanner', tags=['Crawler'], response_class=JSONResponse)
async def xss_scanner_router(url: str = Form(...), payload: str = Form("<Script>alert('hi')</scripT>")):
    result = unsafe.xss_scanner(url=url, js_script=payload)
    return {
        "status": "success",
        "data": result
    }
