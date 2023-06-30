from delphai_fastapi.app import App

from .companies import routes as companies_routes

DESCRIPTION = """
<p>
    This is delphai's API documentation and developer's portal.
    You need to have valid credentials to make calls.
    If you already have them, just click <b>Authorize</b> button to retrieve the token.
</p>
<p>
    Check out
    <a href="https://github.com/delphai/docs/blob/master/auth-flow.md">this page</a>
    for more information about authentication flow and API client examples.
</p>
"""

app = App(
    title="delphai API",
    description=DESCRIPTION,
    version="1.0",
    docs_url="/",
    redoc_url=None,
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    servers=[
        {"url": "https://api.delphai.com", "description": "Production environment"},
    ],
    root_path_in_servers=False,
    swagger_ui_init_oauth={"clientId": "delphai-api"},
)

app.include_router(companies_routes.router, prefix="/v1/companies")
