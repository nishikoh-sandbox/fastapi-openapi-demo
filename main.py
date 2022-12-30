from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_redoc_html
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse

from router import router

def get_redoc_html(
    *,
    openapi_url: str,
    title: str,
    redoc_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    with_google_fonts: bool = True,
) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
        <link rel="shortcut icon" href="{redoc_favicon_url}">
        <!--
        ReDoc doesn't change outer page styles
        -->
        <style>
          body {{
            margin: 0;
            padding: 0;
          }}
        </style>
        </head>
            <body>
                <div id="redoc-container"></div>
                <script src="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.55/bundles/redoc.standalone.min.js"> </script>
                <script src="https://cdn.jsdelivr.net/gh/wll8/redoc-try@1.4.1/dist/try.js"></script>
                <script>
                    initTry({{
                        openApi: `http://127.0.0.1:8000/openapi.json`,
                        redocOptions: {{scrollYOffset: 50}},
                    }})
                </script>
            </body>
        </html>
        """
    return HTMLResponse(html)

tags_metadata = [
    {
        "name": "xyz",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    # dependencies=[Depends(HTTPBearer(description="ローカル開発では`abc`や`123`のような任意のテキストで良い。サービスではエンコード済みのJWT tokenを使う")),],
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local environment"},
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    openapi_tags=tags_metadata,
    # redoc_url=None
)
app.include_router(router)
app.include_router(
    router,
    prefix="/itms",
    tags=["items"],
    dependencies=[Depends(HTTPBearer(description="ローカル開発では`abc`や`123`のような任意のテキストで良い。サービスではエンコード済みのJWT tokenを使う")),],
)
@app.get("/redoc2", include_in_schema=False)  
async def redoc_try_it_out() -> HTMLResponse:  
    title = app.title + "Redoc with try it out"  
    return get_redoc_html(openapi_url=app.openapi_url, title=title)

@app.get("/redoc3", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        # redoc_js_url="/static/redoc.standalone.js",
    )