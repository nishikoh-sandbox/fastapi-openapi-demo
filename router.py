from enum import Enum

from fastapi import FastAPI, Body, Depends, APIRouter
from fastapi.openapi.docs import get_redoc_html
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


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