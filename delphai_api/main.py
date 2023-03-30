from fastapi import FastAPI, Request
from urllib.parse import urlsplit


app = FastAPI(title="Delphai API")


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
