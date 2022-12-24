from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.bruteforce_router import app as bruteforce
from routers.encryption_router import app as encryption
from routers.exifdata_router import app as exif
from routers.proxy_router import app as proxy
from routers.wp_router import app as wp

# FastApi Instance
app = FastAPI()


# CorsMiddleware Handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', tags=["System"], response_class=RedirectResponse)
async def swagger():
    return "/docs"


@app.get('/version', tags=["System"], response_class=JSONResponse)
async def version():
    return {"version": "1.2.2"}

app.include_router(bruteforce)
app.include_router(encryption)
app.include_router(exif)
app.include_router(proxy)
app.include_router(wp)



# this handler return all errors and they type's
@app.exception_handler(Exception)
async def handle_exception(request, exc: Exception):
    return JSONResponse({
        "status": "failed",
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
        version="1.2.2",
        description="RESTful API Service for unsafe Module",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
