from fastapi import FastAPI, Request
from urllib.parse import urlsplit

from .companies import routes as companies_routes
from .utils import include_responses

DESCRIPTION = """
<p>
    This is delphai's API documentation and developer's portal.
    You need to have valid credentials to make calls.
    Just click <b>Authorize</b> button to retrieve the token.
</p>
<p>
    Check out
    <a href="https://github.com/delphai/docs/blob/master/auth-flow.md">this page</a>
    for more information about authentication flow and API client examples.
</p>
"""

app = FastAPI(
    title="delphai API",
    description=DESCRIPTION,
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
