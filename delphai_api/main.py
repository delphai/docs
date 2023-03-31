from fastapi import FastAPI, Request
from urllib.parse import urlsplit

from .companies import routes as companies_routes
from .utils import include_responses

app = FastAPI(
    title="Delphai API",
    docs_url="/",
    redoc_url=None,
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    servers=[
        {"url": "https://api.delphai.com", "description": "Production environment"},
    ],
    root_path_in_servers=False,
    swagger_ui_init_oauth={"clientId": "delphai-api"},
)


@app.middleware("http")
async def set_root_path(request: Request, call_next):
    """
    Set `root_path` to make proper URLs behind a proxy
    https://fastapi.tiangolo.com/advanced/behind-a-proxy/
    """
    original_url = request.headers.get("x-envoy-original-path")
    path = request.url.path

    if original_url:
        original_path = urlsplit(original_url).path

        if original_path.endswith(path):
            request.scope["root_path"] = original_path.removesuffix(path)

    return await call_next(request)


include_responses(app)

app.include_router(companies_routes.router, prefix="/v1/companies")
