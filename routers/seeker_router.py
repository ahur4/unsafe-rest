from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from unsafe import Unsafe
from typing import Optional

unsafe = Unsafe()
app = APIRouter()


@app.post('\google-dorking', tags=['Seeking'], response_class=JSONResponse)
async def google_dorking_router(query: str = Form(...), timeout: int = Form(10), proxy: Optional[str] = Form('')):
    if proxy:
        result = unsafe.google_dorking(query, timeout, proxy)
    else:
        result = unsafe.google_dorking(query, timeout)
    return {
        "status": "success",
        "data": {
            "result_count": len(result),
            "result": result,
        }
    }
