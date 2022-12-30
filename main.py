from enum import Enum

from fastapi import FastAPI, Body, Depends, APIRouter
from fastapi.openapi.docs import get_redoc_html
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


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
router = APIRouter()


class Foo(BaseModel):
    test_1: str = Field(description="""\n
- aaa
- bbb
    """)

class Bar(BaseModel):
    array_1: list[int] =Field(description="""
- ccc
- ccc
    """)

class ModelId(str, Enum):
    alexnet1 = "alexnet"
    resnet2 = "resnet"
    lenet3 = "lenet"

@router.post(
    "/{model_id}:predict",
    summary="Create an item",
    response_model=Bar,
    tags=["xyz"],
    response_description="The created item",
)
async def index(
    model_id: ModelId,
    # authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer(description="ローカル開発では`abc`や`123`のような任意のテキストで良い。サービスではエンコード済みのJWT tokenを使う")),
    foo: Foo =  Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Fooo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Barr",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return 123

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