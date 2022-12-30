FastAPIでOpenAPIを生成するためのサンプル

`pip install uvicorn fastapi pydantic`

`uvicorn main:app --reload`

`curl http://127.0.0.1:8000/openapi.json > openapi.json`

`swagger-cli bundle openapi.json -o openapi.yaml -r -t yaml`

`redoc-cli bundle openapi.yaml`