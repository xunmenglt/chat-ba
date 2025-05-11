from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.cors import CORSMiddleware
from controller import all_api

min_app=FastAPI(
    title="未软接口测试",
    version="1.0",
    description="未软华为卡模型接口适配",
    docs_url=None,
    redoc_url=None,  # 设置 ReDoc 文档的路径
)
min_app.include_router(all_api)

min_app.mount("/static", StaticFiles(directory="static"), name="static")

@min_app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="ChatBA",
        # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger/swagger-ui.css',
        swagger_favicon_url='/static/swagger/img.png',
    )

@min_app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=min_app.openapi_url,
        title=min_app.title + " - ReDoc",
        redoc_js_url="/static/swagger/redoc.standalone.js",
    )

min_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)
if __name__=="__main__":
    
    DEFAULT_BIND_HOST="0.0.0.0"
    SERVER_PORT=6565

    import uvicorn

    uvicorn.run(min_app,
                host=DEFAULT_BIND_HOST,
                port=SERVER_PORT,
                )