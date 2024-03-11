from fastapi import FastAPI

from src.api.v1.workflow import workflow_router

app = FastAPI()

app.include_router(workflow_router)
